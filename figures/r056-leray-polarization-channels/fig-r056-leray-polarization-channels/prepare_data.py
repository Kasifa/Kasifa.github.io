#!/usr/bin/env python3
"""Prepare certificate-backed exact tables for the R0.56 journal figure."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CERTIFICATE = ROOT / "research/certificates/r056/leray-polarization-channels.json"
EXPECTED_CERTIFICATE_SHA256 = (
    "ff0b68729476dfc2d8e53d1483c7a29b383914a5dd8ba761502c57534858fafe"
)
FORMAL_SOURCE_COMMIT = "1b736121127e91727b8ab7ff1b2fd90c2ee873f6"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(name: str, rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def exact_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-commit", required=True)
    arguments = parser.parse_args()
    if re.fullmatch(r"[0-9a-f]{40}", arguments.source_commit) is None:
        raise SystemExit("--source-commit must be a full lowercase Git commit")
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()
    if head != arguments.source_commit:
        raise SystemExit("checked-out HEAD does not match --source-commit")
    started = time.perf_counter()

    if sha256(CERTIFICATE) != EXPECTED_CERTIFICATE_SHA256:
        raise SystemExit("R0.56 certificate hash mismatch")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if len(certificate["checks"]) != 21 or not all(certificate["checks"].values()):
        raise SystemExit("R0.56 certificate checks are incomplete")
    if certificate["git"]["sourceCommit"] != FORMAL_SOURCE_COMMIT:
        raise SystemExit("R0.56 formal source commit changed")

    print("[R0.56 figure] preparing the epsilon=1/8 channel profile", flush=True)
    profile_rows: list[dict[str, object]] = []
    epsilon = Fraction(1, 8)
    for index in range(801):
        mu = Fraction(-1) + Fraction(index, 400)
        normal_squared = 1 - mu * mu
        parallel = epsilon - mu
        denominator = normal_squared + parallel * parallel
        planar_squared = (
            Fraction(0)
            if normal_squared == 0
            else normal_squared * parallel * parallel / denominator
        )
        profile_rows.append(
            {
                "sampleIndex": index,
                "epsilonExact": exact_text(epsilon),
                "muExact": exact_text(mu),
                "muDecimal": format(float(mu), ".17g"),
                "normalGainSquaredExact": exact_text(normal_squared),
                "normalGainDecimal": format(math.sqrt(float(normal_squared)), ".17g"),
                "planarGainSquaredExact": exact_text(planar_squared),
                "planarGainDecimal": format(math.sqrt(float(planar_squared)), ".17g"),
                "formalPlanarUpperBoundExact": "9/16",
                "classification": "exact squared-gain presentation row",
            }
        )
    write_csv("channel-profile.csv", profile_rows)

    print("[R0.56 figure] preparing two exact all-index families", flush=True)
    family_rows: list[dict[str, object]] = []
    for index in range(1, 513):
        saturation_planar_squared = Fraction(1, index * index + 1)
        half_planar_squared = Fraction(
            (index + 1) ** 2,
            2 * (2 * index * index + 2 * index + 1),
        )
        family_rows.append(
            {
                "N": index,
                "saturationNormalGainSquaredExact": "1/1",
                "saturationNormalGainDecimal": "1",
                "saturationPlanarGainSquaredExact": exact_text(
                    saturation_planar_squared
                ),
                "saturationPlanarGainDecimal": format(
                    math.sqrt(float(saturation_planar_squared)), ".17g"
                ),
                "halfLimitNormalGainSquaredExact": "1/2",
                "halfLimitNormalGainDecimal": format(math.sqrt(0.5), ".17g"),
                "halfLimitPlanarGainSquaredExact": exact_text(half_planar_squared),
                "halfLimitPlanarGainDecimal": format(
                    math.sqrt(float(half_planar_squared)), ".17g"
                ),
                "classification": "exact all-index family presentation row",
            }
        )
    write_csv("channel-families.csv", family_rows)

    print("[R0.56 figure] preparing exact angular persistence rows", flush=True)
    angular_rows: list[dict[str, object]] = []
    for index in range(401):
        delta = Fraction(index, 400)
        measure_squared = 2 * delta - delta * delta
        angular_rows.append(
            {
                "sampleIndex": index,
                "deltaExact": exact_text(delta),
                "deltaDecimal": format(float(delta), ".17g"),
                "nearSaturationMeasureSquaredExact": exact_text(measure_squared),
                "nearSaturationMeasureDecimal": format(
                    math.sqrt(float(measure_squared)), ".17g"
                ),
                "classification": "exact squared-measure presentation row",
            }
        )
    write_csv("angular-persistence.csv", angular_rows)

    shutil.copyfile(
        ROOT / "research/certificates/r056/progress.ndjson",
        HERE / "progress.ndjson",
    )
    shutil.copyfile(
        ROOT / "research/certificates/r056/resources.csv",
        HERE / "resources.csv",
    )

    metadata = {
        "schemaVersion": "1.0",
        "createdUtc": datetime.now(timezone.utc).isoformat(),
        "figureSourceCommit": arguments.source_commit,
        "formalSourceCommit": certificate["git"]["sourceCommit"],
        "certificateSha256": EXPECTED_CERTIFICATE_SHA256,
        "certificateChecks": len(certificate["checks"]),
        "profileRows": len(profile_rows),
        "familyRows": len(family_rows),
        "angularRows": len(angular_rows),
        "formalTriadsChecked": certificate["finiteRegressions"]["exhaustiveCube"][
            "noncollinearOrderedTriadsChecked"
        ],
        "formalFamiliesChecked": certificate["finiteRegressions"][
            "allIndexFamilies"
        ]["familiesChecked"],
        "exhaustiveRegressionSha256": certificate["finiteRegressions"][
            "exhaustiveCube"
        ]["recordsSha256"],
        "familyRegressionSha256": certificate["finiteRegressions"][
            "allIndexFamilies"
        ]["recordsSha256"],
        "formalStatements": {
            "normalGain": "g_N=sqrt(1-mu^2), independent of epsilon",
            "planarBound": "g_T<=(1+rho)/2 when epsilon<=rho<1",
            "sharpPlanarLimit": "sup_mu g_T tends to 1/2 as epsilon tends to zero",
            "nearSaturationMeasure": "sqrt(2 delta-delta^2)",
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
        "[R0.56 figure] wrote 801 profile, 512 family, and 401 angular rows",
        flush=True,
    )


if __name__ == "__main__":
    main()

