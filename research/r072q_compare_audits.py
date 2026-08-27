#!/usr/bin/env python3
"""Fail-closed crosscheck for the two independent R0.72Q audit routes."""

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
        help="allow a temporary comparison before all Q sources are committed",
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
    same_max_carrier = (
        isinstance(producer_config.get("maxCarrier"), int)
        and producer_config["maxCarrier"] >= 2
        and independent_config.get("maxCarrier") == producer_config["maxCarrier"]
        and producer_result.get("maxCarrier") == producer_config["maxCarrier"]
        and independent_result.get("maxCarrier") == producer_config["maxCarrier"]
    )

    payload = producer_payload
    shape = payload.get("shapeContract", {})
    geometry = shape.get("criticalGeometry", {})
    budgets = shape.get("jetBudgets", {})
    derivatives = shape.get("derivativeSupremumBounds", {})
    slow = shape.get("slowTime", {})
    envelope = shape.get("boundedEnvelopeCertificate", {})
    caustic = payload.get("twoCarrierCaustic", {})
    ray = caustic.get("rayIntersection", {})
    boundary = payload.get("claimBoundary", {})

    checks = {
        "producerPassed": producer_result.get("status") == "passed",
        "independentPassed": independent_result.get("status") == "passed",
        "sourceCommitMatches": source_commit_matches,
        "formalSourceReady": formal_source_ready,
        "sourceReadyOrExplicitlyAllowed": (
            formal_source_ready or args.allow_unsealed_source
        ),
        "maxCarrierMatches": same_max_carrier,
        "canonicalPayloadsIdentical": producer_payload == independent_payload,
        "payloadPassed": payload.get("passed") is True,
        "q2ImpliesQ1AndQ0": (
            budgets.get("Q2Upper") == "1/2"
            and budgets.get("Q1UpperDerived") == "1/4"
            and budgets.get("Q0UpperDerived") == "1/8"
            and all_true(shape.get("exactChecks", {}))
        ),
        "arbitraryPhaseTwoCriticalContract": (
            geometry.get("criticalCount") == 2
            and geometry.get("arbitraryPhaseUniform") is True
            and geometry.get("radius") == "pi/12"
            and geometry.get("C0") == "81/1"
            and geometry.get("C1") == "36/1"
            and geometry.get("localCurvatureMargin") == "(sqrt(3)-1)/2"
            and geometry.get("localCurvatureMarginGreaterThan") == "1/3"
            and geometry.get("normalizedShapeConstants")
            == {
                "C0": "9/1",
                "conservativeC0AlsoValid": "81/1",
                "C1": "12/1",
            }
            and geometry.get("physicalWindowShapeConstants")
            == {
                "yWindow": "0<=y<=1",
                "C0": "81/1",
                "C1": "36/1",
                "localSlopeLower": "1/9",
                "awaySlopeLower": "1/36",
            }
        ),
        "boundedEnvelopeLedgerExact": (
            envelope.get("partialSumDefinition") == "sum_{n=0}^4 1/n!"
            and envelope.get("partialSum") == "65/24"
            and envelope.get("partialSumExpected") == "65/24"
            and envelope.get("tailMajorantDefinition")
            == "sum_{k=0}^infinity 1/(5!*5^k)"
            and envelope.get("tailUpper") == "1/96"
            and envelope.get("tailUpperExpected") == "1/96"
            and envelope.get("eUpperCertificate") == "87/32"
            and envelope.get("eUpperReassembly") == "65/24+1/96=87/32"
            and envelope.get("eUpperLessThanThree") is True
            and envelope.get("expMinusOneLower") == "1/3"
            and envelope.get("normalizedLocalSlopeLower") == "1/3"
            and envelope.get("normalizedAwaySlopeLower") == "1/12"
            and envelope.get("physicalLocalSlopeLower") == "1/9"
            and envelope.get("physicalAwaySlopeLower") == "1/36"
            and envelope.get("passed") is True
        ),
        "derivativeLedgerExact": (
            derivatives.get("d0") == "9/8"
            and derivatives.get("d1") == "5/4"
            and derivatives.get("d2") == "3/2"
            and derivatives.get("d3Symbolic") == "1+M/2"
        ),
        "slowThresholdExact": (
            slow.get("etaThresholdSymbolic") == "(1+M/2)^(-4)"
            and slow.get("reducedCondition")
            == "(1+M/2)*eta^(1/4)<=1"
            and slow.get("passed") is True
        ),
        "causticParametrizationExact": (
            caustic.get("parametrization")
            == "z(phi)=(1/8)*exp(-3*i*phi)-(3/8)*exp(-i*phi)"
            and caustic.get("implicitEquation")
            == "(abs(z)^2-1/16)^3=(27/1024)*(Im(z))^2"
            and caustic.get("radiusRange") == ["1/4", "1/2"]
            and caustic.get("interiorDisk", {}).get("condition") == "abs(z)<1/4"
            and all_true(caustic.get("exactChecks", {}))
        ),
        "causticUniqueRayIntersectionExact": (
            ray.get("radialSquaredVariable") == "s=abs(z)^2"
            and ray.get("function") == "H(s)=(s-1/16)^3/s"
            and ray.get("rayEquation")
            == "H(s)=(27/1024)*sin(theta)^2"
            and ray.get("derivative")
            == "H'(s)=(s-1/16)^2*(2*s+1/16)/s^2"
            and ray.get("expandedDerivativeNumeratorCoefficients")
            == ["2/1", "-3/16", "0/1", "1/4096"]
            and ray.get("factoredDerivativeNumeratorCoefficients")
            == ["2/1", "-3/16", "0/1", "1/4096"]
            and ray.get("strictPositivityDomain") == "s>1/16"
            and ray.get("endpointValues")
            == {"H(1/16)": "0/1", "H(1/4)": "27/1024"}
            and ray.get("passed") is True
        ),
        "claimBoundaryPreserved": (
            boundary.get("fixedMRequired") is True
            and boundary.get("arbitraryPhases") is True
            and boundary.get("growingMStatus") == "open"
            and boundary.get("commonBandWithoutJetDominanceStatus") == "open"
            and boundary.get("finiteCertificateIsProof") is False
            and boundary.get("causticIsEDFailureCounterexample") is False
            and boundary.get("unnormalizedUniformCurvatureForUnboundedYClaimed")
            is False
        ),
    }
    decisive = {key: value for key, value in checks.items() if key != "formalSourceReady"}
    result = {
        "schemaVersion": 1,
        "status": "passed" if all(decisive.values()) else "failed",
        "checks": checks,
        "sourceCommit": source_commit,
        "maxCarrier": producer_config.get("maxCarrier"),
        "temporaryUnsealedSourceAllowed": args.allow_unsealed_source,
        "limitations": (
            "Exact agreement covers the finite jet, radical, slow-exponent, and "
            "caustic ledger only. It does not replace trigonometric root isolation, "
            "the continuum fixed-M Morse proof, the Coble--He theorem, or a "
            "Navier--Stokes continuation theorem. A run made with "
            "--allow-unsealed-source is temporary and cannot be formally sealed."
        ),
    }
    (root / "crosscheck.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
