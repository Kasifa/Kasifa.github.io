#!/usr/bin/env python3
"""Independently recompute R0.73G provenance, algebra, and claim sentinels."""

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


ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "research/certificates/r073g"
SOURCE_COMMIT = "21c11ba3eef7f2b5dc3f107957e0744a0471745d"
SOURCES = (
    "research/r073g_problem_freeze.md",
    "research/r073g_operator_derivation.md",
    "research/r073g_nonlinear_shadowing_proof.md",
    "research/r073g_independent_analytic_audit.md",
    "research/r073g_adversarial_audit.md",
    "research/r073g_gap_matrix.md",
    "research/r073g_literature_audit.md",
    "research/r073g_report-source.md",
)
EXPERIMENT_SOURCE = "experiments/r073g/nonlinear_row_leakage_diagnostic.py"
EXPERIMENT_FILES = (
    "experiments/r073g/README.md",
    "experiments/r073g/SHA256SUMS",
    "experiments/r073g/command.txt",
    "experiments/r073g/environment.json",
    EXPERIMENT_SOURCE,
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
SUMMARY = "experiments/r073g/nonlinear_row_leakage_summary.json"
ROWS = "experiments/r073g/nonlinear_row_leakage_rows.csv"
COMPARISONS = "experiments/r073g/nonlinear_row_leakage_convergence.csv"
EXPERIMENT_MANIFEST = "experiments/r073g/manifest.json"
EXPERIMENT_SHA256 = "experiments/r073g/SHA256SUMS"
INDEPENDENT_RESULT = "experiments/r073g/independent_validation.json"
INDEPENDENT_SOURCE = "experiments/r073g/independent_validation.py"
FORMAL_SCIENTIFIC_BASENAMES = {
    "nonlinear_row_leakage_rows.csv",
    "nonlinear_row_leakage_convergence.csv",
    "nonlinear_row_leakage_summary.json",
    "fig-r073g-nonlinear-row-leakage.pdf",
    "fig-r073g-nonlinear-row-leakage.svg",
    "fig-r073g-nonlinear-row-leakage.png",
}
FORMAL_SUMMARY_COMPANIONS = FORMAL_SCIENTIFIC_BASENAMES - {
    "nonlinear_row_leakage_summary.json"
}
FORMAL_CUTOFFS = [24, 48, 96, 128]
FORMAL_EPSILONS = [0.01, 0.005, 0.002, 0.001, 0.0005, 0.0002, 0.0001]
FORMAL_CUTOFF_PAIRS = {(24, 48), (48, 96), (96, 128)}
KERNEL_TOLERANCE = 5.0e-12
INDEPENDENT_TOLERANCE = 2.0e-11

ROW_FIELDS = (
    "schemaVersion", "evidenceClass", "diagnosticOnly", "N", "dimension",
    "epsilon", "absoluteLambda", "topEigenvalueFastReal",
    "topEigenvalueFastImag", "topPhysicalGrowthRateReal",
    "topClusterDimensionAtRealTolerance", "topRealGapBelowCluster",
    "topEigenResidualRelative", "physicalPositiveRowL2", "physicalPositiveRowH3",
    "physicalH3ToL2Cost", "kineticBoundaryMassFraction",
    "kineticOuterThreeMassFraction", "h3OuterThreeContributionFraction",
    "kz2ProjectedLeakagePositiveUnitRowKernelA",
    "kz2ProjectedLeakagePositiveUnitRowKernelB",
    "kz2ProjectedLeakageUnitRealPairKernelA",
    "kz0ProjectedLeakageUnscaledRealPairKernelA",
    "kz0ProjectedLeakageUnscaledRealPairKernelB",
    "kz0ProjectedLeakageUnitRealPairKernelA", "kz2KernelScaleOneDifference",
    "kz0KernelScaleOneDifference", "maximumKernelCoefficientScaleOneDifference",
    "kernelCheckPass",
)
COMPARISON_FIELDS = (
    "schemaVersion", "evidenceClass", "diagnosticOnly", "epsilon",
    "absoluteLambda", "coarseN", "fineN", "topEigenvalueRelativeChange",
    "physicalH3ToL2RelativeChange", "kz2LeakageRelativeChange",
    "kz0LeakageRelativeChange", "maximumRelativeChange",
    "ordinaryCutoffAgreementIsTailBound",
)
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

FIGURE_ID = "fig-r073g-nonlinear-row-leakage"
FIGURE_DIRECTORY = f"figures/r073g/{FIGURE_ID}"
FIGURE_FILES = tuple(
    f"{FIGURE_DIRECTORY}/{name}"
    for name in (
        "README.md", "SHA256SUMS", "caption.md", "command.txt", "config.json",
        "figure.pdf", "figure.png", "figure.svg", "manifest.json", "plot.py",
        "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png", "qa-protocol.md",
        "qa-report.md", "requirements.txt", "results.json", "validate.py",
        "validation.json",
    )
)
FIGURE_MANIFEST = f"{FIGURE_DIRECTORY}/manifest.json"
FIGURE_VALIDATION = f"{FIGURE_DIRECTORY}/validation.json"
FIGURE_RESULTS = f"{FIGURE_DIRECTORY}/results.json"
FIGURE_SHA256 = f"{FIGURE_DIRECTORY}/SHA256SUMS"
FIGURE_OUTPUTS = {
    "pdf": f"{FIGURE_DIRECTORY}/figure.pdf",
    "svg": f"{FIGURE_DIRECTORY}/figure.svg",
    "png": f"{FIGURE_DIRECTORY}/figure.png",
}
FIGURE_BOUNDARY = {
    "clayProblemSolved": False,
    "finiteH3CostProvesUniformContinuumH3Bound": False,
    "finiteLeakageProvesNonlinearInstability": False,
    "finiteTopEqualsContinuumTop": False,
    "formalFiniteDiagnosticFigure": True,
    "ordinaryCutoffAgreementIsTailBound": False,
    "threeDimensionalVortexStretchingPresentInThisPlanarRow": False,
    "transitionThresholdEstablished": False,
}
FIGURE_CHECKS = {
    "claimBoundaryFailClosed", "commitChainPassed", "experimentPackageValidated",
    "finiteSentinelsPassed", "inputHashesPassed", "pdfTextPassed",
    "physicalDimensionsPassed", "png600DpiPassed",
    "primaryAndIndependentKernelChecksPassed", "qaRastersPresent",
    "scientificRerunDeterminismPassed", "singlePagePdf", "svgVectorTextPassed",
    "visualQaPassed",
}

GAP_BY_STATE = {
    "CLOSED": {
        "exactDecayingShearPerturbationEquation",
        "selectedSeedPlanarInvariantClass",
        "selectedNonlinearOrbitGlobalSmoothness",
        "topEigenvectorPolynomialH3Cost",
        "fixedWindowH3Bootstrap",
        "allModeQuadraticRemainderBound",
        "nonlinearRelativeAmplification",
        "topEigenvectorDoubleRowLeakage",
    },
    "FALSE": {
        "singleLinearRowNonlinearInvariant",
        "selectedRowCanCreateThreeDimensionalVortexStretching",
        "oneRowGainAloneImpliesFiniteTimeSingularity",
    },
    "FALSE_AS_INFERENCE": {"oneRowGainAloneImpliesOrderOneDeparture"},
    "OPEN": {
        "naturalSeedOrderOneDeparture",
        "sharpBilinearEvolutionAtUnstableRate",
        "transverseThreeDimensionalTriadClosure",
        "singleBackgroundSingleOrbitInstability",
        "completeOSSquireA2DirectSum",
        "Clay",
    },
}
REPORT_BY_STATE = {
    "CLOSED": GAP_BY_STATE["CLOSED"],
    "FALSE": {
        "singleLinearRowNonlinearInvariant",
        "kineticL2QuadraticRemainderBound",
        "selectedRowCanCreateThreeDimensionalVortexStretching",
        "oneRowGainAloneImpliesFiniteTimeSingularity",
    },
    "FALSE_AS_INFERENCE": {"oneRowGainAloneImpliesOrderOneDeparture"},
    "OPEN": {
        "naturalSeedOrderOneDeparture",
        "targetedCubicModeConvolutionEstimate",
        "harmonicResolvedEvenOddPropagation",
        "transverseThreeDimensionalTriadClosure",
        "singleBackgroundSingleOrbitInstability",
        "completeOSSquireA2DirectSum",
        "Clay",
    },
}


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


def blob(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT)


def resolved(commit: str) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", f"{commit}^{{commit}}"], cwd=ROOT, text=True
    ).strip()


def binding(commit: str, path: str) -> dict[str, object]:
    data = blob(commit, path)
    object_name = subprocess.check_output(
        ["git", "rev-parse", f"{commit}:{path}"], cwd=ROOT, text=True
    ).strip()
    return {
        "path": path,
        "commit": commit,
        "gitBlob": object_name,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def object_json(commit: str, path: str) -> dict[str, object]:
    def reject(value: str) -> object:
        raise ValueError(f"non-finite JSON constant in {path}: {value}")

    result = json.loads(blob(commit, path), parse_constant=reject)
    if not isinstance(result, dict):
        raise ValueError(f"expected object in {path}")
    return result


def tree(commit: str, directory: str) -> set[str]:
    output = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", commit, directory],
        cwd=ROOT,
        text=True,
    )
    return set(filter(None, output.splitlines()))


def number(value: object) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    )


def same_number(left: object, right: object) -> bool:
    return number(left) and number(right) and math.isclose(
        float(left), float(right), rel_tol=1.0e-14, abs_tol=1.0e-14
    )


def read_csv(
    commit: str, path: str, field_contract: tuple[str, ...]
) -> list[dict[str, str]]:
    reader = csv.DictReader(
        io.StringIO(blob(commit, path).decode("utf-8"), newline=""),
        strict=True,
    )
    if tuple(reader.fieldnames or ()) != field_contract:
        raise ValueError(f"CSV header mismatch in {path}")
    result = list(reader)
    if any(None in row or any(value is None for value in row.values()) for row in result):
        raise ValueError(f"malformed CSV in {path}")
    return result


def encode_cell(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("non-finite value in summary")
        return format(value, ".17g")
    return str(value)


def rows_equal(
    disk_rows: list[dict[str, str]],
    json_rows: object,
    field_contract: tuple[str, ...],
) -> bool:
    return (
        isinstance(json_rows, list)
        and len(disk_rows) == len(json_rows)
        and all(
            isinstance(row, dict)
            and set(row) == set(field_contract)
            and all(disk[field] == encode_cell(row[field]) for field in field_contract)
            for disk, row in zip(disk_rows, json_rows)
        )
    )


def ledger_ok(commit: str, ledger_path: str, expected: set[str]) -> bool:
    records: dict[str, str] = {}
    for line in blob(commit, ledger_path).decode("utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/\n]+)", line)
        if match is None or match.group(2) in records:
            return False
        records[match.group(2)] = match.group(1)
    if set(records) != {Path(path).name for path in expected}:
        return False
    return all(
        records[Path(path).name] == hashlib.sha256(blob(commit, path)).hexdigest()
        for path in expected
    )


def manifest_rows_ok(commit: str, value: object, expected: set[str]) -> bool:
    if not isinstance(value, list) or len(value) != len(expected):
        return False
    records: dict[str, dict[str, object]] = {}
    for row in value:
        if (
            not isinstance(row, dict)
            or set(row) != {"path", "bytes", "sha256"}
            or not isinstance(row.get("path"), str)
            or row["path"] in records
        ):
            return False
        records[row["path"]] = row
    return set(records) == expected and all(
        records[path]["bytes"] == len(blob(commit, path))
        and records[path]["sha256"] == hashlib.sha256(blob(commit, path)).hexdigest()
        for path in expected
    )


def decisions(text: str) -> dict[str, str]:
    result = {}
    pattern = re.compile(
        r"^(?P<name>[A-Za-z][A-Za-z0-9]*)="
        r"(?P<state>CLOSED|FALSE|FALSE_AS_INFERENCE|OPEN)$"
    )
    for raw in text.splitlines():
        match = pattern.match(raw.strip())
        if match:
            if match["name"] in result:
                raise ValueError("duplicate decision row")
            result[match["name"]] = match["state"]
    return result


def grouped(ledger: dict[str, str]) -> dict[str, set[str]]:
    result = {state: set() for state in GAP_BY_STATE}
    for name, state in ledger.items():
        result.setdefault(state, set()).add(name)
    return result


def pair(value: Fraction) -> list[int]:
    return [value.numerator, value.denominator]


def recompute_sentinels() -> dict[str, object]:
    time_chain = [Fraction(2), Fraction(4)]
    space_chain = [Fraction(2), Fraction(2), Fraction(2)]
    time_factor = Fraction(1)
    for factor in time_chain:
        time_factor *= factor
    space_factor = Fraction(1)
    for factor in space_chain:
        space_factor *= factor

    numerator_coefficients = {
        2: Fraction(1),
        0: Fraction(1, 4),
    }
    denominator_coefficients = {
        2: Fraction(1),
        0: Fraction(1, 4),
    }
    normalized_real_pair = sum(
        Fraction(1, 2) * value for value in (Fraction(1), Fraction(1))
    )

    lifts = [1 for _ in range(2)]
    top_power = sum(lifts)
    squared_power = top_power + top_power
    seed_power = -squared_power

    loss = Fraction(1, 4)
    denominator = Fraction(1) - loss
    multiplier = Fraction(1) / denominator
    half_remainder = Fraction(1, 2)
    retained = Fraction(1) - half_remainder

    ge_expression = (
        1 - 1,
        0 - (-1),
    )
    lt_expression = (1, 0)

    initial = {-1, 1}
    second = set(map(sum, ((a, b) for a in initial for b in initial)))
    third = set(map(sum, ((a, b) for a in initial for b in second)))

    return {
        "physicalScaling": {
            "backgroundTimeDerivativeFactor": pair(time_factor),
            "backgroundLaplacianFactor": pair(space_factor),
            "profileTimePerPhysicalTime": pair(Fraction(4)),
            "physicalEndpointPerProfileEndpoint": pair(Fraction(1, 4)),
            "normalizedShearCoefficient": pair(Fraction(2, 4)),
            "normalizedDiffusionCoefficient": pair(Fraction(4, 4)),
        },
        "rowIsometry": {
            "numeratorPolynomialN2AndConstant": [
                pair(numerator_coefficients[2]),
                pair(numerator_coefficients[0]),
            ],
            "denominatorPolynomialN2AndConstant": [
                pair(denominator_coefficients[2]),
                pair(denominator_coefficients[0]),
            ],
            "realConjugatePairNormSquared": pair(normalized_real_pair),
        },
        "h3ExponentLedger": {
            "ellipticLiftExponents": lifts,
            "topVectorLambdaExponent": top_power,
            "quadraticRemainderLambdaExponent": squared_power,
            "seedCeilingLambdaExponent": seed_power,
            "netPolynomialExponent": squared_power + seed_power,
        },
        "riccati": {
            "maximumDenominatorLoss": pair(loss),
            "denominatorLowerBound": pair(denominator),
            "comparisonMultiplier": pair(multiplier),
            "advertisedMultiplier": pair(Fraction(2)),
        },
        "halfGain": {
            "linearSignalNormalizedByKfInverse": pair(Fraction(1)),
            "remainderUpperNormalizedByKfInverse": pair(half_remainder),
            "retainedSignalNormalizedByKfInverse": pair(retained),
        },
        "positivePartBranches": {
            "coefficientOrder": ["M", "kappa"],
            "branchMGeKappaExpression": list(ge_expression),
            "branchMGeKappaTarget": [0, 1],
            "branchMLtKappaExpression": list(lt_expression),
            "branchMLtKappaUpperUsesAssumptionMltKappa": True,
            "identity": "M-(M-kappa)_+=min(M,kappa)<=kappa",
        },
        "kzParity": {
            "launchingRows": sorted(initial),
            "quadraticRows": sorted(second),
            "quadraticReturnsToLaunchingRows": bool(initial & second),
            "cubicRows": sorted(third),
            "cubicCanReturnToLaunchingRows": initial <= third,
        },
        "planarVorticity": {
            "velocityFirstComponent": 0,
            "x1Derivative": 0,
            "vorticityComponentPattern": ["omega", 0, 0],
            "stretchingFormula": "omega*partial_x1(U)",
            "stretchingZero": True,
        },
    }


def sentinel_checks(sentinels: dict[str, object]) -> dict[str, bool]:
    physical = sentinels["physicalScaling"]
    isometry = sentinels["rowIsometry"]
    h3 = sentinels["h3ExponentLedger"]
    riccati = sentinels["riccati"]
    gain = sentinels["halfGain"]
    positive = sentinels["positivePartBranches"]
    parity = sentinels["kzParity"]
    planar = sentinels["planarVorticity"]
    return {
        "independentPhysicalHeatIdentity": (
            physical["backgroundTimeDerivativeFactor"]
            == physical["backgroundLaplacianFactor"]
            == [8, 1]
            and physical["profileTimePerPhysicalTime"] == [4, 1]
            and physical["normalizedShearCoefficient"] == [1, 2]
            and physical["normalizedDiffusionCoefficient"] == [1, 1]
        ),
        "independentRowIsometryIdentity": (
            isometry["numeratorPolynomialN2AndConstant"]
            == isometry["denominatorPolynomialN2AndConstant"]
            and isometry["realConjugatePairNormSquared"] == [1, 1]
        ),
        "independentH3ExponentLedger": (
            h3["topVectorLambdaExponent"] == 2
            and h3["quadraticRemainderLambdaExponent"] == 4
            and h3["seedCeilingLambdaExponent"] == -4
            and h3["netPolynomialExponent"] == 0
        ),
        "independentRiccatiLedger": (
            riccati["denominatorLowerBound"] == [3, 4]
            and riccati["comparisonMultiplier"] == [4, 3]
            and Fraction(*riccati["comparisonMultiplier"]) < 2
        ),
        "independentHalfGainLedger": (
            gain["retainedSignalNormalizedByKfInverse"] == [1, 2]
        ),
        "independentPositivePartTwoBranches": (
            positive["branchMGeKappaExpression"] == [0, 1]
            and positive["branchMGeKappaTarget"] == [0, 1]
            and positive["branchMLtKappaExpression"] == [1, 0]
            and positive["branchMLtKappaUpperUsesAssumptionMltKappa"] is True
        ),
        "independentKzParity": (
            parity["launchingRows"] == [-1, 1]
            and parity["quadraticRows"] == [-2, 0, 2]
            and parity["quadraticReturnsToLaunchingRows"] is False
            and parity["cubicCanReturnToLaunchingRows"] is True
        ),
        "independentPlanarStretchingIdentity": (
            planar["vorticityComponentPattern"] == ["omega", 0, 0]
            and planar["x1Derivative"] == 0
            and planar["stretchingZero"] is True
        ),
    }


def experiment_recompute(
    experiment_commit: str,
) -> tuple[list[dict[str, object]], dict[str, object], dict[str, bool]]:
    experiment_bindings = [
        binding(experiment_commit, path) for path in EXPERIMENT_FILES
    ]
    by_basename = {Path(row["path"]).name: row for row in experiment_bindings}
    summary = object_json(experiment_commit, SUMMARY)
    manifest = object_json(experiment_commit, EXPERIMENT_MANIFEST)
    independent = object_json(experiment_commit, INDEPENDENT_RESULT)
    declared_rows = summary.get("outputs", [])
    declared = {
        row["path"]: row
        for row in declared_rows
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    }
    output_match = (
        isinstance(declared_rows, list)
        and len(declared_rows) == len(FORMAL_SUMMARY_COMPANIONS)
        and set(declared) == FORMAL_SUMMARY_COMPANIONS
        and all(
            isinstance(row, dict) and set(row) == {"path", "bytes", "sha256"}
            for row in declared_rows
        )
        and all(
            declared[name]["bytes"] == by_basename[name]["bytes"]
            and declared[name]["sha256"] == by_basename[name]["sha256"]
            for name in FORMAL_SUMMARY_COMPANIONS
        )
    )
    ancestry = (
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", SOURCE_COMMIT, experiment_commit],
            cwd=ROOT,
            check=False,
        ).returncode
        == 0
    )
    boundary = summary.get("claimBoundary", {})
    params = summary.get("parameters", {})
    summary_rows = summary.get("rows", [])
    summary_comparisons = summary.get("cutoffComparisons", [])
    disk_rows = read_csv(experiment_commit, ROWS, ROW_FIELDS)
    disk_comparisons = read_csv(
        experiment_commit, COMPARISONS, COMPARISON_FIELDS
    )

    expected_grid = {
        (cutoff, epsilon)
        for cutoff in FORMAL_CUTOFFS
        for epsilon in FORMAL_EPSILONS
    }
    observed_grid: list[tuple[int, float]] = []
    row_defects: list[float] = []
    row_values_valid = isinstance(summary_rows, list)
    if row_values_valid:
        for row in summary_rows:
            if not isinstance(row, dict) or set(row) != set(ROW_FIELDS):
                row_values_valid = False
                break
            cutoff, epsilon = row.get("N"), row.get("epsilon")
            if (
                not isinstance(cutoff, int)
                or isinstance(cutoff, bool)
                or not number(epsilon)
                or row.get("dimension") != 2 * cutoff + 1
                or row.get("schemaVersion") != "r073g-nonlinear-row-leakage-v1"
                or row.get("evidenceClass") != "finite-binary64-diagnostic-only"
                or row.get("diagnosticOnly") is not True
                or not same_number(row.get("absoluteLambda"), 1.0 / float(epsilon))
            ):
                row_values_valid = False
                break
            excluded = {
                "schemaVersion", "evidenceClass", "diagnosticOnly", "N",
                "dimension", "topClusterDimensionAtRealTolerance", "kernelCheckPass",
            }
            if not all(number(row.get(field)) for field in set(ROW_FIELDS) - excluded):
                row_values_valid = False
                break
            defect = max(
                float(row["kz2KernelScaleOneDifference"]),
                float(row["kz0KernelScaleOneDifference"]),
                float(row["maximumKernelCoefficientScaleOneDifference"]),
            )
            if defect < 0.0 or row.get("kernelCheckPass") is not (
                defect <= KERNEL_TOLERANCE
            ):
                row_values_valid = False
                break
            observed_grid.append((cutoff, float(epsilon)))
            row_defects.append(defect)

    expected_comparisons = {
        (epsilon, coarse, fine)
        for epsilon in FORMAL_EPSILONS
        for coarse, fine in FORMAL_CUTOFF_PAIRS
    }
    observed_comparisons: list[tuple[float, int, int]] = []
    comparison_values_valid = isinstance(summary_comparisons, list)
    if comparison_values_valid:
        for row in summary_comparisons:
            if not isinstance(row, dict) or set(row) != set(COMPARISON_FIELDS):
                comparison_values_valid = False
                break
            epsilon, coarse, fine = (
                row.get("epsilon"), row.get("coarseN"), row.get("fineN")
            )
            fields = (
                "topEigenvalueRelativeChange", "physicalH3ToL2RelativeChange",
                "kz2LeakageRelativeChange", "kz0LeakageRelativeChange",
            )
            if (
                not number(epsilon)
                or not isinstance(coarse, int) or isinstance(coarse, bool)
                or not isinstance(fine, int) or isinstance(fine, bool)
                or row.get("schemaVersion") != "r073g-nonlinear-row-leakage-v1"
                or row.get("evidenceClass") != "finite-binary64-diagnostic-only"
                or row.get("diagnosticOnly") is not True
                or row.get("ordinaryCutoffAgreementIsTailBound") is not False
                or not same_number(row.get("absoluteLambda"), 1.0 / float(epsilon))
                or not all(number(row.get(field)) for field in fields)
            ):
                comparison_values_valid = False
                break
            changes = [float(row[field]) for field in fields]
            if any(change < 0.0 for change in changes) or not same_number(
                row.get("maximumRelativeChange"), max(changes)
            ):
                comparison_values_valid = False
                break
            observed_comparisons.append((float(epsilon), coarse, fine))

    maximum_defect = max(row_defects, default=math.inf)
    cross = summary.get("crossValidation", {})
    cross_recomputed = (
        isinstance(cross, dict)
        and set(cross) == {
            "kernelA", "kernelB", "maximumScaleOneDifference", "allKernelChecksPass"
        }
        and same_number(cross.get("maximumScaleOneDifference"), maximum_defect)
        and cross.get("allKernelChecksPass") is True
        and maximum_defect <= KERNEL_TOLERANCE
    )

    cases = independent.get("validations", [])
    expected_cases = {
        (24, 0.01), (24, 0.0001), (96, 0.001), (96, 0.0001), (128, 0.0001)
    }
    observed_cases: list[tuple[int, float]] = []
    independent_errors: list[float] = []
    independent_values_valid = isinstance(cases, list)
    if independent_values_valid:
        for case in cases:
            if not isinstance(case, dict) or set(case) != {
                "N", "absoluteLambda", "epsilon", "independent",
                "maximumScaleOneError", "pass", "scaleOneErrors",
            }:
                independent_values_valid = False
                break
            errors = case.get("scaleOneErrors", {})
            if (
                not isinstance(case.get("N"), int)
                or isinstance(case.get("N"), bool)
                or not number(case.get("epsilon"))
                or not same_number(
                    case.get("absoluteLambda"), 1.0 / float(case["epsilon"])
                )
                or not isinstance(errors, dict)
                or set(errors) != {
                    "kz0Leakage", "kz2Leakage", "physicalH3ToL2Cost",
                    "physicalL2", "topEigenvalue",
                }
                or not all(number(value) and float(value) >= 0.0 for value in errors.values())
            ):
                independent_values_valid = False
                break
            error = max(float(value) for value in errors.values())
            if not same_number(case.get("maximumScaleOneError"), error) or case.get(
                "pass"
            ) is not (error <= INDEPENDENT_TOLERANCE):
                independent_values_valid = False
                break
            observed_cases.append((case["N"], float(case["epsilon"])))
            independent_errors.append(error)
    maximum_independent_error = max(independent_errors, default=math.inf)
    independent_recomputed = (
        set(independent) == {
            "allChecksPass", "claimBoundary", "diagnosticOnly", "evidenceClass",
            "maximumScaleOneError", "methods", "primaryBinding", "release",
            "schemaVersion", "validations", "validatorSource",
        }
        and independent.get("schemaVersion") == "r073g-independent-validation-v1"
        and independent.get("release") == "R0.73G"
        and independent.get("diagnosticOnly") is True
        and independent.get("evidenceClass")
        == "independent-finite-binary64-diagnostic-only"
        and independent.get("claimBoundary") == FINITE_BOUNDARY
        and independent.get("allChecksPass") is True
        and independent.get("methods", {}).get("tolerance") == INDEPENDENT_TOLERANCE
        and same_number(independent.get("maximumScaleOneError"), maximum_independent_error)
        and maximum_independent_error <= INDEPENDENT_TOLERANCE
        and independent.get("primaryBinding") == {
            "bytes": len(blob(experiment_commit, SUMMARY)),
            "path": SUMMARY,
            "sha256": hashlib.sha256(blob(experiment_commit, SUMMARY)).hexdigest(),
        }
        and independent.get("validatorSource") == {
            "path": INDEPENDENT_SOURCE,
            "sha256": hashlib.sha256(blob(experiment_commit, INDEPENDENT_SOURCE)).hexdigest(),
        }
        and independent_values_valid
        and len(observed_cases) == len(expected_cases)
        and len(set(observed_cases)) == len(observed_cases)
        and set(observed_cases) == expected_cases
    )

    expected_manifest_files = set(EXPERIMENT_FILES) - {
        EXPERIMENT_MANIFEST, EXPERIMENT_SHA256
    }
    producer = manifest.get("producerSourceBinding", {})
    manifest_core = (
        manifest.get("schemaVersion") == "r073g-finite-manifest-v1"
        and manifest.get("release") == "R0.73G-finite-diagnostic"
        and manifest.get("status") == "validated"
        and manifest.get("diagnosticOnly") is True
        and manifest.get("evidenceClass") == "finite-binary64-diagnostic-only"
        and manifest.get("claimBoundary") == FINITE_BOUNDARY
        and manifest.get("grid") == {
            "cutoffs": FORMAL_CUTOFFS,
            "epsilons": FORMAL_EPSILONS,
            "rowCount": len(expected_grid),
        }
        and manifest.get("primaryAllChecksPass") is True
        and manifest.get("independentAllChecksPass") is True
        and manifest.get("independentValidatorImportsProducer") is False
        and manifest.get("determinismCheck") == {
            "sameCommandScientificRerunByteIdentical": True,
            "scientificOutputCount": len(FORMAL_SCIENTIFIC_BASENAMES),
        }
        and isinstance(producer, dict)
        and producer.get("path") == EXPERIMENT_SOURCE
        and producer.get("sourceCommit") == SOURCE_COMMIT
        and producer.get("sourceBeforeRunGateEnforced") is True
        and producer.get("workingSourceMatchesCommitAtRun") is True
        and producer.get("bytes") == len(blob(SOURCE_COMMIT, EXPERIMENT_SOURCE))
        and producer.get("sha256")
        == hashlib.sha256(blob(SOURCE_COMMIT, EXPERIMENT_SOURCE)).hexdigest()
    )
    scientific_paths = {
        f"experiments/r073g/{name}" for name in FORMAL_SCIENTIFIC_BASENAMES
    }
    checks = {
        "independentExperimentCommitIsLaterDescendant": (
            experiment_commit != SOURCE_COMMIT and ancestry
        ),
        "independentExperimentScriptBlobUnchanged": (
            blob(experiment_commit, EXPERIMENT_SOURCE)
            == blob(SOURCE_COMMIT, EXPERIMENT_SOURCE)
        ),
        "independentAnalyticBlobsUnchangedAtExperimentCommit": all(
            blob(experiment_commit, path) == blob(SOURCE_COMMIT, path)
            for path in SOURCES
        ),
        "independentExperimentTreeInventoryExact": (
            tree(experiment_commit, "experiments/r073g") == set(EXPERIMENT_FILES)
        ),
        "independentExperimentManifestCore": manifest_core,
        "independentExperimentManifestFiles": manifest_rows_ok(
            experiment_commit, manifest.get("files"), expected_manifest_files
        ),
        "independentExperimentScientificBindings": manifest_rows_ok(
            experiment_commit, manifest.get("scientificOutputs"), scientific_paths
        ),
        "independentExperimentSha256Ledger": ledger_ok(
            experiment_commit,
            EXPERIMENT_SHA256,
            set(EXPERIMENT_FILES) - {EXPERIMENT_SHA256},
        ),
        "independentExperimentSchemaAndMode": (
            summary.get("schemaVersion") == "r073g-nonlinear-row-leakage-v1"
            and summary.get("release") == "R0.73G"
            and summary.get("evidenceClass") == "finite-binary64-diagnostic-only"
            and summary.get("diagnosticOnly") is True
            and summary.get("smokeMode") is False
        ),
        "independentExperimentSourceProvenance": (
            summary.get("sourceProvenance", {}).get("sourceCommit") == SOURCE_COMMIT
            and summary.get("sourceProvenance", {}).get("sourcePath")
            == EXPERIMENT_SOURCE
            and summary.get("sourceProvenance", {}).get(
                "sourceBeforeRunGateEnforced"
            )
            is True
            and summary.get("sourceProvenance", {}).get(
                "workingSourceMatchesHead"
            )
            is True
            and summary.get("sourceProvenance", {}).get("sourcePresentAtHead")
            is True
            and summary.get("sourceProvenance", {}).get("workingSourceSha256")
            == hashlib.sha256(blob(SOURCE_COMMIT, EXPERIMENT_SOURCE)).hexdigest()
        ),
        "independentFormalGrid": (
            params.get("cutoffs") == FORMAL_CUTOFFS
            and params.get("primaryCutoff") == 128
            and params.get("epsilons") == FORMAL_EPSILONS
            and params.get("pngDpi") == 600
            and params.get("gamma") == 0.5
            and params.get("mu") == 0.25
            and params.get("profileTime") == 0.0
            and params.get("kernelScaleOneTolerance") == KERNEL_TOLERANCE
        ),
        "independentExactUniqueRowGrid": (
            row_values_valid
            and len(observed_grid) == len(expected_grid)
            and len(set(observed_grid)) == len(observed_grid)
            and set(observed_grid) == expected_grid
        ),
        "independentExactUniqueComparisonGrid": (
            comparison_values_valid
            and len(observed_comparisons) == len(expected_comparisons)
            and len(set(observed_comparisons)) == len(observed_comparisons)
            and set(observed_comparisons) == expected_comparisons
        ),
        "independentRowsCsvSummaryIdentity": rows_equal(
            disk_rows, summary_rows, ROW_FIELDS
        ),
        "independentComparisonsCsvSummaryIdentity": rows_equal(
            disk_comparisons, summary_comparisons, COMPARISON_FIELDS
        ),
        "independentKernelThresholdRecomputed": (
            row_values_valid
            and bool(row_defects)
            and maximum_defect <= KERNEL_TOLERANCE
            and cross_recomputed
        ),
        "independentValidatorThresholdRecomputed": independent_recomputed,
        "independentCommittedOutputsMatchSummary": output_match,
        "independentFiniteBoundaryExact": boundary == FINITE_BOUNDARY,
    }
    finite = {
        "schemaVersion": summary.get("schemaVersion"),
        "evidenceClass": summary.get("evidenceClass"),
        "diagnosticOnly": summary.get("diagnosticOnly"),
        "smokeMode": summary.get("smokeMode"),
        "parameters": params,
        "crossValidation": summary.get("crossValidation"),
        "primaryCutoffObservedRanges": summary.get(
            "primaryCutoffObservedRanges"
        ),
        "claimBoundary": boundary,
        "continuumConclusion": False,
    }
    return experiment_bindings, finite, checks


def figure_recompute(
    figure_commit: str,
    experiment_commit: str,
) -> tuple[list[dict[str, object]], dict[str, object], dict[str, bool]]:
    bindings = [binding(figure_commit, path) for path in FIGURE_FILES]
    by_path = {row["path"]: row for row in bindings}
    manifest = object_json(figure_commit, FIGURE_MANIFEST)
    validation = object_json(figure_commit, FIGURE_VALIDATION)
    results = object_json(figure_commit, FIGURE_RESULTS)
    expected_manifest_files = set(FIGURE_FILES) - {FIGURE_MANIFEST, FIGURE_SHA256}
    output_rows = manifest.get("figure", {}).get("outputs", [])
    manifest_outputs = {
        f"{FIGURE_DIRECTORY}/{row['path']}": row
        for row in output_rows
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    }
    output_bytes_match = (
        isinstance(output_rows, list)
        and len(output_rows) == 3
        and set(manifest_outputs) == set(FIGURE_OUTPUTS.values())
        and all(
            manifest_outputs[path].get("bytes") == by_path[path]["bytes"]
            and manifest_outputs[path].get("sha256") == by_path[path]["sha256"]
            for path in FIGURE_OUTPUTS.values()
        )
        and manifest_outputs[FIGURE_OUTPUTS["png"]].get("dpi") == 600
        and manifest_outputs[FIGURE_OUTPUTS["png"]].get("pixels") == [4204, 3118]
    )
    validation_passed = (
        set(validation) == {
            "checks", "claimBoundary", "pdfPoints", "pngPixels",
            "schemaVersion", "status",
        }
        and validation.get("schemaVersion") == "r073g-figure-validation-v1"
        and validation.get("status") == "passed"
        and validation.get("claimBoundary") == FIGURE_BOUNDARY
        and isinstance(validation.get("checks"), dict)
        and set(validation["checks"]) == FIGURE_CHECKS
        and all(value is True for value in validation["checks"].values())
        and validation.get("pngPixels") == [4204, 3118]
    )
    manifest_passed = (
        manifest.get("schemaVersion") == "r073g-figure-manifest-v1"
        and manifest.get("figureId") == FIGURE_ID
        and manifest.get("status") == "validated"
        and manifest.get("claimBoundary") == FIGURE_BOUNDARY
        and manifest.get("git", {}).get("sourceCommit") == SOURCE_COMMIT
        and manifest.get("git", {}).get("experimentCommit") == experiment_commit
        and manifest.get("qa", {}).get("status") == "passed"
        and all(
            manifest.get("qa", {}).get(key) is True
            for key in (
                "dataCrossChecked", "finalSizeInspected", "grayscaleInspected",
                "labelsAndLegendsInspected", "scalesAndUnitsInspected",
                "visualInspectionExplicit",
            )
        )
        and manifest.get("experimentManifestBinding") == {
            "bytes": len(blob(experiment_commit, EXPERIMENT_MANIFEST)),
            "path": EXPERIMENT_MANIFEST,
            "sha256": hashlib.sha256(blob(experiment_commit, EXPERIMENT_MANIFEST)).hexdigest(),
            "sourceCommit": experiment_commit,
        }
    )
    result_outputs = {
        row.get("path"): row
        for row in results.get("outputs", [])
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    }
    results_passed = (
        results.get("schemaVersion") == "r073g-formal-figure-results-v1"
        and results.get("figureId") == FIGURE_ID
        and results.get("claimBoundary") == FIGURE_BOUNDARY
        and results.get("crossValidation", {}).get("allChecksPass") is True
        and set(result_outputs) == set(FIGURE_OUTPUTS.values())
        and all(
            result_outputs[path].get("bytes") == by_path[path]["bytes"]
            and result_outputs[path].get("sha256") == by_path[path]["sha256"]
            for path in FIGURE_OUTPUTS.values()
        )
    )
    checks = {
        "independentFigureCommitIsLaterDescendant": (
            figure_commit != experiment_commit
            and subprocess.run(
                ["git", "merge-base", "--is-ancestor", experiment_commit, figure_commit],
                cwd=ROOT,
                check=False,
            ).returncode == 0
        ),
        "independentFigureTreeInventoryExact": (
            tree(figure_commit, FIGURE_DIRECTORY) == set(FIGURE_FILES)
        ),
        "independentFigureManifestFileBindings": manifest_rows_ok(
            figure_commit, manifest.get("files"), expected_manifest_files
        ),
        "independentFigureSha256Ledger": ledger_ok(
            figure_commit, FIGURE_SHA256, set(FIGURE_FILES) - {FIGURE_SHA256}
        ),
        "independentFigureManifestValidated": manifest_passed,
        "independentFigureValidationPassed": validation_passed,
        "independentFigureVisualQaPassed": manifest_passed and validation_passed,
        "independentFigureOutputsBound": output_bytes_match,
        "independentFigureResultsBound": results_passed,
    }
    journal = {
        "figureId": FIGURE_ID,
        "status": "validated",
        "pdf": {key: by_path[FIGURE_OUTPUTS["pdf"]][key] for key in ("path", "bytes", "sha256")},
        "svg": {key: by_path[FIGURE_OUTPUTS["svg"]][key] for key in ("path", "bytes", "sha256")},
        "png": {
            **{key: by_path[FIGURE_OUTPUTS["png"]][key] for key in ("path", "bytes", "sha256")},
            "dpi": 600,
        },
        "validationStatus": "passed",
        "visualQaStatus": "passed",
        "gitSealed": False,
    }
    return bindings, journal, checks


def main() -> int:
    args = arguments()
    source_resolves = resolved(SOURCE_COMMIT) == SOURCE_COMMIT
    experiment_resolves = resolved(args.experiment_commit) == args.experiment_commit
    figure_resolves = (
        resolved(args.figure_package_commit) == args.figure_package_commit
    )
    source_bindings = [binding(SOURCE_COMMIT, path) for path in SOURCES]
    texts = {
        path: blob(SOURCE_COMMIT, path).decode("utf-8") for path in SOURCES
    }

    gap_ledger = decisions(texts["research/r073g_gap_matrix.md"])
    report_ledger = decisions(texts["research/r073g_report-source.md"])
    exact = recompute_sentinels()
    experiment_bindings, finite, experiment_checks = experiment_recompute(
        args.experiment_commit
    )
    figure_bindings, journal_figure, figure_checks = figure_recompute(
        args.figure_package_commit,
        args.experiment_commit,
    )

    proof = texts["research/r073g_nonlinear_shadowing_proof.md"]
    audit = texts["research/r073g_independent_analytic_audit.md"]
    source_checks = {
        "sourceCommitExistsAndResolvesExactly": source_resolves,
        "experimentCommitExistsAndResolvesExactly": experiment_resolves,
        "figureCommitExistsAndResolvesExactly": figure_resolves,
        "allEightSourceBlobsRecomputed": len(source_bindings) == 8,
        "proofContainsPhysicalBackgroundAndEndpoint": (
            r"\overline U_\Lambda(t,y)" in proof
            and r"2\Lambda W(4t,2y)" in proof
            and r"T_D=\frac{d_D}{4}" in proof
        ),
        "proofContainsH3RiccatiAndAllModeRemainder": (
            r"Y'\le a\Lambda Y+bY^2" in proof
            and "without a row projection" in proof
            and r"M_D=\left(\frac c2+2a\right)T_D" in proof
        ),
        "auditContainsSevenPassVerdicts": (
            audit.count("**Verdict: PASS.**") == 7
            and "**Correction obligations:** none" in audit
        ),
        "gapStatesRecomputedExactly": grouped(gap_ledger) == GAP_BY_STATE,
        "reportStatesRecomputedExactly": grouped(report_ledger) == REPORT_BY_STATE,
    }
    checks = {
        **source_checks,
        **sentinel_checks(exact),
        **experiment_checks,
        **figure_checks,
    }
    result = {
        "schemaVersion": "r073g-independent-certificate-recompute-v1",
        "release": "R0.73G",
        "sourceCommit": SOURCE_COMMIT,
        "experimentCommit": args.experiment_commit,
        "figurePackageCommit": args.figure_package_commit,
        "sourceBindings": source_bindings,
        "experimentBindings": experiment_bindings,
        "figureBindings": figure_bindings,
        "checks": checks,
        "allChecksPass": all(checks.values()),
        "exactSentinels": exact,
        "claimLedgers": {
            "gapMatrixReleaseDecisions": gap_ledger,
            "reportSourceBoundary": report_ledger,
        },
        "finiteDiagnostic": finite,
        "journalFigure": journal_figure,
        "claimBoundary": CLAIM_BOUNDARY,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "independent_recompute.json").write_text(
        canonical(result), encoding="utf-8"
    )
    with (OUT / "progress.ndjson").open("a", encoding="utf-8") as stream:
        stream.write(
            json.dumps(
                {
                    "event": "independent-recompute-complete",
                    "allChecksPass": result["allChecksPass"],
                    "experimentCommit": args.experiment_commit,
                    "figurePackageCommit": args.figure_package_commit,
                },
                sort_keys=True,
            )
            + "\n"
        )
    return 0 if result["allChecksPass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
