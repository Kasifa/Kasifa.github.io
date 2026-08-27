#!/usr/bin/env python3
"""Fail-closed comparator for the two independent R0.72R audit routes."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def all_true(mapping: dict[str, Any]) -> bool:
    return bool(mapping) and all(value is True for value in mapping.values())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate-dir", type=Path, required=True)
    parser.add_argument(
        "--allow-unsealed-source",
        action="store_true",
        help="allow a temporary comparison before all R sources are committed",
    )
    args = parser.parse_args()
    root = args.certificate_dir.resolve()

    producer_config = read_json(root / "producer-config.json")
    independent_config = read_json(root / "independent-config.json")
    producer_result = read_json(root / "producer-result.json")
    independent_result = read_json(root / "independent-result.json")
    producer_payload = read_json(root / "producer-payload.json")
    independent_payload = read_json(root / "independent-payload.json")

    source_commit = producer_config.get("gitCommit")
    source_commit_matches = (
        re.fullmatch(r"[0-9a-f]{40}", str(source_commit or "")) is not None
        and independent_config.get("gitCommit") == source_commit
    )
    formal_source_ready = all(
        config.get("sourceTracked") is True
        and config.get("trackedChangesDirty") is False
        for config in (producer_config, independent_config)
    )

    payload = producer_payload
    polydisc = payload.get("polydisc", {})
    heat = payload.get("heatPath", {})
    perturbation = payload.get("perturbation", {})
    geometry = payload.get("criticalGeometry", {})
    shape = payload.get("shapeContract", {})
    derivatives = payload.get("derivativeLedger", {})
    incidence = payload.get("incidence", {})
    real_slice = payload.get("realSlice", {})
    boundary = payload.get("claimBoundary", {})

    checks = {
        "producerPassed": producer_result.get("status") == "passed",
        "independentPassed": independent_result.get("status") == "passed",
        "sourceCommitMatches": source_commit_matches,
        "formalSourceReady": formal_source_ready,
        "sourceReadyOrExplicitlyAllowed": formal_source_ready or args.allow_unsealed_source,
        "canonicalPayloadsIdentical": producer_payload == independent_payload,
        "payloadPassed": payload.get("passed") is True and all_true(payload.get("exactChecks", {})),
        "polydiscAndConeExitExact": (
            polydisc.get("centerZ2") == "3/20"
            and polydisc.get("radiusZ2") == "1/100"
            and polydisc.get("radiusZ3") == "1/1000"
            and polydisc.get("absZ2Range") == ["7/50", "4/25"]
            and polydisc.get("realDimension") == 4
            and polydisc.get("nonemptyInterior") is True
            and heat.get("q2InitialLower") == "14/25"
            and heat.get("coneExitMargin") == "3/50"
        ),
        "heatPathCrossingExact": (
            heat.get("q2AtY1UpperUsingEGreaterThanTwo") == "20489/256000"
            and heat.get("strictlyDecreasing") is True
            and heat.get("uniqueOldConeCrossingOnZeroOne") is True
        ),
        "perturbationLedgerExact": perturbation == {
            "centerSlopeFactorLower": "2/5",
            "d1": "23/1000",
            "d2": "49/1000",
            "d3": "107/1000",
        },
        "criticalGeometryExact": (
            geometry.get("criticalCount") == 2
            and geometry.get("criticalBoxes")
            == ["dist(phi,0)<pi/48", "dist(phi,pi)<pi/48"]
            and geometry.get("sinRadiusLower") == "1535/24576"
            and geometry.get("criticalSineUpper") == "23/400"
            and geometry.get("boundarySignMargin") == "3047/1536000"
            and geometry.get("normalizedCurvatureLower") == "1517/4500"
            and geometry.get("localQuarterMargin") == "103/3000"
            and geometry.get("piBoxOneFifthMargin") == "57/7000"
        ),
        "physicalShapeContractExact": (
            shape.get("radius") == "pi/48"
            and shape.get("criticalCount") == 2
            and shape.get("normalizedLocalSlope") == ["1/4", "5/3"]
            and shape.get("normalizedAwaySlopeLower") == "1/80"
            and shape.get("physicalWindow") == "0<=y<=1"
            and shape.get("physicalLocalSlope") == ["1/12", "5/3"]
            and shape.get("physicalAwaySlopeLower") == "1/240"
            and shape.get("C0") == "144/1"
            and shape.get("C1") == "240/1"
        ),
        "derivativeAndSlowLedgerExact": (
            [derivatives.get(f"d{index}") for index in range(4)]
            == ["1161/1000", "1323/1000", "1649/1000", "2307/1000"]
            and derivatives.get("sumW3Infinity") == "161/25"
            and derivatives.get("mixedBelowSevenThirdsMargin") == "79/3000"
            and derivatives.get("slowEtaThreshold") == "81/2401"
            and derivatives.get("slowEtaSymbolic") == "(3/7)^4"
            and derivatives.get("slowIdentityAtThreshold") == "27/343"
            and derivatives.get("completeThresholdAlsoRequiresEtaCH") is True
        ),
        "complexIncidenceExact": (
            incidence.get("gammaFixedZ3Coefficients")
            == ["1/8", "-3/8", "-15/8", "-3/8"]
            and incidence.get("gammaFixedZ3Exponents") == [-3, -1, 1, -5]
            and incidence.get("fPrimeCoefficients") == {"B": "0/1", "sin": "0/1"}
            and incidence.get("fSecondCoefficients") == {"A": "0/1", "cos": "0/1"}
            and incidence.get("fThirdCoefficients") == {"B": "15/1", "sin": "-3/1"}
            and incidence.get("fFourthCoefficients") == {"A": "45/1", "cos": "-3/1"}
            and incidence.get("degeneracyCondition") == "exists abs(u)=1: D(u)=D'(u)=0"
        ),
        "realSliceExact": (
            real_slice.get("q") == "12*b*x^2+4*a*x+1-3*b"
            and real_slice.get("delta") == "a^2+9*b^2-3*b"
            and real_slice.get("internalArc") == "delta=0 and 1/15<=b<=1/3"
            and real_slice.get("openInteriorArc") == "delta=0 and 1/15<b<=1/3"
            and real_slice.get("exactGridEvaluations") == 121
            and real_slice.get("degreeBoundEachVariable") == 10
            and real_slice.get("tensorGridIdentityProof") is True
        ),
        "claimBoundaryPreserved": (
            boundary.get("finiteCertificateIsContinuumProof") is False
            and boundary.get("completeFourDimensionalChamberClassification") is False
            and boundary.get("causticCrossingEnhancedDissipation") is False
            and boundary.get("arbitraryTimeDependentPhases") is False
            and boundary.get("uniformThirdCarrierAmplitudeFloor") is False
            and boundary.get("generalThreeDimensionalRegularity") is False
        ),
    }
    decisive = {key: value for key, value in checks.items() if key != "formalSourceReady"}
    result = {
        "schemaVersion": 1,
        "status": "passed" if all(decisive.values()) else "failed",
        "checks": checks,
        "sourceCommit": source_commit,
        "temporaryUnsealedSourceAllowed": args.allow_unsealed_source,
        "limitations": (
            "Exact agreement covers the finite coefficient, trigonometric-margin, "
            "shape, slow-time, incidence, and real-slice ledger only. It does not "
            "replace continuum root isolation, Coble--He enhanced dissipation, a "
            "global caustic decomposition, or Navier--Stokes regularity. A run made "
            "with --allow-unsealed-source is temporary and cannot be formally sealed."
        ),
    }
    (root / "crosscheck.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
