#!/usr/bin/env python3
"""Fail-closed cross-validator for the independent R0.72Z certificates."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
from typing import Any


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
EXPECTED_SOURCE_FILES = (
    "research/r072z_report-source.md",
    "research/r072z_gap_matrix.md",
    "research/r072z_literature_audit.md",
    "research/r072z_os_independent_audit.md",
    "research/r072z_squire_independent_audit.md",
    "research/r072z_independent_audit.md",
    "research/certificates/r072z/generate_certificate.py",
    "research/certificates/r072z/independent_recompute.py",
    "research/certificates/r072z/validate_certificate.py",
    "research/certificates/r072z/README.md",
    "research/certificates/r072z/command.txt",
    "research/certificates/r072z/environment.txt",
    "research/release-manifest.json",
    "scripts/generate_r072z_release.py",
    "scripts/add-r072z-translations.mjs",
    "scripts/i18n-snapshots/r072z-missing.json",
    "figures/r072z/fig-r072z-os-squire-threshold/README.md",
    "figures/r072z/fig-r072z-os-squire-threshold/caption.md",
    "figures/r072z/fig-r072z-os-squire-threshold/command.txt",
    "figures/r072z/fig-r072z-os-squire-threshold/config.json",
    "figures/r072z/fig-r072z-os-squire-threshold/contract.json",
    "figures/r072z/fig-r072z-os-squire-threshold/environment.txt",
    "figures/r072z/fig-r072z-os-squire-threshold/figure-contract.md",
    "figures/r072z/fig-r072z-os-squire-threshold/manifest-draft.json",
    "figures/r072z/fig-r072z-os-squire-threshold/plot.py",
    "figures/r072z/fig-r072z-os-squire-threshold/qa-protocol.md",
    "figures/r072z/fig-r072z-os-squire-threshold/requirements.txt",
    "figures/r072z/fig-r072z-os-squire-threshold/validate.py",
    "tests/r072z-deterministic-certificate-source.test.mjs",
    "tests/r072z-os-squire-figure-source.test.mjs",
    "tests/r072z-os-squire-gate.test.mjs",
    "tests/r072z-release.test.mjs",
)
MUTABLE_PUBLICATION_STATE = "research/release-manifest.json"
EXPECTED_SOURCE_BINDING_POLICY = {
    "mutablePublicationState": MUTABLE_PUBLICATION_STATE,
    "sourceCommitBlobPermanentlyBound": True,
    "currentAdvanceAllowedOnlyAtCleanDescendantPublicationCommit": True,
}
EXPECTED_BOUNDARY = {
    "finiteDeterministicAlgebraCertified": True,
    "lowGapOSTransientA2PropagatorProved": False,
    "collisionScaleLimitingPropagatorProved": False,
    "finiteMatrixEqualsFullOperatorNormProved": False,
    "BlochUniformPhysicalVelocityDirectSumProved": False,
    "completeLinearizedShearSubsystemProved": False,
    "nonlinearNavierStokesClosureProved": False,
    "clayMillenniumProblemSolved": False,
}
EXPECTED_CLAIM_COUNTS = {"closed": 15, "false": 10, "open": 8}
FLAT_FILES_WITHOUT_HASH_LEDGER = {
    "README.md", "command.txt", "environment.txt", "generate_certificate.py",
    "independent_recompute.py", "validate_certificate.py", "certificate.json",
    "independent.json", "crosscheck.json", "manifest.json",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def close(left: float | str, right: float | str, tolerance: float = 1e-12) -> bool:
    return math.isclose(float(left), float(right), rel_tol=tolerance, abs_tol=tolerance)


def validate_schema(payload: dict[str, Any], independent: dict[str, Any]) -> None:
    for name, data in (("producer", payload), ("independent", independent)):
        require(data.get("schemaVersion") == 1, f"{name}: schema drift")
        require(data.get("researchRelease") == "R0.72Z", f"{name}: release drift")
        require(data.get("status") == "passed", f"{name}: status is not passed")
    require(payload.get("producerMethod") != independent.get("method"),
            "producer and independent methods unexpectedly coincide")
    require(all(payload.get("exactChecks", {}).values()), "producer exact check is false or missing")
    require(all(independent.get("checks", {}).values()), "independent check is false or missing")


def validate_claim_boundary(payload: dict[str, Any], independent: dict[str, Any]) -> None:
    require(payload.get("claimBoundary") == EXPECTED_BOUNDARY,
            "producer claim boundary is incomplete or has drifted")
    require(independent.get("claimBoundary") == EXPECTED_BOUNDARY,
            "independent claim boundary is incomplete or has drifted")


def validate_claim_ledger(payload: dict[str, Any], independent: dict[str, Any]) -> None:
    producer = payload.get("claimLedger")
    other = independent.get("claimLedger")
    require(producer == other, "claim ledgers disagree")
    require(isinstance(producer, dict) and set(producer) == set(EXPECTED_CLAIM_COUNTS),
            "claim ledger groups missing or unexpected")
    for status, count in EXPECTED_CLAIM_COUNTS.items():
        keys = producer[status]
        require(len(keys) == count and len(set(keys)) == count,
                f"{status}-keys count or uniqueness drift")
    require("lowGapOSTransientA2Propagator" in producer["open"], "low-gap propagator escaped OPEN")
    require("BlochUniformPhysicalVelocityDirectSum" in producer["open"], "physical direct sum escaped OPEN")
    require("nonlinearNavierStokes" in producer["open"], "nonlinear closure escaped OPEN")


def validate_source_hashes(
    payload: dict[str, Any],
    independent: dict[str, Any],
    expected_hashes: dict[str, str] | None = None,
) -> None:
    expected_names = set(EXPECTED_SOURCE_FILES)
    for label, hashes in (("producer", payload.get("sourceHashes")),
                          ("independent", independent.get("sourceHashes"))):
        require(isinstance(hashes, dict) and set(hashes) == expected_names,
                f"{label}: source inventory mismatch")
        for name in EXPECTED_SOURCE_FILES:
            if expected_hashes is None:
                path = REPO / name
                require(path.is_file() and not path.is_symlink(),
                        f"{label}: unsafe or missing source {name}")
                expected = sha(path)
            else:
                expected = expected_hashes.get(name)
            require(hashes[name] == expected, f"{label}: source hash drift {name}")
    require(payload["sourceHashes"] == independent["sourceHashes"], "source hash routes disagree")


def validate_exact_ledger(payload: dict[str, Any], independent: dict[str, Any]) -> dict[str, Any]:
    p_comm, i_comm = payload["commutatorMatrix"], independent["commutatorMatrix"]
    for key in ("DCommutator", "LCommutator", "energyPressureSign", "fourierCoefficients", "matrixFormula"):
        require(p_comm[key] == i_comm[key], f"commutator/matrix mismatch: {key}")
    require(float(p_comm["selfAdjointSampleResidual"]) < 1e-14, "producer matrix not self-adjoint")
    require(float(i_comm["selfAdjointSampleResidual"]) < 1e-14, "independent matrix not self-adjoint")

    p_gap, i_gap = payload["highGapBounds"], independent["highGapBounds"]
    require(p_gap["M3Formula"] == i_gap["M3Formula"], "M3 formula mismatch")
    require(len(p_gap["M3Samples"]) == len(i_gap["M3Samples"]), "M3 sample count mismatch")
    for left, right in zip(p_gap["M3Samples"], i_gap["M3Samples"]):
        require(close(left["M3"], right["triangleBound"]), "M3 value mismatch")
    require(p_gap["sBound"] == i_gap["sBound"], "s bound mismatch")
    for left, right in zip(p_gap["sBoundSamples"], i_gap["sBoundSamples"]):
        require(close(left["sampledSup"], right["sampledSup"]), "s sample mismatch")
        require(left["boundSatisfied"] and right["boundSatisfied"], "s bound sample failed")

    require(payload["alphaPower"]["identity"] == independent["alphaPower"]["identity"], "alpha identity mismatch")
    require(payload["alphaPower"]["alphaExponent"] == independent["alphaPower"]["alphaPower"] == "-2/1",
            "alpha exponent mismatch")

    p_two, i_two = payload["twoModeWitnesses"], independent["twoModeWitnesses"]
    require(p_two["lowMode"]["instantaneousGrowth"] and i_two["lowModeGrows"], "low-mode witness failed")
    require(close(p_two["lowMode"]["halfEnergyDerivative"], i_two["lowModeHalfEnergyDerivative"]),
            "low-mode derivative mismatch")
    for left, right in zip(p_two["highMode"]["samples"], i_two["highModeSamples"]):
        require(left["n"] == right["n"] and close(left["scaled"], right["scaled"]), "high-mode witness mismatch")
    require(p_two["scope"] == i_two["scope"], "two-mode scope mismatch")

    require(payload["tangentResidual"]["imaginaryResidual"].endswith("=0"), "producer tangent residual failed")
    require(independent["tangentResidual"]["imaginaryResidual"] == "0/1", "independent tangent residual failed")
    require(payload["tangentResidual"]["physicalMuZeroVelocityRowCertified"] is False,
            "producer overclaims physical mu=0 row")
    require(independent["tangentResidual"]["physicalMuZeroVelocityRowCertified"] is False,
            "independent overclaims physical mu=0 row")

    for key in ("VLimitCoefficients", "VXXLimitCoefficients"):
        require(payload["scaledCubic"][key] == independent["scaledCubic"][key], f"scaled cubic mismatch: {key}")
    require(not payload["scaledCubic"]["collisionScalePropagatorCertified"], "producer overclaims collision propagator")
    require(not independent["scaledCubic"]["collisionScalePropagatorCertified"], "independent overclaims collision propagator")

    p_orient, i_orient = payload["orientation"], independent["orientation"]
    require(p_orient["chiFormula"] == i_orient["chiFormula"], "chi formula mismatch")
    require([row["chiSquared"] for row in p_orient["chiSamples"]] ==
            [row["chiSquared"] for row in i_orient["chiSamples"]], "chi samples mismatch")
    require(p_orient["LambdaPaymentRequired"] and i_orient["LambdaPaymentRequired"], "Lambda payment missing")
    require(p_orient["cOnlyUniformBound"] is False and i_orient["cOnlyUniformBound"] is False,
            "c-only false claim lost")
    require(close(p_orient["latticeSum"]["closedForm"], i_orient["latticeSum"]["poissonValue"]),
            "lattice identity routes disagree")
    require(float(p_orient["latticeSum"]["tailSizedResidual"]) < 1.1e-5,
            "direct lattice truncation residual too large")

    for p_row, i_row in zip(payload["kernels"]["PhiSamples"], independent["kernels"]["kernelIntegrals"]):
        require(close(p_row["value"], i_row["PhiQuadrature"], 1e-11), "Phi integral mismatch")
    for p_row, i_row in zip(payload["kernels"]["JSamples"], independent["kernels"]["dampingGapConvolutions"]):
        require(close(p_row["value"], i_row["quadrature"], 1e-11), "J convolution mismatch")
    require(payload["kernels"]["equalRateUniformGapDenominator"] is False and
            independent["kernels"]["equalRateUniformGapDenominator"] is False,
            "equal-rate boundary lost")

    return {
        "status": "passed",
        "researchRelease": "R0.72Z",
        "routesIndependent": True,
        "checkedSections": [
            "commutator-and-fourier-matrix", "M3-and-s-bound", "alpha-power",
            "two-mode-low-high-witnesses", "tangent-residual", "scaled-cubic",
            "orientation-chi-and-lattice-sum", "kernel-integrals-and-J-formula",
            "claim-ledger-and-boundary",
        ],
        "excludedFromCertificate": [
            "low-gap OS transient A2 propagator", "collision-scale limiting propagator",
            "finite truncation equals full operator norm", "Bloch-uniform physical velocity direct sum",
            "complete linearized shear subsystem", "nonlinear Navier-Stokes", "Clay Millennium problem",
        ],
    }


def validate_payloads(
    payload: dict[str, Any],
    independent: dict[str, Any],
    *,
    hashes: bool = True,
    expected_hashes: dict[str, str] | None = None,
) -> dict[str, Any]:
    validate_schema(payload, independent)
    validate_claim_boundary(payload, independent)
    validate_claim_ledger(payload, independent)
    if hashes:
        validate_source_hashes(payload, independent, expected_hashes)
    return validate_exact_ledger(payload, independent)


def validate_sha256_ledger() -> None:
    ledger = HERE / "SHA256SUMS"
    require(ledger.is_file() and not ledger.is_symlink(), "SHA256SUMS missing or unsafe")
    rows = ledger.read_text().splitlines()
    names: list[str] = []
    for row in rows:
        pieces = row.split("  ", 1)
        require(len(pieces) == 2 and len(pieces[0]) == 64 and all(c in "0123456789abcdef" for c in pieces[0]),
                "malformed SHA256SUMS row")
        name = pieces[1]
        require("/" not in name and "\\" not in name, "non-flat SHA256SUMS entry")
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"unsafe hashed file: {name}")
        require(sha(path) == pieces[0], f"SHA256 mismatch: {name}")
        names.append(name)
    require(names == sorted(FLAT_FILES_WITHOUT_HASH_LEDGER), "SHA256 file inventory mismatch")
    unexpected = [
        path.name for path in HERE.iterdir()
        if path.name != "SHA256SUMS" and (not path.is_file() or path.is_symlink())
    ]
    require(not unexpected,
            f"certificate directory contains non-flat or linked entries: {sorted(unexpected)}")
    actual = {p.name for p in HERE.iterdir() if p.is_file() and p.name != "SHA256SUMS"}
    require(actual == FLAT_FILES_WITHOUT_HASH_LEDGER, "certificate directory has unexpected or missing files")


def load(name: str) -> dict[str, Any]:
    path = HERE / name
    require(path.is_file() and not path.is_symlink(), f"required regular file is absent: {name}")
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"{name} is not a JSON object")
    return value


def validate_draft_bindings(
    manifest: dict[str, Any], crosscheck: dict[str, Any]
) -> dict[str, str]:
    bindings = manifest.get("sourceBindings")
    require(manifest.get("sourceCommit") is None and crosscheck.get("sourceCommit") is None,
            "draft certificate must not claim a source commit")
    require(isinstance(bindings, list) and bindings == crosscheck.get("sourceBindings"),
            "draft source bindings are missing or inconsistent")
    require([row.get("path") for row in bindings] == list(EXPECTED_SOURCE_FILES),
            "draft source bindings do not cover the expected package sources")
    expected_hashes: dict[str, str] = {}
    seen: set[str] = set()
    for row in bindings:
        relative = row.get("path")
        require(
            isinstance(relative, str)
            and not relative.startswith("/")
            and ".." not in Path(relative).parts
            and relative not in seen,
            "malformed or duplicate draft source binding",
        )
        seen.add(relative)
        path = (REPO / relative).resolve()
        require(REPO.resolve() in path.parents and path.is_file() and not path.is_symlink(),
                f"bound draft source is absent, linked, or escapes repository: {relative}")
        require(row.get("sha256") == sha(path) and row.get("bytes") == path.stat().st_size,
                f"draft source binding drift: {relative}")
        expected_hashes[relative] = row["sha256"]
    return expected_hashes


def git_status() -> tuple[list[str], set[str]]:
    rows = subprocess.check_output(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=REPO,
        text=True,
    ).splitlines()
    paths: set[str] = set()
    for row in rows:
        require(len(row) >= 4, "malformed Git status row")
        state, relative = row[:2], row[3:]
        require("R" not in state and "C" not in state and " -> " not in relative,
                "formal validation refuses ambiguous rename/copy status")
        paths.add(relative)
    return rows, paths


def validate_formal_bindings(
    manifest: dict[str, Any], crosscheck: dict[str, Any]
) -> dict[str, str]:
    commit = str(manifest.get("sourceCommit", ""))
    bindings = manifest.get("sourceBindings")
    require(re.fullmatch(r"[0-9a-f]{40}", commit) is not None,
            "formal source commit is missing or malformed")
    require(isinstance(bindings, list) and bindings == crosscheck.get("sourceBindings"),
            "formal source bindings are missing or inconsistent")
    require([row.get("path") for row in bindings] == list(EXPECTED_SOURCE_FILES),
            "formal source bindings do not cover the complete frozen source set")
    require(crosscheck.get("sourceCommit") == commit,
            "formal crosscheck source commit drifted")
    require(subprocess.run(
        ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
        cwd=REPO,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0, "formal sourceCommit is not a valid Git commit object")
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPO, text=True
    ).strip()
    require(subprocess.run(
        ["git", "merge-base", "--is-ancestor", commit, head],
        cwd=REPO,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0, "formal sourceCommit is not an ancestor of current HEAD")
    status_rows, status_paths = git_status()

    seen: set[str] = set()
    expected_hashes: dict[str, str] = {}
    mutable_publication_state_advanced = False
    for row in bindings:
        relative = row.get("path")
        require(
            isinstance(relative, str)
            and not relative.startswith("/")
            and ".." not in Path(relative).parts
            and relative not in seen
            and row.get("commit") == commit
            and row.get("workingTreeBlobMatches") is True,
            "malformed or duplicate formal source binding",
        )
        seen.add(relative)
        path = (REPO / relative).resolve()
        require(REPO.resolve() in path.parents and path.is_file() and not path.is_symlink(),
                f"bound formal source is absent, linked, or escapes repository: {relative}")
        try:
            committed_blob = subprocess.check_output(
                ["git", "rev-parse", f"{commit}:{relative}"],
                cwd=REPO,
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
        except subprocess.CalledProcessError as error:
            raise RuntimeError(f"formal source is absent from sourceCommit: {relative}") from error
        source_blob_bytes = subprocess.check_output(
            ["git", "cat-file", "blob", committed_blob], cwd=REPO
        )
        committed_sha = hashlib.sha256(source_blob_bytes).hexdigest()
        require(
            row.get("gitBlob") == committed_blob
            and row.get("sha256") == committed_sha
            and row.get("bytes") == len(source_blob_bytes),
            f"formal source binding drift: {relative}",
        )
        expected_hashes[relative] = committed_sha
        working_blob = subprocess.check_output(
            ["git", "hash-object", f"--path={relative}", str(path)],
            cwd=REPO,
            text=True,
        ).strip()
        if working_blob == committed_blob:
            require(sha(path) == committed_sha and path.stat().st_size == len(source_blob_bytes),
                    f"formal working source digest drift: {relative}")
            continue
        require(relative == MUTABLE_PUBLICATION_STATE and head != commit,
                f"immutable formal source drift: {relative}")
        require(relative not in status_paths,
                "publication-state manifest drift must be clean-committed")
        try:
            head_blob = subprocess.check_output(
                ["git", "rev-parse", f"{head}:{relative}"],
                cwd=REPO,
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
        except subprocess.CalledProcessError as error:
            raise RuntimeError(
                "publication-state manifest is absent from descendant HEAD"
            ) from error
        require(working_blob == head_blob,
                "publication-state manifest does not equal its clean descendant blob")
        mutable_publication_state_advanced = True

    allowed_generated_mutations = {
        "research/certificates/r072z/certificate.json",
        "research/certificates/r072z/independent.json",
        "research/certificates/r072z/crosscheck.json",
        "research/certificates/r072z/manifest.json",
        "research/certificates/r072z/SHA256SUMS",
    }
    source_set = set(EXPECTED_SOURCE_FILES)
    for relative in status_paths:
        require(relative not in source_set,
                f"formal validation found a frozen-source working-tree mutation: {relative}")
        if head == commit:
            require(relative in allowed_generated_mutations,
                    "at source HEAD, formal validation permits only certificate outputs: "
                    f"{relative}")
    require(not mutable_publication_state_advanced or not status_rows,
            "an advanced publication-state manifest is accepted only at a completely clean descendant publication commit")
    return expected_hashes


def validate_manifest_files(manifest: dict[str, Any]) -> None:
    require(manifest.get("claimCounts") == EXPECTED_CLAIM_COUNTS,
            "manifest claim counts drifted")
    require(manifest.get("boundary") == EXPECTED_BOUNDARY,
            "manifest claim boundary drifted")
    for name in ("certificate.json", "independent.json", "crosscheck.json"):
        path = HERE / name
        row = manifest.get("files", {}).get(name, {})
        require(row.get("sha256") == sha(path) and row.get("bytes") == path.stat().st_size,
                f"manifest artifact hash drift: {name}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-draft", action="store_true")
    parser.add_argument("--require-formal", action="store_true")
    args = parser.parse_args()
    if args.require_draft == args.require_formal:
        parser.error("choose exactly one of --require-draft or --require-formal")

    producer = load("certificate.json")
    independent = load("independent.json")
    crosscheck = load("crosscheck.json")
    manifest = load("manifest.json")
    expected_stage = "formal" if args.require_formal else "draft"
    require(manifest.get("schemaVersion") == 1 and manifest.get("researchRelease") == "R0.72Z",
            "manifest schema or release drifted")
    require(manifest.get("status") == expected_stage,
            f"certificate manifest is not {expected_stage}")
    require(manifest.get("sourceBindingPolicy") == EXPECTED_SOURCE_BINDING_POLICY,
            "manifest source-binding policy drifted")
    require(crosscheck.get("sourceBindingPolicy") == EXPECTED_SOURCE_BINDING_POLICY,
            "crosscheck source-binding policy drifted")
    require(crosscheck.get("sourceBindings") == manifest.get("sourceBindings"),
            "manifest/crosscheck source bindings disagree")
    if args.require_formal:
        require(crosscheck.get("formalSourceReady") is True,
                "formal crosscheck is not source-ready")
        require(crosscheck.get("temporaryUnsealedSourceAllowed") is False,
                "formal crosscheck permits unsealed source")
        expected_hashes = validate_formal_bindings(manifest, crosscheck)
    else:
        require(crosscheck.get("formalSourceReady") is False,
                "draft crosscheck claims formal readiness")
        require(crosscheck.get("temporaryUnsealedSourceAllowed") is True,
                "draft crosscheck does not expose its temporary source")
        expected_hashes = validate_draft_bindings(manifest, crosscheck)

    exact = validate_payloads(
        producer, independent, hashes=True, expected_hashes=expected_hashes
    )
    source_commit = manifest.get("sourceCommit")
    require(
        producer.get("certificateStage") == expected_stage
        and independent.get("certificateStage") == expected_stage
        and producer.get("sourceCommit") == source_commit
        and independent.get("sourceCommit") == source_commit,
        "certificate stage or sourceCommit propagation drifted",
    )
    require(
        crosscheck.get("schemaVersion") == 1
        and crosscheck.get("researchRelease") == "R0.72Z"
        and crosscheck.get("status") == "passed"
        and crosscheck.get("sourceCommit") == source_commit
        and crosscheck.get("checkedSections") == exact.get("checkedSections")
        and crosscheck.get("certificateSha256") == sha(HERE / "certificate.json")
        and isinstance(crosscheck.get("checks"), dict)
        and crosscheck.get("checks")
        and all(crosscheck["checks"].values()),
        f"{expected_stage} crosscheck is stale or incomplete",
    )
    validate_manifest_files(manifest)
    if args.require_formal:
        require("Formally source-bound finite algebra only." in manifest.get("limitations", ""),
                "formal limitation does not state the source-bound finite scope")
    else:
        require("Formal source-commit binding is absent." in manifest.get("limitations", ""),
                "draft limitation does not state missing formal binding")
    validate_sha256_ledger()
    print(f"R0.72Z strict {expected_stage} certificate validation: passed")


if __name__ == "__main__":
    main()
