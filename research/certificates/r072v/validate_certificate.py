#!/usr/bin/env python3
"""Strict fail-closed validation of a formal R0.72V certificate bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
FIGURE_DIRECTORY = "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization"
EXPECTED_SOURCE_FILES = (
    "research/r072v_report-source.md",
    "research/r072v_gap_matrix.md",
    "research/r072v_literature_audit.md",
    "research/r072v_independent_audit.md",
    "research/certificates/r072v/generate_certificate.py",
    "research/certificates/r072v/independent_recompute.py",
    "research/certificates/r072v/validate_certificate.py",
    "research/certificates/r072v/README.md",
    "research/certificates/r072v/command.txt",
    "research/certificates/r072v/environment.txt",
    "scripts/generate_r072v_figure.py",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/README.md",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/caption.md",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/figure-contract.md",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/contract.json",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/config.json",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/command.txt",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/environment.txt",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/requirements.txt",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/qa-protocol.md",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/plot.py",
    "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization/validate.py",
    "tests/r072v-deterministic-certificate-source.test.mjs",
    "tests/r072v-unit-chart-globalization-figure-source.test.mjs",
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


def validate_claim_boundary(boundary: dict) -> None:
    required_true = {
        "finiteExactAlgebraCertified",
        "analyticWholeLineTheoremProvedInBoundReport",
        "analyticActualSolutionObservabilityProvedInBoundReport",
        "analyticAllL2DataEnergyEvolutionProvedInBoundReport",
        "analyticEnergyBlockContractionProvedForDeclaredClass",
    }
    required_false = {
        "wholeLineFunctionalTheoremMachineChecked",
        "compactnessArgumentMachineChecked",
        "scalarEndpointTracePassageMachineChecked",
        "hMinusOneDirectSumMachineChecked",
        "nonautonomousEvolutionExistenceMachineChecked",
        "timeLengthUniformity",
        "periodicTransferProved",
        "nonlinearNavierStokesClosureProved",
        "clayMillenniumProblemSolved",
    }
    if any(boundary.get(key) is not True for key in required_true):
        raise RuntimeError("proved analytic status or finite scope is incomplete")
    if any(boundary.get(key) is not False for key in required_false):
        raise RuntimeError("claim boundary is incomplete")


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
        "mu2": "1/44",
        "mu4": "3/2288",
        "varianceY2": "5/6292",
        "definition": "mu_j=integral_{-1/2}^{1/2} y^j*q0(y) dy",
    }:
        raise RuntimeError("exact unit-chart moments drifted")

    escaping = certificate.get("escapingCoefficientLedger", {})
    if (
        escaping.get("kappaLowerFloor") != "5/6292"
        or escaping.get("ellFormula") != "ell_{alpha,beta}(t)=beta*(mu4+6*t*mu2)"
        or escaping.get("ellConstant") != "3/2288"
        or escaping.get("ellTimeSlope") != "3/22"
        or escaping.get("unitBlockAbsoluteUpperBoundL") != "315/2288"
        or escaping.get("unitBlockSufficientThreshold") != "693/2"
    ):
        raise RuntimeError("escaping-coefficient ledger drifted")

    translation = certificate.get("spatialTranslation", {})
    if (
        translation.get("quadraticCoefficientA") != "3*k"
        or translation.get("linearConstantCoefficientB") != "3*k^2+6*c"
        or translation.get("removableScalar") != "k^3+6*(c+t)*k"
        or translation.get("symbolicCoefficientMapMatches") is not True
    ):
        raise RuntimeError("spatial translation ledger drifted")

    energy = certificate.get("energyBlockContraction", {})
    if (
        energy.get("rearrangedInequality") != "(T+C2)*E_plus<=C2*E_minus"
        or energy.get("squaredEnergyRatio") != "C2/(T+C2)"
        or energy.get("normRatio") != "C/sqrt(T+C^2)"
        or energy.get("symbolicCoefficientMapMatches") is not True
    ):
        raise RuntimeError("energy-contraction algebra drifted")

    small_time = certificate.get("smallTimeBoundary", {})
    if (
        small_time.get("exactKernelSpatialScale") != "L=T^(-1/3)"
        or small_time.get("normRatioUpperOrder") != "T^(1/3)"
        or small_time.get("graphConstantLowerOrder") != "T^(-1/3)"
        or small_time.get("timeLengthUniformity") is not False
    ):
        raise RuntimeError("small-time boundary drifted")

    boundary = certificate.get("claimBoundary", {})
    validate_claim_boundary(boundary)

    if independent.get("status") != "passed":
        raise RuntimeError("independent recomputation failed")
    for section in (
        "probe",
        "moments",
        "escapingCoefficientLedger",
        "spatialTranslation",
        "energyBlockContraction",
        "smallTimeBoundary",
        "claimBoundary",
    ):
        if independent.get(section) != certificate.get(section):
            raise RuntimeError(f"independent ledger differs: {section}")

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
    print("R0.72V strict formal certificate validation: passed")


if __name__ == "__main__":
    main()
