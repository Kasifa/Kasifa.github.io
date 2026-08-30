#!/usr/bin/env python3
"""Exact rational endpoint and rate-margin identities for R0.73M."""

from __future__ import annotations

import argparse
from fractions import Fraction
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
EXPECTED_CONFIG_SHA256 = "100775fd92e34b939c563546b83b838eda60f677f7452a13459cf6ef2b2252fb"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-commit", default="")
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_gate(commit: str, smoke: bool) -> dict[str, object]:
    if smoke:
        return {"enforced": False, "sourceCommit": None, "allSourceBlobsMatch": False}
    if re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        raise RuntimeError("formal exact certificate requires a full source commit")
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
    bindings = []
    for relative in SOURCE_FILES:
        path = ROOT / relative
        committed = subprocess.check_output(
            ["git", "-C", str(ROOT), "show", f"{commit}:{relative}"],
        )
        if committed != path.read_bytes():
            raise RuntimeError(f"working source differs from source commit: {relative}")
        bindings.append({
            "path": relative,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    return {
        "enforced": True,
        "sourceCommit": commit,
        "headAtRun": head,
        "allSourceBlobsMatch": True,
        "bindings": bindings,
    }


def canonical_fraction(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def parse_fraction(value: object) -> Fraction:
    if not isinstance(value, str) or re.fullmatch(r"-?[0-9]+/[1-9][0-9]*", value) is None:
        raise RuntimeError(f"noncanonical configured fraction: {value!r}")
    numerator, denominator = value.split("/")
    parsed = Fraction(int(numerator), int(denominator))
    if canonical_fraction(parsed) != value:
        raise RuntimeError(f"configured fraction is not reduced: {value}")
    return parsed


def main() -> int:
    args = parse_args()
    output = args.output.resolve()
    if args.smoke:
        if output.is_relative_to(HERE.resolve()):
            raise RuntimeError("smoke exact output must be outside the formal package")
    elif (output != (HERE / "exact_identities.json").resolve()
          or args.config.resolve() != (HERE / "config.json").resolve()):
        raise RuntimeError("formal exact run must use canonical output and config")
    if output.exists() and not args.overwrite:
        raise RuntimeError("refusing to overwrite exact output")
    config = json.loads(args.config.read_text(encoding="utf-8"))
    if sha256(args.config.resolve()) != EXPECTED_CONFIG_SHA256:
        raise RuntimeError("canonical configuration byte contract drift")
    if config.get("schemaVersion") != "r073m-prescribed-action-finite-config-v1":
        raise RuntimeError("configuration schema mismatch")
    if not (config.get("release") == "R0.73M"
            and config.get("diagnosticOnly") is True
            and config.get("profileTimeEnd") == 1.0 / 450.0
            and config.get("physicalTimeEnd") == 1.0 / 1800.0
            and config.get("profileToPhysicalTimeRule") == "d=4t"):
        raise RuntimeError("endpoint or evidence contract drift")
    if (list(config.get("claimBoundary", {}).items())
            != list(EXPECTED_CLAIM_BOUNDARY.items())):
        raise RuntimeError("claim boundary key set, order, spelling, or values drifted")
    provenance = source_gate(args.source_commit, args.smoke)

    d_star = Fraction(1, 450)
    t_star = d_star / 4
    mu_star = Fraction(167, 1000)
    identities = {
        "profileTimeEnd": {
            "left": canonical_fraction(d_star),
            "right": "1/450",
            "equal": d_star == Fraction(1, 450),
        },
        "physicalTimeEnd": {
            "left": canonical_fraction(t_star),
            "right": "1/1800",
            "equal": t_star == Fraction(1, 1800),
        },
        "twoRateMargin": {
            "left": canonical_fraction(2 * mu_star - Fraction(1, 3)),
            "right": "1/1500",
            "equal": 2 * mu_star - Fraction(1, 3) == Fraction(1, 1500),
        },
        "threeRateMargin": {
            "left": canonical_fraction(3 * mu_star - Fraction(1, 2)),
            "right": "1/1000",
            "equal": 3 * mu_star - Fraction(1, 2) == Fraction(1, 1000),
        },
        "fourRateMargin": {
            "left": canonical_fraction(4 * mu_star - Fraction(1, 2)),
            "right": "21/125",
            "equal": 4 * mu_star - Fraction(1, 2) == Fraction(21, 125),
        },
    }
    expected_config = {
        "profileTimeEnd": d_star,
        "physicalTimeEnd": t_star,
        "muStar": mu_star,
        "twoRateMargin": 2 * mu_star - Fraction(1, 3),
        "threeRateMargin": 3 * mu_star - Fraction(1, 2),
        "fourRateMargin": 4 * mu_star - Fraction(1, 2),
    }
    configured = {
        key: parse_fraction(value)
        for key, value in config.get("exactRationals", {}).items()
    }
    checks = {
        "allFractionIdentitiesExact": all(row["equal"] for row in identities.values()),
        "configuredExactRationalsMatchIndependentFractions": configured == expected_config,
        "configuredProfileTimeMatchesExact": (
            float(config["profileTimeEnd"]) == float(d_star)
        ),
        "configuredPhysicalTimeMatchesExact": (
            float(config["physicalTimeEnd"]) == float(t_star)
        ),
        "configuredRuleIsDEqualsFourT": config["profileToPhysicalTimeRule"] == "d=4t",
        "claimBoundaryExact": (
            list(config["claimBoundary"].items())
            == list(EXPECTED_CLAIM_BOUNDARY.items())
        ),
    }
    result = {
        "schemaVersion": "r073m-exact-rational-identities-v1",
        "release": "R0.73M",
        "smokeMode": args.smoke,
        "arithmetic": "fractions.Fraction; no floating-point identity reconstruction",
        "sourceProvenance": {
            "enforced": provenance["enforced"],
            "sourceCommit": provenance["sourceCommit"],
            "allSourceBlobsMatch": provenance["allSourceBlobsMatch"],
            **({"bindings": provenance["bindings"]} if provenance["enforced"] else {}),
        },
        "configurationBinding": {
            "path": str(args.config.resolve().relative_to(ROOT.resolve())),
            "bytes": args.config.stat().st_size,
            "sha256": sha256(args.config),
        },
        "identities": identities,
        "checks": checks,
        "allChecksPass": all(checks.values()),
        "claimBoundary": config["claimBoundary"],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(f".{output.name}.tmp")
    temporary.write_text(
        json.dumps(result, indent=2, sort_keys=False, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, output)
    return 0 if result["allChecksPass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
