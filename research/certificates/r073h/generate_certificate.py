#!/usr/bin/env python3
"""Assemble the R0.73H exact/finite certificate from frozen run outputs.

The resulting JSON keeps the exact continuum-proof subcertificate separate
from the finite binary64 Galerkin diagnostic.  It makes no continuum claim
from cutoff agreement and no PDE claim from the finite rational block alone.
"""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
from typing import Mapping


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_FILES = (
    "research/certificates/r073h/README.md",
    "research/certificates/r073h/command.txt",
    "research/certificates/r073h/config.json",
    "research/certificates/r073h/requirements.txt",
    "research/certificates/r073h/exact_q2_certificate.py",
    "research/certificates/r073h/independent_exact_q2.py",
    "research/certificates/r073h/primary_diagnostic.py",
    "research/certificates/r073h/independent_validate.py",
    "research/certificates/r073h/generate_certificate.py",
    "research/certificates/r073h/validate_certificate.py",
    "research/certificates/r073h/seal_package.py",
)
INPUT_FILES = (
    "exact_q2_certificate.json",
    "independent_exact_q2.json",
    "primary_rows.csv",
    "cutoff_convergence.csv",
    "step_convergence.csv",
    "coefficient_snapshots.npz",
    "environment.json",
    "primary_summary.json",
    "progress.ndjson",
    "primary_manifest.json",
    "independent_validation.json",
    "independent_progress.ndjson",
)
ROW_FIELDS = (
    "schemaVersion", "evidenceClass", "diagnosticOnly", "smokeMode",
    "gridKind", "archivePrefix", "N", "dimensionPerKz", "viscousEpsilon",
    "absoluteLambda", "profileTime", "fastTime", "fastStep",
    "topEigenvalueFastReal", "topEigenvalueFastImag", "topClusterDimension",
    "topRealGap", "topEigenResidualRelative", "generatorRelativeDefect",
    "unitRealLaunchL2", "v1L2", "v1PositiveKzL2", "v2MeanL2",
    "v2DoublePairL2", "v2L2", "v3MeanPathTargetL2",
    "v3DoublePathTargetL2", "v3TargetPairL2", "v3TriplePairL2", "v3L2",
    "quadraticNaturalResponse", "targetCubicNaturalResponse",
    "tripleCubicNaturalResponse", "quadraticCompensated",
    "targetCubicCompensated", "tripleCubicCompensated",
    "meanPathSignedNaturalParallel", "doublePathSignedNaturalParallel",
    "totalSignedNaturalParallel", "meanPathSignedCompensated",
    "doublePathSignedCompensated", "totalSignedCompensated",
    "meanPathCosineWithLinear", "doublePathCosineWithLinear",
    "totalCubicCosineWithLinear", "v1OuterThreeMassFraction",
    "v2OuterThreeMassFraction", "v3OuterThreeMassFraction",
    "maximumDivergenceRelative", "maximumRealityRelative",
    "forbiddenParityRelative", "caseChecksPass",
)
COMPARISON_METRICS = (
    "linearGainRelativeChange",
    "quadraticNaturalRelativeChange",
    "targetCubicNaturalRelativeChange",
    "tripleCubicNaturalRelativeChange",
    "signedCubicRelativeChange",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", default="")
    parser.add_argument("--package-dir", type=Path, default=HERE)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def no_duplicate_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValueError(f"nonfinite JSON constant: {value}")


def load_json(path: Path) -> dict[str, object]:
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=no_duplicate_pairs,
        parse_constant=reject_constant,
    )
    if not isinstance(value, dict):
        raise ValueError(f"top-level JSON value is not an object: {path.name}")
    return value


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def binding(path: Path, base: Path) -> dict[str, object]:
    if not path.is_file() or path.is_symlink():
        raise RuntimeError(f"expected a regular non-symlink file: {path}")
    return {
        "path": path.resolve().relative_to(base.resolve()).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def parse_fraction(text: object) -> Fraction:
    if not isinstance(text, str) or not re.fullmatch(r"-?[0-9]+/[1-9][0-9]*", text):
        raise ValueError(f"noncanonical rational: {text!r}")
    numerator_text, denominator_text = text.split("/")
    value = Fraction(int(numerator_text), int(denominator_text))
    if f"{value.numerator}/{value.denominator}" != text:
        raise ValueError(f"unreduced rational: {text}")
    return value


def close(left: float, right: float, tolerance: float = 2.0e-14) -> bool:
    return math.isfinite(left) and math.isfinite(right) and abs(left - right) <= tolerance * max(
        1.0, abs(left), abs(right)
    )


def relative_change(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def log_slope(rows: list[Mapping[str, str]], field: str) -> float:
    x = [math.log(float(row["viscousEpsilon"])) for row in rows]
    y = [math.log(float(row[field])) for row in rows]
    if any(not math.isfinite(value) for value in x + y):
        raise ValueError("nonfinite log-slope input")
    x_mean = sum(x) / len(x)
    y_mean = sum(y) / len(y)
    denominator = sum((value - x_mean) ** 2 for value in x)
    if denominator == 0.0:
        raise ValueError("degenerate log-slope window")
    return sum((a - x_mean) * (b - y_mean) for a, b in zip(x, y)) / denominator


def source_gate(source_commit: str, smoke: bool) -> dict[str, object]:
    if smoke:
        return {"enforced": False, "sourceCommit": None, "allSourceBlobsMatch": False}
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise RuntimeError("formal assembly requires a full lowercase source commit")
    resolved = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", f"{source_commit}^{{commit}}"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    if resolved != source_commit:
        raise RuntimeError("source commit did not resolve exactly")
    head = subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    if subprocess.run(
        ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", source_commit, head],
        check=False,
    ).returncode != 0:
        raise RuntimeError("source commit is not an ancestor of HEAD")
    bindings = []
    for relative in SOURCE_FILES:
        path = ROOT / relative
        tree = subprocess.run(
            ["git", "-C", str(ROOT), "ls-tree", source_commit, relative],
            check=True, capture_output=True, text=True,
        ).stdout.split()
        if len(tree) < 3 or tree[0] not in {"100644", "100755"}:
            raise RuntimeError(f"source is not a regular Git blob: {relative}")
        committed = subprocess.run(
            ["git", "-C", str(ROOT), "show", f"{source_commit}:{relative}"],
            check=True, capture_output=True,
        ).stdout
        working = path.read_bytes()
        if committed != working:
            raise RuntimeError(f"working source differs from source commit: {relative}")
        bindings.append({
            "path": relative,
            "gitMode": tree[0],
            "bytes": len(working),
            "sha256": hashlib.sha256(working).hexdigest(),
        })
    return {
        "enforced": True,
        "sourceCommit": source_commit,
        "headAtAssembly": head,
        "sourceCommitIsAncestorOfHead": True,
        "allSourceBlobsMatch": True,
        "bindings": bindings,
    }


def require_provenance(value: object, smoke: bool, source_commit: str) -> bool:
    if not isinstance(value, dict):
        return False
    if smoke:
        return (
            value.get("enforced") is False
            and value.get("sourceCommit") is None
            and value.get("allSourceBlobsMatch") is False
        )
    return (
        value.get("enforced") is True
        and value.get("sourceCommit") == source_commit
        and value.get("allSourceBlobsMatch") is True
    )


def verify_bindings(rows: object, base: Path, exact_names: set[str]) -> bool:
    if not isinstance(rows, list) or len(rows) != len(exact_names):
        return False
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"path", "bytes", "sha256"}:
            return False
        name = row["path"]
        if not isinstance(name, str) or name in seen or name not in exact_names:
            return False
        seen.add(name)
        path = base / name
        if binding(path, base) != row:
            return False
    return seen == exact_names


def exact_checks(primary: Mapping[str, object], independent: Mapping[str, object]) -> dict[str, bool]:
    block = primary.get("fourierBlock")
    tail = primary.get("tailCrossSchur")
    perturb = primary.get("profilePerturbation")
    rates = primary.get("rateMargins")
    if not all(isinstance(value, dict) for value in (block, tail, perturb, rates)):
        raise ValueError("exact certificate sections are malformed")
    assert isinstance(block, dict) and isinstance(tail, dict)
    assert isinstance(perturb, dict) and isinstance(rates, dict)
    matrix = [[parse_fraction(value) for value in row] for row in block["matrix"]]
    lower = [[parse_fraction(value) for value in row] for row in block["ldlUnitLower"]]
    pivots = [parse_fraction(value) for value in block["ldlPivots"]]
    shape = len(matrix) == len(lower) == len(pivots) == 9 and all(
        len(row) == 9 for row in matrix + lower
    )
    symmetric = shape and all(matrix[i][j] == matrix[j][i] for i in range(9) for j in range(9))
    triangular = shape and all(
        lower[i][i] == 1 and all(lower[i][j] == 0 for j in range(i + 1, 9))
        for i in range(9)
    )
    reconstruction = shape and all(
        matrix[i][j] == sum(lower[i][k] * pivots[k] * lower[j][k] for k in range(9))
        for i in range(9) for j in range(9)
    )
    minors = [parse_fraction(value) for value in independent["leadingPrincipalMinors"]]
    expected_constants = (
        parse_fraction(tail["lowBlockLower"]) == Fraction(1, 5)
        and parse_fraction(tail["tailLower"]) == Fraction(95, 4)
        and parse_fraction(tail["crossNormUpper"]) == Fraction(27, 16)
        and parse_fraction(tail["targetLower"]) == Fraction(1, 20)
        and parse_fraction(tail["shiftedDeterminant"]) == Fraction(4527, 6400)
        and parse_fraction(perturb["maximumProfileTime"]) == Fraction(1, 450)
        and parse_fraction(perturb["operatorDifferenceUpper"]) == Fraction(1, 40)
        and parse_fraction(perturb["hdLower"]) == Fraction(1, 40)
        and parse_fraction(rates["twoRMinusOneThirdStrictlyGreaterThan"]) == Fraction(221, 30000)
        and parse_fraction(rates["threeRMinusOneHalfStrictlyGreaterThan"]) == Fraction(221, 20000)
    )
    independent_matches = (
        len(minors) == 9
        and all(value > 0 for value in minors)
        and minors[-1] == math.prod(pivots)
        and parse_fraction(independent["schurShiftDeterminant"]) == Fraction(4527, 6400)
        and parse_fraction(independent["perturbedLower"]) == Fraction(1, 40)
        and parse_fraction(independent["twoRateMargin"]) == Fraction(221, 30000)
        and parse_fraction(independent["threeRateMargin"]) == Fraction(221, 20000)
    )
    return {
        "primaryExactScriptPassed": primary.get("allChecksPass") is True,
        "independentExactScriptPassed": independent.get("allChecksPass") is True,
        "nineByNineSymmetricRationalBlock": symmetric,
        "fractionLdlIsUnitLowerWithPositivePivots": triangular and all(value > 0 for value in pivots),
        "fractionLdlReconstructsBlock": reconstruction,
        "bareissLeadingMinorsMatchLdlDeterminant": independent_matches,
        "tailCrossSchurPerturbationAndRatesExact": expected_constants,
        "finiteBlockNotMislabelledAsGalerkinPdeProof": (
            primary.get("finiteGalerkinPdeProof") is False
            and independent.get("claimBoundary", {}).get("finiteGalerkinPdeProof") is False
        ),
    }


def read_csv(path: Path, expected_fields: tuple[str, ...] | None = None) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None or len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError(f"missing or duplicate CSV fields: {path.name}")
        if expected_fields is not None and tuple(reader.fieldnames) != expected_fields:
            raise ValueError(f"unexpected CSV header: {path.name}")
        rows = list(reader)
    if any(None in row for row in rows):
        raise ValueError(f"overflow CSV fields: {path.name}")
    return rows


def finite_checks(
    package: Path,
    config: Mapping[str, object],
    summary: Mapping[str, object],
    manifest: Mapping[str, object],
    independent: Mapping[str, object],
    smoke: bool,
) -> tuple[dict[str, bool], dict[str, object]]:
    rows = read_csv(package / "primary_rows.csv", ROW_FIELDS)
    convergence = read_csv(package / "cutoff_convergence.csv")
    steps = read_csv(package / "step_convergence.csv")
    grid = summary["formalGrid"]
    assert isinstance(grid, dict)
    cutoffs = [int(value) for value in grid["cutoffs"]]
    epsilons = [float(value) for value in grid["viscousEpsilons"]]
    snapshots = [float(value) for value in grid["profileTimeSnapshots"]]
    holdout_configuration = summary["holdout"]["configuration"]
    expected_rows = (len(cutoffs) * len(epsilons) + 1) * len(snapshots)
    expected_convergence = len(epsilons) * (len(cutoffs) - 1)
    step_spec = config["stepConvergence"] if not smoke else None
    if smoke:
        step_epsilon_count = len({float(row["viscousEpsilon"]) for row in steps})
        expected_steps = 2 * step_epsilon_count
    else:
        assert isinstance(step_spec, dict)
        expected_steps = len(step_spec["viscousEpsilons"]) * 2

    keyed: dict[tuple[str, int, float, float], dict[str, str]] = {}
    rows_valid = True
    for row in rows:
        try:
            key = (
                row["gridKind"], int(row["N"]), float(row["viscousEpsilon"]), float(row["profileTime"])
            )
            numeric = [
                float(row[field]) for field in ROW_FIELDS
                if field not in {
                    "schemaVersion", "evidenceClass", "diagnosticOnly", "smokeMode",
                    "gridKind", "archivePrefix", "caseChecksPass",
                }
            ]
            rows_valid = rows_valid and all(math.isfinite(value) for value in numeric)
            rows_valid = rows_valid and row["caseChecksPass"] == "true"
            rows_valid = rows_valid and row["diagnosticOnly"] == "true"
            rows_valid = rows_valid and row["smokeMode"] == ("true" if smoke else "false")
            rows_valid = rows_valid and key not in keyed
            keyed[key] = row
        except (KeyError, TypeError, ValueError):
            rows_valid = False

    d_end = snapshots[-1]
    endpoints = {
        (n_cut, epsilon): keyed.get(("formal", n_cut, epsilon, d_end))
        for n_cut in cutoffs for epsilon in epsilons
    }
    holdout_key = (
        "holdout", int(holdout_configuration["cutoff"]),
        float(holdout_configuration["viscousEpsilon"]), d_end,
    )
    holdout_row = keyed.get(holdout_key)
    endpoint_complete = all(value is not None for value in endpoints.values()) and holdout_row is not None

    convergence_valid = len(convergence) == expected_convergence and endpoint_complete
    finest = max(cutoffs)
    finest_tolerance = float(config["tolerances"]["finestCutoffRelative"])
    convergence_lookup: dict[tuple[float, int, int], dict[str, str]] = {}
    for row in convergence:
        try:
            key = (float(row["viscousEpsilon"]), int(row["coarseN"]), int(row["fineN"]))
            convergence_valid = convergence_valid and key not in convergence_lookup
            convergence_lookup[key] = row
        except (KeyError, TypeError, ValueError):
            convergence_valid = False
    source_fields = {
        "linearGainRelativeChange": "v1L2",
        "quadraticNaturalRelativeChange": "quadraticNaturalResponse",
        "targetCubicNaturalRelativeChange": "targetCubicNaturalResponse",
        "tripleCubicNaturalRelativeChange": "tripleCubicNaturalResponse",
        "signedCubicRelativeChange": "totalSignedNaturalParallel",
    }
    for epsilon in epsilons:
        for coarse, fine in zip(cutoffs, cutoffs[1:]):
            row = convergence_lookup.get((epsilon, coarse, fine))
            left, right = endpoints[(coarse, epsilon)], endpoints[(fine, epsilon)]
            if row is None or left is None or right is None:
                convergence_valid = False
                continue
            recomputed = {
                metric: relative_change(float(left[source]), float(right[source]))
                for metric, source in source_fields.items()
            }
            maximum = max(recomputed.values())
            applied = (not smoke) and fine == finest
            passed = (not applied) or maximum <= finest_tolerance
            convergence_valid = convergence_valid and all(
                close(float(row[metric]), value) for metric, value in recomputed.items()
            )
            convergence_valid = convergence_valid and close(float(row["maximumRelativeChange"]), maximum)
            convergence_valid = convergence_valid and row["finestCutoffGateApplied"] == str(applied).lower()
            convergence_valid = convergence_valid and row["passCheck"] == str(passed).lower()
            convergence_valid = convergence_valid and row["ordinaryCutoffAgreementIsTailProof"] == "false"

    step_tolerance = float(config["tolerances"]["stepRelative"])
    steps_valid = len(steps) == expected_steps
    for row in steps:
        try:
            values = [float(row[field]) for field in COMPARISON_METRICS]
            maximum = max(values)
            passed = maximum <= step_tolerance
            steps_valid = steps_valid and all(math.isfinite(value) and value >= 0.0 for value in values)
            steps_valid = steps_valid and close(float(row["maximumRelativeChange"]), maximum)
            steps_valid = steps_valid and row["passCheck"] == str(passed).lower()
        except (KeyError, TypeError, ValueError):
            steps_valid = False

    fit_epsilons = [float(value) for value in summary["scaling"]["fitWindowViscousEpsilons"]]
    fit_rows = [endpoints[(finest, epsilon)] for epsilon in fit_epsilons]
    slope_valid = all(row is not None for row in fit_rows)
    quadratic_slope = log_slope(fit_rows, "quadraticNaturalResponse") if slope_valid else math.nan
    cubic_slope = log_slope(fit_rows, "targetCubicNaturalResponse") if slope_valid else math.nan
    slope_gate = not smoke
    slope_checks = {
        "quadraticSlopeInFrozenWindow": (
            (not slope_gate) or float(config["tolerances"]["quadraticSlopeMinimum"])
            <= quadratic_slope <= float(config["tolerances"]["quadraticSlopeMaximum"])
        ),
        "targetCubicSlopeInFrozenWindow": (
            (not slope_gate) or float(config["tolerances"]["targetCubicSlopeMinimum"])
            <= cubic_slope <= float(config["tolerances"]["targetCubicSlopeMaximum"])
        ),
    }
    slope_valid = (
        slope_valid
        and close(quadratic_slope, float(summary["scaling"]["quadraticNaturalLogSlope"]))
        and close(cubic_slope, float(summary["scaling"]["targetCubicNaturalLogSlope"]))
        and summary["scaling"]["gateApplied"] is slope_gate
        and summary["scaling"]["checks"] == slope_checks
    )

    predictions = holdout_configuration["predictions"]
    holdout_observed = {
        "quadraticCompensated": float(holdout_row["quadraticCompensated"]) if holdout_row else math.nan,
        "targetCubicCompensated": float(holdout_row["targetCubicCompensated"]) if holdout_row else math.nan,
        "totalSignedCompensated": float(holdout_row["totalSignedCompensated"]) if holdout_row else math.nan,
    }
    holdout_checks = {
        "quadraticCompensatedPrediction": (
            smoke or float(predictions["quadraticCompensatedMinimum"])
            <= holdout_observed["quadraticCompensated"]
            <= float(predictions["quadraticCompensatedMaximum"])
        ),
        "targetCubicCompensatedPrediction": (
            smoke or float(predictions["targetCubicCompensatedMinimum"])
            <= holdout_observed["targetCubicCompensated"]
            <= float(predictions["targetCubicCompensatedMaximum"])
        ),
        "signedParallelCompensatedPrediction": (
            smoke or float(predictions["signedParallelCompensatedMinimum"])
            <= holdout_observed["totalSignedCompensated"]
            <= float(predictions["signedParallelCompensatedMaximum"])
        ),
    }
    holdout_valid = (
        holdout_row is not None
        and summary["holdout"]["gateApplied"] is (not smoke)
        and summary["holdout"]["checks"] == holdout_checks
        and all(
            close(float(summary["holdout"]["endpoint"][field]), float(holdout_row[field]))
            for field in holdout_observed
        )
    )

    primary_binding_names = {
        "primary_rows.csv", "cutoff_convergence.csv", "step_convergence.csv",
        "coefficient_snapshots.npz", "environment.json", "primary_summary.json",
        "progress.ndjson",
    }
    manifest_valid = (
        manifest.get("allChecksPass") is True
        and manifest.get("smokeMode") is smoke
        and verify_bindings(manifest.get("files"), package, primary_binding_names)
    )
    independent_validations = independent.get("validations")
    independent_valid = (
        independent.get("allChecksPass") is True
        and independent.get("smokeMode") is smoke
        and isinstance(independent_validations, list)
        and len(independent_validations) == (3 if smoke else 5)
        and all(isinstance(row, dict) and row.get("pass") is True for row in independent_validations)
        and independent.get("methods", {}).get("importsPrimaryProducer") is False
    )
    checks = {
        "primarySummaryPassed": summary.get("allChecksPass") is True,
        "primaryRowsCompleteUniqueFiniteAndPassing": rows_valid and len(rows) == expected_rows and len(keyed) == expected_rows,
        "archiveIndexCountMatchesCases": len(summary.get("archiveIndex", [])) == len(cutoffs) * len(epsilons) + 1,
        "cutoffComparisonsRecomputed": convergence_valid,
        "stepComparisonsInternallyRecomputed": steps_valid,
        "frozenScalingSlopesRecomputed": slope_valid,
        "holdoutEndpointAndPreregisteredGatesRecomputed": holdout_valid,
        "primaryManifestBindingsMatch": manifest_valid,
        "independentAliasFreeFftSentinelsPassed": independent_valid,
        "finiteDiagnosticNotMislabelledAsContinuumProof": (
            summary.get("diagnosticOnly") is True
            and summary.get("claimBoundary", {}).get("ordinaryCutoffAgreementIsTailProof") is False
            and summary.get("claimBoundary", {}).get("finiteTopEqualsContinuumTop") is False
        ),
    }
    observations = {
        "primaryRowCount": len(rows),
        "cutoffComparisonCount": len(convergence),
        "stepComparisonCount": len(steps),
        "quadraticNaturalLogSlope": quadratic_slope,
        "targetCubicNaturalLogSlope": cubic_slope,
        "holdout": holdout_observed,
        "independentMaximumCoefficientRelativeError": independent["maximumCoefficientRelativeError"],
        "independentMaximumForbiddenParityRelative": independent["maximumForbiddenParityRelative"],
    }
    return checks, observations


def main() -> int:
    args = parse_args()
    package = args.package_dir.resolve()
    if args.smoke:
        if is_within(package, HERE):
            raise RuntimeError("smoke assembly package must be outside the formal source tree")
    elif package != HERE.resolve():
        raise RuntimeError("formal assembly must use research/certificates/r073h")
    output = package / "certificate.json"
    if output.exists() and not args.overwrite:
        raise RuntimeError("refusing to overwrite certificate.json without --overwrite")
    if any((package / name).exists() for name in ("validation.json", "manifest.json", "SHA256SUMS")):
        raise RuntimeError("refusing to assemble beneath stale downstream validation or seal files")
    package.mkdir(parents=True, exist_ok=True)
    provenance = source_gate(args.source_commit, args.smoke)
    for name in INPUT_FILES:
        if not (package / name).is_file() or (package / name).is_symlink():
            raise RuntimeError(f"missing regular input: {name}")

    config = load_json(HERE / "config.json")
    exact = load_json(package / "exact_q2_certificate.json")
    independent_exact = load_json(package / "independent_exact_q2.json")
    summary = load_json(package / "primary_summary.json")
    primary_manifest = load_json(package / "primary_manifest.json")
    independent = load_json(package / "independent_validation.json")
    modes_match = (
        exact.get("schemaVersion") == "r073h-exact-q2-ldl-v1"
        and independent_exact.get("schemaVersion") == "r073h-independent-exact-q2-bareiss-v1"
        and summary.get("schemaVersion") == "r073h-harmonic-duhamel-primary-v1"
        and independent.get("schemaVersion") == "r073h-independent-vorticity-fft-v1"
        and summary.get("smokeMode") is args.smoke
        and independent.get("smokeMode") is args.smoke
    )
    provenance_checks = {
        "assemblySourceGate": (not args.smoke and provenance["allSourceBlobsMatch"] is True) or args.smoke,
        "exactPrimaryProvenance": require_provenance(exact.get("sourceProvenance"), args.smoke, args.source_commit),
        "exactIndependentProvenance": require_provenance(independent_exact.get("sourceProvenance"), args.smoke, args.source_commit),
        "numericPrimaryProvenance": require_provenance(summary.get("sourceProvenance"), args.smoke, args.source_commit),
        "numericIndependentProvenance": require_provenance(independent.get("sourceProvenance"), args.smoke, args.source_commit),
    }
    exact_result = exact_checks(exact, independent_exact)
    finite_result, observations = finite_checks(
        package, config, summary, primary_manifest, independent, args.smoke
    )
    checks = {
        "schemasAndModesMatch": modes_match,
        **provenance_checks,
        **{f"exact::{key}": value for key, value in exact_result.items()},
        **{f"finite::{key}": value for key, value in finite_result.items()},
    }
    result = {
        "schemaVersion": "r073h-combined-certificate-v1",
        "release": "R0.73H",
        "evidenceClass": "exact-continuum-subcertificate-plus-finite-binary64-diagnostic",
        "smokeMode": args.smoke,
        "sourceProvenance": provenance,
        "configBinding": binding(HERE / "config.json", ROOT),
        "inputBindings": [binding(package / name, package) for name in INPUT_FILES],
        "exactContinuumSubcertificate": {
            "status": "PASS_EXACT_SUBCERTIFICATE" if all(exact_result.values()) else "FAIL",
            "scope": "finite exact-rational Fourier block plus analytic tail/cross/Schur/perturbation/rate arithmetic",
            "h0Lower": "1/20",
            "hdLowerForDAtMostOneOver450": "1/40",
            "twoRateStrictMargin": "221/30000",
            "threeRateStrictMargin": "221/20000",
            "checks": exact_result,
            "finiteGalerkinPdeProof": False,
        },
        "finiteHarmonicDiagnostic": {
            "status": "PASS_FINITE_DIAGNOSTIC" if all(finite_result.values()) else "FAIL",
            "amplitudeCoefficientSupport": {
                "V1": ["Kz=-1", "Kz=+1"],
                "V2": ["Kz=0", "Kz=-2", "Kz=+2"],
                "V3": ["Kz=-1", "Kz=+1", "Kz=-3", "Kz=+3"],
            },
            "cubicTargetPaths": ["via Kz=0 mean row", "via Kz=+/-2 doubled rows"],
            "observations": observations,
            "checks": finite_result,
            "continuumConclusion": "none",
        },
        "preregistration": {
            "pilotInformed": config["pilotInformed"],
            "formalGrid": config["formalGrid"],
            "stepConvergence": config["stepConvergence"],
            "independentSentinels": config["independentSentinels"],
            "holdout": config["holdout"],
        },
        "checks": checks,
        "allChecksPass": all(checks.values()),
        "claimLedger": {
            "exactAmplitudeHierarchyAndKzParity": "CLOSED_BY_ALGEBRA",
            "continuumDoubledRowCoercivityArithmetic": "CLOSED_EXACT_SUBCERTIFICATE",
            "fullContinuumHarmonicResolvedSemigroupEstimate": "OPEN",
            "finiteDuhamelResponseAtFrozenGrid": "FINITE_DIAGNOSTIC_ONLY",
            "finiteCutoffAgreementAsTailProof": "NOT_CLAIMED",
            "fourthAndHigherAmplitudeOrders": "OPEN",
            "uniformTaylorRadius": "OPEN",
            "naturalSeedOrderOneDeparture": "OPEN",
            "threeDimensionalVortexStretching": "ABSENT_FOR_SELECTED_PLANAR_LAUNCH",
            "generalThreeDimensionalRegularity": "OPEN",
            "ClayProblem": "OPEN",
        },
    }
    temporary = output.with_name(f".{output.name}.tmp")
    temporary.write_text(canonical(result), encoding="utf-8")
    os.replace(temporary, output)
    return 0 if result["allChecksPass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
