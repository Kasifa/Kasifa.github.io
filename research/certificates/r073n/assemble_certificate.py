#!/usr/bin/env python3
"""Assemble the R0.73N finite diagnostic certificate."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(path: Path) -> dict[str, object]:
    return {"path": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}


def main() -> None:
    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    primary = json.loads((HERE / "diagnostic.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (HERE / "independent_validation.json").read_text(encoding="utf-8")
    )
    if not (
        primary.get("allChecksPass") is True
        and independent.get("allChecksPass") is True
        and primary.get("claimBoundary") == config.get("claimBoundary")
        and independent.get("claimBoundary") == config.get("claimBoundary")
    ):
        raise RuntimeError("certificate prerequisites failed or boundary drifted")
    certificate = {
        "schemaVersion": "r073n-finite-strain-certificate-v1",
        "release": "R0.73N",
        "status": "passed",
        "allChecksPass": True,
        "evidenceClass": config["evidenceClass"],
        "exactStatements": {
            "normalizedHalfStrainEnvelope": "exp(-4t)+exp(-16t)",
            "cumulativeJ": "(1-exp(-4T))/4+(1-exp(-16T))/16",
            "jInfinity": "5/16",
            "strictChain": "j_*>359/324000>173/450000>A_*",
            "strictChainLastStepProvenance": "sealed R0.73M action upper bound",
        },
        "highPrecision": primary["highPrecision"],
        "sourceData": primary["sourceData"],
        "independentValidationCount": len(independent["validations"]),
        "checks": {
            "primaryPassed": True,
            "independentDecimalReconstructionPassed": True,
            "exactRationalChainPassed": True,
            "highPrecisionJStarPassed": True,
            "sourceDataBound": True,
            "claimBoundaryExact": True,
        },
        "inputBindings": [
            record(HERE / "config.json"),
            record(HERE / "diagnostic.json"),
            record(HERE / "independent_validation.json"),
            record(HERE / "source-data.csv"),
        ],
        "claimBoundary": config["claimBoundary"],
        "diagnosticOnly": True,
    }
    (HERE / "certificate.json").write_text(canonical(certificate), encoding="utf-8")
    print(canonical({"status": "passed", "inputs": 4}), end="")


if __name__ == "__main__":
    main()
