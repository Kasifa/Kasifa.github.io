#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the fail-closed transactional R0.73H GitHub Pages release."""

from __future__ import annotations

import hashlib
import argparse
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import tempfile

from generate_r072o_release import assert_clean, once, required, section
from generate_r072p_release import assert_mathjax_clean
from r073h_release_content import (
    CERTIFICATE_RELATIVE,
    CLOSED,
    FALSE,
    FIGURE_ID,
    FIGURE_RELATIVE,
    HOME_H_CARD,
    HOME_LATEST_SPOTLIGHT,
    HOME_NEXT,
    NOTE_ARTICLE,
    NOTE_HERO,
    OPEN,
    R073G_RELEASE_BASELINE,
    R073H_RELEASE_TARGET,
)

ROOT = Path(os.environ.get(
    "R073H_RELEASE_ROOT", Path(__file__).resolve().parents[1]
)).resolve()
PUBLIC = ROOT / "public"

ANALYTIC_SOURCE_COMMIT = "5104cca02adf8b0bf967b352b6652c7c7006a7ac"
CERTIFICATE_PACKAGE_COMMIT = "a2414fbf40908381acff0aa6f6ebf088e392a9b8"
CERTIFIED_REPORT_COMMIT = "b54d1c830a05e6366b9e95cbb4f730663435bef8"
FIGURE_RENDERER_COMMIT = "0e326be588b7318adc8bc4b8651a066fd8876038"
FIGURE_PACKAGE_COMMIT = "60a25759b0e153a6160dd48b246fb48b132c776f"
FIGURE_PACKAGE_COMMIT_PLACEHOLDER = "TO_BE_FILLED_AFTER_FIGURE_PACKAGE_COMMIT"

CLOSED_KEYS = (
    "exactHarmonicTaylorHierarchy",
    "targetHasNoQuadraticOrQuarticTerm",
    "continuumDoubledRowNumericalAbscissa",
    "localizedLinearCumulativeEnergy",
    "localizedQuadraticCubicEnergy",
    "fourthOrderExactRemainder",
    "gainNormalizedFixedDistanceDeparture",
    "selectedOrbitGlobalSmoothness",
)

FALSE_KEYS = (
    "gainLowerBoundDeterminesActualGain",
    "gainNormalizedDepartureImpliesPrescribedSeedDeparture",
    "finiteCubicCoefficientProvesContinuumSaturation",
    "familyDepartureIsSingleBackgroundLyapunovInstability",
    "planarDepartureCreatesThreeDimensionalVortexStretching",
    "planarDepartureImpliesFiniteTimeSingularity",
    "planarDepartureResolvesClay",
)

OPEN_KEYS = (
    "sharpSelectedGainAction",
    "prescribedLowerLawSeedDeparture",
    "uniformTaylorRadiusAtNaturalEndpoint",
    "fullContinuumHarmonicResolvedSemigroupEstimate",
    "singleBackgroundLyapunovSequence",
    "transverseOSSquireEvolution",
    "transverseTriadClosure",
    "finiteTimeSingularity",
    "Clay",
)

SOURCE_PATHS = (
    "research/r073h_problem_freeze.md",
    "research/r073h_harmonic_energy_proof.md",
    "research/r073h_harmonic_derivation.md",
    "research/r073h_independent_analytic_audit.md",
    "research/r073h_adversarial_audit.md",
    "research/r073h_literature_audit.md",
    "research/r073h_gap_matrix.md",
    "research/r073h_bilingual_dictionary.md",
    "research/r073h_report-source.md",
)

CERTIFICATE_FILE_PATHS = (
    "README.md",
    "certificate.json",
    "coefficient_snapshots.npz",
    "command.txt",
    "config.json",
    "cutoff_convergence.csv",
    "environment.json",
    "exact_q2_certificate.json",
    "exact_q2_certificate.py",
    "generate_certificate.py",
    "independent_exact_q2.json",
    "independent_exact_q2.py",
    "independent_progress.ndjson",
    "independent_validate.py",
    "independent_validation.json",
    "primary_diagnostic.py",
    "primary_manifest.json",
    "primary_rows.csv",
    "primary_summary.json",
    "progress.ndjson",
    "requirements.txt",
    "seal_package.py",
    "step_convergence.csv",
    "validate_certificate.py",
    "validation.json",
)

FIGURE_INPUT_PATHS = (
    "research/certificates/r073h/certificate.json",
    "research/certificates/r073h/validation.json",
    "research/certificates/r073h/cutoff_convergence.csv",
    "research/certificates/r073h/exact_q2_certificate.json",
    "research/certificates/r073h/independent_validation.json",
    "research/certificates/r073h/primary_rows.csv",
    "research/certificates/r073h/primary_summary.json",
    "research/certificates/r073h/step_convergence.csv",
)

FIGURE_SOURCE_PATHS = (
    "figures/r073h/fig-r073h-harmonic-feedback/README.md",
    "figures/r073h/fig-r073h-harmonic-feedback/caption.md",
    "figures/r073h/fig-r073h-harmonic-feedback/command.txt",
    "figures/r073h/fig-r073h-harmonic-feedback/config.json",
    "figures/r073h/fig-r073h-harmonic-feedback/contract.json",
    "figures/r073h/fig-r073h-harmonic-feedback/plot.py",
    "figures/r073h/fig-r073h-harmonic-feedback/qa-protocol.md",
    "figures/r073h/fig-r073h-harmonic-feedback/requirements.txt",
    "figures/r073h/fig-r073h-harmonic-feedback/validate.py",
)

FIGURE_FILE_PATHS = (
    "README.md",
    "caption.md",
    "command.txt",
    "config.json",
    "contract.json",
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
    "validate.py",
)

PUBLIC_VOICE_BANS = (
    "\u6211\u4eec", "\u653b\u5173", "\u4e3b\u653b", "\u7a81\u7834",
    "\u7814\u7a76\u7eaa\u5f8b", "\u4e09\u91cd\u5ba1\u8ba1", "\u6740\u6b7b\u9519\u8bef\u60f3\u6cd5",
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
    if not expected_groups:
        raise RuntimeError(label + ": no hash groups requested")
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
                raise RuntimeError(label + ": duplicate hash path in " + group + ": " + relative)
            actual_paths.append(relative)
            candidate = (base / relative) if "/" not in relative else (ROOT / relative)
            if not re.fullmatch(r"[0-9a-f]{64}", expected) or not candidate.is_file():
                raise RuntimeError(label + ": missing hash target in " + group + ": " + relative)
            if digest(candidate) != expected:
                raise RuntimeError(label + ": stale hash in " + group + ": " + relative)
            if not isinstance(row.get("bytes"), int) or candidate.stat().st_size != row["bytes"]:
                raise RuntimeError(label + ": stale byte count in " + group + ": " + relative)
        if tuple(actual_paths) != expected_paths:
            raise RuntimeError(label + ": exact path inventory drifted in " + group)


def ensure_commits_ready() -> None:
    if FIGURE_PACKAGE_COMMIT == FIGURE_PACKAGE_COMMIT_PLACEHOLDER:
        raise RuntimeError(
            "R0.73H release is intentionally sealed shut: replace "
            "TO_BE_FILLED_AFTER_FIGURE_PACKAGE_COMMIT after the formal figure commit"
        )
    chain = (
        ("analytic source", ANALYTIC_SOURCE_COMMIT),
        ("certificate package", CERTIFICATE_PACKAGE_COMMIT),
        ("certified report", CERTIFIED_REPORT_COMMIT),
        ("figure renderer", FIGURE_RENDERER_COMMIT),
        ("figure package", FIGURE_PACKAGE_COMMIT),
    )
    for label, commit in chain:
        require_commit(commit, "R0.73H " + label)
    commits = [commit for _, commit in chain]
    if len(commits) != len(set(commits)):
        raise RuntimeError("R0.73H A/C/R/E/F commits must be distinct")
    for (left_label, left), (right_label, right) in zip(chain, chain[1:]):
        if not is_ancestor(left, right):
            raise RuntimeError(f"R0.73H commit order invalid: {left_label} < {right_label}")
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True,
        capture_output=True, text=True,
    ).stdout.strip()
    if not is_ancestor(FIGURE_PACKAGE_COMMIT, head):
        raise RuntimeError("R0.73H figure package commit is not an ancestor of HEAD")


def validate_analytic_sources() -> None:
    for relative in SOURCE_PATHS:
        path = ROOT / relative
        if not path.is_file() or path.is_symlink():
            raise RuntimeError("missing R0.73H analytic source: " + relative)
        if path.read_bytes() != git_bytes(CERTIFIED_REPORT_COMMIT, relative):
            raise RuntimeError("R0.73H source differs from certified report commit: " + relative)
    report = (ROOT / "research/r073h_report-source.md").read_text(encoding="utf-8")
    gap = (ROOT / "research/r073h_gap_matrix.md").read_text(encoding="utf-8")
    proof = (ROOT / "research/r073h_harmonic_energy_proof.md").read_text(encoding="utf-8")
    derivation = (ROOT / "research/r073h_harmonic_derivation.md").read_text(encoding="utf-8")
    independent = (ROOT / "research/r073h_independent_analytic_audit.md").read_text(encoding="utf-8")
    adversarial = (ROOT / "research/r073h_adversarial_audit.md").read_text(encoding="utf-8")
    literature = (ROOT / "research/r073h_literature_audit.md").read_text(encoding="utf-8")
    dictionary = (ROOT / "research/r073h_bilingual_dictionary.md").read_text(encoding="utf-8")
    for key in CLOSED_KEYS:
        if f"`{key}` | CLOSED" not in gap:
            raise RuntimeError("R0.73H CLOSED ledger drift: " + key)
    for key in FALSE_KEYS:
        status = "FALSE" if key.startswith("planarDeparture") else "FALSE_AS_INFERENCE"
        if f"`{key}` | {status}" not in gap:
            raise RuntimeError("R0.73H FALSE ledger drift: " + key)
    for key in OPEN_KEYS:
        if f"`{key}` | OPEN" not in gap:
            raise RuntimeError("R0.73H OPEN ledger drift: " + key)
    for token in (
        "u_\\Lambda^\\delta(0)=\\frac{\\delta}{G_\\Lambda}\\phi_\\Lambda",
        "\\|\\Pi_{\\{K_z=\\pm1\\}}u_\\Lambda^\\delta(D)\\|_2",
        "H_d\\ge\\frac1{40}I", "\\|e(D)\\|_2\\le C_R\\delta^4",
        "not be restated for the prescribed seed",
    ):
        if token not in proof and token not in report:
            raise RuntimeError("R0.73H theorem source missing token: " + token)
    for token in ("(1,0)", "(0,1)", "(-1,2)", "(2,-1)", "quartic term"):
        if token not in derivation and token not in report:
            raise RuntimeError("R0.73H derivation missing token: " + token)
    if "MATHEMATICAL FINAL PASS" not in independent:
        raise RuntimeError("R0.73H independent audit is not final pass")
    if "No adversarial test above invalidates" not in adversarial:
        raise RuntimeError("R0.73H adversarial audit verdict drifted")
    for token in ("math/0508173", "2206.01318", "1707.00278", "2306.03555", "2410.23798"):
        if token not in literature:
            raise RuntimeError("R0.73H literature audit missing token: " + token)
    for token in ("gain-normalized seed", "prescribed lower-law seed", "FALSE AS INFERENCE"):
        if token not in dictionary:
            raise RuntimeError("R0.73H bilingual dictionary missing token: " + token)
    for label, value in (
        ("report", report), ("gap", gap), ("proof", proof),
        ("derivation", derivation), ("independent audit", independent),
        ("adversarial audit", adversarial), ("literature", literature),
        ("dictionary", dictionary),
    ):
        assert_public_voice(value, "R0.73H " + label)


def validate_certificate() -> dict:
    directory = ROOT / CERTIFICATE_RELATIVE
    verify_exact_directory_at_commit(directory, CERTIFICATE_PACKAGE_COMMIT, "R0.73H certificate")
    verify_flat_ledger(directory, "R0.73H certificate")
    manifest = strict_json(directory / "manifest.json", "R0.73H certificate manifest")
    certificate = strict_json(directory / "certificate.json", "R0.73H certificate")
    validation = strict_json(directory / "validation.json", "R0.73H certificate validation")
    config = strict_json(directory / "config.json", "R0.73H certificate config")
    environment = strict_json(directory / "environment.json", "R0.73H certificate environment")
    primary_manifest = strict_json(directory / "primary_manifest.json", "R0.73H primary manifest")
    primary = strict_json(directory / "primary_summary.json", "R0.73H primary summary")
    independent = strict_json(directory / "independent_validation.json", "R0.73H independent validation")
    exact = strict_json(directory / "exact_q2_certificate.json", "R0.73H exact q2")
    independent_exact = strict_json(directory / "independent_exact_q2.json", "R0.73H independent exact q2")
    schemas = {
        "manifest": (manifest, "r073h-sealed-package-manifest-v1"),
        "certificate": (certificate, "r073h-combined-certificate-v1"),
        "validation": (validation, "r073h-independent-package-validation-v1"),
        "config": (config, "r073h-harmonic-duhamel-config-v1"),
        "environment": (environment, "r073h-environment-v1"),
        "primary manifest": (primary_manifest, "r073h-primary-manifest-v1"),
        "primary summary": (primary, "r073h-harmonic-duhamel-primary-v1"),
        "independent validation": (independent, "r073h-independent-vorticity-fft-v1"),
        "exact q2": (exact, "r073h-exact-q2-ldl-v1"),
        "independent exact q2": (independent_exact, "r073h-independent-exact-q2-bareiss-v1"),
    }
    for label, (payload, expected_schema) in schemas.items():
        if payload.get("schemaVersion") != expected_schema:
            raise RuntimeError("R0.73H " + label + " schema drifted")
    if manifest.get("release") != "R0.73H" or manifest.get("allPrerequisiteChecksPass") is not True:
        raise RuntimeError("R0.73H certificate manifest failed")
    if manifest.get("sourceCommit") != ANALYTIC_SOURCE_COMMIT or manifest.get("smokeMode") is not False:
        raise RuntimeError("R0.73H certificate provenance or mode drifted")
    if certificate.get("allChecksPass") is not True or validation.get("allChecksPass") is not True:
        raise RuntimeError("R0.73H certificate or independent package validation failed")
    if primary.get("allChecksPass") is not True or primary.get("diagnosticOnly") is not True:
        raise RuntimeError("R0.73H primary finite diagnostic failed or escaped scope")
    if independent.get("allChecksPass") is not True or independent.get("diagnosticOnly") is not True:
        raise RuntimeError("R0.73H independent finite diagnostic failed or escaped scope")
    if exact.get("allChecksPass") is not True or independent_exact.get("allChecksPass") is not True:
        raise RuntimeError("R0.73H exact rational subcertificate failed")
    ledger = certificate.get("claimLedger", {})
    expected = {
        "ClayProblem": "OPEN",
        "continuumDoubledRowCoercivityArithmetic": "CLOSED_EXACT_SUBCERTIFICATE",
        "exactAmplitudeHierarchyAndKzParity": "CLOSED_BY_ALGEBRA",
        "finiteCutoffAgreementAsTailProof": "NOT_CLAIMED",
        "finiteDuhamelResponseAtFrozenGrid": "FINITE_DIAGNOSTIC_ONLY",
        "fourthAndHigherAmplitudeOrders": "OPEN",
        "fullContinuumHarmonicResolvedSemigroupEstimate": "OPEN",
        "generalThreeDimensionalRegularity": "OPEN",
        "naturalSeedOrderOneDeparture": "OPEN",
        "threeDimensionalVortexStretching": "ABSENT_FOR_SELECTED_PLANAR_LAUNCH",
        "uniformTaylorRadius": "OPEN",
    }
    if ledger != expected:
        raise RuntimeError("R0.73H certificate claim ledger is not exact")
    observations = certificate.get("finiteHarmonicDiagnostic", {}).get("observations", {})
    holdout = observations.get("holdout", {})
    gates = (
        observations.get("primaryRowCount") == 319,
        observations.get("cutoffComparisonCount") == 21,
        observations.get("stepComparisonCount") == 6,
        abs(float(observations.get("independentMaximumCoefficientRelativeError", 1)) - 2.016330215810811e-9) < 1e-20,
        abs(float(holdout.get("quadraticCompensated", 0)) - 0.9250135448921459) < 1e-14,
        abs(float(holdout.get("targetCubicCompensated", 0)) - 0.884924810690487) < 1e-14,
        abs(float(holdout.get("totalSignedCompensated", 0)) + 0.6597414810027311) < 1e-14,
        len(independent.get("validations", [])) == 5,
        sum(row.get("gridKind") == "formal" for row in independent.get("validations", [])) == 4,
        sum(row.get("gridKind") == "holdout" for row in independent.get("validations", [])) == 1,
    )
    if not all(gates):
        raise RuntimeError("R0.73H finite sentinel/holdout inventory drifted")
    if exact.get("profilePerturbation", {}).get("maximumProfileTime") != "1/450":
        raise RuntimeError("R0.73H theorem window drifted")
    verify_hash_rows(
        manifest,
        {"files": CERTIFICATE_FILE_PATHS},
        directory,
        "R0.73H certificate manifest",
    )
    return certificate


def validate_figure(certificate: dict) -> dict:
    directory = ROOT / FIGURE_RELATIVE
    verify_exact_directory_at_commit(directory, FIGURE_PACKAGE_COMMIT, "R0.73H figure")
    verify_flat_ledger(directory, "R0.73H figure")
    manifest = strict_json(directory / "manifest.json", "R0.73H figure manifest")
    validation = strict_json(directory / "validation.json", "R0.73H figure validation")
    results = strict_json(directory / "results.json", "R0.73H figure results")
    contract = strict_json(directory / "contract.json", "R0.73H figure contract")
    config = strict_json(directory / "config.json", "R0.73H figure config")
    schemas = {
        "manifest": (manifest, "r073h-formal-figure-manifest-v2"),
        "validation": (validation, "r073h-figure-validation-v1"),
        "results": (results, "r073h-formal-figure-results-v1"),
        "contract": (contract, "r073h-figure-contract-v1"),
        "config": (config, "r073h-figure-config-v1"),
    }
    for label, (payload, expected_schema) in schemas.items():
        if payload.get("schemaVersion") != expected_schema:
            raise RuntimeError("R0.73H figure " + label + " schema drifted")
    if manifest.get("release") != "R0.73H" or manifest.get("status") != "formal":
        raise RuntimeError("R0.73H figure is not formal")
    git = manifest.get("git", {})
    if git.get("certificateCommit") != CERTIFICATE_PACKAGE_COMMIT or git.get("rendererSourceCommit") != FIGURE_RENDERER_COMMIT:
        raise RuntimeError("R0.73H figure provenance chain drifted")
    if config.get("certificateCommit") != CERTIFICATE_PACKAGE_COMMIT:
        raise RuntimeError("R0.73H figure config certificate binding drifted")
    if results.get("certificateCommit") != CERTIFICATE_PACKAGE_COMMIT or results.get("rendererSourceCommit") != FIGURE_RENDERER_COMMIT:
        raise RuntimeError("R0.73H figure results provenance chain drifted")
    if validation.get("allChecksPass") is not True or validation.get("status") != "passed":
        raise RuntimeError("R0.73H figure validation failed")
    boundary = contract.get("claimBoundary", {})
    if manifest.get("claimBoundary") != boundary or results.get("claimBoundary") != boundary:
        raise RuntimeError("R0.73H figure claim boundary drifted")
    if boundary != {
        "clayProblemSolved": False,
        "exactContinuumQ2EnergySubcertificate": True,
        "finiteCubicSignIsContinuumSaturation": False,
        "finiteCutoffAgreementIsTailProof": False,
        "finiteHarmonicResponseIsContinuumSemigroupEstimate": False,
        "formalJournalFigure": True,
        "generalThreeDimensionalRegularityConclusion": False,
        "naturalSeedOrderOneDepartureEstablishedByFigure": False,
        "threeDimensionalVortexStretchingPresent": False,
    }:
        raise RuntimeError("R0.73H figure escaped its exact claim boundary")
    observations = manifest.get("observations", {})
    if results.get("observations") != observations or validation.get("keyMetrics") != observations:
        raise RuntimeError("R0.73H figure observation copies are not exact")
    if results.get("inputBindings") != manifest.get("inputs"):
        raise RuntimeError("R0.73H figure certificate input bindings disagree")
    if results.get("sourceBindings") != manifest.get("sourceBindings"):
        raise RuntimeError("R0.73H figure source bindings disagree")
    config_inputs = config.get("inputs")
    if not isinstance(config_inputs, dict) or tuple(config_inputs.values()) != FIGURE_INPUT_PATHS:
        raise RuntimeError("R0.73H figure config input inventory drifted")
    for row in manifest.get("inputs", []):
        if row.get("sourceCommit") != CERTIFICATE_PACKAGE_COMMIT:
            raise RuntimeError("R0.73H figure input escaped the certificate commit")
        if git_bytes(CERTIFICATE_PACKAGE_COMMIT, row["path"]) != (ROOT / row["path"]).read_bytes():
            raise RuntimeError("R0.73H figure input differs from the certificate commit")
    for row in manifest.get("sourceBindings", []):
        if row.get("sourceCommit") != FIGURE_RENDERER_COMMIT:
            raise RuntimeError("R0.73H figure source escaped the renderer commit")
        if git_bytes(FIGURE_RENDERER_COMMIT, row["path"]) != (ROOT / row["path"]).read_bytes():
            raise RuntimeError("R0.73H figure source differs from the renderer commit")

    exact_observations = observations.get("exact", {})
    certificate_exact = certificate.get("exactContinuumSubcertificate", {})
    if exact_observations.get("h0Lower") != certificate_exact.get("h0Lower"):
        raise RuntimeError("R0.73H figure h0 lower bound disagrees with certificate")
    if exact_observations.get("hdLower") != certificate_exact.get("hdLowerForDAtMostOneOver450"):
        raise RuntimeError("R0.73H figure hd lower bound disagrees with certificate")
    finite = observations.get("finite", {})
    certificate_grid = certificate.get("preregistration", {}).get("formalGrid", {})
    certificate_sentinels = certificate.get("preregistration", {}).get("independentSentinels", [])
    certificate_holdout = certificate.get("preregistration", {}).get("holdout", {})
    certificate_finite = certificate.get("finiteHarmonicDiagnostic", {}).get("observations", {})
    certificate_holdout_values = certificate_finite.get("holdout", {})
    if max(certificate_grid.get("profileTimeSnapshots", [-1])) != finite.get("profileEndpoint"):
        raise RuntimeError("R0.73H figure endpoint disagrees with certificate preregistration")
    if len(certificate_sentinels) != finite.get("independentFormalSentinelCount"):
        raise RuntimeError("R0.73H figure sentinel count disagrees with certificate")
    if not certificate_holdout or finite.get("independentHoldoutCount") != 1:
        raise RuntimeError("R0.73H figure holdout count disagrees with certificate")
    for figure_key, certificate_key in (
        ("holdoutQuadraticCompensated", "quadraticCompensated"),
        ("holdoutTargetCubicCompensated", "targetCubicCompensated"),
        ("holdoutTotalSignedCompensated", "totalSignedCompensated"),
    ):
        if finite.get(figure_key) != certificate_holdout_values.get(certificate_key):
            raise RuntimeError("R0.73H figure holdout metric disagrees with certificate: " + figure_key)
    for key in ("quadraticNaturalLogSlope", "targetCubicNaturalLogSlope"):
        if abs(float(finite.get(key, 0)) - float(certificate_finite.get(key, 1))) > 5e-15:
            raise RuntimeError("R0.73H figure scaling metric disagrees with certificate: " + key)
    if finite.get("profileEndpointStrictlyOutsideTheoremWindow") is not True:
        raise RuntimeError("R0.73H figure did not disclose d=0.01 outside D<=1/450")
    if abs(float(finite.get("profileEndpoint", 0)) - 0.01) > 1e-15:
        raise RuntimeError("R0.73H finite endpoint drifted")
    if abs(float(finite.get("theoremWindowUpper", 0)) - 1 / 450) > 1e-15:
        raise RuntimeError("R0.73H theorem-window ledger drifted")
    if finite.get("independentFormalSentinelCount") != 4 or finite.get("independentHoldoutCount") != 1:
        raise RuntimeError("R0.73H figure sentinel/holdout inventory drifted")
    verify_hash_rows(
        manifest,
        {
            "inputs": FIGURE_INPUT_PATHS,
            "sourceBindings": FIGURE_SOURCE_PATHS,
            "files": FIGURE_FILE_PATHS,
        },
        directory,
        "R0.73H figure manifest",
    )
    outputs = manifest.get("figure", {}).get("outputs", [])
    by_name = {Path(str(row.get("path", ""))).name: row for row in outputs if isinstance(row, dict)}
    if set(by_name) != {"figure.pdf", "figure.svg", "figure.png"}:
        raise RuntimeError("R0.73H figure output inventory is not exact")
    for name, row in by_name.items():
        path = directory / name
        if digest(path) != row.get("sha256") or path.stat().st_size != row.get("bytes"):
            raise RuntimeError("R0.73H figure output hash drifted: " + name)
    if not (directory / "figure.pdf").read_bytes().startswith(b"%PDF"):
        raise RuntimeError("R0.73H figure PDF signature invalid")
    svg = (directory / "figure.svg").read_text(encoding="utf-8").lower()
    if "<svg" not in svg or "<image" in svg or "<text" not in svg:
        raise RuntimeError("R0.73H figure SVG is absent or rasterized")
    png = (directory / "figure.png").read_bytes()
    if not png.startswith(b"\x89PNG\r\n\x1a\n") or b"pHYs" not in png:
        raise RuntimeError("R0.73H figure PNG metadata missing")
    return manifest


def validate_inputs() -> tuple[dict, dict]:
    ensure_commits_ready()
    validate_analytic_sources()
    certificate = validate_certificate()
    figure = validate_figure(certificate)
    return certificate, figure


def preflight_release_state() -> str:
    release = strict_json(ROOT / "research/release-manifest.json", "release manifest")
    site = strict_json(PUBLIC / "site-version.json", "site version")
    inventory = strict_json(ROOT / "research/formal-archive-inventory.json", "archive inventory")
    root_version = (ROOT / "VERSION").read_text(encoding="utf-8")
    if release.get("latestCompletedRelease") == "r073h":
        for key, value in R073H_RELEASE_TARGET.items():
            if release.get(key) != value:
                raise RuntimeError("R0.73H target release-manifest drifted: " + key)
        if release.get("latestReleaseGate") != "tests/r073h-gain-normalized-departure-gate.test.mjs":
            raise RuntimeError("R0.73H target gate binding drifted")
        if release.get("latestReleasePublicationTest") != "tests/r073h-release.test.mjs":
            raise RuntimeError("R0.73H target publication-test binding drifted")
        if site != {
            "schemaVersion": "research-site-version-v1",
            "version": "1.48",
            "latestRelease": "R0.73H",
            "publicHtmlNoteCount": 184,
            "publishedDate": "2026-08-30",
        }:
            raise RuntimeError("R0.73H target site-version is not exact")
        if root_version != "1.48\n":
            raise RuntimeError("R0.73H target VERSION is not 1.48")
        state = (
            inventory.get("latestPublishedRelease"),
            inventory.get("publishedReleaseCount"),
            inventory.get("formalSealedReleaseCount"),
            inventory.get("legacyFormalFigureBacklogCount"),
        )
        if state != ("r073h", 86, 62, 24):
            raise RuntimeError("R0.73H target formal archive is not exact")
        baseline_inventory = json.loads(git_bytes(
            FIGURE_PACKAGE_COMMIT, "research/formal-archive-inventory.json"
        ))
        expected_inventory = json.loads(json.dumps(baseline_inventory))
        for key in ("publishedReleases", "formalSealedReleases"):
            rows = expected_inventory.get(key)
            if not isinstance(rows, list) or rows[-1:] != ["r073g"] or "r073h" in rows:
                raise RuntimeError("R0.73H sealed baseline inventory is invalid: " + key)
            rows.append("r073h")
        expected_inventory.update({
            "latestPublishedRelease": "r073h",
            "publishedReleaseCount": 86,
            "formalSealedReleaseCount": 62,
            "legacyFormalFigureBacklogCount": 24,
        })
        if inventory != expected_inventory:
            raise RuntimeError("R0.73H target formal archive is not the exact append-only successor")
        for key, count in (("publishedReleases", 86), ("formalSealedReleases", 62)):
            rows = inventory[key]
            if len(rows) != count or len(set(rows)) != count:
                raise RuntimeError("R0.73H target archive sequence is not unique: " + key)
        if not set(inventory["formalSealedReleases"]).issubset(inventory["publishedReleases"]):
            raise RuntimeError("R0.73H sealed releases are not a subset of published releases")
        inventory_binding = release.get("formalArchiveInventory", {})
        if inventory_binding != {
            "path": "research/formal-archive-inventory.json",
            "sha256": digest(ROOT / "research/formal-archive-inventory.json"),
        }:
            raise RuntimeError("R0.73H target archive-inventory binding drifted")
        if len(list((PUBLIC / "notes").glob("r0-*.html"))) != 184:
            raise RuntimeError("R0.73H target note count is not 184")
        target_html: dict[str, str] = {}
        for relative in (
            "notes/r0-73h.html",
            "recap-r0-61-r0-73h.html",
            "research-review.html",
            "literature-review.html",
            "notes/index.html",
        ):
            path = PUBLIC / relative
            if not path.is_file() or path.is_symlink():
                raise RuntimeError("R0.73H target HTML missing: " + relative)
            value = path.read_text(encoding="utf-8")
            assert_clean(value, "R0.73H target " + relative)
            assert_mathjax_clean(
                value,
                "R0.73H target " + relative,
                check_naked=True,
            )
            assert_public_voice(value, "R0.73H target " + relative)
            if "/i18n-en.js?v=1.48" not in value:
                raise RuntimeError("R0.73H target HTML has stale i18n cache: " + relative)
            target_html[relative] = value
        note = target_html["notes/r0-73h.html"]
        for token in (
            CLOSED, FALSE, OPEN, "CONTINUUM THEOREM", "NOT CLAY",
            "d=0.01>1/450", "4 个预注册独立哨兵", "1 个独立 holdout",
        ):
            if token not in note:
                raise RuntimeError("R0.73H target note lost boundary token: " + token)
        recap = target_html["recap-r0-61-r0-73h.html"]
        start = recap.find('<section id="node-index">')
        end = recap.find("</section>", start)
        if start < 0 or end <= start:
            raise RuntimeError("R0.73H target recap node index is absent")
        recap_links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', recap[start:end])
        if len(recap_links) != 124 or len(set(recap_links)) != 124:
            raise RuntimeError("R0.73H target recap node inventory is not 124 unique links")
        if recap.count('<article class="phase">') != 43:
            raise RuntimeError("R0.73H target recap phase inventory is not 43")
        home = target_html["research-review.html"]
        route = re.search(
            r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73H">(.*?)</nav>',
            home,
            flags=re.S,
        )
        route_links = [] if route is None else re.findall(
            r'href="/notes/(r0-[^"]+)\.html"', route.group(1)
        )
        if len(route_links) != 94 or len(set(route_links)) != 94:
            raise RuntimeError("R0.73H target home route is not 94 unique links")
        if 'id="r073h"' not in home or "/notes/r0-73h.html" not in home:
            raise RuntimeError("R0.73H target home card is absent")
        if (
            "uniformTaylorRadiusAtNaturalEndpoint" not in home
            or "专指按下界指数预设种子的全阶 Taylor 半径" not in home
        ):
            raise RuntimeError("R0.73H target home Taylor-radius boundary is absent")
        if 'data-note="r0-73h"' not in target_html["notes/index.html"]:
            raise RuntimeError("R0.73H target note-index entry is absent")
        literature = target_html["literature-review.html"]
        if 'id="r073h-boundary"' not in literature:
            raise RuntimeError("R0.73H target literature boundary is absent")
        if (
            'class="route-r073h-deck-update"' not in literature
            or "R0.73H 再以实际增益归一化和谐波能量局部化" not in literature
            or "d=0.01>1/450" not in literature
        ):
            raise RuntimeError("R0.73H target literature route deck endpoint is absent")
        return "target"

    if any(release.get(key) != value for key, value in R073G_RELEASE_BASELINE.items()):
        raise RuntimeError("R0.73H release state is neither exact R0.73G source nor exact R0.73H target")
    if site != {
        "schemaVersion": "research-site-version-v1",
        "version": "1.47",
        "latestRelease": "R0.73G",
        "publicHtmlNoteCount": 183,
        "publishedDate": "2026-08-30",
    }:
        raise RuntimeError("R0.73H site-version baseline is not exact")
    if root_version != "1.47\n":
        raise RuntimeError("R0.73H VERSION baseline is not 1.47")
    state = (
        inventory.get("latestPublishedRelease"),
        inventory.get("publishedReleaseCount"),
        inventory.get("formalSealedReleaseCount"),
        inventory.get("legacyFormalFigureBacklogCount"),
    )
    if state != ("r073g", 85, 61, 24):
        raise RuntimeError("R0.73H formal archive baseline is not exact")
    notes = list((PUBLIC / "notes").glob("r0-*.html"))
    if len(notes) != 183:
        raise RuntimeError("R0.73H expected exactly 183 baseline HTML notes")
    absent = (
        PUBLIC / "notes/r0-73h.html",
        PUBLIC / "notes/r0-73h.pdf",
        PUBLIC / "recap-r0-61-r0-73h.html",
        PUBLIC / "recap-r0-61-r0-73h.pdf",
        PUBLIC / "assets/r073h",
    )
    for path in absent:
        if path.exists() or path.is_symlink():
            raise RuntimeError("R0.73H baseline path already exists: " + str(path))
    for relative, tokens in {
        "research-review.html": ("R0.73G", "183", "R0.73H"),
        "literature-review.html": ("R0.73G", "开放接口 · R0.73H"),
        "notes/index.html": ("R0.73G", "183 篇公开研究笔记"),
        "recap-r0-61-r0-73g.html": ("R0.61–R0.73G", "123", "四十二"),
    }.items():
        value = (PUBLIC / relative).read_text(encoding="utf-8")
        for token in tokens:
            if token not in value:
                raise RuntimeError(f"R0.73H baseline {relative} missing {token}")
    return "source"


def build_note() -> str:
    html = (PUBLIC / "notes/r0-73g.html").read_text(encoding="utf-8")
    metadata = (
        ("description", r'<meta name="description" content=".*?">',
         '<meta name="description" content="研究笔记 R0.73H：实际增益归一化种子在平面背景族上产生固定距离偏离；预设指数种子、固定背景、横向三维与 Clay 仍开放。">'),
        ("og title", r'<meta property="og:title" content=".*?">',
         '<meta property="og:title" content="R0.73H｜Gain-normalized planar fixed-distance departure">'),
        ("og description", r'<meta property="og:description" content=".*?">',
         '<meta property="og:description" content="Harmonic energy localization closes a fixed-distance planar departure for an actual-gain-normalized seed; matching gain action and transverse 3D remain open.">'),
        ("og image", r'<meta property="og:image" content=".*?">',
         f'<meta property="og:image" content="https://kasifa.github.io/assets/r073h/{FIGURE_ID}.png">'),
        ("title", r'<title>.*?</title>',
         '<title>R0.73H｜Gain-normalized planar fixed-distance departure</title>'),
    )
    for label, pattern, value in metadata:
        html = section(html, pattern, value, "G note " + label)
    html = required(html, "/i18n-en.js?v=1.47", "/i18n-en.js?v=1.48", "G note i18n")
    toc_items = (
        ("result", "00 · direct decision"),
        ("theorem", "01 · main theorem"),
        ("normalization", "02 · actual-gain normalization"),
        ("hierarchy", "03 · harmonic hierarchy"),
        ("leray", "04 · exact Leray algebra"),
        ("abscissa", "05 · doubled-row bound"),
        ("localization", "06 · localized energies"),
        ("remainder", "07 · fourth-order remainder"),
        ("endpoint", "08 · endpoint"),
        ("finite", "09 · finite diagnostic"),
        ("certificate", "10 · exact certificate"),
        ("literature", "11 · literature boundary"),
        ("audit", "12 · independent audit"),
        ("figure", "13 · journal figure"),
        ("boundary", "14 · exact boundary"),
        ("value", "15 · value"),
        ("next", "16 · R0.73I"),
        ("reproduce", "17 · reproduction"),
    )
    nav = "<nav>" + "".join(
        f'<a href="#{anchor}">{label.split(" · ", 1)[1]}</a>'
        for anchor, label in toc_items
    ) + '<a href="/">返回主页</a></nav>'
    html = section(html, r'<nav><a href="#result">.*?</nav>', nav, "G note nav")
    html = section(html, r'    <header class="hero">.*?</header>', NOTE_HERO, "G note hero")
    toc = (
        '      <aside class="toc"><strong>CONTENTS</strong><ol>\n'
        + "".join(f'        <li><a href="#{anchor}">{label}</a></li>' for anchor, label in toc_items)
        + "\n      </ol></aside>"
    )
    html = section(html, r'      <aside class="toc">.*?</aside>', toc, "G note toc")
    html = section(html, r'      <article>.*?</article>', NOTE_ARTICLE, "G note article")
    footer = (
        "<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>"
        "我按原编号记录推导、反例和未解决的问题。</div>"
        '<div>研究笔记 R0.73H · 2026-08-30<br><a href="/">返回研究主页</a></div></footer>'
    )
    html = section(html, r"<footer>.*?</footer>", footer, "G note footer")
    match = re.search(r"<nav>(.*?)</nav>", html, flags=re.S)
    anchors = re.findall(r'href="#([^"]+)"', match.group(1)) if match else []
    expected = [anchor for anchor, _ in toc_items]
    if anchors != expected or len(anchors) != len(set(anchors)):
        raise RuntimeError("R0.73H note nav anchors are not unique and ordered")
    assert_clean(html, "R0.73H note")
    assert_mathjax_clean(html, "R0.73H note")
    assert_public_voice(html, "R0.73H note")
    return html


def build_recap() -> str:
    html = (PUBLIC / "recap-r0-61-r0-73g.html").read_text(encoding="utf-8")
    metadata = (
        ("description", r'<meta name="description" content=".*?">',
         '<meta name="description" content="R0.60 之后的完整研究回顾：R0.61 到 R0.73H 共 124 个节点；最新一节闭合按实际增益归一化的平面固定距离偏离。">'),
        ("og title", r'<meta property="og:title" content=".*?">',
         '<meta property="og:title" content="R0.61–R0.73H｜R0.60 之后的研究回顾">'),
        ("og description", r'<meta property="og:description" content=".*?">',
         '<meta property="og:description" content="43 个阶段、124 个节点：从约化递推和环带排除到按实际增益归一化的平面固定距离偏离。">'),
        ("title", r"<title>.*?</title>",
         "<title>R0.61–R0.73H｜R0.60 之后的研究回顾</title>"),
    )
    for label, pattern, value in metadata:
        html = section(html, pattern, value, "G recap " + label)
    html = required(html, "/i18n-en.js?v=1.47", "/i18n-en.js?v=1.48", "G recap i18n")
    hero = r'''    <header class="hero"><div class="hero-inner"><div><div class="eyebrow">累计回顾 · R0.61–R0.73H · 2026-08-30</div><h1>R0.60 之后的研究回顾</h1><p class="lead">这页保留 R0.61 到 R0.73H 的全部 124 个节点。R0.61–R0.69W 从约化递推走到严格环带排除；R0.70A–R0.71Z 检查移动尺度、临界账本、内部 entry 与 complete-root 边界；R0.72A–R0.73B 处理 strong coupling、critical log、碰撞几何与完整线性 Fourier--Leray 行；R0.73C–F 依次认证冻结 Rayleigh 不稳定、黏性谱簇持续、固定正半平面传递和移动剖面固定窗口增益；R0.73G 闭合过小种子的非线性相对放大与二维屏障；R0.73H 再以实际选定增益归一化，通过谐波能量局部化得到趋零初态的固定距离端点。预设指数种子、固定背景、横向三维、奇性与 Clay 没有被外推。</p></div><div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.73H</strong><p>收录节点：124</p><p>回顾截止时公开笔记：184</p><p>回顾截止节点：R0.73H</p><p>问题状态：仍未解决</p></div></div></header>'''
    html = section(html, r'    <header class="hero">.*?</header>', hero, "G recap hero")
    for old, new in (
        ("02 · 123 节完整索引", "02 · 124 节完整索引"),
        ("01 · 四十二个研究阶段", "01 · 43 个研究阶段"),
        ("R0.60 之后的路线分成四十二个阶段", "R0.60 之后的路线分成 43 个阶段"),
        ('data-current-route="R0.69P–R0.73G"', 'data-current-route="R0.69P–R0.73H"'),
    ):
        html = required(html, old, new, "G recap counter")
    result = r'''        <section id="result"><div class="section-no">00 / 回顾范围</div><h2>版本数、封存数和数学结论分开报告</h2><div class="metrics"><div class="metric"><strong>124</strong><span>R0.61–R0.73H 研究节点</span></div><div class="metric"><strong>86</strong><span>R0.70A–R0.73H 已公开版本</span></div><div class="metric"><strong>62</strong><span>当前 formal-figure 合同下完整封存</span></div><div class="metric"><strong>24</strong><span>旧版附图档案待回补</span></div></div><p>R0.00–R0.60 保留在上一份阶段回顾。R0.70A–R0.73H 的 86 个版本已经公开，其中 62 个满足当前完整封存合同，24 个历史版本仍欠 formal-figure 回补。公开和封存不表示 Clay 问题已经解决。</p></section>'''
    html = section(html, r'        <section id="result">.*?</section>', result, "G recap result")
    phase = r'''            <article class="phase"><h3>R0.73H · Gain-normalized planar fixed-distance departure</h3><p>对实际选定增益 \(G_\Lambda\) 归一化的初态，精确谐波选择律、倍频行连续数值横坐标界、Stieltjes 累计能量局部化与四阶余项估计给出固定端点目标行下界 \(\delta/2\)。初始 \(H^3\) 范数同时趋于零。</p><p>正式有限计算含 4 个预注册独立哨兵和 1 个独立 holdout。全部响应使用 \(d=0.01>1/450\)，严格在定理区间之外；有限三次负号不证明连续饱和。预设指数种子、固定背景 Lyapunov 不稳定、横向三维、奇性与 Clay 保持 OPEN。</p><p>__CLOSED__。__FALSE__。__OPEN__。其中 <code>uniformTaylorRadiusAtNaturalEndpoint</code> 专指预设下界指数种子的全阶 Taylor 半径。</p><div class="links"><a href="/notes/r0-73h.html">R0.73H</a><a href="/assets/r073h/__FIGURE_ID__.pdf">R0.73H 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073h">R0.73H 证书</a></div></article>
'''.replace("__CLOSED__", CLOSED).replace("__FALSE__", FALSE).replace("__OPEN__", OPEN).replace("__FIGURE_ID__", FIGURE_ID)
    marker = '          </div>\n        </section>\n\n        <section id="node-index">'
    html = once(html, marker, phase + marker, "G recap phase")
    html = required(html, "R0.61–R0.73G 的 123 节公开笔记", "R0.61–R0.73H 的 124 节公开笔记", "G recap node title")
    node_g = '            <span class="node-ref"><a href="/notes/r0-73g.html">R0.73G</a><span class="node-state kind-closed">闭</span></span>\n'
    node_h = '            <span class="node-ref"><a href="/notes/r0-73h.html">R0.73H</a><span class="node-state kind-closed">闭</span></span>\n'
    html = once(html, node_g, node_g + node_h, "G recap node")
    retained = '            <li>R0.73H 对实际选定增益归一化的趋零初态闭合固定距离端点；预设下界指数种子的匹配尺度、固定背景、横向三维、奇性与 Clay 保持 OPEN。</li>\n'
    html = once(html, "          </ul>\n          <p>这些结果可以分别整理成", retained + "          </ul>\n          <p>这些结果可以分别整理成", "G recap retained")
    value = r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>实际增益归一化把相对放大推进为固定距离端点</h2><p>不能把 124 个节点或 86 个公开版本解释成 Clay 完成比例。R0.73H 的严格增量是 varying-background planar fixed-distance departure；种子依赖未知的实际增益，所选轨道全局光滑，不含固定背景、横向三维 vortex stretching 或奇性结论。</p></section>'''
    html = section(html, r'        <section id="value">.*?</section>', value, "G recap value")
    next_gate = r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.73I 建立选定增益的匹配作用量</h2><p>优先给 \(G_\Lambda\) 建立匹配上、下作用量，判断 \(\delta/G_\Lambda\) 能否改写为可预设的显式指数尺度。该门未闭合前，不把本节结论称为自然尺度阈值。</p></section>'''
    html = section(html, r'        <section id="next">.*?</section>', next_gate, "G recap next")
    claims = r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2><p>R0.70A–R0.73H 的 86 节已公开；62 节完整封存；24 节旧档待回补。</p><p>__CLOSED__。</p><p>__FALSE__。</p><p>__OPEN__。</p><p><code>uniformTaylorRadiusAtNaturalEndpoint</code> 只指预设下界指数种子的全阶 Taylor 半径，不否定本节 gain-normalized 四阶直接余项已经闭合。</p></section>'''
    claims = claims.replace("__CLOSED__", CLOSED).replace("__FALSE__", FALSE).replace("__OPEN__", OPEN)
    html = section(html, r'        <section id="claims">.*?</section>', claims, "G recap claims")
    reproduce = r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证明、审计、证书、附图和历史回顾</h2><p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-73g.html">保留 R0.73G 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-73h.html">打开最新节点 R0.73H</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073h_harmonic_energy_proof.md">查看 R0.73H 证明</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073h_harmonic_derivation.md">查看谐波推导</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073h_independent_analytic_audit.md">查看独立解析审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073h">查看正式证书</a> · <a href="/assets/r073h/__FIGURE_ID__.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-73h.pdf">下载同步 PDF</a></p><p>continuum theorem 来自解析证明和独立解析审计。\(d=0.01\) 的 Fourier 数据只做有限诊断。</p></section>'''.replace("__FIGURE_ID__", FIGURE_ID)
    html = section(html, r'        <section id="reproduce">.*?</section>', reproduce, "G recap reproduce")
    footer = '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>我按原编号记录推导、反例和未解决的问题。</div><div>R0.61–R0.73H 回顾 · 2026-08-30<br><a href="/">返回研究主页</a></div></footer>'
    html = section(html, r"<footer>.*?</footer>", footer, "G recap footer")
    start = html.index('<section id="node-index">')
    end = html.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', html[start:end])
    if len(links) != 124 or len(set(links)) != 124:
        raise RuntimeError("R0.73H recap expected 124 unique nodes")
    if html.count('<article class="phase">') != 43:
        raise RuntimeError("R0.73H recap expected 43 phases")
    if "R0.60 之后的研究回顾" not in html or ">R0.61<" not in html:
        raise RuntimeError("R0.73H recap must start after R0.60, at R0.61")
    assert_clean(html, "R0.73H recap")
    assert_mathjax_clean(html, "R0.73H recap", check_naked=False)
    assert_public_voice(html, "R0.73H recap")
    return html


def update_home() -> str:
    html = (PUBLIC / "research-review.html").read_text(encoding="utf-8")
    html = section(
        html,
        r'    <section class="route-overview latest-release-spotlight".*?</section>',
        HOME_LATEST_SPOTLIGHT,
        "G home latest spotlight",
    )
    for old, new in (
        ('data-site-version="1.47"', 'data-site-version="1.48"'),
        ("/i18n-en.js?v=1.47", "/i18n-en.js?v=1.48"),
        ("/site-refresh.js?v=1.47", "/site-refresh.js?v=1.48"),
        ("<strong>v1.47</strong>网页版本", "<strong>v1.48</strong>网页版本"),
        ("<strong>183</strong>公开研究笔记", "<strong>184</strong>公开研究笔记"),
        ("<strong>R0.73G</strong>最新研究节点", "<strong>R0.73H</strong>最新研究节点"),
        ('<a class="route-map-latest" href="#r073g">跳到首页 R0.73G 卡片 →</a>', '<a class="route-map-latest" href="#r073h">跳到首页 R0.73H 卡片 →</a>'),
        ("natural seed / harmonic remainder / transverse 3D coupling", "selected gain matching action / prescribed seed scale"),
        ("Research topology · R0.1–R0.73G", "Research topology · R0.1–R0.73H"),
        ("R0.70A–R0.73G：85 节已公开，61 节完整封存", "R0.70A–R0.73H：86 节已公开，62 节完整封存"),
        ('<span class="route-range">R0.69P–R0.73G</span>', '<span class="route-range">R0.69P–R0.73H</span>'),
        ('aria-label="R0.69P–R0.73G"', 'aria-label="R0.69P–R0.73H"'),
        ("展开 93 篇公开笔记", "展开 94 篇公开笔记"),
        ("本站 R0.69P–R0.73G 路线", "本站 R0.69P–R0.73H 路线"),
        ("五条文献主干", "5 条文献主干"),
        ("综述 v1.47 · 2026-08-30", "综述 v1.48 · 2026-08-30"),
        ("上次综述 v1.46 · 2026-08-30", "上次综述 v1.47 · 2026-08-30"),
    ):
        html = required(html, old, new, "G home " + old)
    html = replace_all(html, "/recap-r0-61-r0-73g.html", "/recap-r0-61-r0-73h.html", "G home recap HTML links")
    html = replace_all(html, "/recap-r0-61-r0-73g.pdf", "/recap-r0-61-r0-73h.pdf", "G home recap PDF links")
    html = required(
        html,
        r"(1.20506130214380835\times10^{-8})",
        r"\(1.20506130214380835\times10^{-8}\)",
        "G home inherited naked TeX repair",
    )
    historical = '<strong style="color:var(--gold)">下一步 R0.73H：</strong>&nbsp;冻结自然种子的 harmonic-resolved 余项，并建立 transverse 3D coupling 的精确接口。'
    html = required(html, historical, historical.replace("下一步", "当时的下一步"), "G home historical next")
    focus = r'<div class="summary-item"><strong>我目前关注</strong><span>R0.73H 已对实际增益归一化的趋零初态闭合平面固定距离偏离。下一关建立选定增益 \(G_\Lambda\) 的匹配作用量，判断能否得到可预设的显式指数种子。</span></div>'
    html = section(html, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', focus, "G home focus")
    html = required(html, "<h3>R0.73G：过小种子的非线性相对放大与精确二维屏障已闭合</h3>", "<h3>R0.73H：按实际增益归一化的平面固定距离偏离已闭合</h3>", "G home current title")
    html = required(html, "<span>R0.72R–R0.73G：</span>", "<span>R0.72R–R0.73H：</span>", "G home path range")
    html = required(
        html,
        "moving-profile fixed-window dichotomy → over-small-seed nonlinear relative amplification / exact planar barrier</p>",
        "moving-profile fixed-window dichotomy → over-small-seed nonlinear relative amplification / exact planar barrier → actual-gain-normalized planar fixed-distance departure</p>",
        "G home path tail",
    )
    link_g = '<a class="milestone" href="/notes/r0-73g.html">R0.73G</a>'
    html = once(html, link_g, link_g + '\n                  <a class="milestone" href="/notes/r0-73h.html">R0.73H</a>', "G home route link")
    route_g = '              <p>R0.73G 用显式 \\(H^3\\) bootstrap 和全模态 \\(L^2\\) 余项估计，把 R0.73F 的一行下界升级为一个过小种子的非线性相对放大。所选真实轨道同时严格留在全局光滑的二维不变子空间；自然种子、order-one departure、横向三维与 Clay 保持 OPEN。</p>\n'
    route_h = '              <p>R0.73H 用实际选定增益归一化初态，并以精确谐波选择律、倍频行连续数值横坐标界、Stieltjes 局部化和四阶余项闭合平面固定距离偏离。预设指数种子、固定背景、横向三维、奇性与 Clay 保持 OPEN。</p>\n'
    html = once(html, route_g, route_h, "G home current route summary")
    html = section(html, r'            <article class="tree-node next">.*?</article>', HOME_NEXT, "G home next gate")
    recap = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem"><p class="eyebrow">累计回顾 R0.61–R0.73H · 2026-08-30</p><h3>R0.60 recap 之后的累计回顾收录 124 个节点；全站现有 184 篇公开研究笔记</h3><p>累计回顾现分 43 个阶段，完整保留 R0.61–R0.73H；最新节点分开记录 continuum theorem、exact subcertificate、finite diagnostic、文献边界和 open gate。</p><p>R0.70A–R0.73H 共 86 个版本已公开；62 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p><p><strong>阶段判断：</strong>&nbsp;实际增益归一化的平面固定距离偏离已经闭合；预设指数种子的匹配尺度、固定背景、横向三维、奇性与 Clay 保持 OPEN。</p><p><a href="/recap-r0-61-r0-73h.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-73h.pdf">下载同步 PDF</a></p></div>'''
    html = section(html, r'          <div class="task-one" id="post-r060-recap".*?</div>', recap, "G home recap")
    marker = '          </div>\n        </section>\n\n      </article>'
    html = once(html, marker, '          </div>\n\n' + HOME_H_CARD + '\n        </section>\n\n      </article>', "G home card")
    if html.count('data-release="r073h"') != 1:
        raise RuntimeError("home must contain exactly one R0.73H card")
    if html.count('<strong style="color:var(--gold)">下一步 R0.73I：') != 1:
        raise RuntimeError("home must contain exactly one current R0.73I gate")
    route = re.search(r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73H">(.*?)</nav>', html, flags=re.S)
    if route is None or len(re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))) != 94:
        raise RuntimeError("home current-route index must contain 94 note links")
    assert_clean(html, "R0.73H home")
    assert_mathjax_clean(html, "R0.73H home")
    assert_public_voice(html, "R0.73H home")
    return html


def update_literature() -> str:
    html = (PUBLIC / "literature-review.html").read_text(encoding="utf-8")
    for old, new in (
        ("/i18n-en.js?v=1.47", "/i18n-en.js?v=1.48"),
        ("本站 R0.69P–R0.73G 只列为研究笔记", "本站 R0.69P–R0.73H 只列为研究笔记"),
        ("文献综述 v1.47 · 2026-08-30", "文献综述 v1.48 · 2026-08-30"),
        ("累计回顾与 123 节索引", "累计回顾与 124 节索引"),
        ("打开 123 节完整索引", "打开 124 节完整索引"),
    ):
        html = required(html, old, new, "G literature " + old)
    html = replace_all(html, "/recap-r0-61-r0-73g.html", "/recap-r0-61-r0-73h.html", "G literature recap links")
    deck_g = "R0.73G 再用显式强范数 bootstrap 与全模态余项能量估计，把该一行下界升级为过小种子的 nonlinear relative amplification；所选真实轨道严格留在全局光滑二维子空间。自然种子、order-one departure、横向三维与 Clay 保持 OPEN。</p>"
    deck_h = deck_g[:-4] + '<span class="route-r073h-deck-update">R0.73H 再以实际增益归一化和谐波能量局部化闭合 varying-background planar fixed-distance departure；\(d=0.01>1/450\) 仅属有限诊断，预设下界指数种子、固定背景 Lyapunov 不稳定、横向三维、奇性与 Clay 保持 OPEN。</span></p>'
    html = required(html, deck_g, deck_h, "G literature route deck H endpoint")
    old_open = r'<div class="route-step pause"><header><b>开放接口 · R0.73H</b><strong>natural seed, harmonic remainder, and transverse 3D coupling</strong></header><p>分离 even 二阶响应与 odd 三阶反馈，检验自然种子的 order-one departure；再建立 \(K_x\ne0\) 或非零第一速度分量的横向三维接口。</p></div>'
    new_steps = r'''<div class="route-step kept"><header><b>R0.73H</b><strong>gain-normalized planar fixed-distance departure</strong></header><p>实际选定增益归一化、精确谐波选择律、倍频行连续数值横坐标界、Stieltjes 局部化与四阶余项给出趋零初态的固定距离端点。有限诊断使用 \(d=0.01>1/450\)，不承担连续定理。<a href="/notes/r0-73h.html">研究笔记</a> <a href="/recap-r0-61-r0-73h.html">当前累计回顾</a> <a href="#r073h-boundary">文献边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.73I</b><strong>matching action for the selected gain</strong></header><p>为 \(G_\Lambda\) 建立匹配上、下作用量，判断 gain-normalized seed 能否改写为可预设的显式指数尺度。</p></div>'''
    html = once(html, old_open, new_steps, "G literature route")
    boundary = r'''

          <h3 id="r073h-boundary">R0.73H 的谐波能量、实际增益归一化与有限诊断边界</h3>
          <p><a href="https://arxiv.org/abs/math/0508173">Friedlander--Pavlović--Shvydkoy 2006</a>给出谱不稳定到非线性不稳定的经典框架；<a href="https://arxiv.org/abs/2206.01318">Bian--Grenier 2022</a>讨论边界层中的三次相互作用与饱和；<a href="https://arxiv.org/abs/1707.00278">Lin--Xu 2019</a>、<a href="https://arxiv.org/abs/2306.03555">Li--Zhao 2024</a>、<a href="https://arxiv.org/abs/2410.23798">Li--Zhao 2025</a>和<a href="https://arxiv.org/abs/2203.10894">Li--Masmoudi--Zhao 2024</a>分别处理周期 Kolmogorov 流、热演化单调剪切、黏性驱动不稳定与近 Couette 阈值。R0.73H 的几何、谱输入和 gain-normalized endpoint 不由这些工作直接推出。本节只作有界 non-collision 检查，不作首创或优先权声明。</p>
          <div class="boundary"><strong>R0.73H 的主张边界</strong><p>__CLOSED__。</p><p>__FALSE__。</p><p>__OPEN__。其中 <code>uniformTaylorRadiusAtNaturalEndpoint</code> 专指按下界指数预设种子的全阶 Taylor 半径。\(d=0.01\) 的有限三次负号不证明 continuum saturation。</p></div>'''
    boundary = boundary.replace("__CLOSED__", CLOSED).replace("__FALSE__", FALSE).replace("__OPEN__", OPEN)
    match = re.search(r'(<h3 id="r073g-boundary">.*?<div class="boundary">.*?</div>)', html, flags=re.S)
    if match is None:
        raise RuntimeError("G literature expected R0.73G boundary")
    html = once(html, match.group(1), match.group(1) + boundary, "G literature boundary")
    references = r'''            <li id="ref-134">Z. Lin and M. Xu. <a href="https://arxiv.org/abs/1707.00278"><em>Metastability of Kolmogorov flows and inviscid damping of shear flows</em></a>. Archive for Rational Mechanics and Analysis 231 (2019), 1811--1852.</li>
            <li id="ref-135">H. Li and N. Masmoudi and W. Zhao. <a href="https://arxiv.org/abs/2203.10894"><em>A dynamical approach to the study of instability near Couette flow</em></a>. Communications on Pure and Applied Mathematics 77 (2024), 3387--3452.</li>
            <li id="ref-136">H. Li and W. Zhao. <a href="https://arxiv.org/abs/2306.03555"><em>Asymptotic stability in the critical space of 2D monotone shear flow in the viscous fluid</em></a>. Communications in Mathematical Physics 405 (2024), article 228.</li>
            <li id="ref-137">H. Li and W. Zhao. <a href="https://arxiv.org/abs/2410.23798"><em>Viscosity driven instability of shear flows without boundaries</em></a>. Journal de Mathématiques Pures et Appliquées 197 (2025), 103724.</li>
            <li id="ref-138">O. A. Ladyzhenskaya. <a href="https://doi.org/10.1002/cpa.3160120303"><em>Solution in the large of the nonstationary boundary value problem for the Navier--Stokes system with two space variables</em></a>. Communications on Pure and Applied Mathematics 12 (1959), 427--433.</li>
'''
    html = once(html, '          </ol>\n          <p class="source-note">', references + '          </ol>\n          <p class="source-note">', "G literature references")
    assert_clean(html, "R0.73H literature")
    assert_mathjax_clean(html, "R0.73H literature", check_naked=False)
    assert_public_voice(html, "R0.73H literature")
    return html


def build_manifest_outputs() -> dict[Path, bytes]:
    release_path = ROOT / "research/release-manifest.json"
    release = strict_json(release_path, "release manifest")
    for key, value in R073G_RELEASE_BASELINE.items():
        if release.get(key) != value:
            raise RuntimeError("release manifest changed during R0.73H generation: " + key)
    release.update({
        **R073H_RELEASE_TARGET,
        "latestReleaseGate": "tests/r073h-gain-normalized-departure-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r073h-release.test.mjs",
    })
    release.pop("nextReleaseSourceStage", None)

    site_path = PUBLIC / "site-version.json"
    site = strict_json(site_path, "site version")
    if site != {
        "schemaVersion": "research-site-version-v1",
        "version": "1.47",
        "latestRelease": "R0.73G",
        "publicHtmlNoteCount": 183,
        "publishedDate": "2026-08-30",
    }:
        raise RuntimeError("site-version changed during R0.73H generation")
    site.update({
        "version": "1.48",
        "latestRelease": "R0.73H",
        "publicHtmlNoteCount": 184,
        "publishedDate": "2026-08-30",
    })

    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = strict_json(inventory_path, "formal archive inventory")
    state = (
        inventory.get("latestPublishedRelease"), inventory.get("publishedReleaseCount"),
        inventory.get("formalSealedReleaseCount"), inventory.get("legacyFormalFigureBacklogCount"),
    )
    if state != ("r073g", 85, 61, 24):
        raise RuntimeError("formal archive changed during R0.73H generation")
    for key in ("publishedReleases", "formalSealedReleases"):
        if inventory[key][-1] != "r073g" or "r073h" in inventory[key]:
            raise RuntimeError("formal archive is not append-only: " + key)
        inventory[key].append("r073h")
    inventory.update({
        "latestPublishedRelease": "r073h",
        "publishedReleaseCount": 86,
        "formalSealedReleaseCount": 62,
        "legacyFormalFigureBacklogCount": 24,
    })
    if len(inventory["publishedReleases"]) != 86 or len(inventory["formalSealedReleases"]) != 62:
        raise RuntimeError("formal archive count mismatch after R0.73H")
    inventory_payload = json_bytes(inventory)
    release["formalArchiveInventory"] = {
        "path": "research/formal-archive-inventory.json",
        "sha256": sha256_bytes(inventory_payload),
    }
    return {
        release_path: json_bytes(release),
        site_path: json_bytes(site),
        inventory_path: inventory_payload,
        ROOT / "VERSION": b"1.48\n",
    }


def build_note_index(site_payload: bytes) -> str:
    import generate_note_index as note_index

    existing = [note_index.parse_note(path) for path in note_index.note_files()]
    if len(existing) != 183 or any(note.slug == "r0-73h" for note in existing):
        raise RuntimeError("R0.73H note-index baseline is not exact")
    latest = note_index.Note(
        slug="r0-73h", code="R0.73H",
        title="Gain-normalized planar fixed-distance departure",
        major=73, has_pdf=True,
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
        note_index.latest_recap_href = lambda: "/recap-r0-61-r0-73h.html"
        index = note_index.render([latest] + existing)
    finally:
        note_index.json = old_json
        note_index.latest_recap_href = old_latest_recap_href
    for token in (
        'data-site-version="1.48"', "184 篇公开研究笔记",
        "<strong>R0.73H</strong><span>最新研究节点</span>",
        'data-note="r0-73h"', "/recap-r0-61-r0-73h.html",
        "研究笔记总索引 · v1.48 · 2026-08-30",
    ):
        if token not in index:
            raise RuntimeError("R0.73H note index missing token: " + token)
    assert_clean(index, "R0.73H note index")
    assert_public_voice(index, "R0.73H note index")
    return index


def stage_figure_assets(staged: dict[Path, bytes], figure_manifest: dict) -> None:
    source = ROOT / FIGURE_RELATIVE
    target = PUBLIC / "assets/r073h"
    rows = figure_manifest.get("figure", {}).get("outputs", [])
    hashes = {Path(str(row["path"])).name: row["sha256"] for row in rows}
    for suffix in ("pdf", "svg", "png"):
        name = f"figure.{suffix}"
        payload = (source / name).read_bytes()
        if sha256_bytes(payload) != hashes.get(name):
            raise RuntimeError("R0.73H public figure source is not manifest-bound")
        staged[target / f"{FIGURE_ID}.{suffix}"] = payload


def validate_staged(staged: dict[Path, bytes]) -> None:
    required_paths = (
        PUBLIC / "notes/r0-73h.html",
        PUBLIC / "recap-r0-61-r0-73h.html",
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
            raise RuntimeError("R0.73H transaction missing staged path " + str(path))
    for path in staged:
        if path.suffix.lower() == ".pdf" and "assets/r073h" not in path.as_posix():
            raise RuntimeError("R0.73H HTML transaction must not generate note or recap PDFs")
    html_paths = (
        PUBLIC / "notes/r0-73h.html", PUBLIC / "recap-r0-61-r0-73h.html",
        PUBLIC / "research-review.html", PUBLIC / "literature-review.html",
        PUBLIC / "notes/index.html",
    )
    for path in html_paths:
        value = staged[path].decode("utf-8")
        assert_clean(value, path.name)
        assert_mathjax_clean(value, path.name, check_naked=True)
        assert_public_voice(value, path.name)
        if "/i18n-en.js?v=1.48" not in value:
            raise RuntimeError("R0.73H staged HTML has stale i18n version: " + path.name)
    note = staged[PUBLIC / "notes/r0-73h.html"].decode("utf-8")
    for token in (CLOSED, FALSE, OPEN, "CONTINUUM THEOREM", "NOT CLAY", "d=0.01>1/450", "4 个预注册独立哨兵", "1 个独立 holdout"):
        if token not in note:
            raise RuntimeError("R0.73H staged note lost boundary token: " + token)
    recap = staged[PUBLIC / "recap-r0-61-r0-73h.html"].decode("utf-8")
    start = recap.index('<section id="node-index">')
    end = recap.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', recap[start:end])
    if len(links) != 124 or len(set(links)) != 124 or recap.count('<article class="phase">') != 43:
        raise RuntimeError("R0.73H staged recap inventory is invalid")
    home = staged[PUBLIC / "research-review.html"].decode("utf-8")
    route = re.search(r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73H">(.*?)</nav>', home, flags=re.S)
    if route is None or len(re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))) != 94:
        raise RuntimeError("R0.73H staged home route inventory is invalid")
    if "专指按下界指数预设种子的全阶 Taylor 半径" not in home:
        raise RuntimeError("R0.73H staged home lost the prescribed-seed Taylor-radius boundary")
    literature = staged[PUBLIC / "literature-review.html"].decode("utf-8")
    if 'class="route-r073h-deck-update"' not in literature or "d=0.01>1/450" not in literature:
        raise RuntimeError("R0.73H staged literature route deck endpoint is invalid")
    site = json.loads(staged[PUBLIC / "site-version.json"])
    release = json.loads(staged[ROOT / "research/release-manifest.json"])
    if site.get("publicHtmlNoteCount") != 184 or release.get("postR060RecapNodeCount") != 124:
        raise RuntimeError("R0.73H staged accounting drifted")


def ensure_transaction_parent(path: Path, created: list[Path]) -> None:
    missing: list[Path] = []
    cursor = path.parent
    while not cursor.exists():
        if cursor == ROOT or ROOT not in cursor.resolve().parents:
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
    descriptor, temporary = tempfile.mkstemp(prefix="." + path.name + ".r073h-", dir=path.parent)
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
        raise RuntimeError("R0.73H transaction is empty")
    for path in ordered:
        resolved = path.resolve()
        if resolved == ROOT or ROOT not in resolved.parents:
            raise RuntimeError("transaction target escaped repository: " + str(path))
        if path.exists() and (not path.is_file() or path.is_symlink()):
            raise RuntimeError("transaction target is not a regular file: " + str(path))
    backups = {path: path.read_bytes() if path.is_file() else None for path in ordered}
    modes = {path: (path.stat().st_mode & 0o777) if path.exists() else 0o644 for path in ordered}
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
    target = PUBLIC / "assets/r073h"
    rows = figure_manifest.get("figure", {}).get("outputs", [])
    expected = {
        Path(str(row.get("path", ""))).name: row
        for row in rows if isinstance(row, dict)
    }
    for suffix in ("pdf", "svg", "png"):
        source_path = source / f"figure.{suffix}"
        target_path = target / f"{FIGURE_ID}.{suffix}"
        row = expected.get(f"figure.{suffix}")
        if row is None or not target_path.is_file() or target_path.is_symlink():
            raise RuntimeError("R0.73H materialized figure asset missing: " + suffix)
        if target_path.read_bytes() != source_path.read_bytes():
            raise RuntimeError("R0.73H public figure is not byte-identical: " + suffix)
        if digest(target_path) != row.get("sha256") or target_path.stat().st_size != row.get("bytes"):
            raise RuntimeError("R0.73H materialized figure asset escaped manifest: " + suffix)


def publication_stage_incomplete() -> bool:
    pdfs = (
        PUBLIC / "notes/r0-73h.pdf",
        PUBLIC / "recap-r0-61-r0-73h.pdf",
    )
    if any(not path.is_file() or path.is_symlink() or not path.read_bytes().startswith(b"%PDF") for path in pdfs):
        return True
    try:
        snapshot = json.loads((ROOT / "scripts/i18n-snapshots/r073h-missing.json").read_text(encoding="utf-8"))
        translations = json.loads((ROOT / "translations/en.json").read_text(encoding="utf-8"))
        bundle = (PUBLIC / "i18n-en.js").read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError, ValueError):
        return True
    if not isinstance(snapshot, list) or not snapshot:
        return True
    by_id = {
        row.get("id"): row for row in translations
        if isinstance(row, dict) and re.fullmatch(r"r073h\d{3}", str(row.get("id", "")))
    } if isinstance(translations, list) else {}
    if len(by_id) != len(snapshot):
        return True
    for index, snapshot_row in enumerate(snapshot, 1):
        row = by_id.get(f"r073h{index:03d}")
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
            "Validate or explicitly apply the staged R0.73H HTML/manifest transaction. "
            "PDF and translation completion remain separate final-publication steps."
        )
    )
    action = parser.add_mutually_exclusive_group()
    action.add_argument(
        "--check-only", action="store_true",
        help="validate sealed inputs and the source or materialized target without writing",
    )
    action.add_argument(
        "--apply", action="store_true",
        help="explicitly apply the HTML/manifest transaction when the exact R0.73G source is present",
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
            "release": "R0.73H", "siteVersion": "1.48", "notes": 184,
            "recapNodes": 124, "published": 86, "formalSealed": 62,
            "legacyBacklog": 24, "phases": 43, "routeNotes": 94,
            "next": "R0.73I", "rootVersion": "1.48", "noOp": True,
            "publicationStageIncomplete": publication_stage_incomplete(),
            "pdfGenerated": False, "translationsGenerated": False,
        }, ensure_ascii=False))
        return
    staged: dict[Path, bytes] = {}
    stage_figure_assets(staged, figure_manifest)
    staged[PUBLIC / "notes/r0-73h.html"] = build_note().encode("utf-8")
    staged[PUBLIC / "recap-r0-61-r0-73h.html"] = build_recap().encode("utf-8")
    staged[PUBLIC / "research-review.html"] = update_home().encode("utf-8")
    staged[PUBLIC / "literature-review.html"] = update_literature().encode("utf-8")
    manifest_outputs = build_manifest_outputs()
    staged.update(manifest_outputs)
    staged[PUBLIC / "notes/index.html"] = build_note_index(staged[PUBLIC / "site-version.json"]).encode("utf-8")
    validate_staged(staged)
    if args.check_only:
        print(json.dumps({
            "release": "R0.73H", "sourceState": "R0.73G",
            "checkOnly": True, "wouldWrite": len(staged),
            "publicationStageIncomplete": True,
        }, ensure_ascii=False))
        return
    commit_transaction(staged)
    if len(list((PUBLIC / "notes").glob("r0-*.html"))) != 184:
        raise RuntimeError("R0.73H postcommit note count is not 184")
    verify_materialized_figure_assets(figure_manifest)
    print(json.dumps({
        "release": "R0.73H", "siteVersion": "1.48", "notes": 184,
        "recapNodes": 124, "published": 86, "formalSealed": 62,
        "legacyBacklog": 24, "phases": 43, "routeNotes": 94,
        "next": "R0.73I", "rootVersion": "1.48",
        "noOp": False, "publicationStageIncomplete": True,
        "pdfGenerated": False, "translationsGenerated": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
