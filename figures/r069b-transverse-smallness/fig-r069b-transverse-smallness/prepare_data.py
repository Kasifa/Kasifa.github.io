#!/usr/bin/env python3
"""Prepare source-bound data for Figure R0.69B."""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import resource
import time
from pathlib import Path

import gmpy2
from gmpy2 import mpfr, mpq


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
R069B = ROOT / "research/certificates/r069b/transverse-critical-smallness.json"
R066 = ROOT / "research/certificates/r066/spectral-audit.json"
R069B_SHA = "53ebc36d199ca2b379270c85a842978aab086f7f77d5e4b4f6c32e944c15ce45"
R066_SHA = "a6f66c8bea8806fee3716b8d6611a2e0720e29969d94d991672cf3626ba8bcb2"
SOURCE_COMMIT = "3342fb092b454df34255b82e142bfd796e5e522d"
CERTIFICATE_COMMIT = "e2584235220dcc4a5721b21b6eb997d88698e2c8"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_rows(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def rss_mib() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024 * 1024) if platform.system() == "Darwin" else value / 1024


def main() -> None:
    started = time.perf_counter()
    if sha256(R069B) != R069B_SHA or sha256(R066) != R066_SHA:
        raise RuntimeError("a pinned input certificate hash does not match")
    transverse = json.loads(R069B.read_text(encoding="utf-8"))
    spectral = json.loads(R066.read_text(encoding="utf-8"))
    if transverse["status"] != "passed":
        raise RuntimeError("R0.69B certificate did not pass")

    lambda_upper = mpq(
        int(spectral["massSpectrum"]["dominantUpperNumerator"]),
        int(spectral["massSpectrum"]["dominantUpperDenominator"]),
    )
    rho_upper_text = transverse["criticalNormBound"]["rho"]["upper"]
    k_upper_text = transverse["criticalNormBound"]["prefactorInterval"]["upper"]
    down = gmpy2.context(precision=256, round=gmpy2.RoundDown)
    up = gmpy2.context(precision=256, round=gmpy2.RoundUp)
    with gmpy2.context(down):
        amplitude_base_lower = mpfr(16) / gmpy2.sqrt(mpfr(lambda_upper))
    with gmpy2.context(up):
        rho_upper = mpfr(rho_upper_text)
        k_upper = mpfr(k_upper_text)

    scale_rows: list[dict[str, object]] = []
    critical_uppers: list[mpfr] = []
    for depth in range(51):
        with gmpy2.context(down):
            amplitude_lower = mpfr(2) * amplitude_base_lower**depth
        with gmpy2.context(up):
            epsilon_upper = rho_upper**depth
            critical_upper = k_upper * epsilon_upper
        critical_uppers.append(critical_upper)
        scale_rows.append({
            "r": depth,
            "physicalAmplitudeLower": f"{amplitude_lower:.40g}",
            "epsilonUpper": f"{epsilon_upper:.40g}",
            "criticalNormUpper": f"{critical_upper:.40g}",
        })
    write_rows(
        "scale-separation.csv",
        ["r", "physicalAmplitudeLower", "epsilonUpper", "criticalNormUpper"],
        scale_rows,
    )

    decision_rows: list[dict[str, object]] = []
    for twentieth in range(121):
        with gmpy2.context(down):
            budget = mpfr(10) ** (-mpfr(twentieth) / 20)
        value = mpfr(k_upper)
        depth = 0
        while value >= budget:
            with gmpy2.context(up):
                value *= rho_upper
            depth += 1
        decision_rows.append({
            "budget": f"{budget:.30g}",
            "minusLog10Budget": f"{twentieth / 20:.2f}",
            "firstDepthStrictlyBelow": depth,
        })
    write_rows(
        "decision-depth.csv",
        ["budget", "minusLog10Budget", "firstDepthStrictlyBelow"],
        decision_rows,
    )

    crossings = transverse["criticalNormBound"]["firstDepthStrictlyBelow"]
    write_rows(
        "certified-crossings.csv",
        ["budget", "firstDepthStrictlyBelow"],
        [
            {"budget": key, "firstDepthStrictlyBelow": crossings[key]}
            for key in ("1", "1e-1", "1e-2", "1e-3", "1e-6")
        ],
    )
    metadata = {
        "status": "passed",
        "sourceCommit": SOURCE_COMMIT,
        "certificateCommit": CERTIFICATE_COMMIT,
        "inputCertificates": {
            str(R069B.relative_to(ROOT)): R069B_SHA,
            str(R066.relative_to(ROOT)): R066_SHA,
        },
        "rhoUpper": rho_upper_text,
        "prefactorUpper": k_upper_text,
        "physicalAmplitudeBaseLower": f"{amplitude_base_lower:.78g}",
        "checksPassed": sum(bool(value) for value in transverse["checks"].values()),
        "checksTotal": len(transverse["checks"]),
        "claimBoundary": transverse["classification"],
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_rows(
        "figure-data-resources.csv",
        ["elapsedSeconds", "maximumRssMiB", "status"],
        [{
            "elapsedSeconds": f"{time.perf_counter() - started:.6f}",
            "maximumRssMiB": f"{rss_mib():.3f}",
            "status": "passed",
        }],
    )


if __name__ == "__main__":
    main()
