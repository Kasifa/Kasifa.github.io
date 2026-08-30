#!/usr/bin/env python3
"""Cross-validate the two R0.73G certificate paths and seal the file ledger."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "research/certificates/r073g"
SOURCE_COMMIT = "21c11ba3eef7f2b5dc3f107957e0744a0471745d"
SOURCE_PATHS = (
    "research/r073g_problem_freeze.md",
    "research/r073g_operator_derivation.md",
    "research/r073g_nonlinear_shadowing_proof.md",
    "research/r073g_independent_analytic_audit.md",
    "research/r073g_adversarial_audit.md",
    "research/r073g_gap_matrix.md",
    "research/r073g_literature_audit.md",
    "research/r073g_report-source.md",
)
EXPERIMENT_PATHS = (
    "experiments/r073g/README.md",
    "experiments/r073g/SHA256SUMS",
    "experiments/r073g/command.txt",
    "experiments/r073g/environment.json",
    "experiments/r073g/nonlinear_row_leakage_diagnostic.py",
    "experiments/r073g/fig-r073g-nonlinear-row-leakage.pdf",
    "experiments/r073g/fig-r073g-nonlinear-row-leakage.svg",
    "experiments/r073g/fig-r073g-nonlinear-row-leakage.png",
    "experiments/r073g/independent_validation.json",
    "experiments/r073g/independent_validation.py",
    "experiments/r073g/manifest.json",
    "experiments/r073g/nonlinear_row_leakage_convergence.csv",
    "experiments/r073g/nonlinear_row_leakage_rows.csv",
    "experiments/r073g/nonlinear_row_leakage_summary.json",
    "experiments/r073g/progress.ndjson",
    "experiments/r073g/requirements.txt",
)
SUMMARY_PATH = "experiments/r073g/nonlinear_row_leakage_summary.json"
FIGURE_ID = "fig-r073g-nonlinear-row-leakage"
FIGURE_DIR = f"figures/r073g/{FIGURE_ID}"
FIGURE_PATHS = tuple(
    f"{FIGURE_DIR}/{name}"
    for name in (
        "README.md", "SHA256SUMS", "caption.md", "command.txt", "config.json",
        "figure.pdf", "figure.png", "figure.svg", "manifest.json", "plot.py",
        "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png", "qa-protocol.md",
        "qa-report.md", "requirements.txt", "results.json", "validate.py",
        "validation.json",
    )
)
FIGURE_OUTPUT_PATHS = {
    "pdf": f"{FIGURE_DIR}/figure.pdf",
    "svg": f"{FIGURE_DIR}/figure.svg",
    "png": f"{FIGURE_DIR}/figure.png",
}
PACKAGE_SOURCES = (
    "README.md",
    "generate_certificate.py",
    "independent_recompute.py",
    "validate_certificate.py",
)
GENERATED_BEFORE_MANIFEST = (
    "certificate.json",
    "independent_recompute.json",
    "progress.ndjson",
    "validation.json",
)

CLAIM_BOUNDARY = {
    "machineProofOfProsePdeArgument": False,
    "finiteDiagnosticProvesContinuumTopSpace": False,
    "finiteDiagnosticProvesUniformH3Bound": False,
    "finiteLeakageProvesNonlinearInstability": False,
    "naturalSeedOrderOneDeparture": False,
    "threeDimensionalVortexStretchingFromSelectedPlanarRow": False,
    "generalThreeDimensionalRegularityConclusion": False,
    "finiteTimeSingularity": False,
    "Clay": False,
}
FINITE_BOUNDARY = {
    "actualFiniteTopEigenprofileUsed": True,
    "finiteBinary64Diagnostic": True,
    "twoIndependentFourierKernelsCrossChecked": True,
    "ordinaryCutoffAgreementIsTailBound": False,
    "finiteTopEqualsContinuumTop": False,
    "finiteH3CostProvesUniformContinuumH3Bound": False,
    "finiteLeakageProvesNonlinearInstability": False,
    "transitionThresholdEstablished": False,
    "threeDimensionalVortexStretchingPresentInThisPlanarRow": False,
    "clayProblemSolved": False,
}

PRIMARY_SOURCE_CHECKS = {
    "analyticSourceCommitResolvedExactly", "allAnalyticSourceBlobsBound",
    "physicalScalingAnchorsPresent", "rowIsometryAnchorsPresent",
    "h3LambdaSquaredLedgerAnchorsPresent", "riccatiThresholdAnchorsPresent",
    "allModeRemainderAndHalfGainAnchorsPresent", "positivePartBothBranchesAudited",
    "kzParityAnchorsPresent", "planarVorticityAndNoStretchingAnchorsPresent",
    "independentAnalyticAuditPassesAllSevenGates", "adversarialAuditFinalPass",
    "boundedLiteratureSearchMakesNoPriorityClaim", "gapDecisionLedgerExact",
    "reportDecisionLedgerExact",
}
PRIMARY_ALGEBRA_CHECKS = {
    "physicalBackgroundHeatFactorsAgree", "physicalProfileTimeIsFourTimesPhysicalTime",
    "normalizedShearCoefficientIsOneHalf", "normalizedDiffusionCoefficientIsOne",
    "rowIsometryPolynomialIdentity", "realPairNormalizationIsOne",
    "twoEllipticLiftsGiveLambdaSquared", "quadraticH3CostAndSeedPowerCancel",
    "riccatiDenominatorAtLeastThreeQuarters", "riccatiComparisonMultiplierBelowTwo",
    "halfGainArithmetic", "positivePartBranchMGeKappaReducesToKappa",
    "positivePartBranchMLtKappaReducesToM", "quadraticKzParityExcludesLaunchingRows",
    "cubicKzParityCanReturnToLaunchingRows", "planarVorticityStretchingZero",
}
PRIMARY_EXPERIMENT_CHECKS = {
    "experimentCommitDistinctFromAnalyticSourceCommit",
    "experimentCommitDescendsFromAnalyticSourceCommit",
    "diagnosticSourceUnchangedFromAnalyticCommit",
    "analyticSourceBlobsUnchangedAtExperimentCommit", "experimentTreeInventoryExact",
    "experimentManifestCoreValidated", "experimentManifestFileBindingsExact",
    "experimentManifestScientificBindingsExact", "experimentSha256LedgerExact",
    "formalExperimentSchema", "formalExperimentNotSmoke",
    "experimentSourceProvenanceMatchesAnalyticCommit",
    "experimentGridMatchesFormalContract", "experimentRowInventoryExactUniqueGrid",
    "experimentComparisonInventoryExactUniqueGrid",
    "experimentRowsCsvMatchesSummaryExactly",
    "experimentConvergenceCsvMatchesSummaryExactly",
    "kernelErrorThresholdRecomputedFromCommittedRows", "summaryObservedRangesRecomputed",
    "independentValidationInventoryAndThresholdRecomputed",
    "experimentOutputBindingsMatchCommittedBytes", "finiteClaimBoundaryExactFailClosed",
}
PRIMARY_FIGURE_CHECKS = {
    "figureCommitDistinctFromExperimentCommit", "figureCommitDescendsFromExperimentCommit",
    "figurePackageTreeInventoryExact", "figurePackageManifestFileBindingsExact",
    "figurePackageSha256LedgerExact", "figurePackageManifestValidated",
    "figurePackageValidationPassed", "figurePackageVisualQaPassed",
    "figurePackageOutputsBoundExactly", "figurePackageResultsBoundExactly",
}
PRIMARY_CHECK_KEYS = (
    PRIMARY_SOURCE_CHECKS | PRIMARY_ALGEBRA_CHECKS
    | PRIMARY_EXPERIMENT_CHECKS | PRIMARY_FIGURE_CHECKS
)

INDEPENDENT_SOURCE_CHECKS = {
    "sourceCommitExistsAndResolvesExactly", "experimentCommitExistsAndResolvesExactly",
    "figureCommitExistsAndResolvesExactly", "allEightSourceBlobsRecomputed",
    "proofContainsPhysicalBackgroundAndEndpoint",
    "proofContainsH3RiccatiAndAllModeRemainder", "auditContainsSevenPassVerdicts",
    "gapStatesRecomputedExactly", "reportStatesRecomputedExactly",
}
INDEPENDENT_ALGEBRA_CHECKS = {
    "independentPhysicalHeatIdentity", "independentRowIsometryIdentity",
    "independentH3ExponentLedger", "independentRiccatiLedger",
    "independentHalfGainLedger", "independentPositivePartTwoBranches",
    "independentKzParity", "independentPlanarStretchingIdentity",
}
INDEPENDENT_EXPERIMENT_CHECKS = {
    "independentExperimentCommitIsLaterDescendant",
    "independentExperimentScriptBlobUnchanged",
    "independentAnalyticBlobsUnchangedAtExperimentCommit",
    "independentExperimentTreeInventoryExact", "independentExperimentManifestCore",
    "independentExperimentManifestFiles", "independentExperimentScientificBindings",
    "independentExperimentSha256Ledger", "independentExperimentSchemaAndMode",
    "independentExperimentSourceProvenance", "independentFormalGrid",
    "independentExactUniqueRowGrid", "independentExactUniqueComparisonGrid",
    "independentRowsCsvSummaryIdentity", "independentComparisonsCsvSummaryIdentity",
    "independentKernelThresholdRecomputed", "independentValidatorThresholdRecomputed",
    "independentCommittedOutputsMatchSummary", "independentFiniteBoundaryExact",
}
INDEPENDENT_FIGURE_CHECKS = {
    "independentFigureCommitIsLaterDescendant", "independentFigureTreeInventoryExact",
    "independentFigureManifestFileBindings", "independentFigureSha256Ledger",
    "independentFigureManifestValidated", "independentFigureValidationPassed",
    "independentFigureVisualQaPassed", "independentFigureOutputsBound",
    "independentFigureResultsBound",
}
INDEPENDENT_CHECK_KEYS = (
    INDEPENDENT_SOURCE_CHECKS | INDEPENDENT_ALGEBRA_CHECKS
    | INDEPENDENT_EXPERIMENT_CHECKS | INDEPENDENT_FIGURE_CHECKS
)

CERTIFICATE_KEYS = {
    "schemaVersion", "release", "created", "status", "evidenceClass",
    "sourceCommit", "experimentCommit", "figurePackageCommit", "sourceBindings",
    "experimentBindings", "figureBindings", "checks", "exactSentinels",
    "claimLedgers", "theorem", "finiteDiagnostic", "journalFigure",
    "claimBoundary", "sealState",
}
INDEPENDENT_KEYS = {
    "schemaVersion", "release", "sourceCommit", "experimentCommit",
    "figurePackageCommit", "sourceBindings", "experimentBindings", "figureBindings",
    "checks", "allChecksPass", "exactSentinels", "claimLedgers", "finiteDiagnostic",
    "journalFigure", "claimBoundary",
}
FINITE_RECORD_KEYS = {
    "schemaVersion", "evidenceClass", "diagnosticOnly", "smokeMode", "parameters",
    "crossValidation", "primaryCutoffObservedRanges", "claimBoundary",
    "continuumConclusion",
}
JOURNAL_FIGURE_KEYS = {
    "figureId", "status", "pdf", "svg", "png", "validationStatus",
    "visualQaStatus", "gitSealed",
}
EXPECTED_GAP_LEDGER = {
    "exactDecayingShearPerturbationEquation": "CLOSED",
    "selectedSeedPlanarInvariantClass": "CLOSED",
    "selectedNonlinearOrbitGlobalSmoothness": "CLOSED",
    "topEigenvectorPolynomialH3Cost": "CLOSED",
    "fixedWindowH3Bootstrap": "CLOSED",
    "allModeQuadraticRemainderBound": "CLOSED",
    "nonlinearRelativeAmplification": "CLOSED",
    "topEigenvectorDoubleRowLeakage": "CLOSED",
    "singleLinearRowNonlinearInvariant": "FALSE",
    "selectedRowCanCreateThreeDimensionalVortexStretching": "FALSE",
    "oneRowGainAloneImpliesOrderOneDeparture": "FALSE_AS_INFERENCE",
    "oneRowGainAloneImpliesFiniteTimeSingularity": "FALSE",
    "naturalSeedOrderOneDeparture": "OPEN",
    "sharpBilinearEvolutionAtUnstableRate": "OPEN",
    "transverseThreeDimensionalTriadClosure": "OPEN",
    "singleBackgroundSingleOrbitInstability": "OPEN",
    "completeOSSquireA2DirectSum": "OPEN",
    "Clay": "OPEN",
}
EXPECTED_REPORT_LEDGER = {
    **EXPECTED_GAP_LEDGER,
    "kineticL2QuadraticRemainderBound": "FALSE",
    "targetedCubicModeConvolutionEstimate": "OPEN",
    "harmonicResolvedEvenOddPropagation": "OPEN",
}
EXPECTED_REPORT_LEDGER.pop("sharpBilinearEvolutionAtUnstableRate")


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"


def full_commit(value: str) -> str:
    if re.fullmatch(r"[0-9a-f]{40}", value) is None:
        raise argparse.ArgumentTypeError("use a full lowercase 40-character hash")
    return value


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment-commit", required=True, type=full_commit)
    parser.add_argument("--figure-package-commit", required=True, type=full_commit)
    return parser.parse_args()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def local_binding(path: Path) -> dict[str, object]:
    return {
        "path": str(path.relative_to(ROOT)),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def git_binding(commit: str, relative: str) -> dict[str, object]:
    data = subprocess.check_output(["git", "show", f"{commit}:{relative}"], cwd=ROOT)
    object_name = subprocess.check_output(
        ["git", "rev-parse", f"{commit}:{relative}"], cwd=ROOT, text=True
    ).strip()
    return {
        "path": relative,
        "commit": commit,
        "gitBlob": object_name,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def git_json(commit: str, relative: str) -> dict[str, object]:
    def reject(value: str) -> object:
        raise ValueError(f"non-finite JSON constant in {relative}: {value}")

    value = json.loads(
        subprocess.check_output(["git", "show", f"{commit}:{relative}"], cwd=ROOT),
        parse_constant=reject,
    )
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object at {relative}")
    return value


def resolved(commit: str) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", f"{commit}^{{commit}}"], cwd=ROOT, text=True
    ).strip()


def is_ancestor(ancestor: str, descendant: str) -> bool:
    return subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=ROOT,
        check=False,
    ).returncode == 0


def exact_true_checks(value: object, expected_keys: set[str]) -> bool:
    return (
        isinstance(value, dict)
        and set(value) == expected_keys
        and all(item is True for item in value.values())
    )


def expected_journal_figure(
    figure_bindings: list[dict[str, object]],
) -> dict[str, object]:
    by_path = {row["path"]: row for row in figure_bindings}
    return {
        "figureId": FIGURE_ID,
        "status": "validated",
        "pdf": {
            key: by_path[FIGURE_OUTPUT_PATHS["pdf"]][key]
            for key in ("path", "bytes", "sha256")
        },
        "svg": {
            key: by_path[FIGURE_OUTPUT_PATHS["svg"]][key]
            for key in ("path", "bytes", "sha256")
        },
        "png": {
            **{
                key: by_path[FIGURE_OUTPUT_PATHS["png"]][key]
                for key in ("path", "bytes", "sha256")
            },
            "dpi": 600,
        },
        "validationStatus": "passed",
        "visualQaStatus": "passed",
        "gitSealed": False,
    }


def local_json(path: Path) -> dict[str, object]:
    def reject(value: str) -> object:
        raise ValueError(f"non-finite JSON constant in {path.name}: {value}")

    value = json.loads(path.read_text(encoding="utf-8"), parse_constant=reject)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object in {path.name}")
    return value


def values_by_state(ledger: dict[str, str], state: str) -> set[str]:
    return {name for name, value in ledger.items() if value == state}


def main() -> int:
    args = arguments()
    if resolved(SOURCE_COMMIT) != SOURCE_COMMIT:
        raise RuntimeError("analytic source commit did not resolve exactly")
    if resolved(args.experiment_commit) != args.experiment_commit:
        raise RuntimeError("experiment commit did not resolve exactly")
    if resolved(args.figure_package_commit) != args.figure_package_commit:
        raise RuntimeError("figure package commit did not resolve exactly")

    certificate = local_json(OUT / "certificate.json")
    independent = local_json(OUT / "independent_recompute.json")
    source_bindings = [git_binding(SOURCE_COMMIT, path) for path in SOURCE_PATHS]
    experiment_bindings = [
        git_binding(args.experiment_commit, path) for path in EXPERIMENT_PATHS
    ]
    figure_bindings = [
        git_binding(args.figure_package_commit, path) for path in FIGURE_PATHS
    ]
    journal_figure = expected_journal_figure(figure_bindings)
    summary = git_json(args.experiment_commit, SUMMARY_PATH)
    expected_finite = {
        "schemaVersion": summary.get("schemaVersion"),
        "evidenceClass": summary.get("evidenceClass"),
        "diagnosticOnly": summary.get("diagnosticOnly"),
        "smokeMode": summary.get("smokeMode"),
        "parameters": summary.get("parameters"),
        "crossValidation": summary.get("crossValidation"),
        "primaryCutoffObservedRanges": summary.get("primaryCutoffObservedRanges"),
        "claimBoundary": summary.get("claimBoundary"),
        "continuumConclusion": False,
    }
    gap = certificate["claimLedgers"]["gapMatrixReleaseDecisions"]
    report = certificate["claimLedgers"]["reportSourceBoundary"]
    exact = certificate["exactSentinels"]

    checks = {
        "certificateTopLevelKeysExact": set(certificate) == CERTIFICATE_KEYS,
        "independentTopLevelKeysExact": set(independent) == INDEPENDENT_KEYS,
        "certificateSchemasExact": (
            certificate.get("schemaVersion")
            == "r073g-planar-nonlinear-shadowing-certificate-v1"
            and certificate.get("release") == "R0.73G"
            and independent.get("schemaVersion")
            == "r073g-independent-certificate-recompute-v1"
            and independent.get("release") == "R0.73G"
        ),
        "sourceCommitAgreement": (
            certificate["sourceCommit"]
            == independent["sourceCommit"]
            == SOURCE_COMMIT
        ),
        "experimentCommitParameterAgreement": (
            certificate["experimentCommit"]
            == independent["experimentCommit"]
            == args.experiment_commit
        ),
        "figureCommitParameterAgreement": (
            certificate.get("figurePackageCommit")
            == independent.get("figurePackageCommit")
            == args.figure_package_commit
        ),
        "commitChainExact": (
            args.experiment_commit != SOURCE_COMMIT
            and args.figure_package_commit != args.experiment_commit
            and is_ancestor(SOURCE_COMMIT, args.experiment_commit)
            and is_ancestor(args.experiment_commit, args.figure_package_commit)
        ),
        "analyticBlobsPreservedAtExperimentCommit": all(
            git_binding(args.experiment_commit, path)["sha256"]
            == git_binding(SOURCE_COMMIT, path)["sha256"]
            for path in SOURCE_PATHS
        ),
        "sourceBindingsIndependentAgreement": (
            certificate["sourceBindings"]
            == independent["sourceBindings"]
            == source_bindings
        ),
        "experimentBindingsIndependentAgreement": (
            certificate["experimentBindings"]
            == independent["experimentBindings"]
            == experiment_bindings
        ),
        "figureBindingsIndependentAgreement": (
            certificate.get("figureBindings")
            == independent.get("figureBindings")
            == figure_bindings
        ),
        "primaryAllChecksPass": (
            certificate["status"] == "validated"
            and exact_true_checks(certificate.get("checks"), PRIMARY_CHECK_KEYS)
        ),
        "independentAllChecksPass": (
            independent["allChecksPass"] is True
            and exact_true_checks(
                independent.get("checks"), INDEPENDENT_CHECK_KEYS
            )
        ),
        "exactSentinelsAgreeIndependently": (
            exact == independent["exactSentinels"]
        ),
        "claimLedgersAgreeIndependently": (
            certificate["claimLedgers"] == independent["claimLedgers"]
            and set(certificate["claimLedgers"])
            == {"gapMatrixReleaseDecisions", "reportSourceBoundary"}
        ),
        "gapBoundaryNamesAndStatesExact": gap == EXPECTED_GAP_LEDGER,
        "reportBoundaryNamesAndStatesExact": report == EXPECTED_REPORT_LEDGER,
        "finiteDiagnosticRecordsAgreeIndependently": (
            certificate["finiteDiagnostic"] == independent["finiteDiagnostic"]
            == expected_finite
            and set(certificate["finiteDiagnostic"]) == FINITE_RECORD_KEYS
        ),
        "journalFigureExactAndNoFormalFigure": (
            "formalFigure" not in certificate
            and "formalFigure" not in independent
            and certificate.get("journalFigure")
            == independent.get("journalFigure")
            == journal_figure
            and set(certificate["journalFigure"]) == JOURNAL_FIGURE_KEYS
            and set(certificate["journalFigure"]["pdf"])
            == {"path", "bytes", "sha256"}
            and set(certificate["journalFigure"]["svg"])
            == {"path", "bytes", "sha256"}
            and set(certificate["journalFigure"]["png"])
            == {"path", "bytes", "sha256", "dpi"}
        ),
        "physicalScalingSentinelExact": (
            exact["physicalScaling"]["backgroundTimeDerivativeFactor"] == [8, 1]
            and exact["physicalScaling"]["backgroundLaplacianFactor"] == [8, 1]
            and exact["physicalScaling"]["profileTimePerPhysicalTime"] == [4, 1]
            and exact["physicalScaling"]["physicalEndpointPerProfileEndpoint"]
            == [1, 4]
            and exact["physicalScaling"]["normalizedShearCoefficient"] == [1, 2]
            and exact["physicalScaling"]["normalizedDiffusionCoefficient"]
            == [1, 1]
        ),
        "rowIsometrySentinelExact": (
            exact["rowIsometry"]["numeratorPolynomialN2AndConstant"]
            == exact["rowIsometry"]["denominatorPolynomialN2AndConstant"]
            and exact["rowIsometry"]["realConjugatePairNormSquared"] == [1, 1]
        ),
        "h3ExponentLedgerExact": (
            exact["h3ExponentLedger"]["topVectorLambdaExponent"] == 2
            and exact["h3ExponentLedger"][
                "quadraticRemainderLambdaExponent"
            ]
            == 4
            and exact["h3ExponentLedger"]["seedCeilingLambdaExponent"] == -4
            and exact["h3ExponentLedger"]["netPolynomialExponent"] == 0
        ),
        "riccatiSentinelExact": (
            exact["riccati"]["maximumDenominatorLoss"] == [1, 4]
            and exact["riccati"]["denominatorLowerBound"] == [3, 4]
            and exact["riccati"]["comparisonMultiplier"] == [4, 3]
            and exact["riccati"]["advertisedMultiplier"] == [2, 1]
        ),
        "halfGainAndPositivePartBranchesExact": (
            exact["halfGain"]["retainedSignalNormalizedByKfInverse"] == [1, 2]
            and exact["positivePartBranches"]["branchMGeKappaExpression"]
            == [0, 1]
            and exact["positivePartBranches"]["branchMGeKappaTarget"] == [0, 1]
            and exact["positivePartBranches"]["branchMLtKappaExpression"]
            == [1, 0]
            and exact["positivePartBranches"][
                "branchMLtKappaUpperUsesAssumptionMltKappa"
            ]
            is True
        ),
        "kzParitySentinelExact": (
            exact["kzParity"]["launchingRows"] == [-1, 1]
            and exact["kzParity"]["quadraticRows"] == [-2, 0, 2]
            and exact["kzParity"]["quadraticReturnsToLaunchingRows"] is False
            and exact["kzParity"]["cubicCanReturnToLaunchingRows"] is True
        ),
        "planarStretchingSentinelExact": (
            exact["planarVorticity"]["vorticityComponentPattern"]
            == ["omega", 0, 0]
            and exact["planarVorticity"]["x1Derivative"] == 0
            and exact["planarVorticity"]["stretchingZero"] is True
        ),
        "claimBoundaryExactFailClosed": (
            certificate.get("claimBoundary")
            == independent.get("claimBoundary")
            == CLAIM_BOUNDARY
        ),
        "finiteEvidenceBoundaryFailClosed": (
            certificate["finiteDiagnostic"]["diagnosticOnly"] is True
            and certificate["finiteDiagnostic"]["continuumConclusion"] is False
            and certificate["finiteDiagnostic"]["claimBoundary"]
            == FINITE_BOUNDARY
        ),
        "sealStateHonest": (
            certificate.get("sealState") == {
                "analyticSourcesAtImmutableGitCommit": True,
                "experimentArtifactsAtImmutableGitCommit": True,
                "journalFigureArtifactsAtImmutableGitCommit": True,
                "certificatePackageGitSealed": False,
            }
        ),
    }
    validation = {
        "schemaVersion": "r073g-certificate-validation-v1",
        "release": "R0.73G",
        "sourceCommit": SOURCE_COMMIT,
        "experimentCommit": args.experiment_commit,
        "figurePackageCommit": args.figure_package_commit,
        "checks": checks,
        "allChecksPass": all(checks.values()),
        "claimLedgers": certificate["claimLedgers"],
        "claimBoundary": certificate["claimBoundary"],
        "journalFigure": journal_figure,
    }
    (OUT / "validation.json").write_text(canonical(validation), encoding="utf-8")
    with (OUT / "progress.ndjson").open("a", encoding="utf-8") as stream:
        stream.write(
            json.dumps(
                {
                    "event": "certificate-validation-complete",
                    "allChecksPass": validation["allChecksPass"],
                    "experimentCommit": args.experiment_commit,
                    "figurePackageCommit": args.figure_package_commit,
                },
                sort_keys=True,
            )
            + "\n"
        )
    if not validation["allChecksPass"]:
        return 2

    package_sources = [local_binding(OUT / name) for name in PACKAGE_SOURCES]
    output_bindings = [
        local_binding(OUT / name) for name in GENERATED_BEFORE_MANIFEST
    ]
    manifest = {
        "schemaVersion": "r073g-certificate-manifest-v1",
        "release": "R0.73G",
        "created": "2026-08-30",
        "status": "validated-content-addressed-unsealed",
        "sourceCommit": SOURCE_COMMIT,
        "experimentCommit": args.experiment_commit,
        "figurePackageCommit": args.figure_package_commit,
        "sourceBindingKind": "immutable Git blobs at the analytic source commit",
        "experimentBindingKind": (
            "immutable Git blobs at the required formal experiment commit"
        ),
        "figureBindingKind": (
            "immutable Git blobs at the required validated journal-figure commit"
        ),
        "sourceBindings": source_bindings,
        "experimentBindings": experiment_bindings,
        "figureBindings": figure_bindings,
        "journalFigure": journal_figure,
        "packageSourceBindings": package_sources,
        "outputBindings": output_bindings,
        "files": [*PACKAGE_SOURCES, *GENERATED_BEFORE_MANIFEST],
        "outputs": [
            *GENERATED_BEFORE_MANIFEST,
            "manifest.json",
            "SHA256SUMS",
        ],
        "inventoryPolicy": {
            "scope": "all regular files directly inside research/certificates/r073g",
            "manifestFilesExcludes": ["manifest.json", "SHA256SUMS"],
            "sha256LedgerExcludes": ["SHA256SUMS"],
            "cacheDirectoriesForbidden": True,
        },
        "sealState": certificate["sealState"],
        "limitations": [
            "the certificate checks immutable provenance, exact algebraic implications, diagnostic bytes, and claim boundaries; it does not machine-prove the prose PDE theorem",
            "the nonlinear relative-amplification theorem is conditional on the R0.73F moving-bundle lower law",
            "the finite binary64 package is diagnostic only and proves no continuum spectral, Sobolev, nonlinear-instability, transition-threshold, or regularity claim",
            "the journal figure is presentation evidence for the finite diagnostic only; its validation and visual QA do not add a continuum conclusion",
            "the constructed nonlinear family remains in a globally regular planar subsystem with zero three-dimensional vortex stretching",
            "natural-seed order-one departure, transverse triad closure, finite-time singularity, general 3D regularity, and the Clay problem remain open",
        ],
    }
    (OUT / "manifest.json").write_text(canonical(manifest), encoding="utf-8")

    unexpected_directories = [path.name for path in OUT.iterdir() if path.is_dir()]
    if unexpected_directories:
        raise RuntimeError(
            "certificate directory contains subdirectories: "
            + ", ".join(sorted(unexpected_directories))
        )
    expected_files = {
        *PACKAGE_SOURCES,
        *GENERATED_BEFORE_MANIFEST,
        "manifest.json",
    }
    actual_files = {
        path.name
        for path in OUT.iterdir()
        if path.is_file() and path.name != "SHA256SUMS"
    }
    if actual_files != expected_files:
        missing = sorted(expected_files - actual_files)
        extra = sorted(actual_files - expected_files)
        raise RuntimeError(
            f"certificate inventory mismatch; missing={missing}, extra={extra}"
        )
    ledger_paths = sorted(
        (
            path
            for path in OUT.iterdir()
            if path.is_file() and path.name != "SHA256SUMS"
        ),
        key=lambda path: path.name,
    )
    (OUT / "SHA256SUMS").write_text(
        "".join(f"{sha256(path)}  {path.name}\n" for path in ledger_paths),
        encoding="utf-8",
    )
    print(
        canonical(
            {
                "event": "r073g-certificate-validated",
                "allChecksPass": True,
                "experimentCommit": args.experiment_commit,
                "figurePackageCommit": args.figure_package_commit,
            }
        ),
        end="",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
