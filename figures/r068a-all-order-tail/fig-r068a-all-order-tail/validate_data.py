#!/usr/bin/env python3
"""Validate R0.68A figure tables against the claimed inequalities."""

from __future__ import annotations

import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def main() -> None:
    tail = rows("tail-bounds.csv")
    rates = rows("contraction-rates.csv")
    orders = rows("order-status.csv")
    metadata = json.loads((HERE / "figure-data-metadata.json").read_text())
    values = {row["quantity"]: float(row["rate"]) for row in rates}
    checks = {
        "seventeenDyadicBlocks": len(tail) == 17,
        "simpleBoundStartsBelowOneOverThirtyThousand": float(tail[0]["certifiedSimpleBound"]) <= 1 / 30_000,
        "simpleBoundStrictlyDecreases": all(
            float(tail[index + 1]["certifiedSimpleBound"])
            < float(tail[index]["certifiedSimpleBound"])
            for index in range(len(tail) - 1)
        ),
        "allDisplayedRatesContract": all(value < 1 for value in values.values()),
        "rootDisplaySharperThanSimpleTheorem": values["root-enclosure display"] < values["simple theorem rate"],
        "eighthMarkedOpen": next(row for row in orders if row["order"] == "8")["status"] == "open",
        "tailMarkedCertified": next(row for row in orders if row["order"] == "10")["status"] == "certified",
        "formalAuditPassedTenChecks": metadata["r068aChecksPassed"] == metadata["r068aChecksTotal"] == 10,
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    print(json.dumps({"status": "passed", "checks": checks}, indent=2))


if __name__ == "__main__":
    main()
