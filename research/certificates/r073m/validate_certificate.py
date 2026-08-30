#!/usr/bin/env python3
"""Independent fail-closed validator for the R0.73M finite package."""

from __future__ import annotations

import argparse
import ast
import csv
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Iterable, Mapping


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE_FILES = (
    "research/r073m_numerical_protocol.md",
    "research/certificates/r073m/README.md",
    "research/certificates/r073m/command.txt",
    "research/certificates/r073m/config.json",
    "research/certificates/r073m/requirements.txt",
    "research/certificates/r073m/primary_diagnostic.py",
    "research/certificates/r073m/independent_linear.py",
    "research/certificates/r073m/independent_hierarchy.py",
    "research/certificates/r073m/exact_identities.py",
    "research/certificates/r073m/generate_certificate.py",
    "research/certificates/r073m/validate_certificate.py",
    "research/certificates/r073m/seal_package.py",
)
PACKAGE_SOURCE_FILES = tuple(Path(name).name for name in SOURCE_FILES[1:])
PRIMARY_FILES = (
    "primary_results.json", "primary_rows.csv", "action_nodes.csv",
    "cutoff_convergence.csv", "step_convergence.csv",
    "coefficient_endpoints.npz", "primary_environment.json",
    "primary_progress.ndjson", "primary_resources.ndjson", "primary_manifest.json",
)
INDEPENDENT_FILES = (
    "independent_linear.json", "independent_linear_progress.ndjson",
    "independent_linear_resources.ndjson", "independent_hierarchy.json",
    "independent_hierarchy_progress.ndjson",
    "independent_hierarchy_resources.ndjson", "exact_identities.json",
)
SCIENTIFIC_INPUTS = (
    "primary_results.json", "primary_rows.csv", "action_nodes.csv",
    "cutoff_convergence.csv", "step_convergence.csv",
    "coefficient_endpoints.npz", "independent_linear.json",
    "independent_hierarchy.json", "exact_identities.json", "certificate.json",
)
ASSEMBLY_SCIENTIFIC_INPUTS = SCIENTIFIC_INPUTS[:-1]
PRE_VALIDATION_FILES = PRIMARY_FILES + INDEPENDENT_FILES + ("certificate.json",)
PRE_SEAL_GENERATED = PRE_VALIDATION_FILES + ("validation.json",)
EXPECTED_CONFIG_SHA256 = "d0f757c41ce96971e64860e028e55d9378166ef1df6de28b7c0c2527c6bbb7d4"
EXPECTED_CLAIM_BOUNDARY = {
    "finiteInviscidActionProxyComputed": True,
    "finiteViscousActionComputedSeparately": True,
    "finitePrescribedActionRecodingComputed": True,
    "finiteABCoefficientsComputed": True,
    "continuumActionCertifiedByFiniteComputation": False,
    "continuumGainPrefactorCertifiedByFiniteComputation": False,
    "prefactorLimitCertified": False,
    "twoTermWKBCertified": False,
    "uniformTaylorRadiusCertified": False,
    "fourthOrderRemainderCertified": False,
    "fullNonlinearNavierStokesTrajectoryComputed": False,
    "finiteCutoffAgreementIsTailProof": False,
    "singleFixedBackgroundLyapunovInstabilityCertified": False,
    "transverseThreeDimensionalClosureCertified": False,
    "finiteTimeSingularityCertified": False,
    "clayProblemSolved": False,
}
STATE_ORDER = (
    "V1", "V2_Kz0", "V2_KzPlusMinus2",
    "V3_via_Kz0", "V3_via_KzPlusMinus2",
)
TEMPORAL_SCIENTIFIC_KEYS = {
    "createdUtc", "wallTimeSeconds", "runtime", "headAtRun",
    "headAtAssembly", "headAtValidation", "headAtSeal",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--package-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--source-commit", default="")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    return parser.parse_args()


ARGS = parse_args()
if ARGS.deps:
    sys.path.insert(0, ARGS.deps)
import numpy as np  # noqa: E402


def fail(message: str) -> None:
    raise RuntimeError(message)


def no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValueError(f"nonfinite JSON constant: {value}")


def loads_json(text: str) -> object:
    return json.loads(
        text, object_pairs_hook=no_duplicates, parse_constant=reject_constant,
    )


def load_json(path: Path) -> dict[str, Any]:
    value = loads_json(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        fail(f"top-level JSON is not an object: {path.name}")
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def binding(path: Path, base: Path) -> dict[str, object]:
    if not path.is_file() or path.is_symlink():
        fail(f"expected regular non-symlink file: {path}")
    return {
        "path": path.resolve().relative_to(base.resolve()).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def source_gate(commit: str, smoke: bool) -> dict[str, object]:
    if smoke:
        return {"enforced": False, "sourceCommit": None, "allSourceBlobsMatch": False}
    if re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        fail("formal validation requires a full lowercase source commit")
    resolved = subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", f"{commit}^{{commit}}"], text=True,
    ).strip()
    if resolved != commit:
        fail("source commit did not resolve exactly")
    head = subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True,
    ).strip()
    if subprocess.run(
        ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", commit, head],
        check=False,
    ).returncode != 0:
        fail("source commit is not an ancestor of HEAD")
    rows = []
    for relative in SOURCE_FILES:
        path = ROOT / relative
        committed = subprocess.check_output(
            ["git", "-C", str(ROOT), "show", f"{commit}:{relative}"],
        )
        if committed != path.read_bytes():
            fail(f"working source differs from source commit: {relative}")
        rows.append(binding(path, ROOT))
    return {
        "enforced": True, "sourceCommit": commit, "headAtValidation": head,
        "allSourceBlobsMatch": True, "bindings": rows,
    }


def stable_provenance(value: Mapping[str, object]) -> dict[str, object]:
    return {
        "enforced": value["enforced"], "sourceCommit": value["sourceCommit"],
        "allSourceBlobsMatch": value["allSourceBlobsMatch"],
        **({"bindings": value["bindings"]} if value["enforced"] else {}),
    }


def finite_tree(value: object) -> bool:
    if isinstance(value, dict):
        return all(finite_tree(child) for child in value.values())
    if isinstance(value, list):
        return all(finite_tree(child) for child in value)
    if isinstance(value, float):
        return math.isfinite(value)
    return True


def no_temporal_keys(value: object) -> bool:
    if isinstance(value, dict):
        return not (set(value) & TEMPORAL_SCIENTIFIC_KEYS) and all(
            no_temporal_keys(child) for child in value.values()
        )
    if isinstance(value, list):
        return all(no_temporal_keys(child) for child in value)
    return True


def close(left: float, right: float, tolerance: float = 5e-12) -> bool:
    return (math.isfinite(left) and math.isfinite(right)
            and abs(left - right) <= tolerance * max(1.0, abs(left), abs(right)))


def relative(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1e-300)


def nested(value: Mapping[str, Any], path: str) -> object:
    current: object = value
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            fail(f"missing configured output path: {path}")
        current = current[part]
    return current


def f(row: Mapping[str, str], key: str) -> float:
    value = float(row[key])
    if not math.isfinite(value):
        fail(f"nonfinite CSV value in {key}")
    return value


def load_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        fields = list(reader.fieldnames or [])
        if len(fields) != len(set(fields)):
            fail(f"duplicate CSV header: {path.name}")
        rows = list(reader)
    if any(None in row for row in rows):
        fail(f"ragged CSV: {path.name}")
    return fields, rows


def load_ndjson(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        value = loads_json(line)
        if not isinstance(value, dict) or not finite_tree(value):
            fail(f"invalid NDJSON row: {path.name}")
        rows.append(value)
    if not rows:
        fail(f"empty NDJSON file: {path.name}")
    return rows


def verify_binding_rows(rows: object, base: Path, expected: set[str]) -> bool:
    if not isinstance(rows, list) or len(rows) != len(expected):
        return False
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"path", "bytes", "sha256"}:
            return False
        name = row.get("path")
        if not isinstance(name, str) or name in seen or name not in expected:
            return False
        if Path(name).is_absolute() or ".." in Path(name).parts:
            return False
        seen.add(name)
        if binding(base / name, base) != row:
            return False
    return seen == expected


def coefficient_metrics(state: np.ndarray, cutoff: int) -> dict[str, float]:
    if state.dtype != np.dtype("complex128") or state.shape != (5, 7, 2 * cutoff + 1, 2):
        fail("coefficient archive dtype or shape mismatch")
    if not bool(np.isfinite(state).all()):
        fail("nonfinite coefficient archive")
    one, two0, two2, three0, three2 = state
    two = two0 + two2
    three = three0 + three2
    target = [2, 4]
    triple = [0, 6]

    def norm(value: np.ndarray) -> float:
        squared = float(np.vdot(value, value).real)
        if not math.isfinite(squared) or squared < -1e-14:
            fail("invalid coefficient norm")
        return math.sqrt(max(0.0, squared))

    one_target = one[target]
    three0_target = three0[target]
    three2_target = three2[target]
    three_target = three0_target + three2_target
    gain = norm(one_target)
    gain2, gain3, gain4 = gain ** 2, gain ** 3, gain ** 4
    modes = np.arange(-cutoff, cutoff + 1, dtype=float)
    ky = 2.0 * modes
    kz = np.arange(-3, 4, dtype=float)

    def divergence(field: np.ndarray) -> float:
        dot = ky[None, :] * field[:, :, 0] + kz[:, None] * field[:, :, 1]
        scale = np.sqrt(ky[None, :] ** 2 + kz[:, None] ** 2)[..., None] * field
        return norm(dot) / max(norm(scale), 1e-300)

    def reality(field: np.ndarray) -> float:
        maximum = 0.0
        scale = max(float(np.max(np.abs(field))), 1e-300)
        for zi in range(7):
            for ni in range(2 * cutoff + 1):
                difference = field[6 - zi, 2 * cutoff - ni] - np.conjugate(field[zi, ni])
                maximum = max(maximum, float(np.max(np.abs(difference))))
        return maximum / scale

    combined = (one, two, three)
    allowed = ({2, 4}, {1, 3, 5}, {0, 2, 4, 6})
    forbidden = 0.0
    for field, allowed_rows in zip(combined, allowed):
        bad = np.concatenate([
            field[index].ravel() for index in range(7) if index not in allowed_rows
        ])
        forbidden = max(forbidden, norm(bad) / max(norm(field), 1e-300))
    outer = np.abs(modes) >= cutoff - 2

    def outer_fraction(field: np.ndarray) -> float:
        return float(np.sum(np.abs(field[:, outer]) ** 2) / max(norm(field) ** 2, 1e-300))

    return {
        "actualPhysicalLinearGain": gain,
        "aEndpointL2": norm(one_target / gain),
        "bEndpointL2": norm(two) / max(gain2, 1e-300),
        "cTargetEndpointL2": norm(three_target) / max(gain3, 1e-300),
        "cTotalSignedParallel": float(np.vdot(one_target, three_target).real
                                      / max(gain4, 1e-300)),
        "v1OuterThreeMassFraction": outer_fraction(one),
        "v2OuterThreeMassFraction": outer_fraction(two),
        "v3OuterThreeMassFraction": outer_fraction(three),
        "maximumDivergenceRelative": max(divergence(field) for field in state),
        "maximumRealityRelative": max(reality(field) for field in state),
        "forbiddenParityRelative": forbidden,
    }


def independent_import_check(path: Path) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name.endswith("primary_diagnostic") for alias in node.names):
                return False
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").endswith("primary_diagnostic"):
                return False
    return True


def verify_seal(package: Path, smoke: bool, provenance: Mapping[str, object],
                claim: Mapping[str, object]) -> bool:
    manifest = load_json(package / "manifest.json")
    if not (manifest.get("schemaVersion") == "r073m-sealed-package-manifest-v1"
            and manifest.get("release") == "R0.73M"
            and manifest.get("smokeMode") is smoke
            and manifest.get("allPrerequisiteChecksPass") is True
            and manifest.get("claimBoundary") == claim):
        return False
    expected = set(PRE_SEAL_GENERATED if smoke
                   else PACKAGE_SOURCE_FILES + PRE_SEAL_GENERATED)
    if not verify_binding_rows(manifest.get("files"), package, expected):
        return False
    source_rows = manifest.get("sourceBindings")
    if not isinstance(source_rows, list):
        return False
    if source_rows != provenance.get("bindings", []):
        return False
    actual = {path.name for path in package.iterdir()
              if path.is_file() and not path.is_symlink()}
    if actual != expected | {"manifest.json", "SHA256SUMS"}:
        return False
    lines = (package / "SHA256SUMS").read_text(encoding="ascii").splitlines()
    expected_sum_names = expected | {"manifest.json"}
    if len(lines) != len(expected_sum_names):
        return False
    seen = set()
    for line in lines:
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/]+)", line)
        if match is None:
            return False
        digest, name = match.groups()
        if name in seen or name not in expected_sum_names:
            return False
        seen.add(name)
        if sha256(package / name) != digest:
            return False
    return seen == expected_sum_names


def validate(package: Path, config: Mapping[str, Any], smoke: bool,
             provenance: Mapping[str, object]) -> tuple[dict[str, bool], dict[str, object]]:
    for name in PRE_VALIDATION_FILES:
        binding(package / name, package)
    primary = load_json(package / "primary_results.json")
    linear = load_json(package / "independent_linear.json")
    hierarchy = load_json(package / "independent_hierarchy.json")
    exact = load_json(package / "exact_identities.json")
    certificate = load_json(package / "certificate.json")
    scientific_jsons = (primary, linear, hierarchy, exact, certificate)
    stable = stable_provenance(provenance)
    claim = config["claimBoundary"]
    tolerances = dict(config["tolerances"])
    if smoke:
        tolerances.update({
            "physicalKineticGainRelative": 5e-4,
            "largestCutoffActionProxyAbsolute": 1e-7,
            "largestCutoffPrefactorAbsolute": 1e-4,
            "hierarchyFinestCutoffRelative": 2e-3,
            "hierarchyStepRelative": 2e-3,
            "independentLinearActionRelative": 2e-3,
            "independentLinearGainRelative": 2e-3,
            "independentLinearPrefactorAbsolute": 2e-3,
            "independentLinearRefinement": 2e-3,
            "independentHierarchyCoefficientRelative": 2e-3,
            "outerThreeMassFraction": 0.1,
        })
        cutoffs, epsilons, sample_count = [8, 10], [0.001, 0.0005], 9
        linear_sentinels = [
            {"cutoff": 8, "viscousEpsilon": 0.001},
            {"cutoff": 10, "viscousEpsilon": 0.0005},
        ]
        linear_steps = [8, 16]
        hierarchy_sentinels = [
            {"cutoff": 8, "viscousEpsilon": 0.001, "fastStep": 0.1},
            {"cutoff": 10, "viscousEpsilon": 0.0005, "fastStep": 0.1},
        ]
    else:
        cutoffs = [int(value) for value in config["cutoffs"]]
        epsilons = [float(value) for value in config["viscousEpsilons"]]
        sample_count = int(config["actionSampleCount"])
        linear_sentinels = config["independentLinear"]["sentinels"]
        linear_steps = config["independentLinear"]["stepCounts"]
        hierarchy_sentinels = config["independentHierarchy"]["sentinels"]

    expected_cases = [(n, epsilon) for n in cutoffs for epsilon in epsilons]
    cases = primary.get("cases", [])
    actual_cases = [(int(row["N"]), float(row["epsilon"])) for row in cases]
    unique_cases = len(actual_cases) == len(set(actual_cases))
    case_grid_exact = actual_cases == expected_cases and unique_cases

    action_fields, action_rows = load_csv(package / "action_nodes.csv")
    expected_action_fields = [
        "branch", "N", "epsilon", "sampleIndex", "d", "lambda",
        "lambdaImaginary", "cumulativeAction", "fixedContourCount",
        "phaseAnchorAbs", "eigenResidualRelative", "finiteCompressionOnly",
    ]
    expected_action_keys = []
    for n in cutoffs:
        expected_action_keys.extend(
            ("inviscid", n, 0.0, index) for index in range(sample_count)
        )
        expected_action_keys.extend(
            ("viscous", n, epsilon, index) for epsilon in epsilons
            for index in range(sample_count)
        )
    actual_action_keys = [
        (row["branch"], int(row["N"]), f(row, "epsilon"), int(row["sampleIndex"]))
        for row in action_rows
    ]
    action_grid_exact = (action_fields == expected_action_fields
                         and actual_action_keys == expected_action_keys
                         and len(actual_action_keys) == len(set(actual_action_keys)))
    all_contours = all(int(row["fixedContourCount"]) == 1 for row in action_rows)
    minimum_anchor = min(f(row, "phaseAnchorAbs") for row in action_rows)
    max_eigen_residual = max(f(row, "eigenResidualRelative") for row in action_rows)
    max_eigen_imaginary = max(abs(f(row, "lambdaImaginary")) for row in action_rows)

    primary_fields, primary_rows = load_csv(package / "primary_rows.csv")
    primary_csv_keys = [(int(row["N"]), f(row, "epsilon")) for row in primary_rows]
    primary_csv_exact = primary_csv_keys == expected_cases and primary_fields == [
        "N", "epsilon", "finiteInviscidActionProxy", "finiteViscousAction",
        "kineticGain", "actualPhysicalLinearGain",
        "finiteInviscidActionPrefactor",
        "finiteViscousActionNormalizedPhysicalGain",
        "physicalKineticGainRelativeDifference", "aEndpointL2", "bEndpointL2",
        "bTargetEndpointL2", "cTargetEndpointL2", "cTripleEndpointL2",
        "cMeanPathSignedParallel", "cDoublePathSignedParallel",
        "cTotalSignedParallel", "forbiddenParityRelative",
        "finiteCompressionOnly",
    ]
    cases_by_key = {
        (int(case["N"]), float(case["epsilon"])): case for case in cases
    }
    csv_sources = {
        "finiteInviscidActionProxy": ("linear", "finiteInviscidActionProxy"),
        "finiteViscousAction": ("linear", "finiteViscousAction"),
        "kineticGain": ("linear", "kineticGain"),
        "actualPhysicalLinearGain": ("hierarchy", "actualPhysicalLinearGain"),
        "finiteInviscidActionPrefactor": (None, "finiteInviscidActionPrefactor"),
        "finiteViscousActionNormalizedPhysicalGain": (
            None, "finiteViscousActionNormalizedPhysicalGain",
        ),
        "physicalKineticGainRelativeDifference": (
            None, "physicalKineticGainRelativeDifference",
        ),
        "aEndpointL2": ("hierarchy", "aEndpointL2"),
        "bEndpointL2": ("hierarchy", "bEndpointL2"),
        "bTargetEndpointL2": ("hierarchy", "bTargetEndpointL2"),
        "cTargetEndpointL2": ("hierarchy", "cTargetEndpointL2"),
        "cTripleEndpointL2": ("hierarchy", "cTripleEndpointL2"),
        "cMeanPathSignedParallel": ("hierarchy", "cMeanPathSignedParallel"),
        "cDoublePathSignedParallel": ("hierarchy", "cDoublePathSignedParallel"),
        "cTotalSignedParallel": ("hierarchy", "cTotalSignedParallel"),
        "forbiddenParityRelative": ("hierarchy", "forbiddenParityRelative"),
    }
    for row in primary_rows:
        case = cases_by_key[(int(row["N"]), f(row, "epsilon"))]
        primary_csv_exact = primary_csv_exact and row["finiteCompressionOnly"] == "true"
        for field, (section, key) in csv_sources.items():
            expected_value = case[key] if section is None else case[section][key]
            primary_csv_exact = primary_csv_exact and close(
                f(row, field), float(expected_value), 2e-14,
            )

    output_schema_ok = all(
        type(nested(case, row["path"])) is float
        for case in cases for row in config["outputSchema"]["caseScalars"]
    ) and primary.get("normalization") == {
        "finiteInviscidActionProxy": "integral of lambda_(N,0) on [0,D*]",
        "finiteViscousAction": "integral of lambda_(N,epsilon) on [0,D*]",
        "finiteInviscidActionPrefactor": "actualPhysicalLinearGain*exp(-A_(N,0)/epsilon)",
        "a": "V1/actualPhysicalLinearGain",
        "b": "V2/actualPhysicalLinearGain^2",
        "c": "V3/actualPhysicalLinearGain^3",
    } and all(case.get("normalization") == {
        "a": "V1/actualPhysicalLinearGain",
        "b": "V2/actualPhysicalLinearGain^2",
        "c": "V3/actualPhysicalLinearGain^3",
    } for case in cases)

    _, cutoff_rows = load_csv(package / "cutoff_convergence.csv")
    _, step_rows = load_csv(package / "step_convergence.csv")
    largest_rows = [row for row in cutoff_rows
                    if int(row["smallN"]) == cutoffs[-2]
                    and int(row["largeN"]) == cutoffs[-1]]
    largest_action = max(f(row, "finiteInviscidActionProxyAbsoluteDifference")
                         for row in largest_rows)
    largest_prefactor = max(
        f(row, "finiteInviscidActionPrefactorAbsoluteDifference")
        for row in largest_rows
    )
    finest_hierarchy = max(
        f(row, "selectedObservableHierarchyMaximumRelativeDifference")
        for row in largest_rows
    )
    step_maximum = max(f(row, "selectedObservableMaximumRelativeDifference")
                       for row in step_rows)

    archive_index = primary.get("archiveIndex", [])
    archive_keys = [row["archiveKey"] for row in archive_index]
    raw_metrics: dict[tuple[int, float], dict[str, float]] = {}
    archive_ok = (
        len(archive_index) == len(cases)
        and [(int(row["N"]), float(row["epsilon"])) for row in archive_index]
        == expected_cases
        and all(row.get("stateOrder") == list(STATE_ORDER)
                and row.get("shape") == [5, 7, 2 * int(row["N"]) + 1, 2]
                for row in archive_index)
    )
    target_ok = True
    case_formula_ok = True
    raw_case_values_ok = True
    with np.load(package / "coefficient_endpoints.npz", allow_pickle=False) as archive:
        archive_ok = archive_ok and set(archive.files) == set(archive_keys) and len(archive.files) == len(archive_keys)
        for case in cases:
            n, epsilon = int(case["N"]), float(case["epsilon"])
            state = archive[case["archiveKey"]]
            metrics = coefficient_metrics(state, n)
            raw_metrics[(n, epsilon)] = metrics
            stored = case["hierarchy"]
            raw_case_values_ok = raw_case_values_ok and all(
                close(float(stored[key]), value, 2e-11) for key, value in metrics.items()
            )
            action0 = float(case["linear"]["finiteInviscidActionProxy"])
            actione = float(case["linear"]["finiteViscousAction"])
            gain = float(stored["actualPhysicalLinearGain"])
            prefactor = float(case["finiteInviscidActionPrefactor"])
            viscous_norm = float(case["finiteViscousActionNormalizedPhysicalGain"])
            case_formula_ok = case_formula_ok and close(
                prefactor, gain * math.exp(-action0 / epsilon), 2e-13,
            ) and close(
                viscous_norm, gain * math.exp(-actione / epsilon), 2e-13,
            ) and action0 != actione
            diagnostics = case.get("thirdOrderTargetDiagnostics", [])
            if [row.get("rho") for row in diagnostics] != [0.02, 0.05]:
                target_ok = False
                continue
            one = state[0][[2, 4]] / gain
            third = (state[3][[2, 4]] + state[4][[2, 4]]) / gain ** 3
            for row in diagnostics:
                rho = float(row["rho"])
                delta = rho * prefactor
                target_norm = float(np.linalg.norm(delta * one + delta ** 3 * third))
                target_ok = target_ok and close(float(row["delta"]), delta, 2e-13)
                target_ok = target_ok and close(float(row["targetRowL2"]), target_norm, 2e-13)
                target_ok = target_ok and row.get("diagnosticOnly") is True
                target_ok = target_ok and row.get(
                    "visualizationChoiceIsCertifiedContinuumTaylorRadius"
                ) is False and row.get("fullNonlinearTrajectoryComputed") is False

    recomputed_maximums = {
        "selectedEigenvalueImaginaryAbs": max_eigen_imaginary,
        "eigenResidualRelative": max_eigen_residual,
        "generatorRelativeDefect": max(float(case["generatorRelativeDefect"])
                                       for case in cases),
        "divergenceRelative": max(row["maximumDivergenceRelative"]
                                  for row in raw_metrics.values()),
        "realityRelative": max(row["maximumRealityRelative"]
                               for row in raw_metrics.values()),
        "forbiddenParityRelative": max(row["forbiddenParityRelative"]
                                       for row in raw_metrics.values()),
        "physicalKineticGainRelative": max(
            float(case["physicalKineticGainRelativeDifference"]) for case in cases
        ),
        "largestCutoffActionProxyAbsolute": largest_action,
        "largestCutoffPrefactorAbsolute": largest_prefactor,
        "hierarchyFinestCutoffRelative": finest_hierarchy,
        "hierarchyStepRelative": step_maximum,
        "aEndpointNormalizationAbsolute": max(
            abs(row["aEndpointL2"] - 1.0) for row in raw_metrics.values()
        ),
        "outerThreeMassFraction": max(
            row[key] for row in raw_metrics.values() for key in (
                "v1OuterThreeMassFraction", "v2OuterThreeMassFraction",
                "v3OuterThreeMassFraction",
            )
        ),
        "minimumPhaseAnchorAbs": minimum_anchor,
    }
    maximums_match = set(primary.get("maximums", {})) == set(recomputed_maximums) and all(
        close(float(primary["maximums"][key]), value, 2e-11)
        for key, value in recomputed_maximums.items()
    )
    generator_samples_ok = all(
        [row["d"] for row in case.get("generatorRelativeDefectSamples", [])]
        == [0.0, 1.0 / 900.0, 1.0 / 450.0]
        and close(float(case["generatorRelativeDefect"]), max(
            float(row["relativeDefect"])
            for row in case["generatorRelativeDefectSamples"]
        )) for case in cases
    )

    primary_gates = {
        "selectedEigenvalueNumericallyReal": max_eigen_imaginary <= tolerances["numericalReality"],
        "eigenResidualRelative": max_eigen_residual <= tolerances["eigenResidualRelative"],
        "generatorRelativeDefect": recomputed_maximums["generatorRelativeDefect"] <= tolerances["generatorRelative"],
        "divergenceRelative": recomputed_maximums["divergenceRelative"] <= tolerances["divergenceRelative"],
        "realityRelative": recomputed_maximums["realityRelative"] <= tolerances["realityRelative"],
        "forbiddenParityRelative": recomputed_maximums["forbiddenParityRelative"] <= tolerances["forbiddenParityRelative"],
        "physicalKineticGainRelative": recomputed_maximums["physicalKineticGainRelative"] <= tolerances["physicalKineticGainRelative"],
        "largestCutoffActionProxyAbsolute": largest_action <= tolerances["largestCutoffActionProxyAbsolute"],
        "largestCutoffPrefactorAbsolute": largest_prefactor <= tolerances["largestCutoffPrefactorAbsolute"],
        "hierarchyFinestCutoffRelative": finest_hierarchy <= tolerances["hierarchyFinestCutoffRelative"],
        "hierarchyStepRelative": step_maximum <= tolerances["hierarchyStepRelative"],
        "aEndpointNormalizationAbsolute": recomputed_maximums["aEndpointNormalizationAbsolute"] <= tolerances["aEndpointNormalizationAbsolute"],
        "outerThreeMassFraction": recomputed_maximums["outerThreeMassFraction"] <= tolerances["outerThreeMassFraction"],
        "allPhaseAnchorsNonzero": minimum_anchor > 1e-12,
        "allFixedContourCountsOne": all_contours,
    }

    linear_validations = linear.get("validations", [])
    linear_sentinel_ok = (linear.get("sentinels") == linear_sentinels
                          and linear.get("stepCounts") == linear_steps
                          and len(linear_validations) == len(linear_sentinels))
    linear_gates_ok = all(
        row.get("pass") is True
        and float(row["finestVsPrimary"]["gainRelative"]) <= tolerances["independentLinearGainRelative"]
        and float(row["finestVsPrimary"]["finiteInviscidActionProxyRelative"]) <= tolerances["independentLinearActionRelative"]
        and float(row["finestVsPrimary"]["finiteViscousActionRelative"]) <= tolerances["independentLinearActionRelative"]
        and float(row["finestVsPrimary"]["finiteInviscidActionPrefactorAbsolute"]) <= tolerances["independentLinearPrefactorAbsolute"]
        and max(float(value) for value in row["lastTwoStepCountsRelative"].values()) <= tolerances["independentLinearRefinement"]
        for row in linear_validations
    )

    hierarchy_validations = hierarchy.get("validations", [])
    hierarchy_sentinel_ok = (hierarchy.get("sentinels") == hierarchy_sentinels
                             and len(hierarchy_validations) == len(hierarchy_sentinels))
    hierarchy_gates_ok = all(
        row.get("pass") is True
        and float(row["maximumCoefficientRelativeError"]) <= tolerances["independentHierarchyCoefficientRelative"]
        and float(row["forbiddenParityRelative"]) <= tolerances["independentHierarchyForbiddenParityRelative"]
        and list(row["pathRelativeErrors"]) == list(STATE_ORDER)
        for row in hierarchy_validations
    )

    expected_identities = {
        "profileTimeEnd": ("1/450", "1/450"),
        "physicalTimeEnd": ("1/1800", "1/1800"),
        "twoRateMargin": ("1/1500", "1/1500"),
        "threeRateMargin": ("1/1000", "1/1000"),
        "fourRateMargin": ("21/125", "21/125"),
    }
    exact_ok = exact.get("allChecksPass") is True and all(
        exact.get("identities", {}).get(key) == {
            "left": left, "right": right, "equal": True,
        } for key, (left, right) in expected_identities.items()
    ) and Fraction(1, 450) / 4 == Fraction(1, 1800)

    primary_manifest = load_json(package / "primary_manifest.json")
    primary_manifest_files = set(PRIMARY_FILES) - {"primary_manifest.json"}
    manifest_ok = (
        primary_manifest.get("allChecksPass") is True
        and primary_manifest.get("smokeMode") is smoke
        and primary_manifest.get("claimBoundary") == claim
        and verify_binding_rows(primary_manifest.get("files"), package,
                                primary_manifest_files)
    )
    monitor_ok = True
    for prefix in ("primary", "independent_linear", "independent_hierarchy"):
        progress = load_ndjson(package / f"{prefix}_progress.ndjson")
        resources = load_ndjson(package / f"{prefix}_resources.ndjson")
        monitor_ok = monitor_ok and progress[0].get("event") == "start"
        monitor_ok = monitor_ok and progress[-1].get("event") == "complete"
        monitor_ok = monitor_ok and resources[0].get("event") == "start"
        monitor_ok = monitor_ok and resources[-1].get("event") == "complete"

    upstream_ok = all(
        sha256(ROOT / row["path"]) == row["sha256"]
        for row in config["upstreamBindings"]
    )
    certificate_ok = (
        certificate.get("schemaVersion") == "r073m-finite-certificate-v1"
        and certificate.get("allChecksPass") is True
        and certificate.get("smokeMode") is smoke
        and certificate.get("claimBoundary") == claim
        and certificate.get("sourceProvenance") == stable
        and certificate.get("continuumConclusion")
        == "none; finite binary64 diagnostics only"
        and verify_binding_rows(
            certificate.get("scientificInputBindings"), package,
            set(ASSEMBLY_SCIENTIFIC_INPUTS),
        )
    )
    checks = {
        "configurationBytesExactlyFrozen": True,
        "sourceGateMatchesScientificPayloads": all(
            row.get("sourceProvenance") == stable for row in scientific_jsons
        ),
        "allScientificJsonFinite": all(finite_tree(row) for row in scientific_jsons),
        "scientificJsonContainsNoOperationalTimeFields": all(
            no_temporal_keys(row) for row in scientific_jsons
        ),
        "claimBoundaryExactEverywhere": all(
            list(row.get("claimBoundary", {}).items())
            == list(EXPECTED_CLAIM_BOUNDARY.items()) for row in scientific_jsons
        ),
        "primaryModeAndPass": primary.get("smokeMode") is smoke and primary.get("allChecksPass") is True,
        "primaryCaseGridExact": case_grid_exact,
        "primaryActionNodeGridExact": action_grid_exact,
        "primaryCsvGridExact": primary_csv_exact,
        "configuredOutputSchemaRealizedExactly": output_schema_ok,
        "coefficientArchiveSchemaExact": archive_ok,
        "rawCoefficientMetricsRecomputed": raw_case_values_ok,
        "separateActionAndPrefactorFormulas": case_formula_ok,
        "thirdOrderTargetDiagnosticsExact": target_ok,
        "generatorDefectThreeTimesExact": generator_samples_ok,
        "primaryMaximumOperandsRecomputed": maximums_match,
        "primaryToleranceGatesRecomputed": all(primary_gates.values()),
        "primaryStoredChecksAllTrue": (
            isinstance(primary.get("checks"), dict)
            and all(primary["checks"].values())
        ),
        "primaryManifestBindingsValid": manifest_ok,
        "operationalMonitorsStartAndComplete": monitor_ok,
        "independentProgramsDoNotImportPrimary": (
            independent_import_check(HERE / "independent_linear.py")
            and independent_import_check(HERE / "independent_hierarchy.py")
            and linear.get("method", {}).get("importsPrimaryProducer") is False
            and hierarchy.get("method", {}).get("importsPrimaryProducer") is False
        ),
        "independentLinearSentinelsExact": linear_sentinel_ok,
        "independentLinearGatesRecomputed": linear_gates_ok,
        "independentHierarchySentinelsExact": hierarchy_sentinel_ok,
        "independentHierarchyGatesRecomputed": hierarchy_gates_ok,
        "exactRationalIdentitiesIndependentlyConfirmed": exact_ok,
        "upstreamRolePathHashesVerified": upstream_ok,
        "assembledCertificateBoundaryAndPassValid": certificate_ok,
    }
    observations = {
        "caseCount": len(cases),
        "actionNodeCount": len(action_rows),
        "minimumPhaseAnchorAbs": minimum_anchor,
        "maximumSelectedEigenvalueImaginaryAbs": max_eigen_imaginary,
        "maximumSelectedEigenResidualRelative": max_eigen_residual,
        "recomputedPrimaryMaximums": recomputed_maximums,
        "primaryGates": primary_gates,
    }
    return checks, observations


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def main() -> int:
    package = ARGS.package_dir.resolve()
    config_path = ARGS.config.resolve()
    if ARGS.smoke:
        if package.is_relative_to(HERE.resolve()):
            fail("smoke validation must be outside the formal package")
    elif package != HERE.resolve() or config_path != (HERE / "config.json").resolve():
        fail("formal validation must use canonical package and config")
    if sha256(config_path) != EXPECTED_CONFIG_SHA256:
        fail("canonical configuration byte contract drift")
    config = load_json(config_path)
    if (list(config.get("claimBoundary", {}).items())
            != list(EXPECTED_CLAIM_BOUNDARY.items())):
        fail("claim boundary key set, order, spelling, or values drifted")
    provenance = source_gate(ARGS.source_commit, ARGS.smoke)
    for row in config["upstreamBindings"]:
        if sha256(ROOT / row["path"]) != row["sha256"]:
            fail(f"upstream hash drift: {row['path']}")

    checks, observations = validate(package, config, ARGS.smoke, provenance)
    report = {
        "schemaVersion": "r073m-independent-package-validation-v1",
        "release": "R0.73M",
        "smokeMode": ARGS.smoke,
        "sourceProvenance": stable_provenance(provenance),
        "configurationBinding": binding(config_path, ROOT),
        "scientificFileBindings": [
            binding(package / name, package) for name in SCIENTIFIC_INPUTS
        ],
        "observations": observations,
        "checks": checks,
        "allChecksPass": all(checks.values()),
        "claimBoundary": config["claimBoundary"],
    }
    output = (ARGS.output.resolve() if ARGS.output
              else package / "validation.json")
    if ARGS.verify_only:
        stored = load_json(package / "validation.json")
        if stored != report:
            fail("stored validation report is not the deterministic recomputation")
        if not verify_seal(package, ARGS.smoke, provenance, config["claimBoundary"]):
            fail("sealed manifest or SHA256SUMS verification failed")
    else:
        if output != package / "validation.json":
            fail("validation output must be package/validation.json")
        if output.exists() and not ARGS.overwrite:
            fail("refusing to overwrite validation.json")
        atomic_json(output, report)
    return 0 if report["allChecksPass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
