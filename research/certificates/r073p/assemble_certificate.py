#!/usr/bin/env python3
"""Assemble the R0.73P formula-diagnostic certificate."""

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


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    primary = json.loads((HERE / "diagnostic.json").read_text(encoding="utf-8"))
    independent = json.loads(
        (HERE / "independent_validation.json").read_text(encoding="utf-8")
    )
    boundary = config.get("claimBoundary")
    require(
        config.get("schemaVersion") == "r073p-formula-diagnostic-config-v1",
        "configuration schema drift",
    )
    require(
        primary.get("schemaVersion") == "r073p-formula-diagnostic-v1"
        and independent.get("schemaVersion")
        == "r073p-formula-diagnostic-independent-validation-v1",
        "diagnostic schema drift",
    )
    require(
        primary.get("allChecksPass") is True
        and all(primary.get("checks", {}).values()),
        "primary diagnostic did not pass",
    )
    require(
        independent.get("allChecksPass") is True
        and all(independent.get("checks", {}).values()),
        "independent diagnostic did not pass",
    )
    require(
        primary.get("claimBoundary") == boundary
        and independent.get("claimBoundary") == boundary,
        "claim-boundary drift",
    )
    require(
        independent.get("method", {}).get("producerCodeImported") is False
        and independent.get("method", {}).get("producerCodeCalled") is False,
        "independent path is not independent",
    )
    panel_c = primary["facts"]["panelC"]
    observations = independent["observations"]
    checks = {
        "primaryPassed": True,
        "independentPassed": True,
        "producerCodeNotImportedOrCalled": True,
        "figureCrossChecksPassed": all(
            primary["checks"][key]
            for key in (
                "figureConfigurationExact",
                "figureSourceRowsByteIdentical",
                "figureResultsCountsExact",
                "figureResultsCutoffExact",
                "figureValidationFormulaBoundaryConsistent",
            )
        )
        and all(
            independent["checks"][key]
            for key in (
                "figureSourceDataByteIdentical",
                "figureSourceDataHashIndependent",
                "figureConfigurationKeyValuesExact",
                "figureResultsIndependent",
                "figureClaimBoundaryConservative",
            )
        ),
        "cutoffGlobalEnclosurePassed": (
            panel_c["cutoffNormSquared"] == 4096
            and panel_c["continuousPeakNormSquaredAtMinimumTau"] == 1500.0
            and panel_c["tailStrictlyDecreasingBeyondCutoff"] is True
            and observations["representableRadiusCountThroughCutoff"] == 3414
        ),
        "sourceDataBound": (
            primary["sourceData"]["sha256"]
            == independent["sourceData"]["sha256"]
        ),
        "claimBoundaryExact": True,
    }
    require(all(checks.values()), "certificate assembly check failed")
    certificate = {
        "schemaVersion": "r073p-formula-diagnostic-certificate-v1",
        "release": "R0.73P",
        "status": "passed",
        "allChecksPass": True,
        "evidenceClass": config["evidenceClass"],
        "formulas": primary["formulas"],
        "exactStatements": {
            "thresholdScaling": ["N^-3", "N^-1/2"],
            "pureModePowers": {
                "L2": "-gamma",
                "H1/2": "1/2-gamma",
                "H3": "3-gamma",
            },
            "openGammaStrip": "1/2<gamma<3",
            "latticeObjective": "max_{k in Z^3 minus {0}} |k|^3 exp(-tau |k|^2)",
            "tauRange": [0.001, 10.0],
            "continuousUpperBound": "(3/(2 e tau))^(3/2)",
            "cutoffEnclosure": "4096 > 3/(2*0.001) = 1500",
        },
        "observations": {
            "sourceRows": primary["sourceData"]["rows"],
            "thresholdRows": primary["sourceData"]["thresholdRows"],
            "sobolevPowerRows": primary["sourceData"]["sobolevPowerRows"],
            "heatLatticeRows": primary["sourceData"]["heatLatticeRows"],
            "representableRadiusCountThroughCutoff": panel_c[
                "representableRadiusCountThroughCutoff"
            ],
            "minimumMaximizerNormSquared": panel_c[
                "minimumMaximizerNormSquared"
            ],
            "maximumMaximizerNormSquared": panel_c[
                "maximumMaximizerNormSquared"
            ],
            "minimumDiscreteToContinuousRatio": panel_c[
                "minimumDiscreteToContinuousRatio"
            ],
            "maximumDiscreteToContinuousRatio": panel_c[
                "maximumDiscreteToContinuousRatio"
            ],
        },
        "sourceData": primary["sourceData"],
        "figureBindings": primary["figureBindings"],
        "checks": checks,
        "inputBindings": [
            record(HERE / "config.json"),
            record(HERE / "diagnostic.json"),
            record(HERE / "independent_validation.json"),
            record(HERE / "source-data.csv"),
        ],
        "claimBoundary": boundary,
        "independentClaimBoundary": independent["claimBoundary"],
        "diagnosticOnly": True,
    }
    (HERE / "certificate.json").write_text(
        canonical(certificate), encoding="utf-8"
    )
    print(canonical({"status": "passed", "checks": len(checks), "inputs": 4}), end="")


if __name__ == "__main__":
    main()
