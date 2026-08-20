#!/usr/bin/env python3
"""Independently verify the archived R0.68B-2h certificate relations."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path


EXPECTED_SOURCE_COMMIT = "efd0d828678ce99fcc5d0f40d751b1883d32f740"
EXPECTED_SOURCE_SHA256 = (
    "487947432d9d4de172004ee4ebbb8ebdc8d1a4ac86d13b657af4da7b3c4336e4"
)
EXPECTED_DEFECT_MANIFEST = (
    "edfb110c8cd7f8369be4d5748cb798d9ca72864a8e35b1146c790662f2acacfc"
)
EXPECTED_MOMENT_RADIUS = (
    "437a8f18234fb8c07ea23661a77e3413eee4dbb674e4dcefd83a17d386a268bf"
)
EXPECTED_HEAT_RADIUS = (
    "ab121c7f974542d42652d823410d23f2bda2502c5960479463206fed80b6432e"
)
CARRY_WEIGHT_AT_OBSERVABLE = Decimal(3_769_909_270)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json_decimal(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(), parse_float=Decimal)


def read_hashes(path: Path) -> dict[str, str]:
    output: dict[str, str] = {}
    for line in path.read_text().splitlines():
        digest, name = line.split(maxsplit=1)
        output[name.strip()] = digest
    return output


def expanded_decimal(
    value: Decimal,
    direction: float,
    steps: int = 8,
) -> Decimal:
    """Expand a serialized binary64 endpoint by a small explicit ULP budget."""
    output = float(value)
    for _ in range(steps):
        output = math.nextafter(output, direction)
    return Decimal.from_float(output)


def verify_payload(data_directory: Path) -> tuple[int, int]:
    manifest = data_directory / "payload-manifest.sha256"
    count = 0
    total = 0
    for line in manifest.read_text().splitlines():
        digest, size, name = line.split(maxsplit=2)
        path = data_directory / name
        assert path.is_file(), f"missing defect payload {name}"
        assert path.stat().st_size == int(size), f"size mismatch for {name}"
        assert sha256_file(path) == digest, f"hash mismatch for {name}"
        count += 1
        total += int(size)
    return count, total


def normalized_replica(summary: dict[str, object]) -> dict[str, object]:
    output = json.loads(json.dumps(summary, default=str), parse_float=Decimal)
    output.pop("elapsedSeconds", None)
    output["provenance"].pop("sourceCommit", None)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--summary", required=True, type=Path)
    parser.add_argument("--metadata", required=True, type=Path)
    parser.add_argument("--data-directory", required=True, type=Path)
    parser.add_argument("--moment-hashes", required=True, type=Path)
    parser.add_argument("--heat-hashes", required=True, type=Path)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--audit-summary", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()

    summary = read_json_decimal(arguments.summary)
    metadata = json.loads(arguments.metadata.read_text())
    audit_summary = read_json_decimal(arguments.audit_summary)
    moment_hashes = read_hashes(arguments.moment_hashes)
    heat_hashes = read_hashes(arguments.heat_hashes)

    payload_count, payload_bytes = verify_payload(arguments.data_directory)
    payload_manifest_hash = sha256_file(
        arguments.data_directory / "payload-manifest.sha256"
    )
    source_hash = sha256_file(arguments.source)

    assert source_hash == EXPECTED_SOURCE_SHA256
    assert payload_manifest_hash == EXPECTED_DEFECT_MANIFEST
    assert metadata["payloadManifest"] == {
        "fileCount": payload_count,
        "totalBytes": payload_bytes,
        "manifestSha256": payload_manifest_hash,
    }
    assert metadata["signatureClasses"] == 44_514
    assert metadata["coveredFreeShifts"] == 16**6
    assert metadata["maximumAbsoluteSignatureEntry"] == 1
    assert metadata["maximumSignatureNonzeros"] == 7
    assert metadata["absolutePathCycle"] == {
        "rows": 1792,
        "columns": 1792,
        "nonzeros": 695_808,
        "maximumEntry": 134_512,
        "maximumRowSum": 54_210_304,
    }
    assert all(
        check["agreesWithSparseCycleEntries"]
        for check in metadata["signatureSpotChecks"]
    )

    provenance = summary["provenance"]
    assert provenance["sourceCommit"] == EXPECTED_SOURCE_COMMIT
    assert provenance["defectPayloadManifestSha256"] == payload_manifest_hash
    assert provenance["centredMomentRadiusSha256"] == EXPECTED_MOMENT_RADIUS
    assert provenance["heatCoefficientRadiusSha256"] == EXPECTED_HEAT_RADIUS
    assert moment_hashes["centred-radius.f128"] == EXPECTED_MOMENT_RADIUS
    assert heat_hashes["heat-coefficient-radius.f128"] == EXPECTED_HEAT_RADIUS
    assert summary["status"] == "strict-passed"
    assert all(summary["checks"].values())
    assert summary["parameters"] == {
        "signatureClasses": 44_514,
        "coveredFreeShifts": 16**6,
        "channels": 8_008,
        "states": 1_792,
        "derivativeOrder": 11,
    }

    with localcontext() as context:
        context.prec = 100
        root = summary["resolvent"]["rootLower"]
        contraction = summary["resolvent"]["remainderContraction"]
        ratio = summary["resolvent"]["ratioUpper"]
        observable = summary["observableDefectUpper"]
        weighted = summary["unaggregated"]["weightedMaximumUpper"]
        resolvent_observable = summary["resolvent"]["observableUpper"]
        derivative = summary["derivativeUpper"]
        correction = summary["derivativeCorrectionUpper"]
        heat = summary["heatJet"]
        corrected = summary["correctedDominantHeat"]

        assert root > 0
        assert contraction == Decimal(1) / Decimal(2**20)
        assert 0 < ratio < 1
        assert ratio >= contraction / root
        reconstructed_resolvent = (
            observable / root
            + CARRY_WEIGHT_AT_OBSERVABLE
            * weighted
            / root
            * ratio
            / (Decimal(1) - ratio)
        )
        assert resolvent_observable >= reconstructed_resolvent

        derivative_exact = Fraction(
            int(metadata["derivativeUpper"]["numerator"]),
            int(metadata["derivativeUpper"]["denominator"]),
        )
        derivative_exact_decimal = (
            Decimal(derivative_exact.numerator)
            / Decimal(derivative_exact.denominator)
        )
        assert derivative >= derivative_exact_decimal
        # JSON stores outward-rounded binary64 renderings of binary128 values.
        # Eight binary64 ULPs enclose the rendered operands and the short
        # chain of rendered results; this is only a serialization consistency
        # check, while the guarded binary128 engine establishes the bound.
        assert expanded_decimal(correction, math.inf) >= (
            resolvent_observable * derivative
        )
        assert heat["radiusUpper"] >= 0
        assert expanded_decimal(heat["lower"], -math.inf) <= (
            heat["centre"] - heat["radiusUpper"]
        )
        assert expanded_decimal(heat["upper"], math.inf) >= (
            heat["centre"] + heat["radiusUpper"]
        )
        assert expanded_decimal(corrected["lower"], -math.inf) <= (
            heat["lower"] - correction
        )
        assert expanded_decimal(corrected["upper"], math.inf) >= (
            heat["upper"] + correction
        )
        assert corrected["upper"] < 0

    assert normalized_replica(summary) == normalized_replica(audit_summary)

    report = {
        "schemaVersion": "1.0",
        "status": "strict-passed",
        "verifier": "independent Decimal and SHA-256 relation audit",
        "checks": {
            "allDefectPayloadHashesAndSizesMatch": True,
            "metadataAndCombinatorialCountsMatch": True,
            "absolutePathCycleMetadataMatches": True,
            "sourceHashMatches": True,
            "upstreamMomentAndHeatHashesMatch": True,
            "resolventUpperRelationHolds": True,
            "serializedDerivativeCorrectionIsEightUlpConsistent": True,
            "serializedCorrectedIntervalIsEightUlpConsistent": True,
            "correctedUpperEndpointIsStrictlyNegative": True,
            "sourceUnlockedAuditAndSourceLockedRunMatch": True,
        },
        "provenance": {
            "sourceCommit": EXPECTED_SOURCE_COMMIT,
            "sourceSha256": source_hash,
            "defectPayloadManifestSha256": payload_manifest_hash,
            "formalSummarySha256": sha256_file(arguments.summary),
            "auditSummarySha256": sha256_file(arguments.audit_summary),
        },
        "parameters": {
            "payloadFiles": payload_count,
            "payloadBytes": payload_bytes,
            "signatureClasses": metadata["signatureClasses"],
            "coveredFreeShifts": metadata["coveredFreeShifts"],
        },
        "correctedDominantHeat": summary["correctedDominantHeat"],
        "boundary": (
            "This verifies one fixed eighth-order coefficient only; it does "
            "not control all Picard orders or prove 3D Navier-Stokes regularity."
        ),
    }
    arguments.output.write_text(
        json.dumps(report, indent=2, default=str) + "\n"
    )
    print(json.dumps(report, indent=2, default=str))


if __name__ == "__main__":
    main()
