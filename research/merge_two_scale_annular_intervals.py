#!/usr/bin/env python3
"""Merge disjoint R0.69W radial-row certificates with outward rounding."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def add_intervals(intervals: list[list[float]]) -> list[float]:
    return [
        math.nextafter(math.fsum(value[0] for value in intervals), -math.inf),
        math.nextafter(math.fsum(value[1] for value in intervals), math.inf),
    ]


def multiply(left: list[float], right: list[float]) -> list[float]:
    products = [
        left[0] * right[0],
        left[0] * right[1],
        left[1] * right[0],
        left[1] * right[1],
    ]
    return [math.nextafter(min(products), -math.inf), math.nextafter(max(products), math.inf)]


def subtract(left: list[float], right: list[float]) -> list[float]:
    return [
        math.nextafter(left[0] - right[1], -math.inf),
        math.nextafter(left[1] - right[0], math.inf),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--source-root", type=Path, default=Path.cwd())
    parser.add_argument("parts", nargs="+", type=Path)
    arguments = parser.parse_args()
    records = [json.loads(path.read_text(encoding="utf-8")) for path in arguments.parts]
    if not records:
        raise SystemExit("no partial certificates supplied")
    first = records[0]
    expected_workers = int(first["partial"]["workers"])
    worker_indices = sorted(int(record["partial"]["workerIndex"]) for record in records)
    if worker_indices != list(range(expected_workers)):
        raise SystemExit(
            f"worker coverage mismatch: expected 0..{expected_workers - 1}, got {worker_indices}"
        )
    invariant_keys = (
        "release",
        "claimBoundary",
        "mollifier",
        "symbolicAudits",
    )
    for record in records:
        if record.get("status") != "partial" or not record.get("partial", {}).get("enabled"):
            raise SystemExit("every input must be a partial certificate")
        for key in invariant_keys:
            if record.get(key) != first.get(key):
                raise SystemExit(f"partial invariant mismatch in {key}")
        if record["provenance"]["sourceCommit"] != first["provenance"]["sourceCommit"]:
            raise SystemExit("partial source commits differ")
        if record["provenance"]["scriptSha256"] != first["provenance"]["scriptSha256"]:
            raise SystemExit("partial producer hashes differ")
        if record["provenance"].get("sourceTreeDirty"):
            raise SystemExit("a partial run reported a dirty source tree")

    merged = json.loads(json.dumps(first))
    for annulus in ("j0", "jMinus2"):
        for degree in range(4):
            key = f"c{degree}"
            merged["coefficientIntervals"][annulus][key] = add_intervals(
                [record["coefficientIntervals"][annulus][key] for record in records]
            )
    j0 = merged["coefficientIntervals"]["j0"]
    jm2 = merged["coefficientIntervals"]["jMinus2"]
    c1, c2, c3 = j0["c1"], j0["c2"], j0["c3"]
    four_c1_c3 = multiply(c1, c3)
    four_c1_c3 = [
        math.nextafter(4 * four_c1_c3[0], -math.inf),
        math.nextafter(4 * four_c1_c3[1], math.inf),
    ]
    discriminant = subtract(multiply(c2, c2), four_c1_c3)
    endpoint = jm2["c0"]
    passed = bool(
        j0["c0"][0] <= 0 <= j0["c0"][1]
        and c3[1] < 0
        and discriminant[1] < 0
        and endpoint[1] < 0
    )
    merged["status"] = "passed" if passed else "failed"
    merged["decision"] = {
        "j0ConstantContainsExactZero": j0["c0"][0] <= 0 <= j0["c0"][1],
        "j0LeadingCoefficientStrictlyNegative": c3[1] < 0,
        "j0QuadraticDiscriminantInterval": discriminant,
        "j0QuadraticDiscriminantStrictlyNegative": discriminant[1] < 0,
        "jMinus2AtZeroInterval": endpoint,
        "jMinus2AtZeroStrictlyNegative": endpoint[1] < 0,
        "allPositiveAmplitudesHaveNegativeJ0": c3[1] < 0 and discriminant[1] < 0,
        "endpointHasNegativeJMinus2": endpoint[1] < 0,
        "entireAmplitudeFamilyExcluded": passed,
    }
    for annulus_key in ("0", "-2"):
        audits = [record["integrationAudits"][annulus_key] for record in records]
        merged["integrationAudits"][annulus_key] = {
            "rule": audits[0]["rule"],
            "radialCells": audits[0]["radialCells"],
            "momentPrimitivePower": audits[0]["momentPrimitivePower"],
            "momentPrimitiveCells": audits[0]["momentPrimitiveCells"],
            "evaluatedRadialBoxes": sum(audit["evaluatedRadialBoxes"] for audit in audits),
            "maximumPointwiseThirdOrderRemainders": [
                max(audit["maximumPointwiseThirdOrderRemainders"][degree] for audit in audits)
                for degree in range(4)
            ],
            "workers": expected_workers,
            "allRowsCoveredExactlyOnce": True,
        }
    merged["method"]["workers"] = expected_workers
    merged["method"]["workerIndex"] = None
    merged["method"]["executionMode"] = "parallel disjoint radial rows, outward-rounded merge"
    merged["partial"] = {
        "enabled": False,
        "mergedWorkers": expected_workers,
        "allRowsCoveredExactlyOnce": True,
    }
    combiner = arguments.source_root / "research/merge_two_scale_annular_intervals.py"
    merged["provenance"]["combinerScript"] = str(
        combiner.resolve().relative_to(arguments.source_root.resolve())
    )
    merged["provenance"]["combinerScriptSha256"] = sha256(combiner)
    merged["provenance"]["partialCertificates"] = [
        {
            "workerIndex": int(record["partial"]["workerIndex"]),
            "path": str(path),
            "sha256": sha256(path),
        }
        for path, record in sorted(
            zip(arguments.parts, records), key=lambda item: item[1]["partial"]["workerIndex"]
        )
    ]
    merged["runtime"] = {
        "parallelWorkerMaximumElapsedSeconds": max(
            record["runtime"]["elapsedSeconds"] for record in records
        ),
        "parallelWorkerSumElapsedSeconds": sum(
            record["runtime"]["elapsedSeconds"] for record in records
        ),
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(merged, indent=2, sort_keys=True) + "\n")
    print(json.dumps(merged["decision"], indent=2, sort_keys=True))
    print(json.dumps({"status": merged["status"], "output": str(arguments.output)}, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
