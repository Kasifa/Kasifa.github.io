#!/usr/bin/env python3
"""Strict fail-closed validation of the generated R0.72T certificate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import argparse
import re
import subprocess


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]


def load(name: str) -> dict:
    value = json.loads((ROOT / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"{name} is not an object")
    return value


def digest(name: str) -> str:
    return hashlib.sha256((ROOT / name).read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-formal", action="store_true")
    args = parser.parse_args()
    certificate = load("certificate.json")
    crosscheck = load("crosscheck.json")
    manifest = load("manifest.json")
    if args.require_formal:
        if manifest.get("status") != "formal" or not re.fullmatch(r"[0-9a-f]{40}", str(manifest.get("sourceCommit", ""))):
            raise RuntimeError("formal certificate manifest required")
        if crosscheck.get("formalSourceReady") is not True or crosscheck.get("sourceCommit") != manifest.get("sourceCommit"):
            raise RuntimeError("formal source lineage is missing")
        if not manifest.get("sourceBindings") or manifest.get("sourceBindings") != crosscheck.get("sourceBindings"):
            raise RuntimeError("formal source bindings are missing or inconsistent")
        source_commit = manifest["sourceCommit"]
        seen = set()
        for record in manifest["sourceBindings"]:
            relative = record.get("path")
            if (
                not isinstance(relative, str) or relative.startswith("/")
                or ".." in Path(relative).parts or relative in seen
                or record.get("commit") != source_commit
            ):
                raise RuntimeError("malformed or duplicate formal source binding")
            seen.add(relative)
            path = (REPOSITORY / relative).resolve()
            if REPOSITORY.resolve() not in path.parents or not path.is_file():
                raise RuntimeError(f"bound source is absent or escapes repository: {relative}")
            committed_blob = subprocess.check_output(
                ["git", "rev-parse", f"{source_commit}:{relative}"],
                cwd=REPOSITORY, text=True, stderr=subprocess.DEVNULL,
            ).strip()
            working_blob = subprocess.check_output(
                ["git", "hash-object", f"--path={relative}", str(path)],
                cwd=REPOSITORY, text=True,
            ).strip()
            if (
                record.get("gitBlob") != committed_blob
                or working_blob != committed_blob
                or record.get("sha256") != hashlib.sha256(path.read_bytes()).hexdigest()
                or record.get("bytes") != path.stat().st_size
                or record.get("workingTreeBlobMatches") is not True
            ):
                raise RuntimeError(f"formal source binding drift: {relative}")
    if certificate.get("status") != "passed" or not all(certificate.get("exactChecks", {}).values()):
        raise RuntimeError("certificate did not pass every exact check")
    if certificate["heatProfile"]["collisionTaylor"] != {
        "x": "0/1", "x^3": "-1/4", "x^5": "1/16", "x^7": "-1/160"
    }:
        raise RuntimeError("heat-profile Taylor ledger drifted")
    if certificate["scaling"]["solution"] != {
        "alpha": "-3/5", "beta": "-2/5", "gamma": "1/5", "delta": "-1/5"
    }:
        raise RuntimeError("unique exponent balance drifted")
    calibration = certificate["driftOnlyCalibration"]
    if calibration.get("minimumAction") != "q^2*(m^2*h^3/12+h^5/720)":
        raise RuntimeError("drift action drifted")
    if calibration.get("qZeroNorm") != "1/1":
        raise RuntimeError("q=0 norm must remain one")
    if certificate["heatProfile"]["translation"] != {
        "hSquared": "-2*d", "differentiatedIdentity": "h*hPrime=-1", "hPrime": "-1/h"
    }:
        raise RuntimeError("translation identity drifted")
    combined = certificate["combinedFixedFunctionMagneticForm"]
    if combined["moments"] != {
        "integral_r_squared_coefficient": "1/12",
        "integral_centered_r_squared_squared_coefficient": "1/180",
        "after_multiplying_by_(a/2)^2": "1/720",
        "oddCross": "0/1",
    } or combined.get("M") != "M(X)=a*c+3*b*X^2" or combined.get("A_av") != "A_av=a*T^2/24" or combined.get("identityOnlyNotEvolvingSolutionObservability") is not True or combined.get("blockContractionProved") is not False or "T||D_av f||_2^2" not in combined.get("fixedFunctionIdentity", "") or "integral_R" not in combined.get("fixedFunctionIdentity", ""):
        raise RuntimeError("combined fixed-forcing moment identity drifted")
    bracket = certificate["cubicBracketCalibration"]
    if bracket["vectorFields"] != {
        "X1": "partial_X",
        "X0": "partial_S-(X^3+6*S*X)*partial_theta",
    } or bracket["brackets"][:4] != [
        "[X1,X0]=-(3*X^2+6*S)*partial_theta",
        "[X0,[X1,X0]]=-6*partial_theta",
        "[X1,[X1,X0]]=-6*X*partial_theta",
        "[X1,[X1,[X1,X0]]]=-6*partial_theta",
    ]:
        raise RuntimeError("mixed bracket drifted")
    boundary = certificate["claimBoundary"]
    required_false = {
        "blockContractionProved", "periodicTransferProved", "allStartSemigroupEstimateProved",
        "combinedCubicAndTimeDriftEstimateProved", "clayMillenniumProblemSolved",
    }
    if boundary.get("fixedFormulaIdentityOnly") is not True or any(boundary.get(key) is not False for key in required_false):
        raise RuntimeError("claim boundary is incomplete")
    if crosscheck.get("status") != "passed" or crosscheck.get("certificateSha256") != digest("certificate.json"):
        raise RuntimeError("crosscheck is stale")
    if not all(crosscheck.get("checks", {}).values()):
        raise RuntimeError("crosscheck failed")
    for name in ("certificate.json", "independent.json", "crosscheck.json"):
        record = manifest.get("files", {}).get(name, {})
        if record.get("sha256") != digest(name) or record.get("bytes") != (ROOT / name).stat().st_size:
            raise RuntimeError(f"manifest drift: {name}")
    if manifest.get("deterministic") is not True:
        raise RuntimeError("manifest must declare deterministic generation")
    rows = (ROOT / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    names = []
    for row in rows:
        expected, name = row.split("  ", 1)
        if expected != digest(name):
            raise RuntimeError(f"SHA256SUMS drift: {name}")
        names.append(name)
    actual = sorted(path.name for path in ROOT.iterdir() if path.is_file() and path.name != "SHA256SUMS")
    if names != actual:
        raise RuntimeError("SHA256SUMS is not a complete sorted flat ledger")
    print("R0.72T strict certificate validation: passed")


if __name__ == "__main__":
    main()
