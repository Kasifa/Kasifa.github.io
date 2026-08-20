#!/usr/bin/env python3
"""Extract Figure R0.68B-2d/e data from pinned research archives."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
import resource
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DERIVATIVE = ROOT / "research/certificates/r068b2d-exact/eighth-order-heat-derivative-exact.json"
MASS = ROOT / "research/certificates/r068b2e-exact/eighth-order-dominant-mass-exact.json"
PILOT = ROOT / "research/certificates/r068b2c2-pilot/eighth-order-heat-defect-pilot.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_rows(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def rss_mib() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024 * 1024) if platform.system() == "Darwin" else value / 1024


def main() -> None:
    started = time.perf_counter()
    derivative = json.loads(DERIVATIVE.read_text())
    mass = json.loads(MASS.read_text())
    pilot = json.loads(PILOT.read_text())

    pure = derivative["derivativeMajorant"]["pureMultiindexUppers"]
    write_rows(
        HERE / "derivative-bounds.csv",
        ["coordinate", "upper", "upperTimes1e6", "isGlobalMaximum"],
        [
            {
                "coordinate": coordinate,
                "upper": record["decimal"],
                "upperTimes1e6": f"{float(record['decimal']) * 1e6:.17e}",
                "isGlobalMaximum": coordinate == 4,
            }
            for coordinate, record in enumerate(pure, start=1)
        ],
    )

    root_width = float(mass["dominantRoot"]["width"]["decimal"])
    mass_width = float(
        mass["dominantMass"]["maximumCoordinateWidth"]["decimal"]
    )
    write_rows(
        HERE / "interval-margins.csv",
        ["quantity", "width", "gate", "decimalOrdersBeyondGate"],
        [
            {
                "quantity": "dominant root",
                "width": f"{root_width:.17e}",
                "gate": "1e-60",
                "decimalOrdersBeyondGate": f"{-math.log10(root_width) - 60:.17e}",
            },
            {
                "quantity": "mass coordinates",
                "width": f"{mass_width:.17e}",
                "gate": "1e-50",
                "decimalOrdersBeyondGate": f"{-math.log10(mass_width) - 50:.17e}",
            },
        ],
    )

    signal = float(pilot["gapDiagnostics"]["heatJetMagnitude"])
    correction = float(pilot["gapDiagnostics"]["allDerivativeCorrectionUpper"])
    gap = signal - correction
    write_rows(
        HERE / "pilot-budget.csv",
        ["component", "value", "valueTimes1e8", "evidence"],
        [
            {
                "component": "heat signal",
                "value": f"{signal:.17e}",
                "valueTimes1e8": f"{signal * 1e8:.17e}",
                "evidence": "binary64 moment and heat pairing",
            },
            {
                "component": "defect correction",
                "value": f"{correction:.17e}",
                "valueTimes1e8": f"{correction * 1e8:.17e}",
                "evidence": "strict derivative times binary64 resolvent",
            },
            {
                "component": "remaining gap",
                "value": f"{gap:.17e}",
                "valueTimes1e8": f"{gap * 1e8:.17e}",
                "evidence": "binary64 diagnostic difference",
            },
        ],
    )

    summary = [
        {
            "derivativeMultiindices": derivative["derivativeMajorant"][
                "multiindexCount"
            ],
            "derivativeMaximum": derivative["derivativeMajorant"][
                "maximumUpper"
            ]["decimal"],
            "derivativeBenchmark": "2.567e-6",
            "derivativeVectorSha256": derivative["derivativeMajorant"][
                "exactVectorSha256"
            ],
            "massStates": mass["parameters"]["states"],
            "massIntervalSha256": mass["dominantMass"][
                "canonicalIntervalVectorSha256"
            ],
            "signal": f"{signal:.17e}",
            "correction": f"{correction:.17e}",
            "gap": f"{gap:.17e}",
        }
    ]
    write_rows(HERE / "certified-summary.csv", list(summary[0]), summary)

    metadata = {
        "derivativeCertificate": str(DERIVATIVE.relative_to(ROOT)),
        "derivativeSha256": digest(DERIVATIVE),
        "derivativeSourceCommit": derivative["provenance"]["sourceCommit"],
        "derivativeArchiveCommit": "201aaf97a931d4f2143207941904c5f53d469962",
        "massCertificate": str(MASS.relative_to(ROOT)),
        "massSha256": digest(MASS),
        "massSourceCommit": mass["provenance"]["sourceCommit"],
        "massArchiveCommit": "c24abb94584f7b9e76b28191f5b1c6426c41dbb5",
        "pilotCertificate": str(PILOT.relative_to(ROOT)),
        "pilotSha256": digest(PILOT),
        "pilotSourceCommit": pilot["provenance"]["sourceCommit"],
        "pilotArchiveCommit": "2c4e90d128f3e51bfefb93bf0e5c94f25a2059a8",
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n"
    )
    write_rows(
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
