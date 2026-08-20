#!/usr/bin/env python3
"""Validate R0.66 figure tables against the pinned certificates."""

from __future__ import annotations

import csv
import hashlib
import json
from decimal import Decimal
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[2]
FINITE_CERTIFICATE = REPOSITORY / "research/certificates/r065/weighted-cycle-audit.json"
SPECTRAL_CERTIFICATE = REPOSITORY / "research/certificates/r066/spectral-audit.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def csv_rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    convergence = csv_rows("cycle-normalized.csv")
    intervals = csv_rows("coefficient-intervals.csv")
    errors = csv_rows("error-budget.csv")
    metadata = json.loads((HERE / "figure-data-metadata.json").read_text(encoding="utf-8"))
    finite = json.loads(FINITE_CERTIFICATE.read_text(encoding="utf-8"))
    spectral = json.loads(SPECTRAL_CERTIFICATE.read_text(encoding="utf-8"))
    error_by_name = {row["component"]: Decimal(row["bound"]) for row in errors}
    checks = {
        "twentyFourConsecutiveFiniteRows": [int(row["r"]) for row in convergence]
        == list(range(1, 25)),
        "finiteSignsMatchCertificate": [row["signCertified"] for row in convergence]
        == [row["signCertified"] for row in finite["scales"]],
        "twoPinnedCoefficientIntervals": len(intervals) == 2,
        "completeCoefficientIntervalIsNegative": Decimal(intervals[1]["upper"]) < 0,
        "completeCoefficientMagnitudeExceedsTwoTimesTenToMinusFive": abs(
            Decimal(intervals[1]["upper"])
        )
        > Decimal("2e-5"),
        "threeErrorsPlusTotalAndMargin": len(errors) == 5,
        "totalErrorMatchesCertificate": error_by_name["total outward error"]
        == Decimal(spectral["errorBudget"]["total"]),
        "distanceToZeroExceedsTotalByTwoHundred": error_by_name[
            "certified distance to zero"
        ]
        > 200 * error_by_name["total outward error"],
        "finiteCertificateHashMatches": metadata["finiteCertificateSha256"]
        == sha256(FINITE_CERTIFICATE),
        "spectralCertificateHashMatches": metadata["spectralCertificateSha256"]
        == sha256(SPECTRAL_CERTIFICATE),
        "bothSourceCertificatesPassed": all(finite["checks"].values())
        and all(spectral["checks"].values()),
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    print(json.dumps({"status": "passed", "checks": checks}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
