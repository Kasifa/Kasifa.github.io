#!/usr/bin/env python3
"""Assemble the primary and independent R0.73Q formula evidence."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import resource
import sys
import time
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
START = time.monotonic()


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink(), "missing regular JSON: " + str(path))
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), "JSON root is not an object: " + str(path))
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def binding(path: Path) -> dict[str, object]:
    return {
        "path": path.resolve().relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def monitor(stage: str, **fields: object) -> None:
    now = datetime.now(timezone.utc).isoformat()
    elapsed = time.monotonic() - START
    raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rss = raw / (1024.0 * 1024.0) if sys.platform == "darwin" else raw / 1024.0
    with (HERE / "progress.ndjson").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({
            "assembler": "evidence-binder",
            "elapsedSeconds": elapsed,
            "stage": stage,
            "timestampUtc": now,
            **fields,
        }, sort_keys=True) + "\n")
    with (HERE / "resource-log.ndjson").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({
            "assembler": "evidence-binder",
            "elapsedSeconds": elapsed,
            "executionHost": platform.node(),
            "gpu": "not used",
            "maximumResidentSetMiB": rss,
            "processes": 1,
            "stage": stage,
            "threadsPerProcess": 1,
            "timestampUtc": now,
        }, sort_keys=True) + "\n")


def main() -> None:
    config_path = HERE / "config.json"
    diagnostic_path = HERE / "diagnostic.json"
    independent_path = HERE / "independent_validation.json"
    source_path = HERE / "source-data.csv"
    config = load_json(config_path)
    diagnostic = load_json(diagnostic_path)
    independent = load_json(independent_path)
    require(diagnostic.get("allChecksPass") is True, "primary diagnostic did not pass")
    require(independent.get("allChecksPass") is True, "independent validation did not pass")
    claim = config["claimBoundary"]
    require(diagnostic.get("claimBoundary") == claim, "primary claim-boundary drift")
    require(independent.get("claimBoundary") == claim, "independent claim-boundary drift")
    monitor("assembly-start")

    certificate = {
        "allPrerequisiteChecksPass": True,
        "claimBoundary": claim,
        "evidenceBindings": {
            "config": binding(config_path),
            "diagnostic": binding(diagnostic_path),
            "independentValidation": binding(independent_path),
            "sourceData": binding(source_path),
        },
        "formulaStatements": {
            "c6": "(5/16)^(1/6)",
            "hhalf": "2^(-1/2) N^(1/4)",
            "heatL4L6": "c6 4^(-1/4) N^(-3/4)",
            "l2": "2^(-1/2) N^(-1/4)",
            "mode": "w_N=N^(-1/4)e_2 sin(N x_1)",
            "timeMapFractionalValue": "n^(3/4)-n^(-1/4) log(2)",
            "timeMapL4FourthPower": "1-log(2)/n",
        },
        "independentCheckCount": int(independent["checkCount"]),
        "modeRows": int(diagnostic["modeRows"]),
        "primaryCheckCount": int(diagnostic["checkCount"]),
        "release": "R0.73Q",
        "schemaVersion": "r073q-finite-heat-flow-certificate-v1",
        "scientificState": {
            "finiteFormulaDiagnostic": "CLOSED",
            "navierStokesSimulation": "NOT_RUN",
            "pdeContinuumProof": "OUTSIDE_CERTIFICATE",
            "timeMapEndpointNoGo": "CLOSED_FOR_SCALAR_FAMILY",
        },
        "timeMapRows": int(diagnostic["timeMapRows"]),
    }
    monitor("assembly-bound", primaryChecks=certificate["primaryCheckCount"], independentChecks=certificate["independentCheckCount"])
    (HERE / "certificate.json").write_text(canonical(certificate), encoding="utf-8")
    print(canonical({
        "allPrerequisiteChecksPass": True,
        "independentChecks": certificate["independentCheckCount"],
        "primaryChecks": certificate["primaryCheckCount"],
    }), end="")


if __name__ == "__main__":
    main()
