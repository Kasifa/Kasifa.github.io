#!/usr/bin/env python3
"""Assemble the deterministic R0.73M finite-diagnostic certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
from typing import Any, Mapping


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
SCIENTIFIC_INPUTS = (
    "primary_results.json",
    "primary_rows.csv",
    "action_nodes.csv",
    "cutoff_convergence.csv",
    "step_convergence.csv",
    "coefficient_endpoints.npz",
    "independent_linear.json",
    "independent_hierarchy.json",
    "exact_identities.json",
)
OPERATIONAL_INPUTS = (
    "primary_environment.json",
    "primary_progress.ndjson",
    "primary_resources.ndjson",
    "primary_manifest.json",
    "independent_linear_progress.ndjson",
    "independent_linear_resources.ndjson",
    "independent_hierarchy_progress.ndjson",
    "independent_hierarchy_resources.ndjson",
)
EXPECTED_CONFIG_SHA256 = "100775fd92e34b939c563546b83b838eda60f677f7452a13459cf6ef2b2252fb"
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--package-dir", type=Path, required=True)
    parser.add_argument("--source-commit", default="")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def reject_constant(value: str) -> None:
    raise ValueError(f"nonfinite JSON constant: {value}")


def no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates,
        parse_constant=reject_constant,
    )
    if not isinstance(value, dict):
        raise RuntimeError(f"top-level JSON is not an object: {path.name}")
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def binding(path: Path, base: Path) -> dict[str, object]:
    if not path.is_file() or path.is_symlink():
        raise RuntimeError(f"expected regular non-symlink file: {path}")
    return {
        "path": path.resolve().relative_to(base.resolve()).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def source_gate(commit: str, smoke: bool) -> dict[str, object]:
    if smoke:
        return {"enforced": False, "sourceCommit": None, "allSourceBlobsMatch": False}
    if re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        raise RuntimeError("formal assembly requires a full lowercase source commit")
    resolved = subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", f"{commit}^{{commit}}"], text=True,
    ).strip()
    if resolved != commit:
        raise RuntimeError("source commit did not resolve exactly")
    head = subprocess.check_output(
        ["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True,
    ).strip()
    if subprocess.run(
        ["git", "-C", str(ROOT), "merge-base", "--is-ancestor", commit, head],
        check=False,
    ).returncode != 0:
        raise RuntimeError("source commit is not an ancestor of HEAD")
    rows = []
    for relative in SOURCE_FILES:
        path = ROOT / relative
        committed = subprocess.check_output(
            ["git", "-C", str(ROOT), "show", f"{commit}:{relative}"],
        )
        if committed != path.read_bytes():
            raise RuntimeError(f"working source differs from commit: {relative}")
        rows.append(binding(path, ROOT))
    return {
        "enforced": True, "sourceCommit": commit, "headAtAssembly": head,
        "allSourceBlobsMatch": True, "bindings": rows,
    }


def stable_provenance(value: Mapping[str, object]) -> dict[str, object]:
    return {
        "enforced": value["enforced"],
        "sourceCommit": value["sourceCommit"],
        "allSourceBlobsMatch": value["allSourceBlobsMatch"],
        **({"bindings": value["bindings"]} if value["enforced"] else {}),
    }


def provenance_matches(value: object, expected: Mapping[str, object]) -> bool:
    return isinstance(value, dict) and value == stable_provenance(expected)


def finite_tree(value: object) -> bool:
    if isinstance(value, dict):
        return all(finite_tree(child) for child in value.values())
    if isinstance(value, list):
        return all(finite_tree(child) for child in value)
    if isinstance(value, float):
        return math.isfinite(value)
    return True


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def main() -> int:
    args = parse_args()
    package = args.package_dir.resolve()
    config_path = args.config.resolve()
    output = package / "certificate.json"
    if args.smoke:
        if package.is_relative_to(HERE.resolve()):
            raise RuntimeError("smoke assembly must be outside the formal package")
    elif package != HERE.resolve() or config_path != (HERE / "config.json").resolve():
        raise RuntimeError("formal assembly must use canonical package and config")

    config = load_json(config_path)
    if sha256(config_path) != EXPECTED_CONFIG_SHA256:
        raise RuntimeError("canonical configuration byte contract drift")
    if (list(config.get("claimBoundary", {}).items())
            != list(EXPECTED_CLAIM_BOUNDARY.items())):
        raise RuntimeError("claim boundary key set, order, spelling, or values drifted")
    provenance = source_gate(args.source_commit, args.smoke)

    if output.exists() and not args.overwrite:
        raise RuntimeError("refusing to overwrite certificate.json")
    for name in SCIENTIFIC_INPUTS + OPERATIONAL_INPUTS:
        binding(package / name, package)

    primary = load_json(package / "primary_results.json")
    independent_linear = load_json(package / "independent_linear.json")
    independent_hierarchy = load_json(package / "independent_hierarchy.json")
    exact = load_json(package / "exact_identities.json")
    payloads = (primary, independent_linear, independent_hierarchy, exact)
    if any(row.get("smokeMode") is not args.smoke for row in payloads):
        raise RuntimeError("input mode mismatch")
    if any(row.get("allChecksPass") is not True for row in payloads):
        raise RuntimeError("an input scientific result did not pass")
    if any(row.get("claimBoundary") != config["claimBoundary"] for row in payloads):
        raise RuntimeError("input claim boundary mismatch")
    if any(not provenance_matches(row.get("sourceProvenance"), provenance)
           for row in payloads):
        raise RuntimeError("input stable source provenance mismatch")
    if not all(finite_tree(row) for row in payloads):
        raise RuntimeError("nonfinite scientific input")

    cases = primary.get("cases", [])
    if len(cases) != int(primary.get("caseCount", -1)):
        raise RuntimeError("primary case count mismatch")
    actions0 = [float(row["linear"]["finiteInviscidActionProxy"]) for row in cases]
    actions_e = [float(row["linear"]["finiteViscousAction"]) for row in cases]
    gains = [float(row["hierarchy"]["actualPhysicalLinearGain"]) for row in cases]
    prefactors = [float(row["finiteInviscidActionPrefactor"]) for row in cases]

    checks = {
        "primaryPassed": primary["allChecksPass"] is True,
        "independentLinearPassed": independent_linear["allChecksPass"] is True,
        "independentHierarchyPassed": independent_hierarchy["allChecksPass"] is True,
        "exactRationalIdentitiesPassed": exact["allChecksPass"] is True,
        "inviscidAndViscousActionsStoredUnderDistinctFields": all(
            "finiteInviscidActionProxy" in row["linear"]
            and "finiteViscousAction" in row["linear"] for row in cases
        ),
        "claimBoundaryExact": all(
            list(row["claimBoundary"].items())
            == list(EXPECTED_CLAIM_BOUNDARY.items()) for row in payloads
        ),
        "finiteScientificInputs": all(finite_tree(row) for row in payloads),
    }
    certificate = {
        "schemaVersion": "r073m-finite-certificate-v1",
        "release": "R0.73M",
        "evidenceClass": config["evidenceClass"],
        "diagnosticOnly": True,
        "smokeMode": args.smoke,
        "sourceProvenance": stable_provenance(provenance),
        "configurationBinding": binding(config_path, ROOT),
        "scientificInputBindings": [
            binding(package / name, package) for name in SCIENTIFIC_INPUTS
        ],
        "parameters": primary["parameters"],
        "caseCount": len(cases),
        "observations": {
            "finiteInviscidActionProxyRange": [min(actions0), max(actions0)],
            "finiteViscousActionRange": [min(actions_e), max(actions_e)],
            "actualPhysicalLinearGainRange": [min(gains), max(gains)],
            "finiteInviscidActionPrefactorRange": [min(prefactors), max(prefactors)],
            "primaryMaximums": primary["maximums"],
            "independentLinearMaximums": independent_linear["maximums"],
            "independentHierarchyMaximumCoefficientRelativeError": (
                independent_hierarchy["maximumCoefficientRelativeError"]
            ),
            "independentHierarchyMaximumForbiddenParityRelative": (
                independent_hierarchy["maximumForbiddenParityRelative"]
            ),
        },
        "exactIdentities": exact["identities"],
        "checks": checks,
        "allChecksPass": all(checks.values()),
        "claimBoundary": config["claimBoundary"],
        "continuumConclusion": "none; finite binary64 diagnostics only",
    }
    if not finite_tree(certificate):
        raise RuntimeError("nonfinite assembled certificate")
    atomic_json(output, certificate)
    return 0 if certificate["allChecksPass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
