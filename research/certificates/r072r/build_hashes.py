#!/usr/bin/env python3
"""Build the fail-closed SHA-256 ledger for the R0.72R certificate bundle."""

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
        raise RuntimeError(f"R0.72R JSON artifact is not an object: {name}")
    return value


def all_true(value: Any) -> bool:
    return isinstance(value, dict) and bool(value) and all(
        item is True for item in value.values()
    )


def validate_seal() -> None:
    crosscheck = read_json("crosscheck.json")
    checks = crosscheck.get("checks", {})
    if crosscheck.get("status") != "passed" or not all_true(checks):
        raise RuntimeError("R0.72R crosscheck is not fully passed")
    if checks.get("formalSourceReady") is not True:
        raise RuntimeError("R0.72R source lineage is not formal-ready")
    if checks.get("sourceCommitMatches") is not True:
        raise RuntimeError("R0.72R source commits do not match")
    if crosscheck.get("temporaryUnsealedSourceAllowed") is not False:
        raise RuntimeError("temporary R0.72R crosscheck cannot be formally hashed")

    configs = {route: read_json(f"{route}-config.json") for route in ROUTES}
    results = {route: read_json(f"{route}-result.json") for route in ROUTES}
    payloads = {route: read_json(f"{route}-payload.json") for route in ROUTES}
    commit = configs["producer"].get("gitCommit")
    if re.fullmatch(r"[0-9a-f]{40}", str(commit or "")) is None:
        raise RuntimeError("R0.72R producer does not record a full source commit")

    for route in ROUTES:
        config = configs[route]
        result = results[route]
        if config.get("gitCommit") != commit:
            raise RuntimeError(f"R0.72R {route} source commit mismatch")
        if config.get("sourceTracked") is not True:
            raise RuntimeError(f"R0.72R {route} source was not tracked at audit time")
        if config.get("trackedChangesDirty") is not False:
            raise RuntimeError(f"R0.72R {route} tracked tree was dirty at audit time")
        if result.get("status") != "passed":
            raise RuntimeError(f"R0.72R {route} result is not passed")

    if crosscheck.get("sourceCommit") != commit:
        raise RuntimeError("R0.72R crosscheck source commit mismatch")
    if payloads["producer"] != payloads["independent"]:
        raise RuntimeError("R0.72R canonical payloads differ")

    payload = payloads["producer"]
    shape = payload.get("shapeContract", {})
    heat = payload.get("heatPath", {})
    real_slice = payload.get("realSlice", {})
    boundary = payload.get("claimBoundary", {})
    if (
        payload.get("theoremId")
        != "R0.72R-four-real-dimensional-caustic-free-core"
        or payload.get("passed") is not True
        or heat.get("coneExitMargin") != "3/50"
        or heat.get("uniqueOldConeCrossingOnZeroOne") is not True
        or shape.get("radius") != "pi/48"
        or shape.get("criticalCount") != 2
        or shape.get("C0") != "144/1"
        or shape.get("C1") != "240/1"
        or real_slice.get("tensorGridIdentityProof") is not True
        or boundary.get("completeFourDimensionalChamberClassification") is not False
        or boundary.get("causticCrossingEnhancedDissipation") is not False
        or boundary.get("uniformThirdCarrierAmplitudeFloor") is not False
        or boundary.get("generalThreeDimensionalRegularity") is not False
    ):
        raise RuntimeError("R0.72R canonical claim boundary is incomplete or stale")


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
    print(f"R0.72R certificate SHA256SUMS: {len(files)} files")


if __name__ == "__main__":
    main()
