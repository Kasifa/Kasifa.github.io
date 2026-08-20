#!/usr/bin/env python3
"""Cross-check the extracted R0.68B-2 figure data."""

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
    one = json.loads((ROOT / "research/certificates/r068b2a/eighth-order-heat-one-cycle-audit.json").read_text())
    jet = json.loads((ROOT / "research/certificates/r068b2b-pilot/eighth-order-heat-jet-pilot.json").read_text())
    compression = rows("state-compression.csv")
    convergence = rows("jet-convergence.csv")
    assert [int(row["stateCount"]) for row in compression] == one["dynamicProgram"]["stateCountsByDepth"]
    assert [int(row["degree"]) for row in convergence] == list(range(9))
    assert abs(float(convergence[-1]["value"]) - jet["heatJet"]["finalPilotValue"]) < 1e-24
    assert float(one["exactTaylor"]["finalLowerDisplay"]) > 0
    assert float(convergence[-1]["value"]) < 0
    print(json.dumps({"status": "passed", "rows": {"compression": len(compression), "convergence": len(convergence)}}))


if __name__ == "__main__":
    main()
