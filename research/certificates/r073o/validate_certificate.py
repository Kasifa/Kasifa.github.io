#!/usr/bin/env python3
"""Fail-closed validator for the R0.73O spectrum certificate package."""

from __future__ import annotations

import argparse
import csv
from decimal import Decimal
import hashlib
import json
import math
from pathlib import Path
import sys


def bootstrap() -> None:
    for index, value in enumerate(sys.argv):
        if value == "--deps" and index + 1 < len(sys.argv):
            sys.path.insert(0, str(Path(sys.argv[index + 1]).resolve()))
            return
        if value.startswith("--deps="):
            sys.path.insert(0, str(Path(value.split("=", 1)[1]).resolve()))
            return


bootstrap()
import numpy as np  # noqa: E402
import scipy  # noqa: E402


HERE = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--verify-only", action="store_true")
    return parser.parse_args()


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_strict(path: Path) -> dict:
    if not path.is_file() or path.is_symlink():
        raise RuntimeError("missing regular JSON file: " + path.name)

    def reject(value: str) -> None:
        raise ValueError("nonfinite constant: " + value)

    def unique(pairs: list[tuple[str, object]]) -> dict:
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate key: " + key)
            result[key] = value
        return result

    value = json.loads(
        path.read_text(encoding="utf-8"),
        parse_constant=reject,
        object_pairs_hook=unique,
    )
    if not isinstance(value, dict):
        raise RuntimeError("JSON root is not an object: " + path.name)
    return value


def finite_tree(value: object) -> bool:
    if isinstance(value, bool) or value is None or isinstance(value, str):
        return True
    if isinstance(value, int):
        return True
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, list):
        return all(finite_tree(row) for row in value)
    if isinstance(value, dict):
        return all(finite_tree(row) for row in value.values())
    return False


def main() -> None:
    args = parse_args()
    config = load_strict(HERE / "config.json")
    primary = load_strict(HERE / "diagnostic.json")
    independent = load_strict(HERE / "independent_validation.json")
    certificate = load_strict(HERE / "certificate.json")
    environment = load_strict(HERE / "environment.json")
    expected_schemas = {
        "config": (config, "r073o-kolmogorov-spectrum-config-v1"),
        "primary": (primary, "r073o-kolmogorov-spectrum-diagnostic-v1"),
        "independent": (
            independent,
            "r073o-kolmogorov-spectrum-independent-validation-v1",
        ),
        "certificate": (
            certificate,
            "r073o-kolmogorov-spectrum-certificate-v1",
        ),
        "environment": (
            environment,
            "r073o-kolmogorov-spectrum-environment-v1",
        ),
    }
    schemas_exact = all(
        payload.get("schemaVersion") == schema
        for payload, schema in expected_schemas.values()
    )
    all_passed = all(
        payload.get("allChecksPass") is True
        and all(payload.get("checks", {}).values())
        for payload in (primary, independent, certificate)
    )

    with (HERE / "source-data.csv").open(
        "r", encoding="utf-8", newline=""
    ) as stream:
        rows = list(csv.DictReader(stream))
    counts = {
        "convergenceRows": sum(
            row["record_type"] == "convergence" for row in rows
        ),
        "sweepRows": sum(row["record_type"] == "sweep" for row in rows),
        "totalRows": len(rows),
    }
    expected_counts = {
        "convergenceRows": int(primary["sourceData"]["convergenceRows"]),
        "sweepRows": int(primary["sourceData"]["sweepRows"]),
        "totalRows": int(primary["sourceData"]["rows"]),
    }
    csv_hash_exact = (
        sha256(HERE / "source-data.csv") == primary["sourceData"]["sha256"]
    )
    csv_numeric_finite = True
    for row in rows:
        for key, value in row.items():
            if key in {"record_type", "record_id", "evidence_boundary"} or value == "":
                continue
            try:
                if not Decimal(value).is_finite():
                    csv_numeric_finite = False
            except Exception:
                csv_numeric_finite = False

    alpha = float(config["alpha"])
    target = float(config["targetReynolds"])
    amplitude = float(config["forcingAmplitude"])
    forcing_mode = int(config["forcingWaveNumber"])
    x_mode = int(config["physicalXWaveNumber"])
    viscosity = float(config["viscosity"])
    critical = [float(value) for value in config["rigorousCriticalInterval"]]
    finite = primary["finiteResults"]
    other = independent["independentFiniteResults"]
    comparison = independent["producerComparison"]
    primary_boundary = config["claimBoundary"]
    independent_boundary = independent["claimBoundary"]
    dependency_lock = (HERE / "requirements.txt").read_text(encoding="utf-8")
    independent_source = (HERE / "independent_validate.py").read_text(
        encoding="utf-8"
    )
    checks = {
        "schemasExact": schemas_exact,
        "allStoredChecksPass": all_passed,
        "scientificJsonFinite": all(
            finite_tree(payload)
            for payload in (config, primary, independent, certificate, environment)
        ),
        "dependencyLockExact": dependency_lock == "numpy==2.3.5\nscipy==1.18.1\n",
        "runtimeVersionsMatchLock": (
            np.__version__ == "2.3.5" and scipy.__version__ == "1.18.1"
        ),
        "environmentNumpyMatchesLock": environment.get("numpy") == "2.3.5",
        "independentRuntimeMatchesLock": (
            independent.get("software", {}).get("numpy") == "2.3.5"
            and independent.get("software", {}).get("scipy") == "1.18.1"
        ),
        "sourceDataCountsExact": counts == expected_counts,
        "sourceDataHashExact": csv_hash_exact,
        "sourceDataNumericFieldsFinite": csv_numeric_finite,
        "alphaEmbeddingIdentity": math.isclose(
            alpha, x_mode / forcing_mode, rel_tol=0.0, abs_tol=1e-15
        ),
        "reynoldsScalingIdentity": math.isclose(
            target,
            amplitude / (viscosity * forcing_mode),
            rel_tol=0.0,
            abs_tol=1e-15,
        ),
        "importedCriticalIntervalExact": critical == [
            3.011528364444,
            3.011528364446,
        ],
        "targetStrictlySupercritical": target > critical[1],
        "producerFiniteSigmaPositive": finite["leadingEigenvalueReal"] > 0.0,
        "independentFiniteSigmaPositive": other["leadingEigenvalueReal"] > 0.0,
        "physicalGrowthScalingExactWithinTolerance": abs(
            finite["physicalGrowthRate"]
            - amplitude * forcing_mode * finite["leadingEigenvalueReal"]
        ) < 1e-13,
        "independentAgreementWithinTolerance": (
            comparison["absoluteSigmaDifference"] < 5e-13
            and comparison["absolutePhysicalGrowthDifference"] < 2e-10
            and comparison["absoluteFiniteCrossingDifference"] < 5e-12
        ),
        "producerCodeNotImported": (
            "import compute_spectrum_diagnostic" not in independent_source
            and "from compute_spectrum_diagnostic" not in independent_source
        ),
        "primaryClaimBoundaryExact": primary.get("claimBoundary") == primary_boundary,
        "certificateClaimBoundaryExact": (
            certificate.get("claimBoundary") == primary_boundary
            and certificate.get("independentClaimBoundary") == independent_boundary
        ),
        "unsupportedPrimaryClaimsRemainFalse": all(
            primary_boundary[key] is False
            for key in (
                "finiteComputationProvesPositiveInfiniteDimensionalSpectrum",
                "finiteComputationReplacesNagatouCertificate",
                "nonlinearEscapeComputed",
                "essentiallyThreeDimensionalInstability",
                "finiteTimeSingularity",
                "clayProblemSolved",
            )
        ),
        "unsupportedIndependentClaimsRemainFalse": all(
            independent_boundary[key] is False
            for key in (
                "provesInfiniteDimensionalSpectrum",
                "replacesNagatouComputerAssistedCertificate",
                "provesNonlinearInstability",
                "provesThreeDimensionalSingularity",
                "solvesClayProblem",
            )
        ),
        "certificateBindingsExact": all(
            (HERE / row["path"]).is_file()
            and not (HERE / row["path"]).is_symlink()
            and (HERE / row["path"]).stat().st_size == row["bytes"]
            and sha256(HERE / row["path"]) == row["sha256"]
            for row in certificate["inputBindings"]
        ),
    }
    if not all(checks.values()):
        failed = [key for key, value in checks.items() if not value]
        raise RuntimeError("certificate validation failed: " + ", ".join(failed))

    validation = {
        "schemaVersion": "r073o-kolmogorov-spectrum-validation-v1",
        "release": "R0.73O",
        "status": "passed",
        "allChecksPass": True,
        "checks": checks,
        "observations": {
            "sourceData": counts,
            "producerLeadingEigenvalueReal": finite["leadingEigenvalueReal"],
            "independentLeadingEigenvalueReal": other["leadingEigenvalueReal"],
            "absoluteSigmaDifference": comparison["absoluteSigmaDifference"],
            "producerFiniteCriticalCrossing": finite["finiteCriticalCrossing"],
            "independentFiniteCriticalCrossing": other["finiteCriticalCrossing"],
        },
        "claimBoundary": primary_boundary,
        "independentClaimBoundary": independent_boundary,
    }
    payload = canonical(validation)
    output = HERE / "validation.json"
    if args.verify_only:
        if not output.is_file() or output.read_text(encoding="utf-8") != payload:
            raise RuntimeError("validation.json is stale")
    else:
        output.write_text(payload, encoding="utf-8")
    print(
        canonical(
            {
                "status": "passed",
                "checks": len(checks),
                "verifyOnly": args.verify_only,
            }
        ),
        end="",
    )


if __name__ == "__main__":
    main()
