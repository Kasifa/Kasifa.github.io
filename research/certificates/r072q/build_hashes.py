#!/usr/bin/env python3
"""Build the fail-closed SHA-256 ledger for the R0.72Q certificate bundle."""

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
    "config.json",
    "payload.json",
    "result.json",
    "progress.ndjson",
    "resource.ndjson",
    "monitor.log",
)
REQUIRED = {
    "README.md",
    "build_hashes.py",
    "command.txt",
    "crosscheck.json",
    "environment.txt",
    "write_environment.py",
    *(f"{route}-{suffix}" for route in ROUTES for suffix in ROUTE_SUFFIXES),
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def read_json(name: str) -> dict[str, Any]:
    value = json.loads((ROOT / name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"R0.72Q JSON artifact is not an object: {name}")
    return value


def all_true(value: Any) -> bool:
    return isinstance(value, dict) and bool(value) and all(
        item is True for item in value.values()
    )


def validate_seal() -> None:
    crosscheck = read_json("crosscheck.json")
    checks = crosscheck.get("checks", {})
    if crosscheck.get("status") != "passed" or not all_true(checks):
        raise RuntimeError("R0.72Q crosscheck is not fully passed")
    if checks.get("formalSourceReady") is not True:
        raise RuntimeError("R0.72Q source lineage is not formal-ready")
    if checks.get("sourceCommitMatches") is not True:
        raise RuntimeError("R0.72Q source commits do not match")
    if crosscheck.get("temporaryUnsealedSourceAllowed") is not False:
        raise RuntimeError("temporary R0.72Q crosscheck cannot be formally hashed")

    configs = {route: read_json(f"{route}-config.json") for route in ROUTES}
    results = {route: read_json(f"{route}-result.json") for route in ROUTES}
    payloads = {route: read_json(f"{route}-payload.json") for route in ROUTES}
    commit = configs["producer"].get("gitCommit")
    carrier = configs["producer"].get("maxCarrier")
    if re.fullmatch(r"[0-9a-f]{40}", str(commit or "")) is None:
        raise RuntimeError("R0.72Q producer does not record a full source commit")
    if not isinstance(carrier, int) or isinstance(carrier, bool) or carrier < 2:
        raise RuntimeError("R0.72Q maxCarrier must be an integer >= 2")

    for route in ROUTES:
        config = configs[route]
        result = results[route]
        if config.get("gitCommit") != commit:
            raise RuntimeError(f"R0.72Q {route} source commit mismatch")
        if config.get("sourceTracked") is not True:
            raise RuntimeError(f"R0.72Q {route} source was not tracked at audit time")
        if config.get("trackedChangesDirty") is not False:
            raise RuntimeError(f"R0.72Q {route} tracked tree was dirty at audit time")
        if config.get("maxCarrier") != carrier or result.get("maxCarrier") != carrier:
            raise RuntimeError(f"R0.72Q {route} maxCarrier mismatch")
        if result.get("status") != "passed":
            raise RuntimeError(f"R0.72Q {route} result is not passed")

    if crosscheck.get("sourceCommit") != commit:
        raise RuntimeError("R0.72Q crosscheck source commit mismatch")
    if crosscheck.get("maxCarrier") != carrier:
        raise RuntimeError("R0.72Q crosscheck maxCarrier mismatch")
    if payloads["producer"] != payloads["independent"]:
        raise RuntimeError("R0.72Q canonical payloads differ")

    payload = payloads["producer"]
    shape = payload.get("shapeContract", {})
    geometry = shape.get("criticalGeometry", {})
    caustic = payload.get("twoCarrierCaustic", {})
    boundary = payload.get("claimBoundary", {})
    if (
        payload.get("theoremId") != "R0.72Q-fixed-M-arbitrary-phase-shape-gate"
        or payload.get("passed") is not True
        or shape.get("fixedM") is not True
        or shape.get("maxCarrier") != carrier
        or shape.get("phaseClass") != "arbitrary phases"
        or geometry.get("criticalCount") != 2
        or geometry.get("radius") != "pi/12"
        or geometry.get("C0") != "81/1"
        or geometry.get("C1") != "36/1"
        or geometry.get("normalizedShapeConstants")
        != {"C0": "9/1", "C1": "12/1", "conservativeC0AlsoValid": "81/1"}
        or geometry.get("physicalWindowShapeConstants")
        != {
            "C0": "81/1",
            "C1": "36/1",
            "awaySlopeLower": "1/36",
            "localSlopeLower": "1/9",
            "yWindow": "0<=y<=1",
        }
        or caustic.get("parametrization")
        != "z(phi)=(1/8)*exp(-3*i*phi)-(3/8)*exp(-i*phi)"
        or caustic.get("interiorDisk", {}).get("condition") != "abs(z)<1/4"
        or boundary.get("fixedMRequired") is not True
        or boundary.get("arbitraryPhases") is not True
        or boundary.get("growingMStatus") != "open"
        or boundary.get("finiteCertificateIsProof") is not False
        or boundary.get("causticIsEDFailureCounterexample") is not False
    ):
        raise RuntimeError("R0.72Q canonical claim boundary is incomplete or stale")


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
    print(f"R0.72Q certificate SHA256SUMS: {len(files)} files")


if __name__ == "__main__":
    main()
