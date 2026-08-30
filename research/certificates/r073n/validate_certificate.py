#!/usr/bin/env python3
"""Fail-closed independent validator for the R0.73N certificate package."""

from __future__ import annotations

import argparse
import csv
from decimal import Decimal
from fractions import Fraction
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
import mpmath as mp  # noqa: E402


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
        "config": (config, "r073n-finite-strain-config-v1"),
        "primary": (primary, "r073n-finite-strain-diagnostic-v1"),
        "independent": (independent, "r073n-independent-decimal-validation-v1"),
        "certificate": (certificate, "r073n-finite-strain-certificate-v1"),
        "environment": (environment, "r073n-finite-strain-environment-v1"),
    }
    schemas_exact = all(
        payload.get("schemaVersion") == schema
        for payload, schema in expected_schemas.values()
    )
    boundary = config["claimBoundary"]
    boundary_exact = all(
        payload.get("claimBoundary") == boundary
        for payload in (primary, independent, certificate)
    )
    all_passed = all(
        payload.get("allChecksPass") is True
        and all(payload.get("checks", {}).values())
        for payload in (primary, independent, certificate)
    )
    with (HERE / "source-data.csv").open("r", encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    counts = {
        "strainSamples": sum(row["record_type"] == "strain_sample" for row in rows),
        "cumulativeSamples": sum(row["record_type"] == "cumulative_sample" for row in rows),
        "markedBasepointSamples": sum(
            row["record_type"] == "marked_basepoint_sample" for row in rows
        ),
        "totalRows": len(rows),
    }
    expected_counts = {
        key: int(primary["sourceData"][key]) for key in counts
    }
    csv_hash_exact = sha256(HERE / "source-data.csv") == primary["sourceData"]["sha256"]
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
    d_star_q = Fraction(config["profileTimeEnd"])
    t_star_q = Fraction(config["physicalTimeEnd"])
    rational_lower_q = Fraction(config["jStarRationalLower"])
    action_upper_q = Fraction(config["inheritedActionUpper"])
    action_lower_q = Fraction(config["inheritedActionLower"])
    mp.mp.dps = int(config["precisionDecimalDigits"])
    t_star = mp.mpf(t_star_q.numerator) / t_star_q.denominator
    recomputed_j_star = -mp.expm1(-4 * t_star) / 4 - mp.expm1(-16 * t_star) / 16
    stored_j_star = mp.mpf(primary["highPrecision"]["jStar"])
    independent_source = (HERE / "independent_validate.py").read_text(encoding="utf-8")
    dependency_lock = (HERE / "requirements.txt").read_text(encoding="utf-8")
    checks = {
        "schemasExact": schemas_exact,
        "claimBoundaryExact": boundary_exact,
        "allStoredChecksPass": all_passed,
        "scientificJsonFinite": all(
            finite_tree(payload) for payload in (
                config, primary, independent, certificate, environment
            )
        ),
        "dependencyLockExact": dependency_lock == "mpmath==1.3.0\n",
        "runtimeVersionMatchesLock": mp.__version__ == "1.3.0",
        "environmentRuntimeMatchesLock": environment.get("mpmath") == "1.3.0",
        "sourceDataCountsExact": counts == expected_counts,
        "sourceDataHashExact": csv_hash_exact,
        "sourceDataNumericFieldsFinite": csv_numeric_finite,
        "profilePhysicalEndpointIdentityExact": 4 * t_star_q == d_star_q,
        "jInfinityExact": Fraction(config["jInfinity"]) == Fraction(5, 16),
        "analyticLowerWitnessExact": (
            d_star_q / 2 - 5 * d_star_q * d_star_q / 8
            == rational_lower_q == Fraction(359, 324000)
        ),
        "rationalChainExact": rational_lower_q > action_upper_q > action_lower_q,
        "recomputedJStarStrictlyAboveWitness": (
            recomputed_j_star
            > mp.mpf(rational_lower_q.numerator) / rational_lower_q.denominator
        ),
        "recomputedJStarMatchesPrimary": abs(recomputed_j_star - stored_j_star) < mp.mpf("1e-80"),
        "independentProducerDoesNotImportPrimary": (
            "import compute_diagnostic" not in independent_source
            and "from compute_diagnostic" not in independent_source
            and "import mpmath" not in independent_source
        ),
        "unsupportedClaimsRemainFalse": all(
            boundary[key] is False for key in (
                "finiteComputationProvesInheritedActionInterval",
                "finiteComputationProvesContinuumEnergyEstimate",
                "finiteComputationProvesFixedMemberStabilityTube",
                "sharpFamilyLipschitzExponentCertified",
                "singleFixedBackgroundLyapunovInstabilityCertified",
                "fullThreeDimensionalFPSH3L2StabilityCertified",
                "transverseCriticalNormGrowthCertified",
                "finiteTimeSingularityCertified",
                "clayProblemSolved",
            )
        ),
        "certificateBindingsExact": all(
            (HERE / row["path"]).is_file()
            and (HERE / row["path"]).stat().st_size == row["bytes"]
            and sha256(HERE / row["path"]) == row["sha256"]
            for row in certificate["inputBindings"]
        ),
    }
    if not all(checks.values()):
        failed = [key for key, value in checks.items() if not value]
        raise RuntimeError("certificate validation failed: " + ", ".join(failed))
    validation = {
        "schemaVersion": "r073n-finite-strain-validation-v1",
        "release": "R0.73N",
        "status": "passed",
        "allChecksPass": True,
        "checks": checks,
        "observations": {
            "sourceData": counts,
            "jStar": primary["highPrecision"]["jStar"],
            "jStarMinusRationalLower": primary["highPrecision"]["margins"][
                "jStarMinusRationalLower"
            ],
            "independentValidationCount": len(independent["validations"]),
        },
        "claimBoundary": boundary,
    }
    payload = canonical(validation)
    output = HERE / "validation.json"
    if args.verify_only:
        if not output.is_file() or output.read_text(encoding="utf-8") != payload:
            raise RuntimeError("validation.json is stale")
    else:
        output.write_text(payload, encoding="utf-8")
    print(canonical({"status": "passed", "checks": len(checks), "verifyOnly": args.verify_only}), end="")


if __name__ == "__main__":
    main()
