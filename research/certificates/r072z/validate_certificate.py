#!/usr/bin/env python3
"""Fail-closed cross-validator for the independent R0.72Z certificates."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
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
    "tests/r072z-deterministic-certificate-source.test.mjs",
)
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


def validate_source_hashes(payload: dict[str, Any], independent: dict[str, Any]) -> None:
    expected_names = set(EXPECTED_SOURCE_FILES)
    for label, hashes in (("producer", payload.get("sourceHashes")),
                          ("independent", independent.get("sourceHashes"))):
        require(isinstance(hashes, dict) and set(hashes) == expected_names,
                f"{label}: source inventory mismatch")
        for name in EXPECTED_SOURCE_FILES:
            path = REPO / name
            require(path.is_file() and not path.is_symlink(), f"{label}: unsafe or missing source {name}")
            require(hashes[name] == sha(path), f"{label}: source hash drift {name}")
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


def validate_payloads(payload: dict[str, Any], independent: dict[str, Any], *, hashes: bool = True) -> dict[str, Any]:
    validate_schema(payload, independent)
    validate_claim_boundary(payload, independent)
    validate_claim_ledger(payload, independent)
    if hashes:
        validate_source_hashes(payload, independent)
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
    actual = {p.name for p in HERE.iterdir() if p.is_file() and p.name != "SHA256SUMS"}
    require(actual == FLAT_FILES_WITHOUT_HASH_LEDGER, "certificate directory has unexpected or missing files")


def write_outputs(crosscheck: dict[str, Any], producer: dict[str, Any], independent: dict[str, Any]) -> None:
    (HERE / "crosscheck.json").write_text(json.dumps(crosscheck, indent=2, sort_keys=True) + "\n")
    manifest = {
        "schemaVersion": 1,
        "researchRelease": "R0.72Z",
        "sourceHashes": producer["sourceHashes"],
        "artifactHashes": {name: sha(HERE / name) for name in ("certificate.json", "independent.json", "crosscheck.json")},
        "claimCounts": EXPECTED_CLAIM_COUNTS,
        "boundary": EXPECTED_BOUNDARY,
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    rows = [f"{sha(HERE / name)}  {name}" for name in sorted(FLAT_FILES_WITHOUT_HASH_LEDGER)]
    (HERE / "SHA256SUMS").write_text("\n".join(rows) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--producer", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--independent", type=Path, default=HERE / "independent.json")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    producer = json.loads(args.producer.read_text())
    independent = json.loads(args.independent.read_text())
    crosscheck = validate_payloads(producer, independent)
    if args.write:
        write_outputs(crosscheck, producer, independent)
        validate_sha256_ledger()
    elif (HERE / "SHA256SUMS").exists():
        validate_sha256_ledger()
    print(json.dumps(crosscheck, sort_keys=True))


if __name__ == "__main__":
    main()
