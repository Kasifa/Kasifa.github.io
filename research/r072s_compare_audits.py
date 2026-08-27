#!/usr/bin/env python3
"""Fail-closed comparator for the two independent R0.72S audit routes."""

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
        "--allow-unsealed", "--allow-unsealed-source",
        dest="allow_unsealed_source", action="store_true",
        help="allow a temporary comparison before all R0.72S sources are committed",
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
    strata = payload.get("incidenceStrata", {})
    miniversality = payload.get("restrictedMiniversality", {})
    a2 = payload.get("a2HeatPath", {})
    a3 = payload.get("a3HeatPath", {})
    benchmarks = payload.get("stationaryBenchmarks", {})
    heat_identity = payload.get("heatEquationIdentity", {})
    boundary = payload.get("claimBoundary", {})

    checks = {
        "producerPassed": producer_result.get("status") == "passed",
        "independentPassed": independent_result.get("status") == "passed",
        "sourceCommitMatches": source_commit_matches,
        "formalSourceReady": formal_source_ready,
        "sourceReadyOrExplicitlyAllowed": formal_source_ready or args.allow_unsealed_source,
        "canonicalPayloadsIdentical": producer_payload == independent_payload,
        "payloadPassed": payload.get("passed") is True and all_true(payload.get("exactChecks", {})),
        "incidencePartitionExact": (
            [entry.get("type") for entry in strata.get("partition", [])]
            == ["A2", "A3", "A4", "A5"]
            and [entry.get("localCodimension") for entry in strata.get("partition", [])]
            == [1, 2, 3, 4]
            and strata.get("f5OnA4Closure") == "-24*sin(phi)"
            and strata.get("f6AtA5") == "-24*cos(phi)"
            and strata.get("higherThanA5Occurs") is False
            and strata.get("classificationTarget") == "incidence-preimages-not-global-image"
        ),
        "incidenceJetsExact": strata.get("jetCoefficients") == {
            "f3": {"B": "15/1", "sin": "-3/1"},
            "f4": {"A": "45/1", "cos": "-3/1"},
            "f5": {"B": "-195/1", "sin": "15/1"},
            "f6": {"A": "-585/1", "cos": "15/1"},
        },
        "restrictedMiniversalityExact": (
            miniversality.get("coefficientOrder")
            == ["Re(z2)", "Im(z2)", "Re(z3)", "Im(z3)"]
            and miniversality.get("derivativeOrders") == [1, 2, 3, 4]
            and miniversality.get("coefficientDerivativeJetAtPhiZero") == [
                [0, -2, 0, -3],
                [-4, 0, -9, 0],
                [0, 8, 0, 27],
                [16, 0, 81, 0],
            ]
            and miniversality.get("coefficientDerivativeJetDeterminant") == "5400/1"
            and miniversality.get("localCodimensions")
            == {"A2": 1, "A3": 2, "A4": 3, "A5": 4}
            and miniversality.get("moduloAdditiveConstants") is True
            and miniversality.get("fullA5MiniversalParameterCountIncludingConstant") == 5
            and miniversality.get("globalEmbeddedStratificationClaimed") is False
        ),
        "a2DerivedLedgerConsistent": (
            a2.get("z20") == ["0/1", "4/1"]
            and a2.get("z30") == ["0/1", "0/1"]
            and a2.get("crossingY") == "log(2)"
            and a2.get("crossingPhi") == "pi/2"
            and a2.get("crossingZ2") == ["0/1", "1/2"]
            and a2.get("otherSineAtCrossing") == "-1/2"
            and a2.get("crossingPowerIdentity")
            == {"tau": "1/2", "8TauCubed": "1/1"}
            and a2.get("kLogDerivative") == "-3/1"
            and a2.get("representativeK")
            == {"before": "2/1", "at": "1/1", "after": "1/2"}
            and a2.get("distinctCriticalCounts") == {"before": 4, "at": 3, "after": 2}
            and a2.get("criticalCountWithMultiplicityAtCrossing") == 4
            and a2.get("uniqueDegenerateEventForYNonnegative") is True
            and a2.get("allNoncollisionCriticalPointsSimple") is True
            and a2.get("fThird") == "-3/1"
            and a2.get("dyFPrime") == "-3/1"
            and a2.get("splitXiSquaredPerDelta") == "-2/1"
            and a2.get("fullCoefficientSpaceTransverse") is True
            and a2.get("thirdCarrierActive") is False
        ),
        "a2FiniteGuardInputsExact": a2.get("globalSignGuards") == {
            "pAtMinusOne": {"constant": "1/1", "k": "1/1"},
            "pAtZero": {"k": "-1/1"},
            "pAtOne": {"constant": "-1/1", "k": "1/1"},
            "rootProduct": "-1/2",
            "offAxisDegeneracyAfterMultiplyBy8k": {
                "constant": "-1/1", "kSquared": "-8/1",
            },
        },
        "a3DerivedLedgerConsistent": (
            a3.get("a0") == "-2563/1280"
            and a3.get("b0") == "1/30"
            and a3.get("monotonicityParentUpper") == "-2307/1280"
            and a3.get("crossingTau") == "1/2"
            and a3.get("crossingA") == "-2563/10240"
            and a3.get("crossingB") == "1/7680"
            and a3.get("crossingPowerIdentities")
            == {"tauCubed": "1/8", "tauEighth": "1/256"}
            and a3.get("representativeTau")
            == {"before": "3/4", "at": "1/2", "after": "1/4"}
            and a3.get("hAtCrossing") == "0/1"
            and a3.get("qXAtCrossing") == "-511/512"
            and a3.get("hYAtCrossing") == "1533/512"
            and a3.get("fFourth") == "-1533/512"
            and a3.get("dyFSecond") == "-1533/512"
            and a3.get("splitPhiSquaredPerDelta") == "-6/1"
            and a3.get("distinctCriticalCounts") == {"before": 4, "at": 2, "after": 2}
            and a3.get("criticalCountWithMultiplicityAtCrossing") == 4
            and a3.get("thirdCarrierActive") is True
            and a3.get("realEvenSliceTransverse") is True
            and a3.get("fullCoefficientSpaceTransverse") is False
        ),
        "a3FiniteGuardInputsExact": a3.get("globalSignGuards") == {
            "qMinusOneCoefficients": ["1/1", "2563/320", "3/10"],
            "qXUpperParentAtTauOne": "-2307/1280",
            "hTauDerivativeParentAtTauOne": "-2307/1280",
        },
        "heatEquationIdentityExact": heat_identity == {
            "identity": "partial_y F=partial_phi^2 F+F",
            "harmonicDecayExponents": {"n1": 0, "n2": 3, "n3": 8},
            "onIncidence": ["partial_y F'=F'''", "partial_y F''=F''''"],
        },
        "stationaryBoundaryExact": (
            benchmarks.get("A2DecayRate") == "nu^(3/5)"
            and benchmarks.get("A3DecayRate") == "nu^(2/3)"
            and benchmarks.get("nonautonomousCollisionEstimateProved") is False
        ),
        "claimBoundaryPreserved": (
            boundary.get("finiteCertificateIsContinuumProof") is False
            and boundary.get("completeGlobalCausticImageClassification") is False
            and boundary.get("allIncidenceSelfIntersectionsClassified") is False
            and boundary.get("causticCrossingEnhancedDissipation") is False
            and boundary.get("generalThreeDimensionalRegularity") is False
            and boundary.get("clayMillenniumProblemSolved") is False
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
            "Exact agreement covers only finite incidence jets, restricted "
            "miniversality, crossing-power identities, nonzero jets, representative "
            "evaluations, sign/monotonicity guards, and the heat identity. The "
            "continuous report proof—not this comparator—derives event uniqueness, "
            "global counts, simplicity, and transversality. It does not "
            "classify global caustic self-intersections, prove enhanced dissipation "
            "through a collision, or imply Navier--Stokes regularity."
        ),
    }
    (root / "crosscheck.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if result["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
