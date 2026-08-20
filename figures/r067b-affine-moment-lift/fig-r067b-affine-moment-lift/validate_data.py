#!/usr/bin/env python3
"""Cross-check the R0.67B figure data against its formal certificate."""

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
        (ROOT / "research/certificates/r067b/sixth-order-affine-moment-audit.json").read_text()
    )
    direct = rows("direct-levels.csv")
    scales = {row["name"]: row for row in rows("spectral-scales.csv")}
    blocks = rows("lift-blocks.csv")
    checks = {
        "certificatePassed": certificate["status"] == "passed",
        "allCertificateChecksPassed": all(certificate["checks"].values()),
        "sevenDirectLevels": len(direct) == 7,
        "lastMassMatches": int(direct[-1]["maximumAbsoluteMass"]) == 51034,
        "lastFirstMomentMatches": int(direct[-1]["maximumAbsoluteFirstMoment"]) == 3785734,
        "firstMomentUpperIs26": float(scales["first-moment spectrum"]["upper"]) == 26,
        "zeroAffineScaleIs256": float(scales["zero-affine remainder"]["lower"]) == 256,
        "otherFiniteUpperIs300": float(scales["other finite spectrum"]["upper"]) == 300,
        "dominantRootExceeds402": float(scales["dominant root mu"]["lower"]) > 402,
        "liftHasNineNonzeroBlocks": len(blocks) == 9,
        "liftHasFourMomentCouplings": sum(row["input"] == "mass" and row["output"] != "mass" for row in blocks) == 4,
        "strictScaleOrdering": 26 < 256 < 300 < float(scales["dominant root mu"]["lower"]),
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
