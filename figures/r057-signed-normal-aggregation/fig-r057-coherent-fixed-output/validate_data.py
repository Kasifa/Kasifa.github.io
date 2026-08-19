#!/usr/bin/env python3
"""Validate the R0.57 figure tables and pinned formal provenance."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    metadata = json.loads((HERE / "figure-data-metadata.json").read_text(encoding="utf-8"))
    certificate_path = ROOT / metadata["formalCertificate"]["path"]
    certificate = json.loads(certificate_path.read_text(encoding="utf-8"))
    if sha256(certificate_path) != metadata["formalCertificate"]["sha256"]:
        raise AssertionError("formal certificate hash mismatch")
    if certificate["git"]["sourceCommit"] != metadata["formalCertificate"]["formalSourceCommit"]:
        raise AssertionError("formal source commit mismatch")
    if not all(certificate["checks"].values()):
        raise AssertionError("formal certificate contains a failed check")

    geometry = rows("packet-geometry.csv")
    if len(geometry) != 8:
        raise AssertionError("unexpected geometry row count")
    for row in geometry:
        index = int(row["N"])
        p = (int(row["pX"]), int(row["pY"]))
        q = (int(row["qX"]), int(row["qY"]))
        if p != (index, 0) or q != (-index, 1):
            raise AssertionError("frequency packet geometry mismatch")
        if (p[0] + q[0], p[1] + q[1]) != (0, 1):
            raise AssertionError("frequency pair does not sum to k")
        if row["forwardNormalContribution"] != "1" or row["reverseContribution"] != "0":
            raise AssertionError("channel contribution mismatch")

    localization = rows("localization.csv")
    if len(localization) != 19:
        raise AssertionError("unexpected localization row count")
    for row in localization:
        exponent = int(row["exponent"])
        packet_size = int(row["L"])
        if packet_size != 2**exponent:
            raise AssertionError("dyadic packet size mismatch")
        if int(row["scaleRatioNumerator"]) != 1 or int(row["scaleRatioDenominator"]) != packet_size:
            raise AssertionError("scale ratio mismatch")
        if int(row["capTangentNumerator"]) != 1 or int(row["capTangentDenominator"]) != packet_size:
            raise AssertionError("cap tangent mismatch")
        if not math.isclose(
            float(row["capAngleRadiansDecimal"]),
            math.atan(1 / packet_size),
            rel_tol=0,
            abs_tol=2e-17,
        ):
            raise AssertionError("cap angle presentation mismatch")
        if row["fixedOutputNormRatioDecimal"] != "1":
            raise AssertionError("fixed-output ratio is not one")
        if int(row["orderedPairs"]) != 2 * packet_size:
            raise AssertionError("ordered-pair count mismatch")

    heat = rows("heat-response.csv")
    if len(heat) != 81:
        raise AssertionError("unexpected heat row count")
    for row in heat:
        packet_size = int(row["L"])
        tau = float(row["scaledTimeTau"])
        time_value = tau / (packet_size * packet_size)
        expected = math.exp(-time_value) * sum(
            math.exp(-2 * index * index * time_value)
            for index in range(packet_size, 2 * packet_size)
        ) / packet_size
        if not math.isclose(
            float(row["normalizedOutput"]), expected, rel_tol=2e-15, abs_tol=2e-17
        ):
            raise AssertionError("heat response mismatch")
        if row["normalizedOutput"] != row["normalizedBlockNormProduct"]:
            raise AssertionError("heat equality was not serialized identically")
        if row["exactNormRatio"] != "1":
            raise AssertionError("heat norm ratio is not one")

    print(
        json.dumps(
            {
                "status": "passed",
                "formalChecks": len(certificate["checks"]),
                "geometryRows": len(geometry),
                "localizationRows": len(localization),
                "heatRows": len(heat),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()

