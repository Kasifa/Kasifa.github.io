#!/usr/bin/env python3
"""Cross-check the R0.32 figure data against the exact certificate."""

from __future__ import annotations

import csv
from fractions import Fraction
import json
from pathlib import Path
import sys


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
CERTIFICATE = REPOSITORY / "research/certificates/r032/edge-singularity-candidates.json"

sys.set_int_max_str_digits(0)


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    diagnostic = payload["diagnostic"]
    data = rows("candidate-poles.csv")
    summary = rows("summary.csv")

    assert payload["git"] == {
        "commit": "a973bc77915181a27158a475e75008e8bdb18d4a",
        "dirty": False,
    }
    assert payload["scope"]["classification"] == (
        "finite exact diagnostic, not a singularity theorem"
    )
    assert payload["scope"]["maximumExactTotalDegree"] == 149
    assert payload["scope"]["maximumEndpointParameter"] == 50
    assert payload["checks"]["checkpointResumeRegression"]["passed"] is True
    assert payload["checks"]["r028EndpointRegression"]["passed"] is True
    assert payload["checks"]["r028EndpointRegression"]["completeHistoricalCoverage"] is True
    assert payload["checks"]["candidateDiagnostics"]["passed"] is True
    assert len(diagnostic["transportApproximants"]) == 22
    assert len(diagnostic["dCenterZeroApproximants"]) == 11
    assert len(data) == 33

    expected_cuts = list(range(30, 51, 2))
    for field in ("U", "V", "D center"):
        selected = [row for row in data if row["field"] == field]
        assert [int(row["coefficient_cut"]) for row in selected] == expected_cuts
        for row in selected:
            cut = int(row["coefficient_cut"])
            assert int(row["pade_order"]) == (cut - 2) // 2
            root = Fraction(row["root_mid"])
            residue = Fraction(row["residue_mid"])
            if field in ("U", "V"):
                assert Fraction(-3, 4) < root < Fraction(-7493, 10000)
                assert residue < Fraction(-1, 2)
                assert row["classification"] == "transport branch candidate"
            else:
                assert Fraction(-29, 40) < root < Fraction(-361, 500)
                assert Fraction(49, 50) < residue < Fraction(103, 100)
                assert row["classification"] == "zero candidate"

    summary_by_name = {row["quantity"]: row for row in summary}
    guaranteed = summary_by_name["fixed-charge guaranteed radius"]
    assert Fraction(guaranteed["lower"]) == Fraction(64, 531441)
    assert guaranteed["lower"] == guaranteed["upper"]
    assert guaranteed["width"] == "0"
    full_hull = summary_by_name["transport cluster, all cuts"]
    tail_hull = summary_by_name["transport cluster, cuts 42-50"]
    assert Fraction(full_hull["width"]) < Fraction(3, 10000)
    assert Fraction(tail_hull["width"]) < Fraction(1, 10000)
    assert Fraction(tail_hull["lower"]) >= Fraction(full_hull["lower"])
    assert Fraction(tail_hull["upper"]) <= Fraction(full_hull["upper"])
    print(
        "validated 33 exact D-log Pade records, candidate classification, "
        "and fixed-charge theorem boundary"
    )


if __name__ == "__main__":
    main()
