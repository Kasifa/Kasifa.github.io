#!/usr/bin/env python3
"""Fail-closed metadata-only formal seal for the R0.73G figure package."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]

SOURCE_COMMIT = "21c11ba3eef7f2b5dc3f107957e0744a0471745d"
FIGURE_PACKAGE_COMMIT = "0d311d22a62cfbc9253e95580de10d33898ecddc"
CERTIFICATE_COMMIT = "589e366ccec6a316b25594542a7eb8cb879156fd"
PREVIOUS_MANIFEST_SHA256 = "ac44709cda2d5d2d955f5b571f5431fda1303c17084867d97da16a17828218de"
FIGURE_RELATIVE = "figures/r073g/fig-r073g-nonlinear-row-leakage"
CERTIFICATE_RELATIVE = "research/certificates/r073g/certificate.json"
CERTIFICATE_DIRECTORY_RELATIVE = "research/certificates/r073g"
EXPERIMENT_COMMIT = "0679192b65a294bb211c96decc47bb046ab60b93"
ANALYTIC_PATHS = (
    "research/r073g_problem_freeze.md",
    "research/r073g_nonlinear_shadowing_proof.md",
    "research/r073g_operator_derivation.md",
    "research/r073g_adversarial_audit.md",
    "research/r073g_independent_analytic_audit.md",
    "research/r073g_literature_audit.md",
    "research/r073g_gap_matrix.md",
    "research/r073g_report-source.md",
)
CHANGED_METADATA = {
    "SHA256SUMS",
    "command.txt",
    "manifest.json",
    "validate.py",
    "validation.json",
}
ADDED_METADATA = {"contract.json"}
EXPECTED_IMMUTABLE_COUNT = 14
CERTIFICATE_PACKAGE_FILES = (
    "README.md",
    "SHA256SUMS",
    "certificate.json",
    "generate_certificate.py",
    "independent_recompute.json",
    "independent_recompute.py",
    "manifest.json",
    "progress.ndjson",
    "validate_certificate.py",
    "validation.json",
)
CERTIFICATE_PACKAGE_SOURCE_FILES = (
    "README.md",
    "generate_certificate.py",
    "independent_recompute.py",
    "validate_certificate.py",
)
CERTIFICATE_GENERATED_FILES = (
    "certificate.json",
    "independent_recompute.json",
    "progress.ndjson",
    "validation.json",
)
CERTIFICATE_LEDGER_FILES = tuple(
    name for name in CERTIFICATE_PACKAGE_FILES if name != "SHA256SUMS"
)
CERTIFICATE_TOP_LEVEL_KEYS = {
    "schemaVersion", "release", "created", "status", "evidenceClass",
    "sourceCommit", "experimentCommit", "figurePackageCommit", "sourceBindings",
    "experimentBindings", "figureBindings", "checks", "exactSentinels",
    "claimLedgers", "theorem", "finiteDiagnostic", "journalFigure",
    "claimBoundary", "sealState",
}
CERTIFICATE_MANIFEST_KEYS = {
    "schemaVersion", "release", "created", "status", "sourceCommit",
    "experimentCommit", "figurePackageCommit", "sourceBindingKind",
    "experimentBindingKind", "figureBindingKind", "sourceBindings",
    "experimentBindings", "figureBindings", "journalFigure",
    "packageSourceBindings", "outputBindings", "files", "outputs",
    "sealState", "inventoryPolicy", "limitations",
}
CERTIFICATE_INDEPENDENT_KEYS = {
    "schemaVersion", "release", "sourceCommit", "experimentCommit",
    "figurePackageCommit", "sourceBindings", "experimentBindings", "figureBindings",
    "checks", "allChecksPass", "exactSentinels", "claimLedgers",
    "finiteDiagnostic", "journalFigure", "claimBoundary",
}
CERTIFICATE_VALIDATION_KEYS = {
    "schemaVersion", "release", "sourceCommit", "experimentCommit",
    "figurePackageCommit", "checks", "allChecksPass", "claimLedgers",
    "claimBoundary", "journalFigure",
}
CERTIFICATE_CHECK_KEYS = frozenset(['adversarialAuditFinalPass', 'allAnalyticSourceBlobsBound', 'allModeRemainderAndHalfGainAnchorsPresent', 'analyticSourceBlobsUnchangedAtExperimentCommit', 'analyticSourceCommitResolvedExactly', 'boundedLiteratureSearchMakesNoPriorityClaim', 'cubicKzParityCanReturnToLaunchingRows', 'diagnosticSourceUnchangedFromAnalyticCommit', 'experimentCommitDescendsFromAnalyticSourceCommit', 'experimentCommitDistinctFromAnalyticSourceCommit', 'experimentComparisonInventoryExactUniqueGrid', 'experimentConvergenceCsvMatchesSummaryExactly', 'experimentGridMatchesFormalContract', 'experimentManifestCoreValidated', 'experimentManifestFileBindingsExact', 'experimentManifestScientificBindingsExact', 'experimentOutputBindingsMatchCommittedBytes', 'experimentRowInventoryExactUniqueGrid', 'experimentRowsCsvMatchesSummaryExactly', 'experimentSha256LedgerExact', 'experimentSourceProvenanceMatchesAnalyticCommit', 'experimentTreeInventoryExact', 'figureCommitDescendsFromExperimentCommit', 'figureCommitDistinctFromExperimentCommit', 'figurePackageManifestFileBindingsExact', 'figurePackageManifestValidated', 'figurePackageOutputsBoundExactly', 'figurePackageResultsBoundExactly', 'figurePackageSha256LedgerExact', 'figurePackageTreeInventoryExact', 'figurePackageValidationPassed', 'figurePackageVisualQaPassed', 'finiteClaimBoundaryExactFailClosed', 'formalExperimentNotSmoke', 'formalExperimentSchema', 'gapDecisionLedgerExact', 'h3LambdaSquaredLedgerAnchorsPresent', 'halfGainArithmetic', 'independentAnalyticAuditPassesAllSevenGates', 'independentValidationInventoryAndThresholdRecomputed', 'kernelErrorThresholdRecomputedFromCommittedRows', 'kzParityAnchorsPresent', 'normalizedDiffusionCoefficientIsOne', 'normalizedShearCoefficientIsOneHalf', 'physicalBackgroundHeatFactorsAgree', 'physicalProfileTimeIsFourTimesPhysicalTime', 'physicalScalingAnchorsPresent', 'planarVorticityAndNoStretchingAnchorsPresent', 'planarVorticityStretchingZero', 'positivePartBothBranchesAudited', 'positivePartBranchMGeKappaReducesToKappa', 'positivePartBranchMLtKappaReducesToM', 'quadraticH3CostAndSeedPowerCancel', 'quadraticKzParityExcludesLaunchingRows', 'realPairNormalizationIsOne', 'reportDecisionLedgerExact', 'riccatiComparisonMultiplierBelowTwo', 'riccatiDenominatorAtLeastThreeQuarters', 'riccatiThresholdAnchorsPresent', 'rowIsometryAnchorsPresent', 'rowIsometryPolynomialIdentity', 'summaryObservedRangesRecomputed', 'twoEllipticLiftsGiveLambdaSquared'])
CERTIFICATE_INDEPENDENT_CHECK_KEYS = frozenset(['allEightSourceBlobsRecomputed', 'auditContainsSevenPassVerdicts', 'experimentCommitExistsAndResolvesExactly', 'figureCommitExistsAndResolvesExactly', 'gapStatesRecomputedExactly', 'independentAnalyticBlobsUnchangedAtExperimentCommit', 'independentCommittedOutputsMatchSummary', 'independentComparisonsCsvSummaryIdentity', 'independentExactUniqueComparisonGrid', 'independentExactUniqueRowGrid', 'independentExperimentCommitIsLaterDescendant', 'independentExperimentManifestCore', 'independentExperimentManifestFiles', 'independentExperimentSchemaAndMode', 'independentExperimentScientificBindings', 'independentExperimentScriptBlobUnchanged', 'independentExperimentSha256Ledger', 'independentExperimentSourceProvenance', 'independentExperimentTreeInventoryExact', 'independentFigureCommitIsLaterDescendant', 'independentFigureManifestFileBindings', 'independentFigureManifestValidated', 'independentFigureOutputsBound', 'independentFigureResultsBound', 'independentFigureSha256Ledger', 'independentFigureTreeInventoryExact', 'independentFigureValidationPassed', 'independentFigureVisualQaPassed', 'independentFiniteBoundaryExact', 'independentFormalGrid', 'independentH3ExponentLedger', 'independentHalfGainLedger', 'independentKernelThresholdRecomputed', 'independentKzParity', 'independentPhysicalHeatIdentity', 'independentPlanarStretchingIdentity', 'independentPositivePartTwoBranches', 'independentRiccatiLedger', 'independentRowIsometryIdentity', 'independentRowsCsvSummaryIdentity', 'independentValidatorThresholdRecomputed', 'proofContainsH3RiccatiAndAllModeRemainder', 'proofContainsPhysicalBackgroundAndEndpoint', 'reportStatesRecomputedExactly', 'sourceCommitExistsAndResolvesExactly'])
CERTIFICATE_VALIDATION_CHECK_KEYS = frozenset(['analyticBlobsPreservedAtExperimentCommit', 'certificateSchemasExact', 'certificateTopLevelKeysExact', 'claimBoundaryExactFailClosed', 'claimLedgersAgreeIndependently', 'commitChainExact', 'exactSentinelsAgreeIndependently', 'experimentBindingsIndependentAgreement', 'experimentCommitParameterAgreement', 'figureBindingsIndependentAgreement', 'figureCommitParameterAgreement', 'finiteDiagnosticRecordsAgreeIndependently', 'finiteEvidenceBoundaryFailClosed', 'gapBoundaryNamesAndStatesExact', 'h3ExponentLedgerExact', 'halfGainAndPositivePartBranchesExact', 'independentAllChecksPass', 'independentTopLevelKeysExact', 'journalFigureExactAndNoFormalFigure', 'kzParitySentinelExact', 'physicalScalingSentinelExact', 'planarStretchingSentinelExact', 'primaryAllChecksPass', 'reportBoundaryNamesAndStatesExact', 'riccatiSentinelExact', 'rowIsometrySentinelExact', 'sealStateHonest', 'sourceBindingsIndependentAgreement', 'sourceCommitAgreement'])


def configure_dependencies(path: str | None) -> None:
    if path:
        sys.path.insert(0, path)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def record(path: Path, relative_to: Path = ROOT) -> dict[str, Any]:
    return {
        "path": str(path.relative_to(relative_to)),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def atomic_write(path: Path, payload: str) -> None:
    temporary = path.with_name(path.name + ".tmp-r073g-formal-seal")
    try:
        temporary.write_text(payload, encoding="utf-8")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def git_bytes(commit: str, relative: str) -> bytes:
    return subprocess.check_output(
        ["git", "show", f"{commit}:{relative}"], cwd=ROOT
    )


def git_blob(commit: str, relative: str) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", f"{commit}:{relative}"], cwd=ROOT, text=True
    ).strip()


def require_commit(commit: str, label: str) -> None:
    result = subprocess.run(
        ["git", "cat-file", "-e", commit + "^{commit}"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(result.returncode == 0, label + " is not a Git commit")


def require_strict_ancestor(older: str, newer: str, message: str) -> None:
    require(older != newer, message + " (commits are equal)")
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", older, newer],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    require(result.returncode == 0, message)


def historical_binding(relative: str) -> dict[str, Any]:
    payload = git_bytes(SOURCE_COMMIT, relative)
    return {
        "path": relative,
        "bytes": len(payload),
        "sha256": sha256_bytes(payload),
        "sourceCommit": SOURCE_COMMIT,
    }


def package_names_at_figure_commit() -> list[str]:
    rows = subprocess.check_output(
        [
            "git",
            "ls-tree",
            "-r",
            "--name-only",
            FIGURE_PACKAGE_COMMIT,
            FIGURE_RELATIVE,
        ],
        cwd=ROOT,
        text=True,
    ).splitlines()
    prefix = FIGURE_RELATIVE + "/"
    require(rows and all(row.startswith(prefix) for row in rows),
            "original figure package is missing or not flat")
    names = sorted(row.removeprefix(prefix) for row in rows)
    require(all("/" not in name for name in names),
            "original figure package unexpectedly contains subdirectories")
    return names


def json_object(payload: bytes, label: str) -> dict[str, Any]:
    def reject_nonfinite(value: str) -> object:
        raise ValueError("non-finite JSON constant: " + value)

    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON key: " + key)
            result[key] = value
        return result

    try:
        parsed = json.loads(
            payload,
            parse_constant=reject_nonfinite,
            object_pairs_hook=unique_object,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise AssertionError(label + " is not strict JSON") from exc
    require(isinstance(parsed, dict), label + " must be a JSON object")
    return parsed


def exact_true_checks(value: object, expected: frozenset[str], label: str) -> None:
    require(isinstance(value, dict), label + " check ledger is missing")
    require(set(value) == expected, label + " check-key inventory mismatch")
    require(bool(value) and all(item is True for item in value.values()),
            label + " contains a failed or non-boolean check")


def certificate_package_tree() -> list[str]:
    rows = subprocess.check_output(
        [
            "git", "ls-tree", "-r", CERTIFICATE_COMMIT,
            CERTIFICATE_DIRECTORY_RELATIVE,
        ],
        cwd=ROOT,
        text=True,
    ).splitlines()
    expected_paths = [
        f"{CERTIFICATE_DIRECTORY_RELATIVE}/{name}"
        for name in CERTIFICATE_PACKAGE_FILES
    ]
    observed_paths: list[str] = []
    for row in rows:
        require("\t" in row, "C certificate tree row is malformed")
        metadata, relative = row.split("\t", 1)
        require(metadata.startswith("100644 blob "),
                "C certificate package contains a non-regular Git entry: " + relative)
        observed_paths.append(relative)
    require(observed_paths == expected_paths,
            "C certificate package inventory is not the fixed 10-file flat package")
    return observed_paths


def verify_certificate_binding_rows(
    manifest: dict[str, Any], key: str, names: tuple[str, ...]
) -> None:
    rows = manifest.get(key)
    require(isinstance(rows, list), "C manifest " + key + " is missing")
    expected_paths = [
        f"{CERTIFICATE_DIRECTORY_RELATIVE}/{name}" for name in names
    ]
    require(
        [row.get("path") for row in rows if isinstance(row, dict)] == expected_paths
        and len(rows) == len(expected_paths),
        "C manifest " + key + " inventory mismatch",
    )
    for row, relative in zip(rows, expected_paths):
        require(isinstance(row, dict), "C manifest binding row is not an object")
        require(set(row) == {"path", "bytes", "sha256"},
                "C manifest binding row schema mismatch: " + relative)
        payload = git_bytes(CERTIFICATE_COMMIT, relative)
        require(row["bytes"] == len(payload),
                "C manifest binding size mismatch: " + relative)
        require(row["sha256"] == sha256_bytes(payload),
                "C manifest binding hash mismatch: " + relative)


def verify_certificate_package() -> dict[str, Any]:
    certificate_package_tree()
    directory = ROOT / CERTIFICATE_DIRECTORY_RELATIVE
    require(directory.is_dir() and not directory.is_symlink(),
            "working C certificate package is missing or not a regular directory")
    current_names = sorted(path.name for path in directory.iterdir())
    require(current_names == list(CERTIFICATE_PACKAGE_FILES),
            "working C certificate inventory differs from the fixed 10-file package")
    for name in CERTIFICATE_PACKAGE_FILES:
        current = directory / name
        require(current.is_file() and not current.is_symlink(),
                "working C certificate entry is not a regular file: " + name)
        relative = f"{CERTIFICATE_DIRECTORY_RELATIVE}/{name}"
        require(current.read_bytes() == git_bytes(CERTIFICATE_COMMIT, relative),
                "working C certificate file differs from C: " + name)

    ledger_payload = git_bytes(
        CERTIFICATE_COMMIT,
        f"{CERTIFICATE_DIRECTORY_RELATIVE}/SHA256SUMS",
    )
    ledger_rows: list[tuple[str, str]] = []
    try:
        ledger_lines = ledger_payload.decode("utf-8").splitlines()
    except UnicodeDecodeError as exc:
        raise AssertionError("C SHA256SUMS is not UTF-8") from exc
    for line in ledger_lines:
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/\\\r\n]+)", line)
        require(match is not None, "C SHA256SUMS contains a malformed row")
        ledger_rows.append((match.group(2), match.group(1)))
    require([name for name, _ in ledger_rows] == list(CERTIFICATE_LEDGER_FILES),
            "C SHA256SUMS inventory is not the exact sorted 9-file ledger")
    for name, expected_hash in ledger_rows:
        relative = f"{CERTIFICATE_DIRECTORY_RELATIVE}/{name}"
        require(
            sha256_bytes(git_bytes(CERTIFICATE_COMMIT, relative)) == expected_hash,
            "C SHA256SUMS hash mismatch: " + name,
        )

    certificate = json_object(
        git_bytes(CERTIFICATE_COMMIT, CERTIFICATE_RELATIVE),
        "C certificate.json",
    )
    independent = json_object(
        git_bytes(
            CERTIFICATE_COMMIT,
            f"{CERTIFICATE_DIRECTORY_RELATIVE}/independent_recompute.json",
        ),
        "C independent_recompute.json",
    )
    manifest = json_object(
        git_bytes(
            CERTIFICATE_COMMIT,
            f"{CERTIFICATE_DIRECTORY_RELATIVE}/manifest.json",
        ),
        "C manifest.json",
    )
    validation = json_object(
        git_bytes(
            CERTIFICATE_COMMIT,
            f"{CERTIFICATE_DIRECTORY_RELATIVE}/validation.json",
        ),
        "C validation.json",
    )

    require(set(certificate) == CERTIFICATE_TOP_LEVEL_KEYS,
            "C certificate top-level schema mismatch")
    require(set(independent) == CERTIFICATE_INDEPENDENT_KEYS,
            "C independent recompute top-level schema mismatch")
    require(set(manifest) == CERTIFICATE_MANIFEST_KEYS,
            "C manifest top-level schema mismatch")
    require(set(validation) == CERTIFICATE_VALIDATION_KEYS,
            "C validation top-level schema mismatch")
    exact_true_checks(
        certificate.get("checks"), CERTIFICATE_CHECK_KEYS, "C certificate"
    )
    exact_true_checks(
        independent.get("checks"),
        CERTIFICATE_INDEPENDENT_CHECK_KEYS,
        "C independent recompute",
    )
    exact_true_checks(
        validation.get("checks"),
        CERTIFICATE_VALIDATION_CHECK_KEYS,
        "C validation",
    )

    identities = (
        (certificate, "r073g-planar-nonlinear-shadowing-certificate-v1", "validated"),
        (independent, "r073g-independent-certificate-recompute-v1", None),
        (manifest, "r073g-certificate-manifest-v1",
         "validated-content-addressed-unsealed"),
        (validation, "r073g-certificate-validation-v1", None),
    )
    for payload, schema, status in identities:
        require(payload.get("schemaVersion") == schema,
                "C package schemaVersion mismatch: " + schema)
        require(payload.get("release") == "R0.73G",
                "C package release mismatch: " + schema)
        require(payload.get("sourceCommit") == SOURCE_COMMIT,
                "C package source commit mismatch: " + schema)
        require(payload.get("experimentCommit") == EXPERIMENT_COMMIT,
                "C package experiment commit mismatch: " + schema)
        require(payload.get("figurePackageCommit") == FIGURE_PACKAGE_COMMIT,
                "C package figure commit mismatch: " + schema)
        if status is not None:
            require(payload.get("status") == status,
                    "C package status mismatch: " + schema)
    require(independent.get("allChecksPass") is True,
            "C independent recompute allChecksPass is not true")
    require(validation.get("allChecksPass") is True,
            "C validation allChecksPass is not true")

    verify_certificate_binding_rows(
        manifest, "packageSourceBindings", CERTIFICATE_PACKAGE_SOURCE_FILES
    )
    verify_certificate_binding_rows(
        manifest, "outputBindings", CERTIFICATE_GENERATED_FILES
    )
    require(
        manifest.get("files")
        == [*CERTIFICATE_PACKAGE_SOURCE_FILES, *CERTIFICATE_GENERATED_FILES],
        "C manifest file inventory is not exact",
    )
    require(
        manifest.get("outputs")
        == [
            *CERTIFICATE_GENERATED_FILES,
            "manifest.json",
            "SHA256SUMS",
        ],
        "C manifest output inventory is not exact",
    )
    require(manifest.get("inventoryPolicy") == {
        "cacheDirectoriesForbidden": True,
        "manifestFilesExcludes": ["manifest.json", "SHA256SUMS"],
        "scope": "all regular files directly inside research/certificates/r073g",
        "sha256LedgerExcludes": ["SHA256SUMS"],
    }, "C manifest inventory policy mismatch")

    for key in (
        "sourceBindings", "experimentBindings", "figureBindings", "journalFigure"
    ):
        require(independent.get(key) == certificate.get(key),
                "C independent payload disagrees with certificate: " + key)
        require(manifest.get(key) == certificate.get(key),
                "C manifest disagrees with certificate: " + key)
    for key in ("claimLedgers", "claimBoundary", "journalFigure"):
        require(validation.get(key) == certificate.get(key),
                "C validation disagrees with certificate: " + key)
        require(independent.get(key) == certificate.get(key),
                "C independent payload disagrees with certificate: " + key)
    return certificate


def current_package_names() -> list[str]:
    unexpected = [
        path.name for path in HERE.iterdir()
        if not path.is_file() or path.is_symlink()
    ]
    require(not unexpected,
            "figure package contains a directory or symlink: " + ", ".join(unexpected))
    return sorted(path.name for path in HERE.iterdir())


def verify_immutable_figure_package(original_names: list[str]) -> None:
    expected = sorted(set(original_names) | ADDED_METADATA)
    require(current_package_names() == expected,
            "figure inventory differs from F plus the allowed contract metadata")
    immutable = sorted(set(original_names) - CHANGED_METADATA)
    require(len(immutable) == EXPECTED_IMMUTABLE_COUNT,
            "metadata migration does not preserve exactly 14 immutable files")
    for name in immutable:
        current = (HERE / name).read_bytes()
        frozen = git_bytes(FIGURE_PACKAGE_COMMIT, f"{FIGURE_RELATIVE}/{name}")
        require(current == frozen,
                "immutable figure-package file differs from F: " + name)


def verify_complete_ledger() -> None:
    rows: list[tuple[str, str]] = []
    for line in (HERE / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/\\\r\n]+)", line)
        require(match is not None, "malformed SHA256SUMS row")
        rows.append((match.group(2), match.group(1)))
    names = [name for name, _ in rows]
    require(names == sorted(names), "SHA256SUMS is not sorted")
    require(len(names) == len(set(names)), "SHA256SUMS has duplicate entries")
    expected = sorted(name for name in current_package_names()
                      if name != "SHA256SUMS")
    require(names == expected, "SHA256SUMS inventory is incomplete")
    for name, expected_hash in rows:
        require(sha256(HERE / name) == expected_hash,
                "SHA256SUMS hash mismatch: " + name)


def certificate_output(
    journal: dict[str, Any], suffix: str, expected: dict[str, Any]
) -> None:
    row = journal.get(suffix)
    require(isinstance(row, dict),
            "certificate journalFigure output is missing: " + suffix)
    keys = {"path", "bytes", "sha256"} | ({"dpi"} if suffix == "png" else set())
    require(set(row) == keys,
            "certificate journalFigure output schema mismatch: " + suffix)
    for key in ("path", "bytes", "sha256"):
        require(row.get(key) == expected[key],
                "certificate journalFigure output mismatch: " + suffix + "/" + key)
    if suffix == "png":
        require(row.get("dpi") == 600,
                "certificate journalFigure PNG dpi mismatch")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default=None)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--figure-package-commit", required=True)
    parser.add_argument("--certificate-commit", required=True)
    args = parser.parse_args()
    configure_dependencies(args.deps)

    from PIL import Image
    from pypdf import PdfReader

    for value, label in (
        (args.source_commit, "source commit"),
        (args.figure_package_commit, "figure-package commit"),
        (args.certificate_commit, "certificate commit"),
    ):
        require(bool(re.fullmatch(r"[0-9a-f]{40}", value)),
                label + " must be lowercase 40-hex")
        require_commit(value, label)
    require(args.source_commit == SOURCE_COMMIT,
            "source commit differs from the R0.73G analytic source")
    require(args.figure_package_commit == FIGURE_PACKAGE_COMMIT,
            "figure-package commit differs from F")
    require(args.certificate_commit == CERTIFICATE_COMMIT,
            "certificate commit differs from C")
    require_strict_ancestor(SOURCE_COMMIT, FIGURE_PACKAGE_COMMIT,
                            "S is not a strict ancestor of F")
    require_strict_ancestor(FIGURE_PACKAGE_COMMIT, CERTIFICATE_COMMIT,
                            "F is not a strict ancestor of C")

    previous_manifest_bytes = git_bytes(
        FIGURE_PACKAGE_COMMIT, f"{FIGURE_RELATIVE}/manifest.json"
    )
    require(sha256_bytes(previous_manifest_bytes) == PREVIOUS_MANIFEST_SHA256,
            "historical F manifest hash mismatch")
    previous_manifest = json.loads(previous_manifest_bytes)
    require(previous_manifest.get("figureId") == "fig-r073g-nonlinear-row-leakage",
            "historical F figure identity mismatch")
    require(previous_manifest.get("status") == "validated",
            "historical F manifest was not validated")
    require(previous_manifest.get("git", {}).get("sourceCommit") == SOURCE_COMMIT,
            "historical F manifest source commit mismatch")

    original_names = package_names_at_figure_commit()
    require(len(original_names) == 19,
            "historical F package must contain exactly 19 files")
    verify_immutable_figure_package(original_names)

    previous_validation = json.loads(git_bytes(
        FIGURE_PACKAGE_COMMIT, f"{FIGURE_RELATIVE}/validation.json"
    ))
    require(previous_validation.get("status") == "passed",
            "historical F validation was not passed")
    previous_checks = previous_validation.get("checks")
    require(isinstance(previous_checks, dict) and previous_checks
            and all(value is True for value in previous_checks.values()),
            "historical F validation contains a failed or empty check ledger")

    certificate = verify_certificate_package()
    require(certificate.get("sourceCommit") == SOURCE_COMMIT,
            "certificate source commit mismatch")
    require(certificate.get("figurePackageCommit") == FIGURE_PACKAGE_COMMIT,
            "certificate figure-package commit mismatch")
    require(certificate.get("status") == "validated",
            "certificate is not validated")
    require("formalFigure" not in certificate,
            "historical C unexpectedly contains a formalFigure field")
    journal_figure = certificate.get("journalFigure")
    require(isinstance(journal_figure, dict),
            "certificate journalFigure is missing")
    require(set(journal_figure) == {
        "figureId", "status", "pdf", "svg", "png",
        "validationStatus", "visualQaStatus", "gitSealed",
    }, "certificate journalFigure field inventory mismatch")
    require(journal_figure.get("figureId") == previous_manifest["figureId"],
            "certificate journalFigure identity mismatch")
    require(journal_figure.get("status") == "validated",
            "certificate journalFigure historical status mismatch")
    require(journal_figure.get("validationStatus") == "passed",
            "certificate journalFigure validation did not pass")
    require(journal_figure.get("visualQaStatus") == "passed",
            "certificate journalFigure visual QA did not pass")
    require(journal_figure.get("gitSealed") is False,
            "certificate journalFigure historical gitSealed state changed")

    figure_bindings = certificate.get("figureBindings")
    require(isinstance(figure_bindings, list),
            "certificate figureBindings is missing")
    expected_binding_paths = [
        f"{FIGURE_RELATIVE}/{name}" for name in original_names
    ]
    require([row.get("path") for row in figure_bindings]
            == expected_binding_paths,
            "certificate figureBindings inventory differs from F")
    for row in figure_bindings:
        relative = row["path"]
        payload = git_bytes(FIGURE_PACKAGE_COMMIT, relative)
        require(row.get("commit") == FIGURE_PACKAGE_COMMIT,
                "certificate figure binding commit mismatch: " + relative)
        require(row.get("bytes") == len(payload),
                "certificate figure binding size mismatch: " + relative)
        require(row.get("sha256") == sha256_bytes(payload),
                "certificate figure binding hash mismatch: " + relative)
        if "gitBlob" in row:
            require(row["gitBlob"] == git_blob(FIGURE_PACKAGE_COMMIT, relative),
                    "certificate figure binding blob mismatch: " + relative)

    certificate_source_rows = {
        row["path"]: row for row in certificate.get("sourceBindings", [])
    }
    analytic_bindings = [historical_binding(path) for path in ANALYTIC_PATHS]
    require(analytic_bindings == previous_manifest.get("sourceBindings"),
            "historical F source bindings changed")
    for binding in analytic_bindings:
        row = certificate_source_rows.get(binding["path"], {})
        bound_commit = row.get("commit", row.get("sourceCommit"))
        require(bound_commit == SOURCE_COMMIT,
                "certificate source binding commit mismatch: " + binding["path"])
        require(row.get("bytes") == binding["bytes"],
                "certificate source binding size mismatch: " + binding["path"])
        require(row.get("sha256") == binding["sha256"],
                "certificate source binding hash mismatch: " + binding["path"])
        if "gitBlob" in row:
            require(row["gitBlob"] == git_blob(SOURCE_COMMIT, binding["path"]),
                    "certificate source binding blob mismatch: " + binding["path"])

    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    results = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
    for item in results["inputs"]:
        path = ROOT / item["path"]
        require(path.is_file(), "missing source-data input: " + item["path"])
        require(path.stat().st_size == item["bytes"],
                "source-data size changed: " + item["path"])
        require(sha256(path) == item["sha256"],
                "source-data hash changed: " + item["path"])
        require(path.read_bytes() == git_bytes(FIGURE_PACKAGE_COMMIT, item["path"]),
                "source-data input differs from F: " + item["path"])
    require(previous_manifest.get("sourceData") == results["inputs"],
            "historical sourceData binding changed")
    require(results["configBinding"]["sha256"] == sha256(HERE / "config.json"),
            "figure config changed after rendering")

    boundary = results["claimBoundary"]
    require(boundary == previous_manifest.get("claimBoundary"),
            "historical claim boundary changed")
    require(boundary.get("formalFiniteDiagnosticFigure") is True,
            "formal finite diagnostic declaration missing")
    for key, value in boundary.items():
        if key != "formalFiniteDiagnosticFigure":
            require(value is False, "escaped claim boundary: " + key)
    facts = results["diagnosticFacts"]
    require(facts == previous_manifest.get("diagnosticFacts"),
            "historical diagnostic facts changed")
    require(facts and all(facts.values()), "a declared diagnostic fact is false")

    reader = PdfReader(HERE / "figure.pdf")
    require(len(reader.pages) == 1, "PDF must contain exactly one page")
    page = reader.pages[0]
    points = [float(page.mediabox.width), float(page.mediabox.height)]
    expected_points = [
        config["widthMillimetres"] / 25.4 * 72,
        config["heightMillimetres"] / 25.4 * 72,
    ]
    require(max(abs(a - b) for a, b in zip(points, expected_points)) < 0.8,
            "PDF physical dimensions changed")
    pdf_text = page.extract_text() or ""
    for token in (
        "Frozen top eigenvalue",
        "Physical Sobolev cost",
        "Generated rows",
        "Numerical cross-checks",
        "diagnostic only",
    ):
        require(token in pdf_text, "PDF text missing: " + token)

    with Image.open(HERE / "figure.png") as image:
        pixels = list(image.size)
        dpi = image.info.get("dpi", (0, 0))
        require(abs(pixels[0] - 4205) <= 2 and abs(pixels[1] - 3118) <= 2,
                "PNG pixel dimensions changed")
        require(min(dpi) > 599 and max(dpi) < 601,
                "PNG is not tagged at 600 dpi")
    svg = (HERE / "figure.svg").read_text(encoding="utf-8")
    require("<image" not in svg, "SVG unexpectedly contains a raster image")
    for token in ("Frozen top eigenvalue", "Generated rows", "diagnostic only"):
        require(token in svg, "SVG text missing: " + token)

    observed = results["observed"]
    require(abs(observed["maximumFinestCutoffRelativeChange"]
                - 5.749359085030244e-14) < 1e-26,
            "cutoff-comparison sentinel changed")
    require(results["crossValidation"]["allChecksPass"] is True,
            "figure cross-validation status failed")
    require(results["crossValidation"]["primaryMaximumScaleOneDifference"] < 1e-12,
            "primary kernel discrepancy exceeded tolerance")
    require(results["crossValidation"]["independentMaximumScaleOneError"] < 1e-12,
            "independent kernel discrepancy exceeded tolerance")

    output_records: list[dict[str, Any]] = []
    for suffix in ("pdf", "svg", "png"):
        name = f"figure.{suffix}"
        item = record(HERE / name, HERE)
        if suffix == "png":
            item.update({"dpi": 600, "pixels": pixels})
        output_records.append(item)
        expected_certificate = {
            "path": f"{FIGURE_RELATIVE}/{name}",
            "bytes": item["bytes"],
            "sha256": item["sha256"],
        }
        if suffix == "png":
            expected_certificate["dpi"] = 600
        certificate_output(journal_figure, suffix, expected_certificate)
    require(output_records == previous_manifest["figure"]["outputs"],
            "formal output records differ from F")

    contract = {
        "schemaVersion": "r073g-figure-contract-v1",
        "release": "R0.73G",
        "figureId": previous_manifest["figureId"],
        "requiredOutputs": ["figure.pdf", "figure.svg", "figure.png"],
        "requiredDiagnostics": ["results.json", "validation.json"],
        "claimBoundary": boundary,
    }
    atomic_write(HERE / "contract.json", canonical(contract))

    checks = {
        "provenanceChainPassed": True,
        "historicalManifestBindingPassed": True,
        "originalPackageInventoryPreserved": True,
        "fourteenImmutableFilesByteIdenticalToF": True,
        "metadataOnlyMigrationPassed": True,
        "certificateBlobPassed": True,
        "certificateSourceBindingPassed": True,
        "certificateFullFigurePackageBindingPassed": True,
        "certificateJournalFigureBindingPassed": True,
        "certificateFormalFigureAbsentRecorded": True,
        "inputHashesPassed": True,
        "claimBoundaryFailClosed": True,
        "diagnosticFactsPassed": True,
        "singlePagePdf": True,
        "physicalDimensionsPassed": True,
        "pdfTextPassed": True,
        "png600DpiPassed": True,
        "svgVectorTextPassed": True,
        "finiteSentinelsPassed": True,
        "qaArtifactsByteIdenticalToFigureCommit": True,
        "visualQaPassedAtFigureCommitAndCertificateRun": True,
        "formalContractPassed": True,
    }
    validation = {
        "schemaVersion": "r073g-figure-validation-v1",
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
        "provenance": {
            "sourceCommit": SOURCE_COMMIT,
            "figurePackageCommit": FIGURE_PACKAGE_COMMIT,
            "certificateCommit": CERTIFICATE_COMMIT,
            "previousManifestSha256": PREVIOUS_MANIFEST_SHA256,
            "certificateFigureLedger": "journalFigure",
            "certificateFormalFigureFieldPresent": False,
            "metadataOnlySeal": True,
            "immutableOriginalFilesVerified": EXPECTED_IMMUTABLE_COUNT,
        },
        "pdfPoints": points,
        "pngPixels": pixels,
        "claimBoundary": boundary,
    }
    atomic_write(HERE / "validation.json", canonical(validation))

    command = (
        "From the repository root, run the metadata-only formal seal. This command does\n"
        "not invoke plot.py or rewrite scientific, figure, or QA artifacts.\n\n"
        "R073G_DEPS_DIR=/tmp/r073c-deps\n"
        "PYTHON=/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/"
        "dependencies/python/bin/python3\n\n"
        "env PYTHONPATH=\"$R073G_DEPS_DIR\" \"$PYTHON\" "
        f"{FIGURE_RELATIVE}/validate.py --deps \"$R073G_DEPS_DIR\" "
        f"--source-commit {SOURCE_COMMIT} "
        f"--figure-package-commit {FIGURE_PACKAGE_COMMIT} "
        f"--certificate-commit {CERTIFICATE_COMMIT}\n"
    )
    atomic_write(HERE / "command.txt", command)

    file_names = sorted(
        name for name in current_package_names()
        if name not in ("manifest.json", "SHA256SUMS")
    )
    require(len(file_names) == 18,
            "formal manifest must cover exactly 18 non-ledger files")
    file_records = [record(HERE / name) for name in file_names]

    previous_computation = previous_manifest["computation"]
    computation = {
        key: value for key, value in previous_computation.items() if key != "command"
    }
    computation.update({
        "formalCommand": (
            "python3 validate.py --source-commit <S> "
            "--figure-package-commit <F> --certificate-commit <C>"
        ),
        "originalGenerationCommand": previous_computation["command"],
        "metadataOnlySeal": True,
        "scientificComputationRerun": False,
    })

    previous_git = previous_manifest["git"]
    manifest = {
        "schemaVersion": previous_manifest["schemaVersion"],
        "release": "R0.73G",
        "figureId": previous_manifest["figureId"],
        "status": "formal",
        "analyticalQuestion": previous_manifest["analyticalQuestion"],
        "supportedClaim": previous_manifest["supportedClaim"],
        "createdAt": previous_manifest["createdAt"],
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": SOURCE_COMMIT,
            "experimentCommit": previous_git["experimentCommit"],
            "rendererSourceCommit": previous_git["rendererSourceCommit"],
            "figurePackageCommit": FIGURE_PACKAGE_COMMIT,
            "certificateCommit": CERTIFICATE_COMMIT,
            "dirtyAtCertifiedRun": False,
            "dirtyAtFigureGeneration": True,
            "figureSourcesBoundBySha256": True,
            "certificateBindsFigurePackage": True,
            "certificateBindsFigureOutputsBySha256": True,
            "certificateFigureLedger": "journalFigure",
            "certificateJournalFigureGitSealed": journal_figure["gitSealed"],
            "certificateFormalFigureFieldPresent": False,
            "certificateAttestsFormalStatus": False,
            "formalSealKind": "metadata-only",
            "originalFigureGenerationBaseCommit": SOURCE_COMMIT,
            "sourceCommitMeaning": (
                "clean analytic sources frozen at S and named by the C certificate"
            ),
            "figurePackageCommitMeaning": (
                "original validated figure package F; all scientific, figure, and "
                "QA blobs remain byte-identical"
            ),
            "certificateCommitMeaning": (
                "certificate package C binds the full F package and the journalFigure "
                "outputs by SHA-256; it does not contain a formalFigure field or "
                "attest this later metadata-only formal status"
            ),
            "dirtyAtCertifiedRunMeaning": (
                "certified provenance is read only from immutable S, F, and C Git blobs"
            ),
        },
        "manifestMigration": {
            "kind": "metadata-schema-only",
            "sealKind": "metadata-only",
            "previousManifestCommit": FIGURE_PACKAGE_COMMIT,
            "previousManifestSha256": PREVIOUS_MANIFEST_SHA256,
            "previousStatus": "validated",
            "currentStatus": "formal",
            "addedMetadataFiles": ["contract.json"],
            "changedMetadataFiles": sorted(CHANGED_METADATA),
            "immutableOriginalFilesVerified": EXPECTED_IMMUTABLE_COUNT,
            "scientificInputsChanged": False,
            "plotOrResultsChanged": False,
            "formalOutputsChanged": False,
            "qaArtifactsChanged": False,
            "certificatePayloadChanged": False,
        },
        "certificateBinding": {
            "path": CERTIFICATE_RELATIVE,
            "commit": CERTIFICATE_COMMIT,
            "figurePackageCommit": FIGURE_PACKAGE_COMMIT,
            "figureLedgerField": "journalFigure",
            "figureStatusAtCertificateRun": "validated",
            "validationStatusAtCertificateRun": "passed",
            "visualQaStatusAtCertificateRun": "passed",
            "outputsBoundBySha256": True,
            "fullFigurePackageBound": True,
            "formalFigureFieldPresent": False,
            "formalStatusAttestedByCertificate": False,
        },
        "sourceBindings": analytic_bindings,
        "experimentManifestBinding": previous_manifest["experimentManifestBinding"],
        "computation": computation,
        "compute": previous_manifest["compute"],
        "environment": previous_manifest["environment"],
        "data": previous_manifest["data"],
        "sourceData": previous_manifest["sourceData"],
        "inputs": previous_manifest["sourceData"],
        "figure": {**previous_manifest["figure"], "outputs": output_records},
        "outputs": output_records,
        "caption": previous_manifest["caption"],
        "qa": previous_manifest["qa"],
        "diagnosticFacts": facts,
        "claimBoundary": boundary,
        "contract": record(HERE / "contract.json"),
        "validation": record(HERE / "validation.json"),
        "inventoryPolicy": {
            "scope": "all regular files directly inside the figure package",
            "manifestFilesExcludes": ["manifest.json", "SHA256SUMS"],
            "sha256LedgerExcludes": ["SHA256SUMS"],
            "cacheDirectoriesForbidden": True,
            "originalInventoryExtendedOnlyBy": ["contract.json"],
        },
        "files": file_records,
    }

    for key in (
        "schemaVersion",
        "figureId",
        "analyticalQuestion",
        "supportedClaim",
        "createdAt",
        "sourceBindings",
        "experimentManifestBinding",
        "compute",
        "environment",
        "data",
        "sourceData",
        "figure",
        "caption",
        "qa",
        "diagnosticFacts",
        "claimBoundary",
    ):
        require(manifest[key] == previous_manifest[key],
                "metadata seal changed frozen manifest field: " + key)
    require(manifest["outputs"] == previous_manifest["figure"]["outputs"],
            "top-level output ledger differs from F")
    require(contract["claimBoundary"] == manifest["claimBoundary"],
            "contract and manifest claim boundaries differ")
    require(validation["status"] == "passed", "formal validation failed")

    atomic_write(HERE / "manifest.json", canonical(manifest))
    ledger_names = sorted(name for name in current_package_names()
                          if name != "SHA256SUMS")
    atomic_write(
        HERE / "SHA256SUMS",
        "".join(f"{sha256(HERE / name)}  {name}\n" for name in ledger_names),
    )

    verify_complete_ledger()
    verify_immutable_figure_package(original_names)
    stored_manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    require(stored_manifest["status"] == "formal",
            "stored manifest did not retain formal status")
    require(stored_manifest["git"]["sourceCommit"] == SOURCE_COMMIT,
            "stored manifest lost S binding")
    require(stored_manifest["git"]["figurePackageCommit"] == FIGURE_PACKAGE_COMMIT,
            "stored manifest lost F binding")
    require(stored_manifest["git"]["certificateCommit"] == CERTIFICATE_COMMIT,
            "stored manifest lost C binding")
    require(stored_manifest["contract"]["sha256"] == sha256(HERE / "contract.json"),
            "stored manifest contract binding changed")

    print(canonical({
        "event": "r073g-figure-formal-metadata-seal",
        "status": "formal",
        "package": str(HERE.relative_to(ROOT)),
        "sourceCommit": SOURCE_COMMIT,
        "figurePackageCommit": FIGURE_PACKAGE_COMMIT,
        "certificateCommit": CERTIFICATE_COMMIT,
        "immutableOriginalFilesVerified": EXPECTED_IMMUTABLE_COUNT,
        "errors": [],
        "warnings": [],
    }), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
