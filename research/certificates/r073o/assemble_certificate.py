#!/usr/bin/env python3
"""Assemble the R0.73O finite Kolmogorov-spectrum certificate."""

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
        and independent.get("method", {}).get("producerCodeImported") is False
    ):
        raise RuntimeError("certificate prerequisites failed or boundary drifted")

    finite = primary["finiteResults"]
    other = independent["independentFiniteResults"]
    comparison = independent["producerComparison"]
    certificate = {
        "schemaVersion": "r073o-kolmogorov-spectrum-certificate-v1",
        "release": "R0.73O",
        "status": "passed",
        "allChecksPass": True,
        "evidenceClass": (
            "finite-fourier-diagnostic-with-independent-generalized-pencil-recomputation"
        ),
        "parameters": primary["parameters"],
        "externalRigorousInput": primary["externalRigorousInput"],
        "finiteResults": {
            "producerLeadingEigenvalueReal": finite["leadingEigenvalueReal"],
            "independentLeadingEigenvalueReal": other["leadingEigenvalueReal"],
            "producerPhysicalGrowthRate": finite["physicalGrowthRate"],
            "independentPhysicalGrowthRate": other["physicalGrowthRate"],
            "producerFiniteCriticalCrossing": finite["finiteCriticalCrossing"],
            "independentFiniteCriticalCrossing": other["finiteCriticalCrossing"],
            "producerRelativeResidual": finite["relativeResidual"],
            "independentEquilibratedRelativeResidual": other[
                "equilibratedRelativeGeneralizedResidual"
            ],
            "absoluteSigmaDifference": comparison["absoluteSigmaDifference"],
            "absoluteCriticalCrossingDifference": comparison[
                "absoluteFiniteCrossingDifference"
            ],
        },
        "sourceData": primary["sourceData"],
        "checks": {
            "primaryPassed": True,
            "independentPencilPassed": True,
            "producerCodeNotImported": True,
            "finiteSigmaPositiveOnBothPaths": (
                finite["leadingEigenvalueReal"] > 0.0
                and other["leadingEigenvalueReal"] > 0.0
            ),
            "finiteCriticalCrossingAgrees": (
                comparison["absoluteFiniteCrossingDifference"] < 5e-12
            ),
            "sourceDataBound": True,
            "claimBoundaryPreserved": True,
        },
        "inputBindings": [
            record(HERE / "config.json"),
            record(HERE / "diagnostic.json"),
            record(HERE / "independent_validation.json"),
            record(HERE / "source-data.csv"),
        ],
        "claimBoundary": config["claimBoundary"],
        "independentClaimBoundary": independent["claimBoundary"],
        "diagnosticOnly": True,
    }
    if not all(certificate["checks"].values()):
        raise RuntimeError("certificate assembly check failed")
    (HERE / "certificate.json").write_text(
        canonical(certificate), encoding="utf-8"
    )
    print(canonical({"status": "passed", "inputs": 4}), end="")


if __name__ == "__main__":
    main()
