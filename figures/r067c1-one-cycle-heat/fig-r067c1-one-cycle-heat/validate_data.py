#!/usr/bin/env python3
"""Cross-check R0.67C-1 plotted data against the formal certificate."""

from __future__ import annotations

import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def main() -> None:
    certificate = json.loads(
        (ROOT / "research/certificates/r067c1/sixth-order-heat-one-cycle-audit.json").read_text()
    )
    partial = rows("partial-sums.csv")
    enumeration = rows("enumeration-by-a.csv")
    scales = {row["name"]: row for row in rows("certificate-scales.csv")}
    lower = float(scales["coefficient lower"]["value"])
    upper = float(scales["coefficient upper"]["value"])
    tail = float(scales["absolute Taylor tail"]["value"])
    checks = {
        "certificatePassed": certificate["status"] == "passed",
        "allEightCertificateChecksPassed": sum(certificate["checks"].values()) == 8,
        "thirtyThreePartialSums": len(partial) == 33,
        "finalPartialInsideCertificate": lower < float(partial[-1]["partialSum"]) < upper,
        "sixteenCarrierASlices": len(enumeration) == 16,
        "validTupleTotalMatches": sum(int(row["validTuples"]) for row in enumeration) == 34690,
        "signedMassTotalMatches": sum(int(row["signedMass"]) for row in enumeration) == 500,
        "strictPositiveInterval": 0 < lower < upper,
        "tailBelowTwoTimesTenToMinusTwelve": tail < 2e-12,
        "signalExceedsTailByTenOrders": lower / tail > 1e10,
    }
    report = {
        "status": "passed" if all(checks.values()) else "failed",
        "checks": checks,
        "checksPassed": sum(checks.values()),
        "checksTotal": len(checks),
    }
    print(json.dumps(report, indent=2))
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
