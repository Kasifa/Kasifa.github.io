#!/usr/bin/env python3
"""Validate the Figure R0.69A tables against the formal theorem."""

from __future__ import annotations

import csv
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def main() -> None:
    limits = rows("limit-interval.csv")
    rates = rows("decay-rates.csv")
    envelopes = rows("rate-envelopes.csv")
    orders = rows("order-status.csv")
    metadata = json.loads((HERE / "figure-data-metadata.json").read_text())
    rate_values = {row["component"]: float(row["rate"]) for row in rates}
    checks = {
        "twoLimitIntervals": len(limits) == 2,
        "positiveCorrectionExcludesZero": float(limits[0]["lower"]) > 0,
        "completeLimitStrictlyExceedsOne": float(limits[1]["lower"]) > 1,
        "threeRatesStrictlyContract": len(rates) == 3 and all(
            0 < value < 1 for value in rate_values.values()
        ),
        "twentyOneEnvelopeBlocks": len(envelopes) == 21,
        "everyEnvelopeStrictlyDecreases": all(
            all(
                float(envelopes[index + 1][key]) < float(envelopes[index][key])
                for index in range(len(envelopes) - 1)
            )
            for key in ("sixth_order", "eighth_order", "orders_at_least_ten")
        ),
        "allOrdersAssignedAClosedStatus": all(
            row["status"] in {"absent", "limit one", "support zero", "positive limit", "vanishes"}
            for row in orders
        ),
        "formalAssemblyPassedEighteenChecks": metadata["checksPassed"] == metadata["checksTotal"] == 18,
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    print(json.dumps({"status": "passed", "checks": checks}, indent=2))


if __name__ == "__main__":
    main()
