#!/usr/bin/env python3
"""Assemble the R0.73R matched-phase shell certificate."""

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
        "bytes": path.stat().st_size,
        "path": path.resolve().relative_to(ROOT).as_posix(),
        "sha256": sha256(path),
    }


def monitor(stage: str, **fields: object) -> None:
    now = datetime.now(timezone.utc).isoformat()
    elapsed = time.monotonic() - START
    raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rss = raw / (1024.0 * 1024.0) if sys.platform == "darwin" else raw / 1024.0
    with (HERE / "progress.ndjson").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({
            "assembler": "evidence-binding",
            "elapsedSeconds": elapsed,
            "stage": stage,
            "timestampUtc": now,
            **fields,
        }, sort_keys=True) + "\n")
    with (HERE / "resource-log.ndjson").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({
            "assembler": "evidence-binding",
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
            "annularHeatProxy": "N^(-1/2) ||W_{R,m}||_6; diagnostic proxy, not an exact heat norm",
            "coefficientMagnitudeSquared": "1/(2*m^2)",
            "dirichletUnivariateL6Sixth": "(11*m^5+5*m^3+4*m)/20",
            "field": "W_{R,m}=(sqrt(2)/m)e_3 Re[e^(iNx_1)R_m(e^(ix_1))R_m(e^(ix_2))]",
            "fieldL2Squared": "1",
            "fieldL6Sixth": "5*S_R^2/(2*m^6)",
            "scalingAmplitude": "alpha_m=N^(1/2)*m^(-2/3)",
            "supportSize": "2*m^2",
        },
        "independentCheckCount": int(independent["checkCount"]),
        "primaryCheckCount": int(diagnostic["checkCount"]),
        "release": "R0.73R",
        "rowCount": int(diagnostic["rowCount"]),
        "scalingEndpointSlopes": diagnostic["scalingEndpointSlopes"],
        "theoreticalScalingExponentsInM": diagnostic["theoreticalScalingExponentsInM"],
        "schemaVersion": "r073r-matched-phase-shell-certificate-v1",
        "scientificState": {
            "exactFiniteFourierIdentities": "CLOSED_ON_CONFIGURED_GRID",
            "heatFlowIntegration": "NOT_RUN",
            "navierStokesSimulation": "NOT_RUN",
            "pdeContinuumProof": "OUTSIDE_CERTIFICATE",
        },
    }
    monitor(
        "assembly-bound",
        independentChecks=certificate["independentCheckCount"],
        primaryChecks=certificate["primaryCheckCount"],
    )
    (HERE / "certificate.json").write_text(canonical(certificate), encoding="utf-8")
    print(canonical({
        "allPrerequisiteChecksPass": True,
        "independentChecks": certificate["independentCheckCount"],
        "primaryChecks": certificate["primaryCheckCount"],
        "rows": certificate["rowCount"],
    }), end="")


if __name__ == "__main__":
    main()
