#!/usr/bin/env python3
"""Extract deterministic figure data from the formal R0.67B certificate."""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import resource
import time
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CERTIFICATE = ROOT / "research/certificates/r067b/sixth-order-affine-moment-audit.json"


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
    started = time.perf_counter()
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    direct_rows = [
        {
            **row,
            "normalizedFirstMoment": row["maximumAbsoluteFirstMoment"] / row["M"],
        }
        for row in certificate["directConvolutionAudit"]
    ]
    write_csv(
        HERE / "direct-levels.csv",
        [
            "level",
            "M",
            "target",
            "maximumAbsoluteMass",
            "maximumAbsoluteFirstMoment",
            "normalizedFirstMoment",
        ],
        direct_rows,
    )
    separation = certificate["spectralSeparation"]
    write_csv(
        HERE / "spectral-scales.csv",
        ["name", "lower", "upper", "kind", "rigor"],
        [
            {"name": "first-moment spectrum", "lower": 0, "upper": 26, "kind": "upper", "rigor": "strict"},
            {"name": "zero-affine remainder", "lower": 256, "upper": 256, "kind": "exact", "rigor": "exact"},
            {"name": "other finite spectrum", "lower": 0, "upper": 300, "kind": "upper", "rigor": "strict"},
            {
                "name": "dominant root mu",
                "lower": f"{float(Fraction(separation['dominantMassRootLower'])):.15f}",
                "upper": f"{float(Fraction(separation['dominantMassRootUpper'])):.15f}",
                "kind": "interval",
                "rigor": "strict enclosure",
            },
        ],
    )
    write_csv(
        HERE / "lift-blocks.csv",
        ["output", "input", "operator", "scale"],
        [
            {"output": "mass", "input": "mass", "operator": "W", "scale": "1"},
            *[
                {"output": coordinate, "input": "mass", "operator": f"E_{coordinate}", "scale": "1/16"}
                for coordinate in ("A", "B", "C", "D")
            ],
            *[
                {"output": coordinate, "input": coordinate, "operator": "W", "scale": "1/16"}
                for coordinate in ("A", "B", "C", "D")
            ],
        ],
    )
    metadata = {
        "certificate": str(CERTIFICATE.relative_to(ROOT)),
        "certificateSha256": sha256(CERTIFICATE),
        "sourceCommit": certificate["provenance"]["sourceCommit"],
        "certificateCommit": "74d09579d5cf859dab79840528abaa43a1f56f1d",
        "checksPassed": sum(certificate["checks"].values()),
        "checksTotal": len(certificate["checks"]),
        "directLevels": len(direct_rows),
        "finiteLiftDimension": certificate["stateSpace"]["finiteLiftDimension"],
        "strictOrdering": separation["strictOrdering"],
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
