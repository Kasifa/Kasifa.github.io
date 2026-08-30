#!/usr/bin/env python3
"""Seal the R0.73M source/results package with an exact flat inventory."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess


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
GENERATED_FILES = (
    "primary_results.json", "primary_rows.csv", "action_nodes.csv",
    "cutoff_convergence.csv", "step_convergence.csv",
    "coefficient_endpoints.npz", "primary_environment.json",
    "primary_progress.ndjson", "primary_resources.ndjson", "primary_manifest.json",
    "independent_linear.json", "independent_linear_progress.ndjson",
    "independent_linear_resources.ndjson", "independent_hierarchy.json",
    "independent_hierarchy_progress.ndjson",
    "independent_hierarchy_resources.ndjson", "exact_identities.json",
    "certificate.json", "validation.json",
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


def no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
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
        return {"enforced": False, "sourceCommit": None,
                "allSourceBlobsMatch": False, "bindings": []}
    if re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        raise RuntimeError("formal seal requires a full lowercase source commit")
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
            raise RuntimeError(f"working source differs from source commit: {relative}")
        rows.append(binding(path, ROOT))
    return {
        "enforced": True, "sourceCommit": commit, "headAtSeal": head,
        "allSourceBlobsMatch": True, "bindings": rows,
    }


def stable_provenance(value: dict[str, object]) -> dict[str, object]:
    return {
        "enforced": value["enforced"], "sourceCommit": value["sourceCommit"],
        "allSourceBlobsMatch": value["allSourceBlobsMatch"],
        **({"bindings": value["bindings"]} if value["enforced"] else {}),
    }


def main() -> int:
    args = parse_args()
    package = args.package_dir.resolve()
    config_path = args.config.resolve()
    if args.smoke:
        if package.is_relative_to(HERE.resolve()):
            raise RuntimeError("smoke seal must be outside the formal package")
    elif package != HERE.resolve() or config_path != (HERE / "config.json").resolve():
        raise RuntimeError("formal seal must use canonical package and config")
    if sha256(config_path) != EXPECTED_CONFIG_SHA256:
        raise RuntimeError("canonical configuration byte contract drift")
    config = load_json(config_path)
    if (list(config.get("claimBoundary", {}).items())
            != list(EXPECTED_CLAIM_BOUNDARY.items())):
        raise RuntimeError("claim boundary key set, order, spelling, or values drifted")
    provenance = source_gate(args.source_commit, args.smoke)

    expected = set(GENERATED_FILES if args.smoke
                   else PACKAGE_SOURCE_FILES + GENERATED_FILES)
    manifest_path = package / "manifest.json"
    sums_path = package / "SHA256SUMS"
    if (manifest_path.exists() or sums_path.exists()) and not args.overwrite:
        raise RuntimeError("refusing to overwrite existing package seal")
    for name in expected:
        binding(package / name, package)
    allowed = expected | ({"manifest.json", "SHA256SUMS"} if args.overwrite else set())
    actual_entries = {path.name for path in package.iterdir()}
    if actual_entries != allowed:
        raise RuntimeError(
            "package inventory mismatch before seal; "
            f"missing={sorted(expected - actual_entries)}, "
            f"extra={sorted(actual_entries - allowed)}"
        )

    certificate = load_json(package / "certificate.json")
    validation = load_json(package / "validation.json")
    prerequisites = (
        certificate.get("allChecksPass") is True
        and validation.get("allChecksPass") is True
        and certificate.get("smokeMode") is args.smoke
        and validation.get("smokeMode") is args.smoke
        and certificate.get("sourceProvenance") == stable_provenance(provenance)
        and validation.get("sourceProvenance") == stable_provenance(provenance)
        and certificate.get("claimBoundary") == config["claimBoundary"]
        and validation.get("claimBoundary") == config["claimBoundary"]
    )
    if not prerequisites:
        raise RuntimeError("certificate or validation prerequisite failed")

    manifest = {
        "schemaVersion": "r073m-sealed-package-manifest-v1",
        "release": "R0.73M",
        "smokeMode": args.smoke,
        "sourceCommit": None if args.smoke else args.source_commit,
        "sourceBindings": provenance["bindings"],
        "inventory": {
            "sourceFileCount": 0 if args.smoke else len(PACKAGE_SOURCE_FILES),
            "generatedFileCount": len(GENERATED_FILES),
            "manifestBoundFileCount": len(expected),
            "sha256SumsLineCount": len(expected) + 1,
        },
        "files": [binding(package / name, package) for name in sorted(expected)],
        "allPrerequisiteChecksPass": True,
        "claimBoundary": config["claimBoundary"],
    }
    manifest_temporary = package / ".manifest.json.tmp"
    sums_temporary = package / ".SHA256SUMS.tmp"
    manifest_temporary.write_text(
        json.dumps(manifest, indent=2, sort_keys=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    rows = [f"{sha256(package / name)}  {name}" for name in sorted(expected)]
    rows.append(f"{sha256(manifest_temporary)}  manifest.json")
    rows.sort(key=lambda row: row.split("  ", 1)[1])
    sums_temporary.write_text("\n".join(rows) + "\n", encoding="ascii")
    os.replace(manifest_temporary, manifest_path)
    os.replace(sums_temporary, sums_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
