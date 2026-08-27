#!/usr/bin/env python3
"""Build the fail-closed SHA-256 ledger for the R0.72P certificate bundle."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
LEDGER = ROOT / "SHA256SUMS"
TEMP_LEDGER = ROOT / ".SHA256SUMS.tmp"
EXCLUDED = {LEDGER.name, TEMP_LEDGER.name, ".DS_Store"}
REQUIRED = {
    "README.md",
    "build_hashes.py",
    "command.txt",
    "crosscheck.json",
    "environment.txt",
    "independent-config.json",
    "independent-environment.txt",
    "independent-exponents.json",
    "independent-monitor.log",
    "independent-progress.ndjson",
    "independent-resource.ndjson",
    "independent-result.json",
    "independent-shape.csv",
    "independent-wall.csv",
    "producer-config.json",
    "producer-exponents.json",
    "producer-monitor.log",
    "producer-progress.ndjson",
    "producer-resource.ndjson",
    "producer-result.json",
    "producer-shape.csv",
    "producer-wall.csv",
    "write_environment.py",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def read_json(name: str) -> dict:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def validate_seal() -> None:
    crosscheck = read_json("crosscheck.json")
    if crosscheck.get("status") != "passed":
        raise RuntimeError("R0.72P crosscheck is not passed")
    checks = crosscheck.get("checks", {})
    if checks.get("formalSourceReady") is not True:
        raise RuntimeError("R0.72P source lineage is not formal-ready")
    if crosscheck.get("temporaryUnsealedSourceAllowed") is not False:
        raise RuntimeError("temporary R0.72P crosscheck cannot be formally hashed")

    producer = read_json("producer-config.json")
    independent = read_json("independent-config.json")
    commit = producer.get("gitCommit")
    if (
        re.fullmatch(r"[0-9a-f]{40}", str(commit or "")) is None
        or independent.get("gitCommit") != commit
    ):
        raise RuntimeError("R0.72P audit routes do not record one source commit")
    for label, config in (("producer", producer), ("independent", independent)):
        if config.get("sourceTracked") is not True:
            raise RuntimeError(f"R0.72P {label} source was not tracked at audit time")
        if config.get("trackedChangesDirty") is not False:
            raise RuntimeError(f"R0.72P {label} tracked tree was dirty at audit time")


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
    TEMP_LEDGER.write_text(payload, encoding="utf-8", newline="\n")
    TEMP_LEDGER.replace(LEDGER)
    print(f"R0.72P certificate SHA256SUMS: {len(files)} files")


if __name__ == "__main__":
    main()
