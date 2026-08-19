#!/usr/bin/env python3
"""Prepare deterministic presentation tables for the R0.57 formal figure."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform
import shutil
import subprocess
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CERTIFICATE_DIR = ROOT / "research" / "certificates" / "r057"
CERTIFICATE = CERTIFICATE_DIR / "signed-normal-aggregation.json"
FORMAL_PROGRESS = CERTIFICATE_DIR / "progress.ndjson"
FORMAL_RESOURCES = CERTIFICATE_DIR / "resources.csv"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def require_source_commit(expected: str) -> None:
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()
    if len(expected) != 40 or any(character not in "0123456789abcdef" for character in expected):
        raise AssertionError("--source-commit must be a full lowercase hash")
    if head != expected:
        raise AssertionError("the checked-out HEAD does not match --source-commit")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-commit", required=True)
    arguments = parser.parse_args()
    require_source_commit(arguments.source_commit)
    started = time.perf_counter()

    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate["git"]["sourceCommit"] != "001a40b166d20c912e78fca4d565c3e2eadd3203":
        raise AssertionError("unexpected formal source commit")
    if not all(certificate["checks"].values()):
        raise AssertionError("the formal certificate did not pass all checks")

    geometry_rows: list[dict[str, object]] = []
    presentation_l = 8
    for index in range(presentation_l, 2 * presentation_l):
        geometry_rows.append(
            {
                "N": index,
                "pX": index,
                "pY": 0,
                "qX": -index,
                "qY": 1,
                "kX": 0,
                "kY": 1,
                "forwardNormalContribution": 1,
                "reverseContribution": 0,
            }
        )
    write_csv(
        HERE / "packet-geometry.csv",
        [
            "N",
            "pX",
            "pY",
            "qX",
            "qY",
            "kX",
            "kY",
            "forwardNormalContribution",
            "reverseContribution",
        ],
        geometry_rows,
    )

    localization_rows: list[dict[str, object]] = []
    for exponent in range(19):
        packet_size = 2**exponent
        localization_rows.append(
            {
                "exponent": exponent,
                "L": packet_size,
                "scaleRatioNumerator": 1,
                "scaleRatioDenominator": packet_size,
                "scaleRatioDecimal": format(1 / packet_size, ".17g"),
                "capTangentNumerator": 1,
                "capTangentDenominator": packet_size,
                "capAngleRadiansDecimal": format(math.atan(1 / packet_size), ".17g"),
                "fixedOutputNormRatioNumerator": 1,
                "fixedOutputNormRatioDenominator": 1,
                "fixedOutputNormRatioDecimal": "1",
                "orderedPairs": 2 * packet_size,
            }
        )
    write_csv(
        HERE / "localization.csv",
        [
            "exponent",
            "L",
            "scaleRatioNumerator",
            "scaleRatioDenominator",
            "scaleRatioDecimal",
            "capTangentNumerator",
            "capTangentDenominator",
            "capAngleRadiansDecimal",
            "fixedOutputNormRatioNumerator",
            "fixedOutputNormRatioDenominator",
            "fixedOutputNormRatioDecimal",
            "orderedPairs",
        ],
        localization_rows,
    )

    heat_rows: list[dict[str, object]] = []
    heat_l = 64
    for step in range(81):
        tau = step / 20
        time_value = tau / (heat_l * heat_l)
        response = math.exp(-time_value) * sum(
            math.exp(-2 * index * index * time_value)
            for index in range(heat_l, 2 * heat_l)
        ) / heat_l
        heat_rows.append(
            {
                "step": step,
                "L": heat_l,
                "scaledTimeTau": format(tau, ".17g"),
                "physicalTimeNuEqualsOne": format(time_value, ".17g"),
                "normalizedOutput": format(response, ".17g"),
                "normalizedBlockNormProduct": format(response, ".17g"),
                "exactNormRatio": "1",
            }
        )
    write_csv(
        HERE / "heat-response.csv",
        [
            "step",
            "L",
            "scaledTimeTau",
            "physicalTimeNuEqualsOne",
            "normalizedOutput",
            "normalizedBlockNormProduct",
            "exactNormRatio",
        ],
        heat_rows,
    )

    shutil.copyfile(FORMAL_PROGRESS, HERE / "formal-progress.ndjson")
    shutil.copyfile(FORMAL_RESOURCES, HERE / "formal-resources.csv")

    metadata = {
        "schemaVersion": "1.0",
        "createdUtc": datetime.now(timezone.utc).isoformat(),
        "sourceCommit": arguments.source_commit,
        "formalCertificate": {
            "path": str(CERTIFICATE.relative_to(ROOT)),
            "sha256": sha256(CERTIFICATE),
            "formalSourceCommit": certificate["git"]["sourceCommit"],
            "checks": len(certificate["checks"]),
            "packetSize": certificate["finiteRegressions"]["coherentPacket"]["packetSize"],
            "orderedPairs": certificate["finiteRegressions"]["coherentPacket"]["orderedPairsAtOutput"],
            "familyIndices": certificate["finiteRegressions"]["allIndexFamily"]["indicesChecked"],
        },
        "presentationRows": {
            "geometry": len(geometry_rows),
            "localization": len(localization_rows),
            "heat": len(heat_rows),
        },
        "heatPresentation": {
            "packetSize": heat_l,
            "viscosity": 1,
            "scaledTimeDefinition": "tau=nu*L^2*t",
            "formula": "exp(-nu*t)*L^-1*sum_(N=L)^(2L-1) exp(-2*nu*N^2*t)",
            "classification": "floating-point presentation of an analytic equality; no formal decision uses these decimals",
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "randomness": False,
            "floatingPointDecisionUse": False,
        },
        "wallSeconds": time.perf_counter() - started,
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(
        json.dumps(
            {
                "status": "passed",
                "geometryRows": len(geometry_rows),
                "localizationRows": len(localization_rows),
                "heatRows": len(heat_rows),
                "wallSeconds": metadata["wallSeconds"],
            },
            sort_keys=True,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()

