#!/usr/bin/env python3
"""Extract deterministic figure data from the formal R0.67C-2 certificate."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import resource
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CERTIFICATE = ROOT / "research/certificates/r067c2/sixth-order-heat-dominant-projection-audit.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rss_mib() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024 * 1024) if platform.system() == "Darwin" else value / 1024


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate-commit", required=True)
    arguments = parser.parse_args()
    started = time.perf_counter()
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    conclusion = certificate["conclusion"]
    finite = certificate["finiteJet"]
    resolvent = certificate["resolvent"]
    derivative = certificate["analyticDerivativeBound"]
    base_lower, base_upper = finite["guardedJetBaseInterval"]
    correction = resolvent["heatCorrectionAbsoluteUpper"]
    projection_lower = conclusion["dominantHeatProjectionLower"]
    projection_upper = conclusion["dominantHeatProjectionUpper"]

    write_csv(
        HERE / "projection-intervals.csv",
        ["quantity", "lower", "upper", "raw", "rigor"],
        [
            {
                "quantity": "degree-six jet",
                "lower": base_lower,
                "upper": base_upper,
                "raw": finite["rawJetBase"],
                "rigor": "guarded interval",
            },
            {
                "quantity": "resolvent correction",
                "lower": -correction,
                "upper": correction,
                "raw": 0,
                "rigor": "absolute upper",
            },
            {
                "quantity": "complete projection",
                "lower": projection_lower,
                "upper": projection_upper,
                "raw": "",
                "rigor": "strict guarded interval",
            },
        ],
    )
    threshold = -base_upper / resolvent["observableUpper"]
    write_csv(
        HERE / "derivative-budget.csv",
        ["quantity", "value", "rigor"],
        [
            {
                "quantity": "raw analytic majorant",
                "value": derivative["rawMaximum"],
                "rigor": "computed upper",
            },
            {
                "quantity": "declared guard",
                "value": derivative["guardedUpper"],
                "rigor": "certificate upper",
            },
            {
                "quantity": "zero-contact threshold",
                "value": threshold,
                "rigor": "strict lower from guarded base",
            },
        ],
    )
    write_csv(
        HERE / "spectral-scales.csv",
        ["quantity", "value", "role"],
        [
            {
                "quantity": "degree-six remainder",
                "value": 1 / 4096,
                "role": "zero-sixth-jet transfer scale",
            },
            {
                "quantity": "affine remainder",
                "value": 256,
                "role": "R0.67B zero-affine scale",
            },
            {
                "quantity": "other finite spectrum",
                "value": 300,
                "role": "strict upper",
            },
            {
                "quantity": "dominant root",
                "value": certificate["dominantRoot"]["display"],
                "role": "mu",
            },
        ],
    )
    metadata = {
        "certificate": str(CERTIFICATE.relative_to(ROOT)),
        "certificateSha256": sha256(CERTIFICATE),
        "sourceCommit": certificate["provenance"]["sourceCommit"],
        "certificateCommit": arguments.certificate_commit,
        "checksPassed": sum(certificate["checks"].values()),
        "checksTotal": len(certificate["checks"]),
        "runtimeSeconds": certificate["runtime"]["elapsedSeconds"],
        "claimBoundary": certificate["classification"],
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n", encoding="utf-8"
    )
    write_csv(
        HERE / "figure-data-resources.csv",
        ["elapsedSeconds", "maximumRssMiB", "status"],
        [
            {
                "elapsedSeconds": f"{time.perf_counter() - started:.6f}",
                "maximumRssMiB": f"{rss_mib():.3f}",
                "status": "passed",
            }
        ],
    )


if __name__ == "__main__":
    main()
