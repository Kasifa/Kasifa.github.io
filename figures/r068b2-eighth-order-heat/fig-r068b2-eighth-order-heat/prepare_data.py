#!/usr/bin/env python3
"""Extract Figure R0.68B-2 data from the pinned research archives."""

from __future__ import annotations

import csv
import hashlib
import json
import resource
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ONE_CYCLE = ROOT / "research/certificates/r068b2a/eighth-order-heat-one-cycle-audit.json"
JET = ROOT / "research/certificates/r068b2b-pilot/eighth-order-heat-jet-pilot.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    started = time.perf_counter()
    one_cycle = json.loads(ONE_CYCLE.read_text())
    jet = json.loads(JET.read_text())
    state_counts = one_cycle["dynamicProgram"]["stateCountsByDepth"]
    transition_counts = one_cycle["dynamicProgram"]["transitionCountsByDepth"]
    write_rows(
        HERE / "state-compression.csv",
        ["depth", "stateCount", "transitionCount"],
        [
            {
                "depth": depth,
                "stateCount": state_count,
                "transitionCount": transition_count,
            }
            for depth, (state_count, transition_count) in enumerate(
                zip(state_counts, transition_counts), start=1
            )
        ],
    )
    partial = jet["heatJet"]["partialByDegree"]
    previous = None
    jet_rows = []
    for record in partial:
        value = float(record["value"])
        jet_rows.append(
            {
                "degree": record["degree"],
                "value": f"{value:.17e}",
                "scaledValueTimes1e8": f"{value * 1e8:.17e}",
                "increment": "" if previous is None else f"{value - previous:.17e}",
                "absoluteIncrement": "" if previous is None else f"{abs(value - previous):.17e}",
            }
        )
        previous = value
    write_rows(
        HERE / "jet-convergence.csv",
        ["degree", "value", "scaledValueTimes1e8", "increment", "absoluteIncrement"],
        jet_rows,
    )
    write_rows(
        HERE / "moment-residuals.csv",
        ["degree", "cumulativeChannels", "neumannTerms", "relativeLinearResidual"],
        [
            {
                "degree": record["degree"],
                "cumulativeChannels": record["cumulativeChannels"],
                "neumannTerms": record["neumannTerms"],
                "relativeLinearResidual": f"{float(record['relativeLinearResidual']):.17e}",
            }
            for record in jet["momentLift"]
        ],
    )
    summary = [{
        "validCarrierTuples": one_cycle["parameters"]["validCarrierTuples"],
        "signedPaths": one_cycle["parameters"]["signedPaths"],
        "maximumRetainedStates": max(state_counts),
        "finalRetainedStates": state_counts[-1],
        "oneCycleLower": one_cycle["exactTaylor"]["finalLowerDisplay"],
        "oneCycleUpper": one_cycle["exactTaylor"]["finalUpperDisplay"],
        "oneCycleTail": one_cycle["exactTaylor"]["absoluteTailBoundDisplay"],
        "degreeEightJetPilot": jet["heatJet"]["finalPilotValue"],
        "heatOrderCrossCheck": jet["heatJet"]["heatOrderCrossCheckMaximumDifference"],
    }]
    write_rows(
        HERE / "certified-summary.csv",
        list(summary[0]),
        summary,
    )
    metadata = {
        "oneCycleCertificate": str(ONE_CYCLE.relative_to(ROOT)),
        "oneCycleSha256": digest(ONE_CYCLE),
        "oneCycleSourceCommit": one_cycle["provenance"]["sourceCommit"],
        "jetPilotArchive": str(JET.relative_to(ROOT)),
        "jetPilotSha256": digest(JET),
        "jetPilotSourceCommit": jet["provenance"]["sourceCommit"],
        "oneCycleArchiveCommit": "ccd31ce7fc83bf0134b9f0bcdb47fa476af9bf61",
        "jetPilotArchiveCommit": "32f6ba3353ebf9875b8d9a337ded05ae7b0934e1",
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n"
    )
    write_rows(
        HERE / "figure-data-resources.csv",
        ["elapsedSeconds", "maximumRssMiB", "status"],
        [{
            "elapsedSeconds": f"{time.perf_counter() - started:.6f}",
            "maximumRssMiB": f"{resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024):.3f}",
            "status": "passed",
        }],
    )


if __name__ == "__main__":
    main()
