#!/usr/bin/env python3
"""Build the fail-closed SHA-256 ledger for the R0.72S certificate bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
from typing import Any


ROOT = Path(__file__).resolve().parent
LEDGER = ROOT / "SHA256SUMS"
TEMP_LEDGER = ROOT / ".SHA256SUMS.tmp"
EXCLUDED = {LEDGER.name, TEMP_LEDGER.name, ".DS_Store"}
ROUTES = ("producer", "independent")
ROUTE_SUFFIXES = (
    "config.json", "payload.json", "result.json", "progress.ndjson",
    "resource.ndjson", "monitor.log",
)
REQUIRED_CROSSCHECK_CHECKS = {
    "producerPassed", "independentPassed", "sourceCommitMatches",
    "formalSourceReady", "sourceReadyOrExplicitlyAllowed",
    "canonicalPayloadsIdentical", "payloadPassed", "incidencePartitionExact",
    "incidenceJetsExact", "restrictedMiniversalityExact",
    "a2DerivedLedgerConsistent", "a2FiniteGuardInputsExact",
    "a3DerivedLedgerConsistent", "a3FiniteGuardInputsExact",
    "heatEquationIdentityExact", "stationaryBoundaryExact",
    "claimBoundaryPreserved",
}
REQUIRED = {
    "README.md", "build_hashes.py", "command.txt", "crosscheck.json",
    "environment.txt", "write_environment.py",
    *(f"{route}-{suffix}" for route in ROUTES for suffix in ROUTE_SUFFIXES),
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_json(name: str) -> dict[str, Any]:
    value = json.loads((ROOT / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"R0.72S JSON artifact is not an object: {name}")
    return value


def all_true(value: Any) -> bool:
    return isinstance(value, dict) and bool(value) and all(
        item is True for item in value.values()
    )


def validate_seal() -> None:
    crosscheck = read_json("crosscheck.json")
    checks = crosscheck.get("checks", {})
    if crosscheck.get("status") != "passed" or not all_true(checks):
        raise RuntimeError("R0.72S crosscheck is not fully passed")
    missing_checks = REQUIRED_CROSSCHECK_CHECKS - set(checks)
    if missing_checks:
        raise RuntimeError(
            "R0.72S crosscheck uses a stale schema: "
            + ", ".join(sorted(missing_checks))
        )
    if checks.get("formalSourceReady") is not True:
        raise RuntimeError("R0.72S source lineage is not formal-ready")
    if checks.get("sourceCommitMatches") is not True:
        raise RuntimeError("R0.72S source commits do not match")
    if crosscheck.get("temporaryUnsealedSourceAllowed") is not False:
        raise RuntimeError("temporary R0.72S crosscheck cannot be formally hashed")

    configs = {route: read_json(f"{route}-config.json") for route in ROUTES}
    results = {route: read_json(f"{route}-result.json") for route in ROUTES}
    payloads = {route: read_json(f"{route}-payload.json") for route in ROUTES}
    commit = configs["producer"].get("gitCommit")
    if re.fullmatch(r"[0-9a-f]{40}", str(commit or "")) is None:
        raise RuntimeError("R0.72S producer does not record a full source commit")
    for route in ROUTES:
        config = configs[route]
        if config.get("gitCommit") != commit:
            raise RuntimeError(f"R0.72S {route} source commit mismatch")
        if config.get("sourceTracked") is not True:
            raise RuntimeError(f"R0.72S {route} source was not tracked")
        if config.get("trackedChangesDirty") is not False:
            raise RuntimeError(f"R0.72S {route} tracked tree was dirty")
        if results[route].get("status") != "passed":
            raise RuntimeError(f"R0.72S {route} result is not passed")
    if crosscheck.get("sourceCommit") != commit:
        raise RuntimeError("R0.72S crosscheck source commit mismatch")
    if payloads["producer"] != payloads["independent"]:
        raise RuntimeError("R0.72S canonical payloads differ")

    payload = payloads["producer"]
    miniversality = payload.get("restrictedMiniversality", {})
    a2 = payload.get("a2HeatPath", {})
    a3 = payload.get("a3HeatPath", {})
    heat_identity = payload.get("heatEquationIdentity", {})
    boundary = payload.get("claimBoundary", {})
    if (
        payload.get("theoremId")
        != "R0.72S-exact-Ak-strata-and-two-heat-collisions"
        or payload.get("passed") is not True
        or not all_true(payload.get("exactChecks"))
        or miniversality.get("coefficientOrder")
        != ["Re(z2)", "Im(z2)", "Re(z3)", "Im(z3)"]
        or miniversality.get("derivativeOrders") != [1, 2, 3, 4]
        or miniversality.get("coefficientDerivativeJetAtPhiZero") != [
            [0, -2, 0, -3],
            [-4, 0, -9, 0],
            [0, 8, 0, 27],
            [16, 0, 81, 0],
        ]
        or miniversality.get("coefficientDerivativeJetDeterminant") != "5400/1"
        or miniversality.get("localCodimensions")
        != {"A2": 1, "A3": 2, "A4": 3, "A5": 4}
        or miniversality.get("moduloAdditiveConstants") is not True
        or miniversality.get("fullA5MiniversalParameterCountIncludingConstant") != 5
        or miniversality.get("globalEmbeddedStratificationClaimed") is not False
        or a2.get("crossingPowerIdentity")
        != {"tau": "1/2", "8TauCubed": "1/1"}
        or a2.get("kLogDerivative") != "-3/1"
        or a2.get("representativeK")
        != {"before": "2/1", "at": "1/1", "after": "1/2"}
        or a2.get("distinctCriticalCounts") != {"before": 4, "at": 3, "after": 2}
        or a2.get("criticalCountWithMultiplicityAtCrossing") != 4
        or a2.get("uniqueDegenerateEventForYNonnegative") is not True
        or a2.get("globalSignGuards") != {
            "pAtMinusOne": {"constant": "1/1", "k": "1/1"},
            "pAtZero": {"k": "-1/1"},
            "pAtOne": {"constant": "-1/1", "k": "1/1"},
            "rootProduct": "-1/2",
            "offAxisDegeneracyAfterMultiplyBy8k": {
                "constant": "-1/1", "kSquared": "-8/1",
            },
        }
        or a3.get("distinctCriticalCounts") != {"before": 4, "at": 2, "after": 2}
        or a3.get("criticalCountWithMultiplicityAtCrossing") != 4
        or a3.get("crossingPowerIdentities")
        != {"tauCubed": "1/8", "tauEighth": "1/256"}
        or a3.get("representativeTau")
        != {"before": "3/4", "at": "1/2", "after": "1/4"}
        or a3.get("globalSignGuards") != {
            "qMinusOneCoefficients": ["1/1", "2563/320", "3/10"],
            "qXUpperParentAtTauOne": "-2307/1280",
            "hTauDerivativeParentAtTauOne": "-2307/1280",
        }
        or a3.get("fullCoefficientSpaceTransverse") is not False
        or heat_identity != {
            "identity": "partial_y F=partial_phi^2 F+F",
            "harmonicDecayExponents": {"n1": 0, "n2": 3, "n3": 8},
            "onIncidence": ["partial_y F'=F'''", "partial_y F''=F''''"],
        }
        or boundary.get("completeGlobalCausticImageClassification") is not False
        or boundary.get("causticCrossingEnhancedDissipation") is not False
        or boundary.get("generalThreeDimensionalRegularity") is not False
        or boundary.get("clayMillenniumProblemSolved") is not False
    ):
        raise RuntimeError("R0.72S canonical claim boundary is incomplete or stale")


def artifacts() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.iterdir():
        if path.name in EXCLUDED:
            continue
        if path.is_symlink():
            raise RuntimeError(f"certificate artifact must not be a symlink: {path.name}")
        if not path.is_file():
            raise RuntimeError(f"unexpected non-file certificate artifact: {path.name}")
        if "\n" in path.name or "\r" in path.name:
            raise RuntimeError("certificate artifact name contains a newline")
        files.append(path)
    names = {path.name for path in files}
    missing = sorted(REQUIRED - names)
    if missing:
        raise RuntimeError(f"certificate bundle is incomplete: {', '.join(missing)}")
    unexpected = sorted(names - REQUIRED)
    if unexpected:
        raise RuntimeError(f"unexpected certificate artifacts: {', '.join(unexpected)}")
    return sorted(files, key=lambda path: path.name.encode("utf-8"))


def main() -> None:
    validate_seal()
    files = artifacts()
    payload = "".join(f"{digest(path)}  {path.name}\n" for path in files)
    TEMP_LEDGER.write_text(payload, encoding="utf-8")
    TEMP_LEDGER.replace(LEDGER)
    print(f"R0.72S certificate SHA256SUMS: {len(files)} files")


if __name__ == "__main__":
    main()
