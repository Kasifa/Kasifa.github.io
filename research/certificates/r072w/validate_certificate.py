#!/usr/bin/env python3
"""Fail-closed validator for a formal R0.72W certificate."""

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
    "research/r072w_report-source.md",
    "research/r072w_gap_matrix.md",
    "research/r072w_literature_audit.md",
    "research/r072w_independent_audit.md",
    "research/certificates/r072w/generate_certificate.py",
    "research/certificates/r072w/independent_recompute.py",
    "research/certificates/r072w/validate_certificate.py",
    "research/certificates/r072w/README.md",
    "research/certificates/r072w/command.txt",
    "research/certificates/r072w/environment.txt",
    "scripts/generate_r072w_figure.py",
    "scripts/generate_r072w_release.py",
    "scripts/add-r072w-translations.mjs",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/README.md",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/caption.md",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/contract.json",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/config.json",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/command.txt",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/environment.txt",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/requirements.txt",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/qa-protocol.md",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/plot.py",
    "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer/validate.py",
    "tests/r072w-deterministic-certificate-source.test.mjs",
    "tests/r072w-exact-periodic-gate.test.mjs",
    "tests/r072w-exact-tail-transfer-figure-source.test.mjs",
    "tests/r072w-release.test.mjs",
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
        "analyticExactPeriodicUnitChartTheoremProvedInBoundReport",
        "analyticTorusGraphTheoremProvedInBoundReport",
        "analyticPeriodicScalarEnergyContractionProvedInBoundReport",
        "exactPeriodicScalarTransferProved",
    }
    required_false = {
        "heatSeriesBeyondH9MachineChecked",
        "compactnessArgumentMachineChecked",
        "scalarEndpointTracePassageMachineChecked",
        "varyingCellGraphSpacePassageMachineChecked",
        "torusHMinusOneDirectSumMachineChecked",
        "nonautonomousEvolutionExistenceMachineChecked",
        "timeLengthUniformity",
        "nonlinearNavierStokesClosureProved",
        "clayMillenniumProblemSolved",
    }
    if any(boundary.get(key) is not True for key in required_true):
        raise RuntimeError("proved analytic status or finite scope is incomplete")
    if any(boundary.get(key) is not False for key in required_false):
        raise RuntimeError("claim boundary is incomplete")


def validate_exact_ledger(certificate: dict) -> None:
    if certificate.get("status") != "passed" or not all(certificate.get("exactChecks", {}).values()):
        raise RuntimeError("certificate exact checks did not all pass")
    heat = certificate.get("heatSeriesThroughH9", {})
    if heat.get("physicalCoefficientsH3H5H7H9") != ["-1/4", "1/16", "-1/160", "17/48384"]:
        raise RuntimeError("physical H3/H5/H7/H9 series drifted")
    if heat.get("scaledCoefficientsH3H5H7H9") != ["1/1", "-1/4", "1/40", "-17/12096"]:
        raise RuntimeError("scaled H3/H5/H7/H9 series drifted")
    if (
        heat.get("exactPotentialHeatIdentity") != "V_S=V_XX"
        or heat.get("chartCoefficientTimeIdentities")
        != "b_S=V_XXX and a_S=V_XXXX/2 for b=V_X and a=V_XX/2"
        or heat.get("derivativeScaling") != "V_XXX=O_T(1), V_XXXX=O_T(alpha)"
    ):
        raise RuntimeError("exact potential derivative ledger drifted")
    if set(heat.get("heatIdentityChecks", {})) != {
        "H3HeatIdentity", "H5HeatIdentity", "H7HeatIdentity", "H9HeatIdentity"
    } or not all(heat["heatIdentityChecks"].values()):
        raise RuntimeError("heat identity ledger drifted")

    probe = certificate.get("scaledProbe", {})
    if probe.get("baseMomentsAtEllOne") != {
        "mu0": "1/1", "mu2": "1/44", "mu4": "3/2288", "varianceY2": "5/6292"
    }:
        raise RuntimeError("scaled probe moments drifted")
    if probe.get("uniformFloorForEllInOneTwo") != "5/6292":
        raise RuntimeError("scaled probe floor drifted")

    common = certificate.get("commonZeroAndFiniteType", {})
    if (
        common.get("monicPolynomialGcd") != ["-1/1", "1/1"]
        or common.get("finiteTypeMatrix") != [[1, -1], [-1, 4]]
        or common.get("finiteTypeDeterminant") != 3
        or common.get("cosineSquareMinimum") != "7/16"
    ):
        raise RuntimeError("common-zero or finite-type ledger drifted")

    no_go = certificate.get("noGoAndLocalAbsorption", {})
    if (
        no_go.get("jointStrictThreshold") != "2/25"
        or no_go.get("criticalExponentsH5H7H9") != ["0/1", "-6/25", "-12/25"]
        or no_go.get("absorbableGrowingRadius") != "R=o(kappa^(2/25))"
        or no_go.get("farTranslationGraphRatios", {}).get("H5OverP0GraphPowerInL") != 2
    ):
        raise RuntimeError("no-go or absorption ledger drifted")

    partition = certificate.get("torusPartition", {})
    if (
        partition.get("chartRange") != "1<=ell<=2"
        or partition.get("finiteCellHMinusOneDirectSumConstant") != "1"
        or partition.get("integerInequalityChecked") is not True
    ):
        raise RuntimeError("torus partition ledger drifted")

    energy = certificate.get("energyBlockContraction", {})
    if (
        energy.get("rearrangedInequality") != "(T+C2)*E_plus<=C2*E_minus"
        or energy.get("squaredEnergyRatio") != "C2/(T+C2)"
        or energy.get("normRatio") != "C/sqrt(T+C^2)"
        or energy.get("coefficientCollectionChecked") is not True
    ):
        raise RuntimeError("energy contraction ledger drifted")
    validate_claim_boundary(certificate.get("claimBoundary", {}))


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
    for section in (
        "heatSeriesThroughH9",
        "scaledProbe",
        "commonZeroAndFiniteType",
        "noGoAndLocalAbsorption",
        "torusPartition",
        "energyBlockContraction",
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
    actual = sorted(
        path.name for path in ROOT.iterdir()
        if path.is_file() and path.name != "SHA256SUMS"
    )
    if names != sorted(set(names)) or names != actual:
        raise RuntimeError("SHA256SUMS must cover every flat regular file exactly once")
    print("R0.72W strict formal certificate validation: passed")


if __name__ == "__main__":
    main()
