#!/usr/bin/env python3
"""Fail-closed validator for the R0.73P formula-diagnostic package."""

from __future__ import annotations

import argparse
import csv
from decimal import Decimal, InvalidOperation
import hashlib
import json
import math
from pathlib import Path
import re


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CSV_FIELDS = (
    "record_type",
    "sample_index",
    "N",
    "h3_threshold",
    "hhalf_threshold",
    "gamma",
    "l2_power",
    "hhalf_power",
    "h3_power",
    "tau",
    "discrete_heat",
    "continuous_heat_bound",
    "discrete_to_continuous",
    "maximizer_norm_squared",
    "k1",
    "k2",
    "k3",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-only", action="store_true")
    return parser.parse_args()


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_strict(path: Path) -> dict:
    require(path.is_file() and not path.is_symlink(), "missing regular JSON: " + path.name)

    def reject(value: str) -> None:
        raise ValueError("nonfinite JSON constant: " + value)

    def unique(pairs: list[tuple[str, object]]) -> dict:
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON key: " + key)
            result[key] = value
        return result

    value = json.loads(
        path.read_text(encoding="utf-8"),
        parse_constant=reject,
        object_pairs_hook=unique,
    )
    require(isinstance(value, dict), "JSON root is not an object: " + path.name)
    return value


def finite_tree(value: object) -> bool:
    if value is None or isinstance(value, (bool, str, int)):
        return True
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, list):
        return all(finite_tree(item) for item in value)
    if isinstance(value, dict):
        return all(finite_tree(item) for item in value.values())
    return False


def exact_binding(row: dict[str, object], *, relative_to_root: bool) -> bool:
    raw = row.get("path")
    if not isinstance(raw, str):
        return False
    path = ROOT / raw if relative_to_root else HERE / raw
    try:
        return (
            path.is_file()
            and not path.is_symlink()
            and path.stat().st_size == row.get("bytes")
            and sha256(path) == row.get("sha256")
        )
    except OSError:
        return False


def main() -> None:
    args = parse_args()
    config = load_strict(HERE / "config.json")
    primary = load_strict(HERE / "diagnostic.json")
    independent = load_strict(HERE / "independent_validation.json")
    certificate = load_strict(HERE / "certificate.json")
    environment = load_strict(HERE / "environment.json")
    expected_schemas = {
        "config": (config, "r073p-formula-diagnostic-config-v1"),
        "primary": (primary, "r073p-formula-diagnostic-v1"),
        "independent": (
            independent,
            "r073p-formula-diagnostic-independent-validation-v1",
        ),
        "certificate": (certificate, "r073p-formula-diagnostic-certificate-v1"),
        "environment": (environment, "r073p-formula-diagnostic-environment-v1"),
    }
    schemas_exact = all(
        payload.get("schemaVersion") == schema
        for payload, schema in expected_schemas.values()
    )
    stored_checks_pass = all(
        payload.get("allChecksPass") is True
        and payload.get("status") == "passed"
        and payload.get("checks")
        and all(value is True for value in payload["checks"].values())
        for payload in (primary, independent, certificate)
    )

    source_path = HERE / "source-data.csv"
    with source_path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        csv_schema_exact = tuple(reader.fieldnames or ()) == CSV_FIELDS
        rows = list(reader)
    kinds = {"threshold", "sobolev_power", "heat_lattice"}
    counts = {
        "thresholdRows": sum(row["record_type"] == "threshold" for row in rows),
        "sobolevPowerRows": sum(row["record_type"] == "sobolev_power" for row in rows),
        "heatLatticeRows": sum(row["record_type"] == "heat_lattice" for row in rows),
        "totalRows": len(rows),
    }
    expected_counts = {
        "thresholdRows": int(primary["sourceData"]["thresholdRows"]),
        "sobolevPowerRows": int(primary["sourceData"]["sobolevPowerRows"]),
        "heatLatticeRows": int(primary["sourceData"]["heatLatticeRows"]),
        "totalRows": int(primary["sourceData"]["rows"]),
    }
    numeric_finite = True
    blank_fields_valid = True
    expected_nonblank = {
        "threshold": {"record_type", "sample_index", "N", "h3_threshold", "hhalf_threshold"},
        "sobolev_power": {"record_type", "sample_index", "gamma", "l2_power", "hhalf_power", "h3_power"},
        "heat_lattice": {"record_type", "sample_index", "tau", "discrete_heat", "continuous_heat_bound", "discrete_to_continuous", "maximizer_norm_squared", "k1", "k2", "k3"},
    }
    for row in rows:
        kind = row.get("record_type", "")
        if kind not in kinds:
            blank_fields_valid = False
            continue
        nonblank = {key for key, value in row.items() if value != ""}
        blank_fields_valid = blank_fields_valid and nonblank == expected_nonblank[kind]
        for key, value in row.items():
            if key == "record_type" or value == "":
                continue
            try:
                numeric_finite = numeric_finite and Decimal(value).is_finite()
            except (InvalidOperation, ValueError):
                numeric_finite = False

    panel_a_rows = [row for row in rows if row["record_type"] == "threshold"]
    panel_b_rows = [row for row in rows if row["record_type"] == "sobolev_power"]
    panel_c_rows = [row for row in rows if row["record_type"] == "heat_lattice"]
    formula_tolerance = float(config["tolerances"]["formulaRelative"])
    panel_a_formulas = all(
        math.isclose(float(row["h3_threshold"]), int(row["N"]) ** -3.0, rel_tol=formula_tolerance)
        and math.isclose(float(row["hhalf_threshold"]), int(row["N"]) ** -0.5, rel_tol=formula_tolerance)
        for row in panel_a_rows
    )
    panel_b_formulas = all(
        math.isclose(float(row["l2_power"]), -float(row["gamma"]), rel_tol=0.0, abs_tol=formula_tolerance)
        and math.isclose(float(row["hhalf_power"]), 0.5 - float(row["gamma"]), rel_tol=0.0, abs_tol=formula_tolerance)
        and math.isclose(float(row["h3_power"]), 3.0 - float(row["gamma"]), rel_tol=0.0, abs_tol=formula_tolerance)
        for row in panel_b_rows
    )
    panel_b_strip = all(
        not (0.5 < float(row["gamma"]) < 3.0)
        or (
            float(row["l2_power"]) < 0.0
            and float(row["hhalf_power"]) < 0.0
            and float(row["h3_power"]) > 0.0
        )
        for row in panel_b_rows
    )
    panel_c_formulas = all(
        int(row["k1"]) ** 2 + int(row["k2"]) ** 2 + int(row["k3"]) ** 2
        == int(row["maximizer_norm_squared"])
        and math.isclose(
            float(row["discrete_heat"]),
            int(row["maximizer_norm_squared"]) ** 1.5
            * math.exp(-float(row["tau"]) * int(row["maximizer_norm_squared"])),
            rel_tol=formula_tolerance,
        )
        and math.isclose(
            float(row["continuous_heat_bound"]),
            (3.0 / (2.0 * math.e * float(row["tau"]))) ** 1.5,
            rel_tol=formula_tolerance,
        )
        and float(row["discrete_to_continuous"])
        <= 1.0 + float(config["tolerances"]["continuousEnvelopeSlack"])
        for row in panel_c_rows
    )

    boundary = config["claimBoundary"]
    required_boundary = {
        "formulaDiagnosticOnly": True,
        "closedFormThresholdComparison": True,
        "pureModeSobolevScaling": True,
        "finiteLatticeGlobalMaximumOnConfiguredTauGrid": True,
        "continuousLinearHeatUpperBound": True,
        "navierStokesSimulation": False,
        "nonlinearEntryCertified": False,
        "pdeNecessityEstablished": False,
        "globalRegularityEstablished": False,
        "finiteTimeSingularityEstablished": False,
        "clayProblemSolved": False,
    }
    independent_source = (HERE / "independent_validate.py").read_text(encoding="utf-8")
    forbidden_independent_patterns = (
        r"\bimport\s+compute_formula_diagnostic\b",
        r"\bfrom\s+compute_formula_diagnostic\s+import\b",
        r"subprocess\s*\.",
        r"runpy\s*\.",
    )
    requirement_lock = (HERE / "requirements.txt").read_text(encoding="utf-8")
    figure_source = ROOT / str(config["figureReference"]) / "source-data.csv"
    cutoff = int(config["panelC"]["cutoffNormSquared"])
    minimum_tau = float(config["panelC"]["minimumTau"])
    certificate_binding_names = [row.get("path") for row in certificate["inputBindings"]]
    expected_binding_names = [
        "config.json",
        "diagnostic.json",
        "independent_validation.json",
        "source-data.csv",
    ]
    checks = {
        "schemasExact": schemas_exact,
        "allStoredChecksPass": stored_checks_pass,
        "scientificJsonFinite": all(
            finite_tree(payload)
            for payload in (config, primary, independent, certificate, environment)
        ),
        "dependencyLockExact": requirement_lock == "# Python standard library only; no third-party packages.\n",
        "sourceDataSchemaExact": csv_schema_exact,
        "sourceDataCountsExact": counts == expected_counts == {
            "thresholdRows": 198,
            "sobolevPowerRows": 351,
            "heatLatticeRows": 241,
            "totalRows": 790,
        },
        "sourceDataHashAndSizeExact": (
            source_path.stat().st_size == primary["sourceData"]["bytes"]
            and sha256(source_path) == primary["sourceData"]["sha256"]
            and sha256(source_path) == independent["sourceData"]["sha256"]
        ),
        "sourceDataNumericFieldsFinite": numeric_finite,
        "sourceDataBlankFieldsExact": blank_fields_valid,
        "panelAFormulasRechecked": panel_a_formulas,
        "panelBFormulasRechecked": panel_b_formulas and panel_b_strip,
        "panelCFormulasRechecked": panel_c_formulas,
        "cutoffIdentityExact": cutoff == int(config["panelC"]["latticeHalfWidth"]) ** 2 == 4096,
        "cutoffStrictlyBeyondAllContinuousPeaks": cutoff > 3.0 / (2.0 * minimum_tau) == 1500.0,
        "independentThreeSquareCountExact": independent["observations"]["representableRadiusCountThroughCutoff"] == 3414,
        "independentProducerIsolationSourceCheck": not any(
            re.search(pattern, independent_source) for pattern in forbidden_independent_patterns
        ),
        "primaryClaimBoundaryExact": primary.get("claimBoundary") == boundary == required_boundary,
        "independentClaimBoundaryExact": independent.get("claimBoundary") == boundary,
        "certificateClaimBoundaryExact": (
            certificate.get("claimBoundary") == boundary
            and certificate.get("independentClaimBoundary") == boundary
            and certificate.get("diagnosticOnly") is True
        ),
        "figureBindingsExact": (
            len(primary["figureBindings"]) == 4
            and all(exact_binding(row, relative_to_root=True) for row in primary["figureBindings"])
        ),
        "figureSourceDataByteIdentical": source_path.read_bytes() == figure_source.read_bytes(),
        "certificateBindingsExact": (
            certificate_binding_names == expected_binding_names
            and all(exact_binding(row, relative_to_root=False) for row in certificate["inputBindings"])
        ),
        "unsupportedClaimsRemainFalse": all(
            boundary[key] is False
            for key in (
                "navierStokesSimulation",
                "nonlinearEntryCertified",
                "pdeNecessityEstablished",
                "globalRegularityEstablished",
                "finiteTimeSingularityEstablished",
                "clayProblemSolved",
            )
        ),
    }
    require(all(checks.values()), "certificate validation failed: " + ", ".join(
        key for key, passed in checks.items() if not passed
    ))
    validation = {
        "schemaVersion": "r073p-formula-diagnostic-validation-v1",
        "release": "R0.73P",
        "status": "passed",
        "allChecksPass": True,
        "checks": checks,
        "observations": {
            "sourceData": counts,
            "sourceDataSha256": sha256(source_path),
            "figureSourceDataSha256": sha256(figure_source),
            "cutoffNormSquared": cutoff,
            "continuousPeakNormSquaredAtMinimumTau": 3.0 / (2.0 * minimum_tau),
            "representableRadiusCountThroughCutoff": independent["observations"]["representableRadiusCountThroughCutoff"],
            "minimumMaximizerNormSquared": independent["observations"]["minimumMaximizerNormSquared"],
            "maximumMaximizerNormSquared": independent["observations"]["maximumMaximizerNormSquared"],
        },
        "claimBoundary": boundary,
        "independentClaimBoundary": independent["claimBoundary"],
    }
    payload = canonical(validation)
    output = HERE / "validation.json"
    if args.verify_only:
        require(output.is_file() and not output.is_symlink(), "validation.json missing")
        require(output.read_text(encoding="utf-8") == payload, "validation.json is stale")
    else:
        output.write_text(payload, encoding="utf-8")
    print(canonical({
        "status": "passed",
        "checks": len(checks),
        "verifyOnly": args.verify_only,
    }), end="")


if __name__ == "__main__":
    main()
