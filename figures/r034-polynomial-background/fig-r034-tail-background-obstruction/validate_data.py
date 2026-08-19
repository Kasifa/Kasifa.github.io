#!/usr/bin/env python3
"""Cross-check the R0.34 figure tables against the exact certificate."""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
CERTIFICATE = (
    REPOSITORY / "research/certificates/r034/edge-polynomial-background.json"
)


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("ascii")).hexdigest()


def main() -> None:
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    thresholds = rows("thresholds.csv")
    tail = rows("tail-search.csv")
    witnesses = rows("witnesses.csv")

    assert payload["git"] == {
        "commit": "11cb3c386814a4d725944251a2d46faef0f5c53c",
        "dirty": False,
    }
    assert payload["input"]["r032"]["sha256"] == (
        "bd70ed05779631b729e89c269f82d287da361fdcea34e3c42703a712222f5575"
    )
    assert payload["input"]["r033"]["sha256"] == (
        "ccbf8ab05615378f6d4b9824e86b679b6d0df2882cbc6e563b063b8769292367"
    )
    assert all(payload["checks"].values())
    assert len(thresholds) == 4
    assert len(tail) == 40
    assert len(witnesses) == 4

    expected = {
        "B_U": (43, 44, 3, "0;1;2", "c8fb036dea3c66834b07b39666537f0b85ea138ac105b6315f7519d0488a3e2a"),
        "B_V": (44, 45, 3, "0;1;2", "516aaee23c11bcf030247d5d3d657ad754289d83ade88d1a70bafba1fb782ccb"),
        "H_U": (46, 47, 1, "0", "0f9c04e0620e89dd27f5a440b4cb7787ce22f22d0545595e14063415fdad8b66"),
        "H_V": (45, 46, 2, "0;1", "815da2c07cddb84f25ed8cdbfc4f7a5c8aa96b81f9420077522eb83fbc8680ae"),
    }
    observed = {
        record["sequence"]: (
            int(record["maximum_excluded_degree"]),
            int(record["witness_shift"]),
            int(record["witness_order"]),
            record["monomial_indices"],
            record["determinant_sha256"],
        )
        for record in thresholds
    }
    assert observed == expected

    for record in witnesses:
        determinant = Fraction(record["determinant"])
        assert determinant < 0
        assert sha256_text(record["determinant"]) == record["determinant_sha256"]
        assert len(str(abs(determinant.numerator))) == int(record["numerator_digits"])
        assert len(str(determinant.denominator)) == int(record["denominator_digits"])

    searches = payload["finiteWindowAudit"]["searches"]
    for record in tail:
        sequence = record["sequence"]
        shift = int(record["shift"])
        available = bool(int(record["available"]))
        certificate_rows = {
            int(item["shift"]): item
            for item in searches[sequence]["shiftSummaries"]
        }
        assert available == (shift in certificate_rows)
        if not available:
            assert sequence in {"H_U", "H_V"} and shift == 49
            continue
        source = certificate_rows[shift]
        assert int(record["principal_minor_count"]) == source["principalMinorCount"]
        assert int(record["negative_count"]) == source["negativeCount"]
        assert bool(int(record["is_maximal_witness_shift"])) == (
            shift == searches[sequence]["maximalNegativeShift"]
        )
        assert (
            ";".join(str(value) for value in source["negativeOrders"])
            == record["negative_orders"]
        )
    print(
        "validated four exact degree thresholds, four negative theorem "
        "witnesses, and 40 displayed tail-search cells"
    )


if __name__ == "__main__":
    main()
