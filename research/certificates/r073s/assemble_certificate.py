#!/usr/bin/env python3
"""Bind the primary and independent R0.73S finite evidence."""

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
    require(isinstance(value, dict), "JSON root is not an object")
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
    paths = {
        name: HERE / name
        for name in (
            "config.json", "diagnostic.json", "independent_validation.json",
            "source-data.csv", "environment.json",
        )
    }
    config = load_json(paths["config.json"])
    diagnostic = load_json(paths["diagnostic.json"])
    independent = load_json(paths["independent_validation.json"])
    require(diagnostic.get("allChecksPass") is True, "primary diagnostic failed")
    require(independent.get("allChecksPass") is True, "independent validation failed")
    require(diagnostic.get("recordsSha256") == independent.get("recordsSha256"), "record digest disagreement")
    require(diagnostic.get("claimBoundary") == independent.get("claimBoundary") == config.get("claimBoundary"), "claim boundary drift")
    monitor("assembly-start")
    certificate = {
        "allPrerequisiteChecksPass": True,
        "claimBoundary": config["claimBoundary"],
        "evidenceBindings": {
            "config": binding(paths["config.json"]),
            "diagnostic": binding(paths["diagnostic.json"]),
            "environment": binding(paths["environment.json"]),
            "independentValidation": binding(paths["independent_validation.json"]),
            "sourceData": binding(paths["source-data.csv"]),
        },
        "formulaStatements": {
            "autocorrelation": "C(h)=sum_k a(k+h) dot conjugate(a(k))=Fourier(|f|^2)(h)",
            "autocorrelationSupport": "D_C=cardinality(support(C))",
            "differenceSet": "D_delta=cardinality(S-S), with D_C<=D_delta",
            "exactQuartic": "Q=sum_h |C(h)|^2=||f||_4^4",
            "matchedProxy": "scaled alpha_m*N^(-1/2)*(A_m*Q_m)^(1/6)",
            "quadraticCertificate": "||f||_6^6 <= A*Q, A=sum_h |C(h)|",
            "supportSurrogates": "A <= min(M*E^2, sqrt(D_C*Q)) <= min(M*E^2, sqrt(|S-S|*Q))",
        },
        "independentCheckCount": int(independent["checkCount"]),
        "primaryCheckCount": int(diagnostic["checkCount"]),
        "recordsSha256": diagnostic["recordsSha256"],
        "release": "R0.73S",
        "rowCount": int(diagnostic["rowCount"]),
        "schemaVersion": "r073s-quadratic-autocorrelation-certificate-v1",
        "scientificState": {
            "boundedQuarticFiniteGrid": "CLOSED",
            "classicalInequalityCollision": "CONFIRMED_OUTSIDE_CERTIFICATE",
            "exactFiniteFormulaGrid": "CLOSED",
            "heatFlowIntegration": "NOT_RUN",
            "navierStokesSimulation": "NOT_RUN",
            "pdeContinuumProof": "OUTSIDE_CERTIFICATE",
            "realDivergenceFreeLiftFiniteAudit": "CLOSED_ON_CONFIGURED_GRID",
            "runtimeLowerBound": "NOT_CLAIMED",
        },
    }
    (HERE / "certificate.json").write_text(canonical(certificate), encoding="utf-8")
    monitor("assembly-complete", primaryChecks=diagnostic["checkCount"], independentChecks=independent["checkCount"])
    print(canonical({
        "allPrerequisiteChecksPass": True,
        "independentChecks": independent["checkCount"],
        "primaryChecks": diagnostic["checkCount"],
        "rows": diagnostic["rowCount"],
    }), end="")


if __name__ == "__main__":
    main()
