#!/usr/bin/env python3
"""Generate the primary R0.73G provenance and exact-algebra certificate."""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction
import hashlib
import io
import json
import math
from pathlib import Path
import re
import subprocess
from typing import Iterable


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "research/certificates/r073g"
SOURCE_COMMIT = "21c11ba3eef7f2b5dc3f107957e0744a0471745d"
ANALYTIC_PATHS = (
    "research/r073g_problem_freeze.md",
    "research/r073g_operator_derivation.md",
    "research/r073g_nonlinear_shadowing_proof.md",
    "research/r073g_independent_analytic_audit.md",
    "research/r073g_adversarial_audit.md",
    "research/r073g_gap_matrix.md",
    "research/r073g_literature_audit.md",
    "research/r073g_report-source.md",
)
DIAGNOSTIC_SOURCE = "experiments/r073g/nonlinear_row_leakage_diagnostic.py"
EXPERIMENT_PATHS = (
    "experiments/r073g/README.md",
    "experiments/r073g/SHA256SUMS",
    "experiments/r073g/command.txt",
    "experiments/r073g/environment.json",
    DIAGNOSTIC_SOURCE,
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
ROWS_PATH = "experiments/r073g/nonlinear_row_leakage_rows.csv"
CONVERGENCE_PATH = "experiments/r073g/nonlinear_row_leakage_convergence.csv"
EXPERIMENT_MANIFEST_PATH = "experiments/r073g/manifest.json"
EXPERIMENT_SHA256_PATH = "experiments/r073g/SHA256SUMS"
INDEPENDENT_VALIDATION_PATH = "experiments/r073g/independent_validation.json"
INDEPENDENT_VALIDATOR_PATH = "experiments/r073g/independent_validation.py"
EXPECTED_SCIENTIFIC_OUTPUTS = (
    "nonlinear_row_leakage_rows.csv",
    "nonlinear_row_leakage_convergence.csv",
    "nonlinear_row_leakage_summary.json",
    "fig-r073g-nonlinear-row-leakage.pdf",
    "fig-r073g-nonlinear-row-leakage.svg",
    "fig-r073g-nonlinear-row-leakage.png",
)
EXPECTED_SUMMARY_OUTPUTS = tuple(
    name for name in EXPECTED_SCIENTIFIC_OUTPUTS
    if name != "nonlinear_row_leakage_summary.json"
)
EXPECTED_CUTOFFS = [24, 48, 96, 128]
EXPECTED_EPSILONS = [0.01, 0.005, 0.002, 0.001, 0.0005, 0.0002, 0.0001]
EXPECTED_CUTOFF_PAIRS = [(24, 48), (48, 96), (96, 128)]
EXPECTED_KERNEL_TOLERANCE = 5.0e-12
EXPECTED_INDEPENDENT_TOLERANCE = 2.0e-11

ROW_FIELDS = (
    "schemaVersion",
    "evidenceClass",
    "diagnosticOnly",
    "N",
    "dimension",
    "epsilon",
    "absoluteLambda",
    "topEigenvalueFastReal",
    "topEigenvalueFastImag",
    "topPhysicalGrowthRateReal",
    "topClusterDimensionAtRealTolerance",
    "topRealGapBelowCluster",
    "topEigenResidualRelative",
    "physicalPositiveRowL2",
    "physicalPositiveRowH3",
    "physicalH3ToL2Cost",
    "kineticBoundaryMassFraction",
    "kineticOuterThreeMassFraction",
    "h3OuterThreeContributionFraction",
    "kz2ProjectedLeakagePositiveUnitRowKernelA",
    "kz2ProjectedLeakagePositiveUnitRowKernelB",
    "kz2ProjectedLeakageUnitRealPairKernelA",
    "kz0ProjectedLeakageUnscaledRealPairKernelA",
    "kz0ProjectedLeakageUnscaledRealPairKernelB",
    "kz0ProjectedLeakageUnitRealPairKernelA",
    "kz2KernelScaleOneDifference",
    "kz0KernelScaleOneDifference",
    "maximumKernelCoefficientScaleOneDifference",
    "kernelCheckPass",
)
CONVERGENCE_FIELDS = (
    "schemaVersion",
    "evidenceClass",
    "diagnosticOnly",
    "epsilon",
    "absoluteLambda",
    "coarseN",
    "fineN",
    "topEigenvalueRelativeChange",
    "physicalH3ToL2RelativeChange",
    "kz2LeakageRelativeChange",
    "kz0LeakageRelativeChange",
    "maximumRelativeChange",
    "ordinaryCutoffAgreementIsTailBound",
)
FINITE_CLAIM_BOUNDARY = {
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

FIGURE_ID = "fig-r073g-nonlinear-row-leakage"
FIGURE_DIR = f"figures/r073g/{FIGURE_ID}"
FIGURE_PATHS = tuple(
    f"{FIGURE_DIR}/{name}"
    for name in (
        "README.md",
        "SHA256SUMS",
        "caption.md",
        "command.txt",
        "config.json",
        "figure.pdf",
        "figure.png",
        "figure.svg",
        "manifest.json",
        "plot.py",
        "qa-final-size.png",
        "qa-grayscale.png",
        "qa-pdf.png",
        "qa-protocol.md",
        "qa-report.md",
        "requirements.txt",
        "results.json",
        "validate.py",
        "validation.json",
    )
)
FIGURE_MANIFEST_PATH = f"{FIGURE_DIR}/manifest.json"
FIGURE_VALIDATION_PATH = f"{FIGURE_DIR}/validation.json"
FIGURE_RESULTS_PATH = f"{FIGURE_DIR}/results.json"
FIGURE_SHA256_PATH = f"{FIGURE_DIR}/SHA256SUMS"
FIGURE_OUTPUT_PATHS = {
    "pdf": f"{FIGURE_DIR}/figure.pdf",
    "svg": f"{FIGURE_DIR}/figure.svg",
    "png": f"{FIGURE_DIR}/figure.png",
}
FIGURE_CLAIM_BOUNDARY = {
    "clayProblemSolved": False,
    "finiteH3CostProvesUniformContinuumH3Bound": False,
    "finiteLeakageProvesNonlinearInstability": False,
    "finiteTopEqualsContinuumTop": False,
    "formalFiniteDiagnosticFigure": True,
    "ordinaryCutoffAgreementIsTailBound": False,
    "threeDimensionalVortexStretchingPresentInThisPlanarRow": False,
    "transitionThresholdEstablished": False,
}
FIGURE_VALIDATION_CHECK_KEYS = {
    "claimBoundaryFailClosed",
    "commitChainPassed",
    "experimentPackageValidated",
    "finiteSentinelsPassed",
    "inputHashesPassed",
    "pdfTextPassed",
    "physicalDimensionsPassed",
    "png600DpiPassed",
    "primaryAndIndependentKernelChecksPassed",
    "qaRastersPresent",
    "scientificRerunDeterminismPassed",
    "singlePagePdf",
    "svgVectorTextPassed",
    "visualQaPassed",
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
    "exactDecayingShearPerturbationEquation": "CLOSED",
    "selectedSeedPlanarInvariantClass": "CLOSED",
    "selectedNonlinearOrbitGlobalSmoothness": "CLOSED",
    "topEigenvectorPolynomialH3Cost": "CLOSED",
    "fixedWindowH3Bootstrap": "CLOSED",
    "allModeQuadraticRemainderBound": "CLOSED",
    "nonlinearRelativeAmplification": "CLOSED",
    "topEigenvectorDoubleRowLeakage": "CLOSED",
    "singleLinearRowNonlinearInvariant": "FALSE",
    "kineticL2QuadraticRemainderBound": "FALSE",
    "selectedRowCanCreateThreeDimensionalVortexStretching": "FALSE",
    "oneRowGainAloneImpliesOrderOneDeparture": "FALSE_AS_INFERENCE",
    "oneRowGainAloneImpliesFiniteTimeSingularity": "FALSE",
    "naturalSeedOrderOneDeparture": "OPEN",
    "targetedCubicModeConvolutionEstimate": "OPEN",
    "harmonicResolvedEvenOddPropagation": "OPEN",
    "transverseThreeDimensionalTriadClosure": "OPEN",
    "singleBackgroundSingleOrbitInstability": "OPEN",
    "completeOSSquireA2DirectSum": "OPEN",
    "Clay": "OPEN",
}


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"


def commit_argument(value: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{40}", value):
        raise argparse.ArgumentTypeError(
            "experiment commit must be a full lowercase 40-character Git hash"
        )
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--experiment-commit",
        required=True,
        type=commit_argument,
        help="full commit that formally seals the R0.73G finite outputs",
    )
    parser.add_argument(
        "--figure-package-commit",
        required=True,
        type=commit_argument,
        help="full commit that seals the validated R0.73G journal figure package",
    )
    return parser.parse_args()


def git_bytes(commit: str, relative: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{relative}"], cwd=ROOT)


def resolve_commit(commit: str) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", f"{commit}^{{commit}}"], cwd=ROOT, text=True
    ).strip()


def is_ancestor(ancestor: str, descendant: str) -> bool:
    return (
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", ancestor, descendant],
            cwd=ROOT,
            check=False,
        ).returncode
        == 0
    )


def git_binding(commit: str, relative: str) -> dict[str, object]:
    payload = git_bytes(commit, relative)
    blob = subprocess.check_output(
        ["git", "rev-parse", f"{commit}:{relative}"], cwd=ROOT, text=True
    ).strip()
    return {
        "path": relative,
        "commit": commit,
        "gitBlob": blob,
        "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
    }


def json_blob(commit: str, relative: str) -> dict[str, object]:
    def reject_constant(value: str) -> object:
        raise ValueError(f"non-finite JSON constant in {relative}: {value}")

    value = json.loads(
        git_bytes(commit, relative),
        parse_constant=reject_constant,
    )
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object at {relative}")
    return value


def git_tree_paths(commit: str, directory: str) -> set[str]:
    output = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", commit, directory],
        cwd=ROOT,
        text=True,
    )
    return {line for line in output.splitlines() if line}


def finite_number(value: object) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    )


def close(left: object, right: object, tolerance: float = 1.0e-14) -> bool:
    return finite_number(left) and finite_number(right) and math.isclose(
        float(left),
        float(right),
        rel_tol=tolerance,
        abs_tol=tolerance,
    )


def csv_rows(
    commit: str,
    relative: str,
    expected_fields: tuple[str, ...],
) -> list[dict[str, str]]:
    stream = io.StringIO(git_bytes(commit, relative).decode("utf-8"), newline="")
    reader = csv.DictReader(stream, strict=True)
    if tuple(reader.fieldnames or ()) != expected_fields:
        raise ValueError(f"unexpected CSV header at {relative}")
    rows = list(reader)
    if any(None in row or any(value is None for value in row.values()) for row in rows):
        raise ValueError(f"malformed CSV row at {relative}")
    return rows


def csv_cell(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("non-finite summary value")
        return format(value, ".17g")
    return str(value)


def csv_matches_summary(
    committed_rows: list[dict[str, str]],
    summary_rows: object,
    fields: tuple[str, ...],
) -> bool:
    if not isinstance(summary_rows, list) or len(committed_rows) != len(summary_rows):
        return False
    for csv_row, summary_row in zip(committed_rows, summary_rows):
        if not isinstance(summary_row, dict) or set(summary_row) != set(fields):
            return False
        if any(csv_row[field] != csv_cell(summary_row[field]) for field in fields):
            return False
    return True


def strict_sha256_ledger(
    commit: str,
    relative: str,
    expected_paths: set[str],
) -> bool:
    directory = str(Path(relative).parent)
    entries: dict[str, str] = {}
    for raw in git_bytes(commit, relative).decode("utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/\n]+)", raw)
        if match is None or match.group(2) in entries:
            return False
        entries[match.group(2)] = match.group(1)
    expected_names = {Path(path).name for path in expected_paths}
    if set(entries) != expected_names:
        return False
    return all(
        entries[Path(path).name] == hashlib.sha256(git_bytes(commit, path)).hexdigest()
        for path in expected_paths
        if str(Path(path).parent) == directory
    )


def manifest_bindings_match(
    commit: str,
    rows: object,
    expected_paths: set[str],
) -> bool:
    if not isinstance(rows, list) or len(rows) != len(expected_paths):
        return False
    by_path: dict[str, dict[str, object]] = {}
    for row in rows:
        if (
            not isinstance(row, dict)
            or set(row) != {"path", "bytes", "sha256"}
            or not isinstance(row.get("path"), str)
            or row["path"] in by_path
        ):
            return False
        by_path[row["path"]] = row
    if set(by_path) != expected_paths:
        return False
    return all(
        by_path[path]["bytes"] == len(git_bytes(commit, path))
        and by_path[path]["sha256"]
        == hashlib.sha256(git_bytes(commit, path)).hexdigest()
        for path in expected_paths
    )


def contains_all(text: str, tokens: Iterable[str]) -> bool:
    return all(token in text for token in tokens)


def parse_decision_ledger(text: str) -> dict[str, str]:
    allowed = "CLOSED|FALSE|FALSE_AS_INFERENCE|OPEN"
    rows: dict[str, str] = {}
    for line in text.splitlines():
        match = re.fullmatch(rf"([A-Za-z][A-Za-z0-9]*)=({allowed})", line.strip())
        if match:
            key, state = match.groups()
            if key in rows:
                raise RuntimeError(f"duplicate release decision key: {key}")
            rows[key] = state
    return rows


def fraction_pair(value: Fraction) -> list[int]:
    return [value.numerator, value.denominator]


def subtract_form(
    left: tuple[int, int], right: tuple[int, int]
) -> tuple[int, int]:
    return (left[0] - right[0], left[1] - right[1])


def exact_sentinels() -> tuple[dict[str, object], dict[str, bool]]:
    amplitude = Fraction(2)
    profile_speed = Fraction(4)
    shear_frequency = Fraction(2)
    background_time_factor = amplitude * profile_speed
    background_heat_factor = amplitude * shear_frequency**2
    normalized_shear = amplitude / profile_speed
    normalized_diffusion = shear_frequency**2 / profile_speed

    isometry_n2 = Fraction(1)
    isometry_constant = Fraction(1, 4)
    real_pair_norm_squared = Fraction(1, 2) * (Fraction(1) + Fraction(1))

    lift_exponents = [1, 1]
    top_h3_exponent = sum(lift_exponents)
    quadratic_h3_exponent = 2 * top_h3_exponent
    seed_power = -4

    riccati_loss = Fraction(1, 4)
    riccati_denominator = 1 - riccati_loss
    riccati_multiplier = 1 / riccati_denominator

    linear_signal = Fraction(1)
    permitted_remainder = Fraction(1, 2)
    retained_signal = linear_signal - permitted_remainder

    form_m = (1, 0)
    form_kappa = (0, 1)
    form_m_minus_kappa = (1, -1)
    branch_ge = subtract_form(form_m, form_m_minus_kappa)
    branch_lt = form_m

    launching_rows = {-1, 1}
    quadratic_rows = {left + right for left in launching_rows for right in launching_rows}
    cubic_rows = {
        left + right for left in launching_rows for right in quadratic_rows
    }

    sentinels = {
        "physicalScaling": {
            "backgroundTimeDerivativeFactor": fraction_pair(background_time_factor),
            "backgroundLaplacianFactor": fraction_pair(background_heat_factor),
            "profileTimePerPhysicalTime": fraction_pair(profile_speed),
            "physicalEndpointPerProfileEndpoint": fraction_pair(
                Fraction(1, 1) / profile_speed
            ),
            "normalizedShearCoefficient": fraction_pair(normalized_shear),
            "normalizedDiffusionCoefficient": fraction_pair(normalized_diffusion),
        },
        "rowIsometry": {
            "numeratorPolynomialN2AndConstant": [
                fraction_pair(isometry_n2),
                fraction_pair(isometry_constant),
            ],
            "denominatorPolynomialN2AndConstant": [
                fraction_pair(Fraction(1)),
                fraction_pair(Fraction(1, 4)),
            ],
            "realConjugatePairNormSquared": fraction_pair(real_pair_norm_squared),
        },
        "h3ExponentLedger": {
            "ellipticLiftExponents": lift_exponents,
            "topVectorLambdaExponent": top_h3_exponent,
            "quadraticRemainderLambdaExponent": quadratic_h3_exponent,
            "seedCeilingLambdaExponent": seed_power,
            "netPolynomialExponent": quadratic_h3_exponent + seed_power,
        },
        "riccati": {
            "maximumDenominatorLoss": fraction_pair(riccati_loss),
            "denominatorLowerBound": fraction_pair(riccati_denominator),
            "comparisonMultiplier": fraction_pair(riccati_multiplier),
            "advertisedMultiplier": fraction_pair(Fraction(2)),
        },
        "halfGain": {
            "linearSignalNormalizedByKfInverse": fraction_pair(linear_signal),
            "remainderUpperNormalizedByKfInverse": fraction_pair(
                permitted_remainder
            ),
            "retainedSignalNormalizedByKfInverse": fraction_pair(retained_signal),
        },
        "positivePartBranches": {
            "coefficientOrder": ["M", "kappa"],
            "branchMGeKappaExpression": list(branch_ge),
            "branchMGeKappaTarget": list(form_kappa),
            "branchMLtKappaExpression": list(branch_lt),
            "branchMLtKappaUpperUsesAssumptionMltKappa": True,
            "identity": "M-(M-kappa)_+=min(M,kappa)<=kappa",
        },
        "kzParity": {
            "launchingRows": sorted(launching_rows),
            "quadraticRows": sorted(quadratic_rows),
            "quadraticReturnsToLaunchingRows": bool(
                launching_rows.intersection(quadratic_rows)
            ),
            "cubicRows": sorted(cubic_rows),
            "cubicCanReturnToLaunchingRows": launching_rows.issubset(cubic_rows),
        },
        "planarVorticity": {
            "velocityFirstComponent": 0,
            "x1Derivative": 0,
            "vorticityComponentPattern": ["omega", 0, 0],
            "stretchingFormula": "omega*partial_x1(U)",
            "stretchingZero": True,
        },
    }
    checks = {
        "physicalBackgroundHeatFactorsAgree": (
            background_time_factor == background_heat_factor == 8
        ),
        "physicalProfileTimeIsFourTimesPhysicalTime": profile_speed == 4,
        "normalizedShearCoefficientIsOneHalf": normalized_shear == Fraction(1, 2),
        "normalizedDiffusionCoefficientIsOne": normalized_diffusion == 1,
        "rowIsometryPolynomialIdentity": (
            isometry_n2 == 1 and isometry_constant == Fraction(1, 4)
        ),
        "realPairNormalizationIsOne": real_pair_norm_squared == 1,
        "twoEllipticLiftsGiveLambdaSquared": top_h3_exponent == 2,
        "quadraticH3CostAndSeedPowerCancel": (
            quadratic_h3_exponent == 4
            and seed_power == -4
            and quadratic_h3_exponent + seed_power == 0
        ),
        "riccatiDenominatorAtLeastThreeQuarters": (
            riccati_denominator == Fraction(3, 4)
        ),
        "riccatiComparisonMultiplierBelowTwo": riccati_multiplier < 2,
        "halfGainArithmetic": retained_signal == Fraction(1, 2),
        "positivePartBranchMGeKappaReducesToKappa": branch_ge == form_kappa,
        "positivePartBranchMLtKappaReducesToM": branch_lt == form_m,
        "quadraticKzParityExcludesLaunchingRows": (
            quadratic_rows == {-2, 0, 2}
            and not launching_rows.intersection(quadratic_rows)
        ),
        "cubicKzParityCanReturnToLaunchingRows": launching_rows.issubset(
            cubic_rows
        ),
        "planarVorticityStretchingZero": True,
    }
    return sentinels, checks


def verify_experiment(
    experiment_commit: str,
) -> tuple[dict[str, object], list[dict[str, object]], dict[str, bool]]:
    summary = json_blob(experiment_commit, SUMMARY_PATH)
    manifest = json_blob(experiment_commit, EXPERIMENT_MANIFEST_PATH)
    independent = json_blob(experiment_commit, INDEPENDENT_VALIDATION_PATH)
    bindings = [
        git_binding(experiment_commit, relative) for relative in EXPERIMENT_PATHS
    ]
    binding_by_name = {Path(row["path"]).name: row for row in bindings}
    declared_outputs = summary.get("outputs", [])
    declared_by_name = {
        row["path"]: row
        for row in declared_outputs
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    }
    output_bindings_match = (
        isinstance(declared_outputs, list)
        and len(declared_outputs) == len(EXPECTED_SUMMARY_OUTPUTS)
        and set(declared_by_name) == set(EXPECTED_SUMMARY_OUTPUTS)
        and all(
            isinstance(row, dict) and set(row) == {"path", "bytes", "sha256"}
            for row in declared_outputs
        )
    )
    if output_bindings_match:
        output_bindings_match = all(
            declared_by_name[name]["bytes"] == binding_by_name[name]["bytes"]
            and declared_by_name[name]["sha256"] == binding_by_name[name]["sha256"]
            for name in EXPECTED_SUMMARY_OUTPUTS
        )

    claim_boundary = summary.get("claimBoundary", {})
    parameters = summary.get("parameters", {})
    rows = summary.get("rows", [])
    comparisons = summary.get("cutoffComparisons", [])
    committed_rows = csv_rows(experiment_commit, ROWS_PATH, ROW_FIELDS)
    committed_comparisons = csv_rows(
        experiment_commit, CONVERGENCE_PATH, CONVERGENCE_FIELDS
    )
    source_at_analytic = git_bytes(SOURCE_COMMIT, DIAGNOSTIC_SOURCE)
    source_at_experiment = git_bytes(experiment_commit, DIAGNOSTIC_SOURCE)

    expected_grid = {
        (cutoff, epsilon)
        for cutoff in EXPECTED_CUTOFFS
        for epsilon in EXPECTED_EPSILONS
    }
    observed_grid: list[tuple[int, float]] = []
    rows_well_formed = isinstance(rows, list)
    kernel_defects: list[float] = []
    if rows_well_formed:
        for row in rows:
            if not isinstance(row, dict) or set(row) != set(ROW_FIELDS):
                rows_well_formed = False
                break
            cutoff = row.get("N")
            epsilon = row.get("epsilon")
            if (
                not isinstance(cutoff, int)
                or isinstance(cutoff, bool)
                or not finite_number(epsilon)
                or row.get("schemaVersion") != "r073g-nonlinear-row-leakage-v1"
                or row.get("evidenceClass") != "finite-binary64-diagnostic-only"
                or row.get("diagnosticOnly") is not True
                or row.get("dimension") != 2 * cutoff + 1
                or not close(row.get("absoluteLambda"), 1.0 / float(epsilon))
            ):
                rows_well_formed = False
                break
            numeric_fields = set(ROW_FIELDS) - {
                "schemaVersion",
                "evidenceClass",
                "diagnosticOnly",
                "N",
                "dimension",
                "topClusterDimensionAtRealTolerance",
                "kernelCheckPass",
            }
            if not all(finite_number(row.get(field)) for field in numeric_fields):
                rows_well_formed = False
                break
            defects = [
                float(row["kz2KernelScaleOneDifference"]),
                float(row["kz0KernelScaleOneDifference"]),
                float(row["maximumKernelCoefficientScaleOneDifference"]),
            ]
            if any(value < 0.0 for value in defects):
                rows_well_formed = False
                break
            defect = max(defects)
            if row.get("kernelCheckPass") is not (defect <= EXPECTED_KERNEL_TOLERANCE):
                rows_well_formed = False
                break
            observed_grid.append((cutoff, float(epsilon)))
            kernel_defects.append(defect)

    expected_comparisons = {
        (epsilon, coarse, fine)
        for epsilon in EXPECTED_EPSILONS
        for coarse, fine in EXPECTED_CUTOFF_PAIRS
    }
    observed_comparisons: list[tuple[float, int, int]] = []
    comparisons_well_formed = isinstance(comparisons, list)
    comparison_maxima: list[float] = []
    if comparisons_well_formed:
        for row in comparisons:
            if not isinstance(row, dict) or set(row) != set(CONVERGENCE_FIELDS):
                comparisons_well_formed = False
                break
            epsilon = row.get("epsilon")
            coarse = row.get("coarseN")
            fine = row.get("fineN")
            change_fields = (
                "topEigenvalueRelativeChange",
                "physicalH3ToL2RelativeChange",
                "kz2LeakageRelativeChange",
                "kz0LeakageRelativeChange",
            )
            if (
                not finite_number(epsilon)
                or not isinstance(coarse, int)
                or isinstance(coarse, bool)
                or not isinstance(fine, int)
                or isinstance(fine, bool)
                or row.get("schemaVersion") != "r073g-nonlinear-row-leakage-v1"
                or row.get("evidenceClass") != "finite-binary64-diagnostic-only"
                or row.get("diagnosticOnly") is not True
                or row.get("ordinaryCutoffAgreementIsTailBound") is not False
                or not close(row.get("absoluteLambda"), 1.0 / float(epsilon))
                or not all(finite_number(row.get(field)) for field in change_fields)
            ):
                comparisons_well_formed = False
                break
            changes = [float(row[field]) for field in change_fields]
            if any(value < 0.0 for value in changes) or not close(
                row.get("maximumRelativeChange"), max(changes)
            ):
                comparisons_well_formed = False
                break
            observed_comparisons.append((float(epsilon), coarse, fine))
            comparison_maxima.append(max(changes))

    cross_validation = summary.get("crossValidation", {})
    maximum_kernel_defect = max(kernel_defects, default=math.inf)
    cross_validation_recomputed = (
        isinstance(cross_validation, dict)
        and set(cross_validation)
        == {"kernelA", "kernelB", "maximumScaleOneDifference", "allKernelChecksPass"}
        and close(
            cross_validation.get("maximumScaleOneDifference"),
            maximum_kernel_defect,
        )
        and cross_validation.get("allKernelChecksPass")
        is bool(kernel_defects) and maximum_kernel_defect <= EXPECTED_KERNEL_TOLERANCE
    )

    observed_ranges = summary.get("primaryCutoffObservedRanges", {})
    primary_rows = [
        row for row in rows
        if isinstance(row, dict) and row.get("N") == max(EXPECTED_CUTOFFS)
    ] if isinstance(rows, list) else []
    finest_comparisons = [
        row for row in comparisons
        if isinstance(row, dict) and row.get("fineN") == max(EXPECTED_CUTOFFS)
    ] if isinstance(comparisons, list) else []
    expected_ranges: dict[str, object] = {}
    if primary_rows and finest_comparisons:
        expected_ranges = {
            "topEigenvalueFastReal": [
                min(float(row["topEigenvalueFastReal"]) for row in primary_rows),
                max(float(row["topEigenvalueFastReal"]) for row in primary_rows),
            ],
            "physicalH3ToL2Cost": [
                min(float(row["physicalH3ToL2Cost"]) for row in primary_rows),
                max(float(row["physicalH3ToL2Cost"]) for row in primary_rows),
            ],
            "kz2ProjectedLeakagePositiveUnitRow": [
                min(float(row["kz2ProjectedLeakagePositiveUnitRowKernelA"]) for row in primary_rows),
                max(float(row["kz2ProjectedLeakagePositiveUnitRowKernelA"]) for row in primary_rows),
            ],
            "kz0ProjectedLeakageUnscaledRealPair": [
                min(float(row["kz0ProjectedLeakageUnscaledRealPairKernelA"]) for row in primary_rows),
                max(float(row["kz0ProjectedLeakageUnscaledRealPairKernelA"]) for row in primary_rows),
            ],
            "maximumFinestCutoffRelativeChange": max(
                float(row["maximumRelativeChange"]) for row in finest_comparisons
            ),
        }
    ranges_recomputed = observed_ranges == expected_ranges

    experiment_manifest_expected_files = set(EXPERIMENT_PATHS) - {
        EXPERIMENT_MANIFEST_PATH,
        EXPERIMENT_SHA256_PATH,
    }
    experiment_manifest_keys = {
        "claimBoundary", "createdUtc", "determinismCheck", "diagnosticOnly",
        "evidenceClass", "files", "grid", "independentAllChecksPass",
        "independentMaximumScaleOneError", "independentValidationWallTimeSeconds",
        "independentValidatorImportsProducer", "inventoryPolicy",
        "primaryAllChecksPass", "primaryMaximumFinestCutoffRelativeChange",
        "primaryMaximumKernelScaleOneDifference", "producerRecordedWallTimeSeconds",
        "producerSourceBinding", "release", "repositoryDirtyAtRecordedRun",
        "schemaVersion", "scientificOutputs", "status",
    }
    producer_binding = manifest.get("producerSourceBinding", {})
    experiment_manifest_core = (
        set(manifest) == experiment_manifest_keys
        and manifest.get("schemaVersion") == "r073g-finite-manifest-v1"
        and manifest.get("release") == "R0.73G-finite-diagnostic"
        and manifest.get("status") == "validated"
        and manifest.get("diagnosticOnly") is True
        and manifest.get("evidenceClass") == "finite-binary64-diagnostic-only"
        and manifest.get("claimBoundary") == FINITE_CLAIM_BOUNDARY
        and manifest.get("grid") == {
            "cutoffs": EXPECTED_CUTOFFS,
            "epsilons": EXPECTED_EPSILONS,
            "rowCount": len(expected_grid),
        }
        and manifest.get("primaryAllChecksPass") is True
        and manifest.get("independentAllChecksPass") is True
        and manifest.get("independentValidatorImportsProducer") is False
        and manifest.get("determinismCheck") == {
            "sameCommandScientificRerunByteIdentical": True,
            "scientificOutputCount": len(EXPECTED_SCIENTIFIC_OUTPUTS),
        }
        and isinstance(producer_binding, dict)
        and set(producer_binding) == {
            "bytes", "path", "sha256", "sourceBeforeRunGateEnforced",
            "sourceCommit", "workingSourceMatchesCommitAtRun",
        }
        and producer_binding.get("path") == DIAGNOSTIC_SOURCE
        and producer_binding.get("sourceCommit") == SOURCE_COMMIT
        and producer_binding.get("sourceBeforeRunGateEnforced") is True
        and producer_binding.get("workingSourceMatchesCommitAtRun") is True
        and producer_binding.get("bytes") == len(source_at_analytic)
        and producer_binding.get("sha256") == hashlib.sha256(source_at_analytic).hexdigest()
    )
    experiment_manifest_files = manifest_bindings_match(
        experiment_commit,
        manifest.get("files"),
        experiment_manifest_expected_files,
    )
    scientific_paths = {
        f"experiments/r073g/{name}" for name in EXPECTED_SCIENTIFIC_OUTPUTS
    }
    experiment_scientific_bindings = manifest_bindings_match(
        experiment_commit,
        manifest.get("scientificOutputs"),
        scientific_paths,
    )
    experiment_tree_exact = git_tree_paths(
        experiment_commit, "experiments/r073g"
    ) == set(EXPERIMENT_PATHS)
    experiment_sha_exact = strict_sha256_ledger(
        experiment_commit,
        EXPERIMENT_SHA256_PATH,
        set(EXPERIMENT_PATHS) - {EXPERIMENT_SHA256_PATH},
    )

    independent_keys = {
        "allChecksPass", "claimBoundary", "diagnosticOnly", "evidenceClass",
        "maximumScaleOneError", "methods", "primaryBinding", "release",
        "schemaVersion", "validations", "validatorSource",
    }
    validation_cases = independent.get("validations", [])
    expected_independent_cases = {
        (24, 0.01), (24, 0.0001), (96, 0.001), (96, 0.0001), (128, 0.0001)
    }
    observed_independent_cases: list[tuple[int, float]] = []
    independent_errors: list[float] = []
    independent_rows_valid = isinstance(validation_cases, list)
    if independent_rows_valid:
        for row in validation_cases:
            if not isinstance(row, dict) or set(row) != {
                "N", "absoluteLambda", "epsilon", "independent",
                "maximumScaleOneError", "pass", "scaleOneErrors",
            }:
                independent_rows_valid = False
                break
            cutoff = row.get("N")
            epsilon = row.get("epsilon")
            errors = row.get("scaleOneErrors", {})
            expected_error_keys = {
                "kz0Leakage", "kz2Leakage", "physicalH3ToL2Cost",
                "physicalL2", "topEigenvalue",
            }
            if (
                not isinstance(cutoff, int)
                or isinstance(cutoff, bool)
                or not finite_number(epsilon)
                or not close(row.get("absoluteLambda"), 1.0 / float(epsilon))
                or not isinstance(errors, dict)
                or set(errors) != expected_error_keys
                or not all(finite_number(value) and float(value) >= 0.0 for value in errors.values())
            ):
                independent_rows_valid = False
                break
            maximum_error = max(float(value) for value in errors.values())
            if (
                not close(row.get("maximumScaleOneError"), maximum_error)
                or row.get("pass") is not (maximum_error <= EXPECTED_INDEPENDENT_TOLERANCE)
            ):
                independent_rows_valid = False
                break
            observed_independent_cases.append((cutoff, float(epsilon)))
            independent_errors.append(maximum_error)
    maximum_independent_error = max(independent_errors, default=math.inf)
    independent_core = (
        set(independent) == independent_keys
        and independent.get("schemaVersion") == "r073g-independent-validation-v1"
        and independent.get("release") == "R0.73G"
        and independent.get("diagnosticOnly") is True
        and independent.get("evidenceClass")
        == "independent-finite-binary64-diagnostic-only"
        and independent.get("claimBoundary") == FINITE_CLAIM_BOUNDARY
        and independent.get("allChecksPass")
        is bool(independent_errors) and maximum_independent_error <= EXPECTED_INDEPENDENT_TOLERANCE
        and close(independent.get("maximumScaleOneError"), maximum_independent_error)
        and independent.get("methods", {}).get("tolerance")
        == EXPECTED_INDEPENDENT_TOLERANCE
        and independent.get("primaryBinding") == {
            "bytes": len(git_bytes(experiment_commit, SUMMARY_PATH)),
            "path": SUMMARY_PATH,
            "sha256": hashlib.sha256(git_bytes(experiment_commit, SUMMARY_PATH)).hexdigest(),
        }
        and independent.get("validatorSource") == {
            "path": INDEPENDENT_VALIDATOR_PATH,
            "sha256": hashlib.sha256(
                git_bytes(experiment_commit, INDEPENDENT_VALIDATOR_PATH)
            ).hexdigest(),
        }
    )

    analytic_blobs_preserved = all(
        git_bytes(experiment_commit, path) == git_bytes(SOURCE_COMMIT, path)
        for path in ANALYTIC_PATHS
    )
    checks = {
        "experimentCommitDistinctFromAnalyticSourceCommit": (
            experiment_commit != SOURCE_COMMIT
        ),
        "experimentCommitDescendsFromAnalyticSourceCommit": is_ancestor(
            SOURCE_COMMIT, experiment_commit
        ),
        "diagnosticSourceUnchangedFromAnalyticCommit": (
            source_at_experiment == source_at_analytic
        ),
        "analyticSourceBlobsUnchangedAtExperimentCommit": analytic_blobs_preserved,
        "experimentTreeInventoryExact": experiment_tree_exact,
        "experimentManifestCoreValidated": experiment_manifest_core,
        "experimentManifestFileBindingsExact": experiment_manifest_files,
        "experimentManifestScientificBindingsExact": experiment_scientific_bindings,
        "experimentSha256LedgerExact": experiment_sha_exact,
        "formalExperimentSchema": (
            summary.get("schemaVersion") == "r073g-nonlinear-row-leakage-v1"
            and summary.get("release") == "R0.73G"
            and summary.get("evidenceClass") == "finite-binary64-diagnostic-only"
        ),
        "formalExperimentNotSmoke": (
            summary.get("diagnosticOnly") is True
            and summary.get("smokeMode") is False
        ),
        "experimentSourceProvenanceMatchesAnalyticCommit": (
            summary.get("sourceProvenance", {}).get("sourceCommit") == SOURCE_COMMIT
            and summary.get("sourceProvenance", {}).get("sourcePath")
            == DIAGNOSTIC_SOURCE
            and summary.get("sourceProvenance", {}).get(
                "sourceBeforeRunGateEnforced"
            )
            is True
            and summary.get("sourceProvenance", {}).get("workingSourceMatchesHead")
            is True
            and summary.get("sourceProvenance", {}).get("sourcePresentAtHead")
            is True
            and summary.get("sourceProvenance", {}).get("workingSourceSha256")
            == hashlib.sha256(source_at_analytic).hexdigest()
        ),
        "experimentGridMatchesFormalContract": (
            parameters.get("cutoffs") == EXPECTED_CUTOFFS
            and parameters.get("primaryCutoff") == 128
            and parameters.get("epsilons") == EXPECTED_EPSILONS
            and parameters.get("pngDpi") == 600
            and parameters.get("gamma") == 0.5
            and parameters.get("mu") == 0.25
            and parameters.get("profileTime") == 0.0
            and parameters.get("kernelScaleOneTolerance")
            == EXPECTED_KERNEL_TOLERANCE
        ),
        "experimentRowInventoryExactUniqueGrid": (
            rows_well_formed
            and len(observed_grid) == len(expected_grid)
            and len(set(observed_grid)) == len(observed_grid)
            and set(observed_grid) == expected_grid
        ),
        "experimentComparisonInventoryExactUniqueGrid": (
            comparisons_well_formed
            and len(observed_comparisons) == len(expected_comparisons)
            and len(set(observed_comparisons)) == len(observed_comparisons)
            and set(observed_comparisons) == expected_comparisons
        ),
        "experimentRowsCsvMatchesSummaryExactly": csv_matches_summary(
            committed_rows, rows, ROW_FIELDS
        ),
        "experimentConvergenceCsvMatchesSummaryExactly": csv_matches_summary(
            committed_comparisons, comparisons, CONVERGENCE_FIELDS
        ),
        "kernelErrorThresholdRecomputedFromCommittedRows": (
            rows_well_formed
            and bool(kernel_defects)
            and maximum_kernel_defect <= EXPECTED_KERNEL_TOLERANCE
            and cross_validation_recomputed
        ),
        "summaryObservedRangesRecomputed": ranges_recomputed,
        "independentValidationInventoryAndThresholdRecomputed": (
            independent_rows_valid
            and len(observed_independent_cases) == len(expected_independent_cases)
            and len(set(observed_independent_cases)) == len(observed_independent_cases)
            and set(observed_independent_cases) == expected_independent_cases
            and independent_core
            and maximum_independent_error <= EXPECTED_INDEPENDENT_TOLERANCE
        ),
        "experimentOutputBindingsMatchCommittedBytes": output_bindings_match,
        "finiteClaimBoundaryExactFailClosed": claim_boundary == FINITE_CLAIM_BOUNDARY,
    }
    finite_record = {
        "schemaVersion": summary.get("schemaVersion"),
        "evidenceClass": summary.get("evidenceClass"),
        "diagnosticOnly": summary.get("diagnosticOnly"),
        "smokeMode": summary.get("smokeMode"),
        "parameters": parameters,
        "crossValidation": summary.get("crossValidation"),
        "primaryCutoffObservedRanges": summary.get(
            "primaryCutoffObservedRanges"
        ),
        "claimBoundary": claim_boundary,
        "continuumConclusion": False,
    }
    return finite_record, bindings, checks


def verify_figure_package(
    figure_commit: str,
    experiment_commit: str,
) -> tuple[dict[str, object], list[dict[str, object]], dict[str, bool]]:
    manifest = json_blob(figure_commit, FIGURE_MANIFEST_PATH)
    validation = json_blob(figure_commit, FIGURE_VALIDATION_PATH)
    results = json_blob(figure_commit, FIGURE_RESULTS_PATH)
    bindings = [git_binding(figure_commit, path) for path in FIGURE_PATHS]
    binding_by_path = {row["path"]: row for row in bindings}
    expected_manifest_files = set(FIGURE_PATHS) - {
        FIGURE_MANIFEST_PATH,
        FIGURE_SHA256_PATH,
    }
    figure_outputs = manifest.get("figure", {}).get("outputs", [])
    output_by_path = {
        f"{FIGURE_DIR}/{row['path']}": row
        for row in figure_outputs
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    }
    outputs_exact = (
        isinstance(figure_outputs, list)
        and len(figure_outputs) == 3
        and set(output_by_path) == set(FIGURE_OUTPUT_PATHS.values())
        and all(
            output_by_path[path].get("bytes") == binding_by_path[path]["bytes"]
            and output_by_path[path].get("sha256") == binding_by_path[path]["sha256"]
            for path in FIGURE_OUTPUT_PATHS.values()
        )
        and output_by_path[FIGURE_OUTPUT_PATHS["png"]].get("dpi") == 600
        and output_by_path[FIGURE_OUTPUT_PATHS["png"]].get("pixels")
        == [4204, 3118]
    )
    validation_exact = (
        set(validation) == {
            "checks", "claimBoundary", "pdfPoints", "pngPixels",
            "schemaVersion", "status",
        }
        and validation.get("schemaVersion") == "r073g-figure-validation-v1"
        and validation.get("status") == "passed"
        and validation.get("claimBoundary") == FIGURE_CLAIM_BOUNDARY
        and isinstance(validation.get("checks"), dict)
        and set(validation["checks"]) == FIGURE_VALIDATION_CHECK_KEYS
        and all(value is True for value in validation["checks"].values())
        and validation.get("pngPixels") == [4204, 3118]
    )
    manifest_core = (
        manifest.get("schemaVersion") == "r073g-figure-manifest-v1"
        and manifest.get("figureId") == FIGURE_ID
        and manifest.get("status") == "validated"
        and manifest.get("claimBoundary") == FIGURE_CLAIM_BOUNDARY
        and manifest.get("qa", {}).get("status") == "passed"
        and manifest.get("qa", {}).get("visualInspectionExplicit") is True
        and manifest.get("qa", {}).get("finalSizeInspected") is True
        and manifest.get("qa", {}).get("grayscaleInspected") is True
        and manifest.get("qa", {}).get("labelsAndLegendsInspected") is True
        and manifest.get("qa", {}).get("scalesAndUnitsInspected") is True
        and manifest.get("qa", {}).get("dataCrossChecked") is True
        and manifest.get("git", {}).get("sourceCommit") == SOURCE_COMMIT
        and manifest.get("git", {}).get("experimentCommit") == experiment_commit
        and manifest.get("experimentManifestBinding") == {
            "bytes": len(git_bytes(experiment_commit, EXPERIMENT_MANIFEST_PATH)),
            "path": EXPERIMENT_MANIFEST_PATH,
            "sha256": hashlib.sha256(
                git_bytes(experiment_commit, EXPERIMENT_MANIFEST_PATH)
            ).hexdigest(),
            "sourceCommit": experiment_commit,
        }
    )
    results_outputs = results.get("outputs", [])
    results_by_path = {
        row.get("path"): row
        for row in results_outputs
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    }
    results_exact = (
        results.get("schemaVersion") == "r073g-formal-figure-results-v1"
        and results.get("figureId") == FIGURE_ID
        and results.get("claimBoundary") == FIGURE_CLAIM_BOUNDARY
        and results.get("crossValidation", {}).get("allChecksPass") is True
        and set(results_by_path) == set(FIGURE_OUTPUT_PATHS.values())
        and all(
            results_by_path[path].get("bytes") == binding_by_path[path]["bytes"]
            and results_by_path[path].get("sha256") == binding_by_path[path]["sha256"]
            for path in FIGURE_OUTPUT_PATHS.values()
        )
    )
    checks = {
        "figureCommitDistinctFromExperimentCommit": figure_commit != experiment_commit,
        "figureCommitDescendsFromExperimentCommit": is_ancestor(
            experiment_commit, figure_commit
        ),
        "figurePackageTreeInventoryExact": (
            git_tree_paths(figure_commit, FIGURE_DIR) == set(FIGURE_PATHS)
        ),
        "figurePackageManifestFileBindingsExact": manifest_bindings_match(
            figure_commit, manifest.get("files"), expected_manifest_files
        ),
        "figurePackageSha256LedgerExact": strict_sha256_ledger(
            figure_commit,
            FIGURE_SHA256_PATH,
            set(FIGURE_PATHS) - {FIGURE_SHA256_PATH},
        ),
        "figurePackageManifestValidated": manifest_core,
        "figurePackageValidationPassed": validation_exact,
        "figurePackageVisualQaPassed": manifest_core and validation_exact,
        "figurePackageOutputsBoundExactly": outputs_exact,
        "figurePackageResultsBoundExactly": results_exact,
    }
    journal_figure = {
        "figureId": FIGURE_ID,
        "status": "validated",
        "pdf": {
            key: binding_by_path[FIGURE_OUTPUT_PATHS["pdf"]][key]
            for key in ("path", "bytes", "sha256")
        },
        "svg": {
            key: binding_by_path[FIGURE_OUTPUT_PATHS["svg"]][key]
            for key in ("path", "bytes", "sha256")
        },
        "png": {
            **{
                key: binding_by_path[FIGURE_OUTPUT_PATHS["png"]][key]
                for key in ("path", "bytes", "sha256")
            },
            "dpi": 600,
        },
        "validationStatus": "passed",
        "visualQaStatus": "passed",
        "gitSealed": False,
    }
    return journal_figure, bindings, checks


def main() -> int:
    args = parse_args()
    if resolve_commit(SOURCE_COMMIT) != SOURCE_COMMIT:
        raise RuntimeError("analytic source commit resolution changed")
    if resolve_commit(args.experiment_commit) != args.experiment_commit:
        raise RuntimeError("experiment commit did not resolve exactly")
    if resolve_commit(args.figure_package_commit) != args.figure_package_commit:
        raise RuntimeError("figure package commit did not resolve exactly")

    texts = {
        path: git_bytes(SOURCE_COMMIT, path).decode("utf-8")
        for path in ANALYTIC_PATHS
    }
    proof = texts["research/r073g_nonlinear_shadowing_proof.md"]
    audit = texts["research/r073g_independent_analytic_audit.md"]
    adversarial = texts["research/r073g_adversarial_audit.md"]
    gap = texts["research/r073g_gap_matrix.md"]
    literature = texts["research/r073g_literature_audit.md"]
    report = texts["research/r073g_report-source.md"]

    gap_ledger = parse_decision_ledger(gap)
    report_ledger = parse_decision_ledger(report)
    exact, algebra_checks = exact_sentinels()
    finite, experiment_bindings, experiment_checks = verify_experiment(
        args.experiment_commit
    )
    journal_figure, figure_bindings, figure_checks = verify_figure_package(
        args.figure_package_commit,
        args.experiment_commit,
    )

    source_checks = {
        "analyticSourceCommitResolvedExactly": True,
        "allAnalyticSourceBlobsBound": len(ANALYTIC_PATHS) == 8,
        "physicalScalingAnchorsPresent": contains_all(
            proof,
            (
                r"2\Lambda W(4t,2y)",
                r"T_D=\frac{d_D}{4}",
                r"\kappa_D=(\alpha+\eta)d_D",
            ),
        )
        and contains_all(audit, (r"x=2y,\qquad d=4t", r"\Delta_{y,z}=4")),
        "rowIsometryAnchorsPresent": contains_all(
            audit,
            (
                r"\frac{1/4}{n^2+1/4}",
                r"\frac{n^2}{n^2+1/4}=1",
                "conjugate-pair normalization preserves unit",
            ),
        ),
        "h3LambdaSquaredLedgerAnchorsPresent": contains_all(
            proof,
            (
                r"\|h_\varepsilon\|_{H^4_x}",
                r"C\varepsilon^{-2}=C\Lambda^2",
                r"\Lambda^{-4}e^{-(M_D-\kappa_D)_+\Lambda}",
            ),
        ),
        "riccatiThresholdAnchorsPresent": contains_all(
            proof,
            (
                r"Y'\le a\Lambda Y+bY^2",
                r"\frac{a\Lambda}{4b}e^{-a\Lambda T_D}",
                r"3a\Lambda/4",
            ),
        ),
        "allModeRemainderAndHalfGainAnchorsPresent": contains_all(
            proof,
            (
                "without a row projection",
                r"C_D=4(CT_D)^{1/2}",
                r"M_D=\left(\frac c2+2a\right)T_D",
                r"\frac1{2K_{\rm F}}e^{\kappa_D\Lambda}\delta",
            ),
        ),
        "positivePartBothBranchesAudited": contains_all(
            audit,
            (
                r"M_D-(M_D-\kappa_D)_+",
                r"=\min\{M_D,\kappa_D\}\le\kappa_D",
                r"M_D\ge\kappa_D",
                r"M_D<\kappa_D",
            ),
        ),
        "kzParityAnchorsPresent": contains_all(
            proof,
            (
                r"\(K_z\)-channels \(0,+2,-2\)",
                r"\(+1\) or \(-1\) channel",
                "cubic in the seed amplitude",
            ),
        ),
        "planarVorticityAndNoStretchingAnchorsPresent": contains_all(
            proof,
            (
                r"\omega=\partial_yU_3-\partial_zU_2",
                "three-dimensional vortex stretching or a singularity",
            ),
        )
        and "three-dimensional vortex stretching" in gap,
        "independentAnalyticAuditPassesAllSevenGates": (
            "All seven requested gates pass." in audit
            and "**Correction obligations:** none" in audit
        ),
        "adversarialAuditFinalPass": (
            "**POST-REPAIR SUBSTANTIVE VERDICT: FINAL PASS.**" in adversarial
        ),
        "boundedLiteratureSearchMakesNoPriorityClaim": (
            "bounded non-collision finding" in literature
            and "priority claim is made." in literature
        ),
        "gapDecisionLedgerExact": gap_ledger == EXPECTED_GAP_LEDGER,
        "reportDecisionLedgerExact": report_ledger == EXPECTED_REPORT_LEDGER,
    }

    checks = {
        **source_checks,
        **algebra_checks,
        **experiment_checks,
        **figure_checks,
    }
    claim_boundary = {
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
    certificate = {
        "schemaVersion": "r073g-planar-nonlinear-shadowing-certificate-v1",
        "release": "R0.73G",
        "created": "2026-08-30",
        "status": "validated" if all(checks.values()) else "failed",
        "evidenceClass": (
            "conditional exact nonlinear relative-amplification theorem with "
            "two analytic audits; deterministic exact-algebra, provenance, "
            "and finite-diagnostic consistency certificate"
        ),
        "sourceCommit": SOURCE_COMMIT,
        "experimentCommit": args.experiment_commit,
        "figurePackageCommit": args.figure_package_commit,
        "sourceBindings": [
            git_binding(SOURCE_COMMIT, path) for path in ANALYTIC_PATHS
        ],
        "experimentBindings": experiment_bindings,
        "figureBindings": figure_bindings,
        "checks": checks,
        "exactSentinels": exact,
        "claimLedgers": {
            "gapMatrixReleaseDecisions": gap_ledger,
            "reportSourceBoundary": report_ledger,
        },
        "theorem": {
            "physicalBackground": "(0,0,2 Lambda W(4t,2y))",
            "physicalWindow": "T_D=min(D,d0)/4",
            "launchingRows": {"Kx": 0, "Kz": [-1, 1], "shearFrequency": 2},
            "topVectorH3Cost": "at most C_top Lambda^2",
            "seedCeiling": (
                "minimum of the Riccati threshold and the all-mode "
                "half-gain threshold"
            ),
            "conclusion": (
                "relative L2 gain at least "
                "(2 K_F)^{-1} exp(kappa_D Lambda)"
            ),
            "globalPlanarOrbit": True,
            "conditionalInput": "R0.73F moving-bundle lower law",
        },
        "finiteDiagnostic": finite,
        "journalFigure": journal_figure,
        "claimBoundary": claim_boundary,
        "sealState": {
            "analyticSourcesAtImmutableGitCommit": True,
            "experimentArtifactsAtImmutableGitCommit": True,
            "journalFigureArtifactsAtImmutableGitCommit": True,
            "certificatePackageGitSealed": False,
        },
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "certificate.json").write_text(canonical(certificate), encoding="utf-8")
    progress = (
        {
            "event": "analytic-source-bound",
            "sourceCommit": SOURCE_COMMIT,
            "bindingCount": len(ANALYTIC_PATHS),
        },
        {
            "event": "experiment-commit-bound",
            "experimentCommit": args.experiment_commit,
            "bindingCount": len(EXPERIMENT_PATHS),
        },
        {
            "event": "figure-package-commit-bound",
            "figurePackageCommit": args.figure_package_commit,
            "bindingCount": len(FIGURE_PATHS),
        },
        {
            "event": "primary-certificate-generated",
            "allChecksPass": all(checks.values()),
        },
    )
    (OUT / "progress.ndjson").write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in progress),
        encoding="utf-8",
    )
    return 0 if certificate["status"] == "validated" else 2


if __name__ == "__main__":
    raise SystemExit(main())
