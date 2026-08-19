#!/usr/bin/env python3
"""Cross-check every R0.35 plotted value against the exact certificate."""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
CERTIFICATE = (
    REPOSITORY / "research/certificates/r035/edge-continuation-geometry.json"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "13d147790926f3f3d04ea8f6d93574e1c992dd2b30dc6e12c777e68868a4fede"
)


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    assert hashlib.sha256(CERTIFICATE.read_bytes()).hexdigest() == (
        EXPECTED_CERTIFICATE_SHA256
    )
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert payload["git"] == {
        "commit": "c95c74eb19c36962b55de887ee75654a12e3a833",
        "dirty": False,
    }
    assert all(payload["checks"].values())
    assert payload["operatorScale"]["halfRadiusBilinearBound"]["total"] == (
        "121/48"
    )

    geometry = {record["metric"]: record for record in rows("geometry.csv")}
    assert len(geometry) == 6
    assert Fraction(geometry["r031_bivariate_radius"]["exact_lower"]) == Fraction(4, 81)
    assert Fraction(geometry["r031_fixed_charge_radius"]["exact_lower"]) == Fraction(4, 81) ** 3
    candidate_r = geometry["r032_candidate_abs_R"]
    candidate_b = geometry["r032_candidate_balanced_radius"]
    r_lower, r_upper = Fraction(candidate_r["exact_lower"]), Fraction(candidate_r["exact_upper"])
    b_lower, b_upper = Fraction(candidate_b["exact_lower"]), Fraction(candidate_b["exact_upper"])
    assert b_lower**3 <= r_lower < (b_lower + Fraction(1, 10**30)) ** 3
    assert (b_upper - Fraction(1, 10**30)) ** 3 <= r_upper < b_upper**3
    ratio = geometry["balanced_radius_ratio"]
    assert Fraction(ratio["exact_lower"]) > 18
    assert Fraction(ratio["exact_upper"]) < 19

    witnesses = rows("operator-witness.csv")
    assert len(witnesses) == 128
    for record in witnesses:
        n = int(record["N"])
        same = Fraction(record["same_radius_exact"])
        half = Fraction(record["half_radius_exact"])
        assert same == Fraction(3 * n * n, 4 * (2 * n - 1))
        assert half == same / (4**n)
    assert Fraction(witnesses[-1]["same_radius_exact"]) == Fraction(4096, 85)

    constants = {record["name"]: record for record in rows("operator-constants.csv")}
    assert {name: Fraction(record["exact"]) for name, record in constants.items()} == {
        "first_derivative_multiplier": Fraction(1, 2),
        "second_derivative_multiplier": Fraction(9, 8),
        "mixed_derivative_multiplier": Fraction(1, 4),
        "half_radius_bilinear_bound": Fraction(121, 48),
    }
    print(
        "validated six continuation-geometry intervals, 128 exact "
        "same/half-radius witnesses, and four operator constants"
    )


if __name__ == "__main__":
    main()
