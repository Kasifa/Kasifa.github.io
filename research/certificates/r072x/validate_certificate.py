#!/usr/bin/env python3
"""Strict fail-closed validator for a formal R0.72X certificate bundle."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
FIGURE_DIRECTORY = "figures/r072x-all-center/fig-r072x-all-center-transfer"
EXPECTED_SOURCE_FILES = (
    "research/r072x_report-source.md",
    "research/r072x_gap_matrix.md",
    "research/r072x_literature_audit.md",
    "research/r072x_independent_audit.md",
    "research/certificates/r072x/generate_certificate.py",
    "research/certificates/r072x/independent_recompute.py",
    "research/certificates/r072x/validate_certificate.py",
    "research/certificates/r072x/README.md",
    "research/certificates/r072x/command.txt",
    "research/certificates/r072x/environment.txt",
    "scripts/generate_r072x_figure.py",
    "scripts/generate_r072x_release.py",
    "scripts/add-r072x-translations.mjs",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/README.md",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/caption.md",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/contract.json",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/config.json",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/command.txt",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/environment.txt",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/requirements.txt",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/qa-protocol.md",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/plot.py",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/validate.py",
    "tests/r072x-deterministic-certificate-source.test.mjs",
    "tests/r072x-exact-path-gate.test.mjs",
    "tests/r072x-all-center-figure-source.test.mjs",
    "tests/r072x-release.test.mjs",
)
COMPARED_SECTIONS = (
    "commonZeroAndLocalJet",
    "shrinkingInterfacePowers",
    "blockTilingAndIntegratedEnergy",
    "blochTwist",
    "scalarDamping",
    "zeroCouplingCounterexample",
    "claimBoundary",
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
    commit = str(manifest.get("sourceCommit", ""))
    bindings = manifest.get("sourceBindings")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise RuntimeError("formal source commit is missing")
    if not isinstance(bindings, list) or not bindings or bindings != crosscheck.get("sourceBindings"):
        raise RuntimeError("formal source bindings are missing or inconsistent")
    if [record.get("path") for record in bindings] != list(EXPECTED_SOURCE_FILES):
        raise RuntimeError("formal source bindings do not cover the complete frozen source set")
    if crosscheck.get("sourceCommit") != commit or crosscheck.get("formalSourceReady") is not True:
        raise RuntimeError("crosscheck source lineage is inconsistent")
    if subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
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
            or record.get("commit") != commit
        ):
            raise RuntimeError("malformed or duplicate source binding")
        seen.add(relative)
        path = (REPOSITORY / relative).resolve()
        if REPOSITORY.resolve() not in path.parents or not path.is_file() or path.is_symlink():
            raise RuntimeError(f"bound source is absent, linked, or escapes repository: {relative}")
        committed_blob = subprocess.check_output(
            ["git", "rev-parse", f"{commit}:{relative}"],
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
        "analyticAllCenterExactFamilyGraphCoercivityProvedInBoundReport",
        "analyticAllStartExactPathSemigroupProvedInBoundReport",
        "analyticAllStartIntegratedA2ScaleProvedInBoundReport",
        "analyticUniformTwistedPeriodicGraphProvedInBoundReport",
        "analyticStrongRowDirectSumNoCountLossProvedInBoundReport",
        "analyticFixedMarginA1EnhancedDissipationImportedInBoundReport",
        "analyticPeriodicRepresentativeA1A2A1ConcatenationProvedInBoundReport",
    }
    required_false = {
        "compactnessArgumentMachineChecked",
        "boundedCenterGraphLimitMachineChecked",
        "scalarEndpointTracePassageMachineChecked",
        "twistedHMinusOneDirectSumMachineChecked",
        "nonautonomousEvolutionExistenceMachineChecked",
        "cobleHeTheoremMachineChecked",
        "cobleHeApplicationHypothesesMachineChecked",
        "endpointIntegrationByPartsMachineChecked",
        "shrinkingInterfaceFixedShapeA1Hypotheses",
        "prefactorOneAllGapExponential",
        "blochUniformFastA1ConcatenationProved",
        "allPhysicalRowsUniformContraction",
        "forcedHMinusOneTransferProved",
        "completeLinearizedShearSubsystemProved",
        "nonlinearNavierStokesClosureProved",
        "clayMillenniumProblemSolved",
    }
    if set(boundary) != required_true | required_false:
        raise RuntimeError("claim boundary key set drifted")
    if any(boundary.get(key) is not True for key in required_true):
        raise RuntimeError("bound-report analytic status or finite scope is incomplete")
    if any(boundary.get(key) is not False for key in required_false):
        raise RuntimeError("claim boundary is incomplete")


def validate_exact_ledger(certificate: dict) -> None:
    if certificate.get("schemaVersion") != 1:
        raise RuntimeError("unsupported certificate schema")
    if certificate.get("theoremId") != "R0.72X-all-center-outer-time-finite-ledger":
        raise RuntimeError("theorem id drifted")
    checks = certificate.get("exactChecks", {})
    if certificate.get("status") != "passed" or not checks or not all(checks.values()):
        raise RuntimeError("certificate exact checks did not all pass")

    common = certificate.get("commonZeroAndLocalJet", {})
    if (
        common.get("branchEliminationChecked") is not True
        or common.get("onlyCommonZero") != "D=0 and theta=0 mod 2*pi"
    ):
        raise RuntimeError("common-zero conclusion drifted")
    if common.get("nonzeroSineBranch", {}).get("realSolutionExists") is not False:
        raise RuntimeError("nonzero-sine branch is not excluded")
    if common.get("sineZeroBranch", {}).get("selected") != "r=1, cos(theta)=1":
        raise RuntimeError("sine-zero branch drifted")
    if common.get("jacobianAtOrigin") != [["3/1", "0/1"], ["0/1", "3/1"]]:
        raise RuntimeError("Jacobian is not diag(3,3)")
    if common.get("jacobianDeterminant") != "9/1":
        raise RuntimeError("Jacobian determinant drifted")
    if common.get("fJetThroughTotalDegreeThree") != {
        "D": "3/1",
        "D^2": "-15/2",
        "theta^2": "3/2",
        "D^3": "21/2",
        "D*theta^2": "-15/2",
    }:
        raise RuntimeError("f jet coefficients drifted")
    if common.get("gJetThroughTotalDegreeThree") != {
        "theta": "3/1",
        "D*theta": "-15/1",
        "D^2*theta": "63/2",
        "theta^3": "-5/2",
    }:
        raise RuntimeError("g jet coefficients drifted")

    interface = certificate.get("shrinkingInterfacePowers", {})
    if interface.get("alphaPowers") != {
        "epsilon_c": "-5/1",
        "h_alpha": "2/1",
        "preCriticalPointHalfSeparation": "1/1",
        "preMorseCurvatureFloor": "1/1",
        "postAwayGradientFloor": "2/1",
        "preA1DiagnosticRate": "-2/1",
        "postMonotoneDiagnosticRate": "-2/1",
        "exactFamilyCollisionRate": "-2/1",
    }:
        raise RuntimeError("alpha interface powers drifted")
    if interface.get("kappaPowers", {}).get("matchedRate") != "2/5":
        raise RuntimeError("kappa collision-rate power drifted")
    if interface.get("postGradientLedger", {}).get("hCoefficientsThroughTwo") != ["-3/2", "15/4"]:
        raise RuntimeError("post-interface gradient coefficients drifted")
    if interface.get("fixedShapeA1UniformAtShrinkingInterface") is not False:
        raise RuntimeError("shrinking-interface A1 no-go drifted")

    tiling = certificate.get("blockTilingAndIntegratedEnergy", {})
    if (
        tiling.get("fullBlockCount") != "N=floor(L/(2*T*alpha^2))"
        or tiling.get("floorInequality") != "floor(z)>=z-1"
        or tiling.get("finiteRationalFloorGridChecked") is not True
        or tiling.get("finiteGeometricTelescopingChecked") is not True
        or tiling.get("prefactorOneAllGapExponential") is not False
        or tiling.get("physicalIntegratedEnergyBound")
        != "2*T*alpha^2/(1-q^2)*E(d_1)"
        or tiling.get("forcedHMinusOneTransferInferred") is not False
    ):
        raise RuntimeError("block-floor, prefactor, or geometric ledger drifted")
    if tiling.get("shortGapCounterexample", {}).get("fullBlockCount") != 0:
        raise RuntimeError("short-gap counterexample drifted")

    bloch = certificate.get("blochTwist", {})
    if (
        bloch.get("boundaryPhaseExponent") != "alpha*beta*L_alpha=2*pi*beta"
        or bloch.get("alphaPowerInBoundaryPhase") != "0/1"
        or bloch.get("twistedBoundary")
        != "w(X+L_alpha)=exp(2*pi*i*beta)*w(X)"
        or bloch.get("endpointIntegrationByPartsCancellationMachineChecked") is not False
    ):
        raise RuntimeError("Bloch twist ledger drifted")

    damping = certificate.get("scalarDamping", {})
    if (
        damping.get("normDampingFactor") != "exp(-mu*L)"
        or damping.get("squaredEnergyDampingFactor") != "exp(-2*mu*L)"
        or damping.get("normBlockFactor") != "exp(-mu*L)*q^N"
        or damping.get("squaredEnergyBlockFactor") != "exp(-2*mu*L)*q^(2*N)"
        or damping.get("energyExponentToNormExponent") != 2
    ):
        raise RuntimeError("scalar damping norm/energy ledger drifted")

    zero = certificate.get("zeroCouplingCounterexample", {})
    if (
        zero.get("effectiveCouplingFormula") != "epsilon_j=2*|delta*K_z,j|*a/R^2"
        or zero.get("rowParameters")
        != {"K_z": "0", "epsilon_j": "0", "beta": "0", "mu": "0"}
        or zero.get("laplacian") != "partial_x^2 G=0"
        or zero.get("timeDerivative") != "partial_d G=0"
        or zero.get("normalizedSquaredNorm") != "1"
        or zero.get("constantEquationChecked") is not True
        or zero.get("strictContraction") is not False
    ):
        raise RuntimeError("zero-coupling constant counterexample drifted")
    validate_claim_boundary(certificate.get("claimBoundary", {}))


def validate_hash_ledger() -> None:
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
    actual = sorted(
        path.name for path in ROOT.iterdir()
        if path.is_file() and path.name != "SHA256SUMS"
    )
    if names != sorted(set(names)) or names != actual:
        raise RuntimeError("SHA256SUMS must cover every flat regular file exactly once")


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
    validate_exact_ledger(certificate)
    if manifest.get("claimBoundary") != certificate.get("claimBoundary"):
        raise RuntimeError("manifest claim boundary drift")

    if independent.get("status") != "passed":
        raise RuntimeError("independent recomputation failed")
    for section in COMPARED_SECTIONS:
        if independent.get(section) != certificate.get(section):
            raise RuntimeError(f"independent ledger differs: {section}")

    if (
        crosscheck.get("status") != "passed"
        or crosscheck.get("temporaryUnsealedSourceAllowed") is not False
        or crosscheck.get("certificateSha256") != digest(ROOT / "certificate.json")
        or crosscheck.get("comparedSections") != list(COMPARED_SECTIONS)
        or not all(crosscheck.get("checks", {}).values())
    ):
        raise RuntimeError("crosscheck is stale or incomplete")

    for name in ("certificate.json", "independent.json", "crosscheck.json"):
        record = manifest.get("files", {}).get(name, {})
        path = ROOT / name
        if record.get("sha256") != digest(path) or record.get("bytes") != path.stat().st_size:
            raise RuntimeError(f"manifest drift: {name}")

    validate_hash_ledger()
    print("R0.72X strict formal certificate validation: passed")


if __name__ == "__main__":
    main()
