#!/usr/bin/env python3
"""Crosscheck the independent R0.72P exact-arithmetic audit routes."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import re
from typing import Any


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def normalized_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    return [
        {
            key: value.lower() if key == "passed" else value
            for key, value in row.items()
        }
        for row in rows
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate-dir", type=Path, required=True)
    parser.add_argument(
        "--allow-unsealed-source",
        action="store_true",
        help="allow a temporary run before the P sources are committed",
    )
    args = parser.parse_args()
    root = args.certificate_dir.resolve()

    producer_result = read_json(root / "producer-result.json")
    independent_result = read_json(root / "independent-result.json")
    producer_config = read_json(root / "producer-config.json")
    independent_config = read_json(root / "independent-config.json")
    producer_exact = read_json(root / "producer-exponents.json")
    independent_exact = read_json(root / "independent-exponents.json")
    producer_shape = read_csv(root / "producer-shape.csv")
    independent_shape = read_csv(root / "independent-shape.csv")
    producer_wall = read_csv(root / "producer-wall.csv")
    independent_wall = read_csv(root / "independent-wall.csv")

    source_commit = producer_config.get("gitCommit")
    source_commit_matches = (
        re.fullmatch(r"[0-9a-f]{40}", str(source_commit or "")) is not None
        and independent_config.get("gitCommit") == source_commit
    )
    formal_source_ready = all(
        (
            config.get("sourceTracked") is True
            and config.get("trackedChangesDirty") is False
        )
        for config in (producer_config, independent_config)
    )
    exact_equal = producer_exact == independent_exact
    shape_equal = normalized_rows(producer_shape) == normalized_rows(independent_shape)
    wall_equal = normalized_rows(producer_wall) == normalized_rows(independent_wall)

    claim = producer_exact["exponentLedger"]["claimContract"]
    integral_terminal = all(
        claim[name]["required"] is True
        and claim[name]["status"] == "proved-analytically-for-declared-class"
        for name in ("integratedEstimate", "terminalEstimate")
    )
    scope_preserved = (
        claim["status"] == "proved-for-declared-real-collinear-phase-1:2-class"
        and claim["arbitraryCommonBandStatus"] == "open"
        and claim["growingCarrierCountStatus"] == "open"
        and claim["finiteCertificateIsProof"] is False
        and claim["constantScope"] == "enhanced-dissipation-estimate"
        and claim["constantsMayDependOn"]
        == ["fixed upper shape class", "lambda_max"]
        and "lambda_minus" in claim["constantsIndependentOf"]
        and claim["physicalAmplitudeBalanceMayDependOn"] == ["lambda_minus"]
    )
    parameters = producer_exact["exponentLedger"]["parameters"]
    n2_p2 = parameters == {"B": "2/1", "N": "2/1", "pSquared": "1/2"}

    checks = {
        "producerPassed": producer_result.get("status") == "passed",
        "independentPassed": independent_result.get("status") == "passed",
        "sourceCommitMatches": source_commit_matches,
        "formalSourceReady": formal_source_ready,
        "sourceReadyOrExplicitlyAllowed": (
            formal_source_ready or args.allow_unsealed_source
        ),
        "exactLedgersIdentical": exact_equal,
        "shapeTablesIdentical": shape_equal,
        "wallTablesIdentical": wall_equal,
        "cellFactorExact": (
            producer_exact["cellFactor"]["rescaledCoefficientOverEpsilon"]
            == "1/1"
            and producer_exact["cellFactor"]["affineInvariantRow"]
            == "{(nR,q_*):n∈Z}"
            and producer_exact["cellFactor"]["rowIsomorphicTo"] == "RZ"
            and producer_exact["cellFactor"]["passed"] is True
        ),
        "shapeAndSlowBoundsExact": (
            producer_exact["shapeBounds"]["passed"] is True
            and producer_exact["slowThreshold"]["passed"] is True
        ),
        "integralAndTerminalContractPresent": integral_terminal,
        "claimScopePreserved": scope_preserved,
        "n2PSquaredLedgerExact": n2_p2,
        "morseWallIsApplicabilityOnly": (
            producer_exact["morseWall"]["absLambda"] == "1/4"
            and producer_exact["morseWall"]["status"]
            == "Morse-applicability-wall-only"
        ),
    }
    decisive_checks = {
        key: value for key, value in checks.items() if key != "formalSourceReady"
    }
    result = {
        "schemaVersion": 1,
        "status": "passed" if all(decisive_checks.values()) else "failed",
        "checks": checks,
        "sourceCommit": source_commit,
        "temporaryUnsealedSourceAllowed": args.allow_unsealed_source,
        "rowCounts": {
            "shape": len(producer_shape),
            "wall": len(producer_wall),
        },
        "limitations": (
            "Agreement audits finite exact algebra and claim wiring only. It "
            "does not replace the analytic full-superposition semigroup proof, "
            "the proof-level uniformity extraction, or a Navier-Stokes "
            "continuation theorem. A crosscheck produced with "
            "--allow-unsealed-source is temporary and must not enter a formal "
            "certificate bundle."
        ),
    }
    (root / "crosscheck.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2))
    if result["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
