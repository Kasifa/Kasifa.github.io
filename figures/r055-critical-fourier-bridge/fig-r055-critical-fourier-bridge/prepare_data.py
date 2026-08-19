#!/usr/bin/env python3
"""Prepare certificate-backed tables for the R0.55 journal figure."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import shutil
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CERTIFICATE = ROOT / "research/certificates/r055/fourier-critical-charge-bridge.json"
EXPECTED_CERTIFICATE_SHA256 = (
    "feacd0c47aa123d508f4889bfb1e6770c40da1fef6e438acc1aa9ecd99fc19ae"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(name: str, rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-commit", required=True)
    arguments = parser.parse_args()
    if re.fullmatch(r"[0-9a-f]{40}", arguments.source_commit) is None:
        raise SystemExit("--source-commit must be a full lowercase Git commit")
    started = time.perf_counter()

    if sha256(CERTIFICATE) != EXPECTED_CERTIFICATE_SHA256:
        raise SystemExit("R0.55 certificate hash mismatch")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if len(certificate["checks"]) != 17 or not all(certificate["checks"].values()):
        raise SystemExit("R0.55 certificate checks are incomplete")
    if certificate["git"]["sourceCommit"] != "640cf4ce9b97c2caa8d22f9159b4d0aa2e3a65a0":
        raise SystemExit("R0.55 formal source commit changed")

    print("[R0.55 figure] preparing exact critical-scaling samples", flush=True)
    scaling_rows: list[dict[str, object]] = []
    for index in range(81):
        sigma = Fraction(-2) + Fraction(index, 20)
        exponent = sigma + 1
        scaling_rows.append(
            {
                "sampleIndex": index,
                "sigmaExact": str(sigma),
                "sigmaDecimal": format(float(sigma), ".17g"),
                "spatialScalingExponentExact": str(exponent),
                "spatialScalingExponentDecimal": format(float(exponent), ".17g"),
                "classification": "exact change-of-variables presentation sample",
            }
        )
    write_csv("critical-scaling.csv", scaling_rows)

    print("[R0.55 figure] preparing the exact high-high-to-low family", flush=True)
    triad_rows: list[dict[str, object]] = []
    for index in range(1, 257):
        triad_rows.append(
            {
                "N": index,
                "leftFrequencySquaredExact": index * index,
                "rightFrequencySquaredExact": index * index + 1,
                "outputFrequencySquaredExact": 1,
                "criticalSymbolRatioExact": "1",
                "criticalSymbolRatioDecimal": "1.0",
                "minimumInputOutputSeparationExact": index,
                "minimumInputOutputSeparationDecimal": f"{index}.0",
                "classification": "formal all-index identity presentation row",
            }
        )
    write_csv("triad-saturation.csv", triad_rows)

    print("[R0.55 figure] recording the three bridge decisions", flush=True)
    bridge_rows = [
        {
            "order": 1,
            "route": "critical scalar degree majorant",
            "status": "finite",
            "basis": "X^-1 Fourier-Leray cancellation plus heat",
            "classification": "formal all-frequency upper bound",
        },
        {
            "order": 2,
            "route": "nontrivial scalar charge",
            "status": "impossible under both axioms",
            "basis": "convolution additivity plus rotation invariance implies chi=0",
            "classification": "formal algebraic no-go theorem",
        },
        {
            "order": 3,
            "route": "direction-resolved state",
            "status": "open",
            "basis": "retain shell, angle, and Leray polarization",
            "classification": "next research alternative; no theorem claimed",
        },
    ]
    write_csv("bridge-decisions.csv", bridge_rows)

    source_progress = ROOT / "research/certificates/r055/progress.ndjson"
    source_resources = ROOT / "research/certificates/r055/resources.csv"
    shutil.copyfile(source_progress, HERE / "progress.ndjson")
    shutil.copyfile(source_resources, HERE / "resources.csv")

    metadata = {
        "schemaVersion": "1.0",
        "createdUtc": datetime.now(timezone.utc).isoformat(),
        "figureSourceCommit": arguments.source_commit,
        "formalSourceCommit": certificate["git"]["sourceCommit"],
        "certificateSha256": EXPECTED_CERTIFICATE_SHA256,
        "certificateChecks": len(certificate["checks"]),
        "scalingRows": len(scaling_rows),
        "triadRows": len(triad_rows),
        "bridgeRows": len(bridge_rows),
        "formalTriadsChecked": certificate["exactSaturationFamily"]["finiteRegression"][
            "checkedTriads"
        ],
        "formalRotationWitnessesChecked": certificate["scalarChargeNoGo"][
            "finiteRegression"
        ]["integerVectorsChecked"],
        "triadRegressionSha256": certificate["exactSaturationFamily"][
            "finiteRegression"
        ]["recordsSha256"],
        "rotationRegressionSha256": certificate["scalarChargeNoGo"][
            "finiteRegression"
        ]["recordsSha256"],
        "catalanCoefficientSha256": certificate["scalarDegreeMajorant"][
            "coefficientDigestSha256"
        ],
        "formalStatements": {
            "criticalScaling": "||u_lambda||_X^sigma=lambda^(sigma+1)||u||_X^sigma",
            "duhamelBridge": "||T(u,v)||_E_nu<=nu^-1||u||_E_nu||v||_E_nu",
            "triadSaturation": "|k|^-1|B_k(a,b)|/(|a||b|)=1 for every positive integer N",
            "chargeNoGo": "additive and rotation-invariant scalar charge implies chi=0",
        },
        "displayRowsAreProof": False,
        "randomness": False,
        "floatingPointDecisionUse": False,
        "wallSeconds": time.perf_counter() - started,
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        "[R0.55 figure] wrote 81 scaling rows, 256 triads, and 3 bridge decisions",
        flush=True,
    )


if __name__ == "__main__":
    main()
