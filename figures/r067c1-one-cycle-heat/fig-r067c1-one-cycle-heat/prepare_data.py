#!/usr/bin/env python3
"""Extract deterministic R0.67C-1 figure data from the formal certificate."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
import resource
import sys
import time
from decimal import Decimal, localcontext
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CERTIFICATE = ROOT / "research/certificates/r067c1/sixth-order-heat-one-cycle-audit.json"
sys.path.insert(0, str(ROOT / "research"))
import sixth_order_cycle_audit as r067  # noqa: E402


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
    coefficients = [
        int(value)
        for value in certificate["exactTaylor"]["completeHomogeneousIntegerCoefficients"]
    ]
    with localcontext() as context:
        context.prec = 60
        time_value = Decimal(2).ln() / 2
        high = Decimal(certificate["parameters"]["H"])
        partial = Decimal(0)
        partial_rows = []
        for degree, coefficient in enumerate(coefficients):
            partial += (
                (-1 if degree % 2 else 1)
                * Decimal(coefficient)
                * time_value ** (degree + 5)
                / (high ** (2 * degree) * Decimal(math.factorial(degree + 5)))
            )
            partial_rows.append(
                {"degree": degree, "partialSum": format(partial, ".20E")}
            )
    write_csv(
        HERE / "partial-sums.csv",
        ["degree", "partialSum"],
        partial_rows,
    )

    pair, _companion = r067.rudin_shapiro_pair(4)
    by_a = []
    for a in range(16):
        valid = 0
        signed_mass = 0
        for b in range(16):
            for c in range(16):
                for d in range(16):
                    e = a + b + c - d - 2
                    if not 0 <= e < 16:
                        continue
                    valid += 1
                    signed_mass += pair[2] * pair[a] * pair[b] * pair[c] * pair[d] * pair[e]
        by_a.append({"a": a, "validTuples": valid, "signedMass": signed_mass})
    write_csv(
        HERE / "enumeration-by-a.csv",
        ["a", "validTuples", "signedMass"],
        by_a,
    )

    exact = certificate["exactTaylor"]
    lower = Decimal(exact["finalLowerDisplay"])
    upper = Decimal(exact["finalUpperDisplay"])
    tail = Decimal(exact["absoluteTailBoundDisplay"])
    write_csv(
        HERE / "certificate-scales.csv",
        ["name", "value", "rigor"],
        [
            {"name": "coefficient lower", "value": lower, "rigor": "strict"},
            {"name": "coefficient upper", "value": upper, "rigor": "strict"},
            {"name": "absolute Taylor tail", "value": tail, "rigor": "upper"},
            {
                "name": "signal-to-tail lower ratio",
                "value": lower / tail,
                "rigor": "strict lower",
            },
        ],
    )

    metadata = {
        "certificate": str(CERTIFICATE.relative_to(ROOT)),
        "certificateSha256": sha256(CERTIFICATE),
        "sourceCommit": certificate["provenance"]["sourceCommit"],
        "certificateCommit": "bc7c318781afccc72ba6ff3fe034c9e72ee0f18c",
        "checksPassed": sum(certificate["checks"].values()),
        "checksTotal": len(certificate["checks"]),
        "validCarrierTuples": certificate["parameters"]["validCarrierTuples"],
        "signedPaths": certificate["parameters"]["signedPaths"],
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
