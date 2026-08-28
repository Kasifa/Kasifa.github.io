#!/usr/bin/env python3
"""Strict fail-closed validation of a formal R0.72U certificate bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
EXPECTED_SOURCE_FILES = (
    "research/r072u_report-source.md",
    "research/r072u_gap_matrix.md",
    "research/r072u_independent_audit.md",
    "research/r072u_literature_audit.md",
    "research/certificates/r072u/generate_certificate.py",
    "research/certificates/r072u/independent_recompute.py",
    "research/certificates/r072u/validate_certificate.py",
    "research/certificates/r072u/README.md",
    "research/certificates/r072u/command.txt",
    "research/certificates/r072u/environment.txt",
    "scripts/generate_r072u_figure.py",
    "figures/r072u-local-observability/fig-r072u-two-moment-coercivity/README.md",
    "figures/r072u-local-observability/fig-r072u-two-moment-coercivity/caption.md",
    "figures/r072u-local-observability/fig-r072u-two-moment-coercivity/figure-contract.md",
    "figures/r072u-local-observability/fig-r072u-two-moment-coercivity/contract.json",
    "figures/r072u-local-observability/fig-r072u-two-moment-coercivity/config.json",
    "figures/r072u-local-observability/fig-r072u-two-moment-coercivity/command.txt",
    "figures/r072u-local-observability/fig-r072u-two-moment-coercivity/environment.txt",
    "figures/r072u-local-observability/fig-r072u-two-moment-coercivity/requirements.txt",
    "figures/r072u-local-observability/fig-r072u-two-moment-coercivity/qa-protocol.md",
    "figures/r072u-local-observability/fig-r072u-two-moment-coercivity/plot.py",
    "figures/r072u-local-observability/fig-r072u-two-moment-coercivity/validate.py",
    "tests/r072u-deterministic-certificate-source.test.mjs",
    "tests/r072u-two-moment-figure-source.test.mjs",
)


def load(name: str) -> dict:
    path = ROOT / name
    if not path.is_file() or path.is_symlink():
        raise RuntimeError(f"required regular file is absent: {name}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"{name} is not a JSON object")
    return value


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_source_bindings(manifest: dict, crosscheck: dict) -> None:
    source_commit = str(manifest.get("sourceCommit", ""))
    bindings = manifest.get("sourceBindings")
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise RuntimeError("formal source commit is missing")
    if not isinstance(bindings, list) or not bindings or bindings != crosscheck.get("sourceBindings"):
        raise RuntimeError("formal source bindings are missing or inconsistent")
    if [record.get("path") for record in bindings] != list(EXPECTED_SOURCE_FILES):
        raise RuntimeError("formal source bindings do not cover the complete frozen source set")
    if crosscheck.get("sourceCommit") != source_commit or crosscheck.get("formalSourceReady") is not True:
        raise RuntimeError("crosscheck source lineage is inconsistent")
    if subprocess.run(
        ["git", "cat-file", "-e", f"{source_commit}^{{commit}}"],
        cwd=REPOSITORY,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode:
        raise RuntimeError("sourceCommit is not a valid Git commit")

    seen: set[str] = set()
    for record in bindings:
        relative = record.get("path")
        if (
            not isinstance(relative, str)
            or relative.startswith("/")
            or ".." in Path(relative).parts
            or relative in seen
            or record.get("commit") != source_commit
        ):
            raise RuntimeError("malformed or duplicate source binding")
        seen.add(relative)
        path = (REPOSITORY / relative).resolve()
        if REPOSITORY.resolve() not in path.parents or not path.is_file() or path.is_symlink():
            raise RuntimeError(f"bound source is absent, linked, or escapes repository: {relative}")
        committed_blob = subprocess.check_output(
            ["git", "rev-parse", f"{source_commit}:{relative}"],
            cwd=REPOSITORY,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        working_blob = subprocess.check_output(
            ["git", "hash-object", f"--path={relative}", str(path)],
            cwd=REPOSITORY,
            text=True,
        ).strip()
        if (
            record.get("gitBlob") != committed_blob
            or working_blob != committed_blob
            or record.get("sha256") != digest(path)
            or record.get("bytes") != path.stat().st_size
            or record.get("workingTreeBlobMatches") is not True
        ):
            raise RuntimeError(f"formal source binding drift: {relative}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-formal", action="store_true")
    args = parser.parse_args()
    if not args.require_formal:
        parser.error("strict validation requires --require-formal")

    certificate = load("certificate.json")
    independent = load("independent.json")
    crosscheck = load("crosscheck.json")
    manifest = load("manifest.json")
    if manifest.get("status") != "formal" or manifest.get("deterministic") is not True:
        raise RuntimeError("formal deterministic manifest required")
    validate_source_bindings(manifest, crosscheck)

    if certificate.get("status") != "passed" or not all(certificate.get("exactChecks", {}).values()):
        raise RuntimeError("certificate exact checks did not all pass")
    if certificate.get("moments") != {
        "mu0": "1/1",
        "mu2": "1/11",
        "mu4": "3/143",
        "definition": "mu_j=integral_{-1}^{1} X^j*rho(X) dX",
    }:
        raise RuntimeError("exact probe moments drifted")
    large = certificate.get("twoMomentLargeCenter", {})
    if (
        large.get("coefficient") != "K_c(s)=3/143+6*(c+s)/11"
        or large.get("threshold") != "27/13"
        or large.get("thresholdFloor") != "81/143"
        or large.get("positiveThresholdMinimum") != "87/143"
        or large.get("negativeThresholdMaximum") != "-81/143"
    ):
        raise RuntimeError("large-centre moment ledger drifted")
    gauge = certificate.get("fixedGaugeInviscidCalibration", {})
    if gauge.get("unitBlockFloor") != "4/5" or gauge.get("isViscousContraction") is not False:
        raise RuntimeError("fixed-gauge calibration drifted")

    boundary = certificate.get("claimBoundary", {})
    required_false = {
        "boundedChartFunctionalAnalysisMachineChecked",
        "wholeLineBlockContractionProved",
        "periodicTransferProved",
        "nonlinearNavierStokesClosureProved",
        "clayMillenniumProblemSolved",
    }
    if any(boundary.get(key) is not False for key in required_false):
        raise RuntimeError("claim boundary is incomplete")

    if independent.get("status") != "passed":
        raise RuntimeError("independent recomputation failed")
    if independent.get("moments") != certificate["moments"]:
        raise RuntimeError("independent moment ledger differs")
    if independent.get("twoMomentLargeCenter") != certificate["twoMomentLargeCenter"]:
        raise RuntimeError("independent large-centre ledger differs")
    if independent.get("fixedGaugeInviscidCalibration") != certificate["fixedGaugeInviscidCalibration"]:
        raise RuntimeError("independent fixed-gauge ledger differs")
    if independent.get("claimBoundary") != boundary:
        raise RuntimeError("independent claim boundary differs")

    if (
        crosscheck.get("status") != "passed"
        or crosscheck.get("temporaryUnsealedSourceAllowed") is not False
        or crosscheck.get("certificateSha256") != digest(ROOT / "certificate.json")
        or not all(crosscheck.get("checks", {}).values())
    ):
        raise RuntimeError("crosscheck is stale or incomplete")

    for name in ("certificate.json", "independent.json", "crosscheck.json"):
        record = manifest.get("files", {}).get(name, {})
        path = ROOT / name
        if record.get("sha256") != digest(path) or record.get("bytes") != path.stat().st_size:
            raise RuntimeError(f"manifest drift: {name}")

    ledger = ROOT / "SHA256SUMS"
    if not ledger.is_file() or ledger.is_symlink():
        raise RuntimeError("flat SHA256SUMS ledger is absent")
    names: list[str] = []
    for row in ledger.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/\\\r\n]+)", row)
        if not match:
            raise RuntimeError(f"malformed SHA256SUMS row: {row}")
        expected, name = match.groups()
        path = ROOT / name
        if not path.is_file() or path.is_symlink() or digest(path) != expected:
            raise RuntimeError(f"SHA256SUMS drift: {name}")
        names.append(name)
    actual = sorted(path.name for path in ROOT.iterdir() if path.is_file() and path.name != "SHA256SUMS")
    if names != sorted(set(names)) or names != actual:
        raise RuntimeError("SHA256SUMS must cover every flat regular file exactly once")
    print("R0.72U strict formal certificate validation: passed")


if __name__ == "__main__":
    main()
