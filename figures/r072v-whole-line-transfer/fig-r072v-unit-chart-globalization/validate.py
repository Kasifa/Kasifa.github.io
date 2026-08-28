#!/usr/bin/env python3
"""Strict fail-closed validation of a formal R0.72V figure package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
CERTIFICATE_ROOT = REPOSITORY / "research/certificates/r072v"
FIGURE_ID = "fig-r072v-unit-chart-globalization"
GENERATED = {
    "data.csv",
    "results.json",
    "validation.json",
    "progress.ndjson",
    "resource-log.ndjson",
    "qa-report.md",
    "figure.svg",
    "figure.pdf",
    "figure.png",
    "qa-final-size.png",
    "qa-grayscale.png",
    "qa-pdf.png",
    "manifest.json",
    "SHA256SUMS",
}
SOURCE_FILES = {
    "README.md",
    "caption.md",
    "command.txt",
    "config.json",
    "contract.json",
    "environment.txt",
    "figure-contract.md",
    "plot.py",
    "qa-protocol.md",
    "requirements.txt",
    "validate.py",
}
EXPECTED_ROWS = 2592


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    if not path.is_file() or path.is_symlink():
        raise RuntimeError(f"required regular file is absent: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"JSON root must be an object: {path}")
    return value


def validate_certificate_commit(manifest: dict) -> dict:
    certificate_manifest = load(CERTIFICATE_ROOT / "manifest.json")
    git = manifest.get("git", {})
    source_commit = str(git.get("sourceCommit", ""))
    certificate_commit = str(git.get("certificateCommit", ""))
    if (
        certificate_manifest.get("status") != "formal"
        or source_commit != certificate_manifest.get("sourceCommit")
        or not re.fullmatch(r"[0-9a-f]{40}", source_commit)
        or not re.fullmatch(r"[0-9a-f]{40}", certificate_commit)
        or source_commit == certificate_commit
        or manifest.get("qa", {}).get("visualInspectionExplicit") is not True
    ):
        raise RuntimeError(
            "formal source/certificate/visual-QA lineage is inconsistent"
        )
    for commit in (source_commit, certificate_commit):
        if subprocess.run(
            ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
            cwd=REPOSITORY,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode:
            raise RuntimeError(f"invalid formal lineage commit: {commit}")
    if subprocess.run(
        ["git", "merge-base", "--is-ancestor", source_commit, certificate_commit],
        cwd=REPOSITORY,
    ).returncode:
        raise RuntimeError("certificateCommit does not descend from sourceCommit")
    for name in (
        "manifest.json",
        "certificate.json",
        "independent.json",
        "crosscheck.json",
        "SHA256SUMS",
    ):
        relative = f"research/certificates/r072v/{name}"
        committed = subprocess.check_output(
            ["git", "show", f"{certificate_commit}:{relative}"],
            cwd=REPOSITORY,
        )
        working = (REPOSITORY / relative).read_bytes()
        if committed != working:
            raise RuntimeError(
                f"working formal certificate differs from "
                f"{certificate_commit}:{relative}"
            )
    subprocess.run(
        [
            sys.executable,
            "research/certificates/r072v/validate_certificate.py",
            "--require-formal",
        ],
        cwd=REPOSITORY,
        check=True,
    )
    return load(CERTIFICATE_ROOT / "certificate.json")


def validate_claim_boundaries(contract: dict, certificate: dict) -> None:
    contract_boundary = contract.get("claimBoundary", {})
    required_contract_true = {
        "analyticWholeLineTheoremProvedInBoundReport",
        "analyticActualSolutionObservabilityProvedInBoundReport",
        "analyticEnergyBlockContractionProvedForDeclaredClass",
    }
    required_contract_false = {
        "finiteCertificateMachineChecksFunctionalAnalysis",
        "timeLengthUniformity",
        "periodicTransferProved",
        "nonlinearNavierStokesClosureProved",
        "clayMillenniumProblemSolved",
    }
    if any(
        contract_boundary.get(key) is not True
        for key in required_contract_true
    ) or any(
        contract_boundary.get(key) is not False
        for key in required_contract_false
    ):
        raise RuntimeError("source figure claim boundary drift")

    certificate_boundary = certificate.get("claimBoundary", {})
    required_certificate_true = {
        "finiteExactAlgebraCertified",
        "analyticWholeLineTheoremProvedInBoundReport",
        "analyticActualSolutionObservabilityProvedInBoundReport",
        "analyticEnergyBlockContractionProvedForDeclaredClass",
    }
    required_certificate_false = {
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
    if any(
        certificate_boundary.get(key) is not True
        for key in required_certificate_true
    ) or any(
        certificate_boundary.get(key) is not False
        for key in required_certificate_false
    ):
        raise RuntimeError("formal certificate claim boundary drift")


def validate_ledger() -> None:
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
        if (
            not path.is_file()
            or path.is_symlink()
            or digest(path) != expected
        ):
            raise RuntimeError(f"SHA256SUMS drift: {name}")
        names.append(name)
    actual = sorted(
        path.name
        for path in ROOT.iterdir()
        if path.is_file() and path.name != "SHA256SUMS"
    )
    if names != sorted(set(names)) or names != actual:
        raise RuntimeError(
            "SHA256SUMS must cover every flat regular file exactly once"
        )
    if set(actual) != (SOURCE_FILES | GENERATED) - {"SHA256SUMS"}:
        raise RuntimeError(
            "formal figure package contains an unexpected or missing file"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-formal", action="store_true")
    args = parser.parse_args()
    if not args.require_formal:
        parser.error("strict validation requires --require-formal")

    manifest = load(ROOT / "manifest.json")
    validation = load(ROOT / "validation.json")
    contract = load(ROOT / "contract.json")
    config = load(ROOT / "config.json")
    if (
        manifest.get("status") != "formal"
        or manifest.get("release") != "R0.72V"
        or manifest.get("figureId") != FIGURE_ID
        or contract.get("figureId") != FIGURE_ID
        or contract.get("stage") != "source-only"
        or config.get("pdeSimulation") is not False
    ):
        raise RuntimeError("formal R0.72V identity or source contract drift")
    if (
        validation.get("status") != "passed"
        or not all(validation.get("checks", {}).values())
        or validation.get("rowCount") != EXPECTED_ROWS
    ):
        raise RuntimeError("automatic figure validation failed")

    certificate = validate_certificate_commit(manifest)
    validate_claim_boundaries(contract, certificate)

    rows = list(csv.DictReader((ROOT / "data.csv").open(encoding="utf-8")))
    if (
        len(rows) != EXPECTED_ROWS
        or {row.get("panel") for row in rows} != {"A", "B", "C"}
    ):
        raise RuntimeError("analytic presentation sample ledger drift")
    allowed = {
        "analytic presentation only",
        "exact integer-cell marker",
        "analytic formula presentation only",
    }
    if any(row.get("status") not in allowed for row in rows):
        raise RuntimeError("non-analytic or simulation row detected")

    results = load(ROOT / "results.json")
    claims_not_made = results.get("claimsNotMade", [])
    if (
        results.get("status") != "passed"
        or results.get("pdeSimulation") is not False
        or results.get("presentationOnly") is not True
        or "numerical value or fitted estimate of C_T" not in claims_not_made
        or "periodic transfer" not in claims_not_made
        or "Clay problem" not in claims_not_made
    ):
        raise RuntimeError("result or claim-boundary drift")

    for record in manifest.get("figure", {}).get("outputs", []):
        path = ROOT / record.get("path", "")
        if (
            not path.is_file()
            or path.is_symlink()
            or digest(path) != record.get("sha256")
        ):
            raise RuntimeError(f"figure output drift: {path.name}")

    publication = manifest.get("publication", {})
    if (
        publication.get("directory") != "public/assets/r072v"
        or publication.get("publicCopiesComplete") is not True
        or len(publication.get("assets", [])) != 3
    ):
        raise RuntimeError("formal publication asset ledger is incomplete")
    for record in publication["assets"]:
        path = REPOSITORY / record.get("path", "")
        master = ROOT / f"figure{path.suffix}"
        if (
            not path.is_file()
            or path.is_symlink()
            or digest(path) != digest(master)
            or record.get("sha256") != digest(path)
            or record.get("byteIdenticalToMaster") is not True
        ):
            raise RuntimeError(f"public asset drift: {path.name}")

    if set(GENERATED) - {
        path.name for path in ROOT.iterdir() if path.is_file()
    }:
        raise RuntimeError("formal generated file set is incomplete")
    validate_ledger()

    generic = subprocess.run(
        [
            sys.executable,
            "research/validate_figure_package.py",
            str(ROOT),
        ],
        cwd=REPOSITORY,
        text=True,
        capture_output=True,
    )
    if generic.returncode:
        raise RuntimeError(
            "generic archive validation failed:\n"
            f"{generic.stdout}\n{generic.stderr}"
        )
    print("R0.72V strict formal figure validation: passed")


if __name__ == "__main__":
    main()
