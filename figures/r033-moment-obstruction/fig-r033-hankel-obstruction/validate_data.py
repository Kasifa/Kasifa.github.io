#!/usr/bin/env python3
"""Cross-check the R0.33 formal figure data against the exact certificate."""

from __future__ import annotations

import csv
from fractions import Fraction
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
CERTIFICATE = REPOSITORY / "research/certificates/r033/edge-moment-structure.json"


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    turan = rows("turan.csv")
    hankel = rows("hankel-signs.csv")
    witnesses = rows("witnesses.csv")

    assert payload["git"] == {
        "commit": "c717fc1e8ae16bedc88f639ca35bebe38de51801",
        "dirty": False,
    }
    assert payload["input"]["sha256"] == (
        "bd70ed05779631b729e89c269f82d287da361fdcea34e3c42703a712222f5575"
    )
    assert all(payload["checks"].values())
    assert len(turan) == 96
    assert len(hankel) == 96
    assert len(witnesses) == 4

    expected_witnesses = {
        ("B_U", "ordinary", 2): Fraction(-437, 24192),
        ("B_V", "shifted", 2): Fraction(-43522897, 685843200),
        ("H_U", "shifted", 1): Fraction(-32, 63),
        ("H_V", "ordinary", 2): Fraction(-29699111, 12700800),
    }
    observed_witnesses = {
        (record["sequence"], record["matrix_kind"], int(record["order"])):
        Fraction(record["determinant"])
        for record in witnesses
    }
    assert observed_witnesses == expected_witnesses
    assert all(value < 0 for value in observed_witnesses.values())

    for sequence, expected_negative in (("B_U", 13), ("B_V", 20)):
        selected = [record for record in turan if record["sequence"] == sequence]
        assert [int(record["index"]) for record in selected] == list(range(1, 49))
        assert sum(int(record["sign"]) < 0 for record in selected) == expected_negative
        for record in selected:
            minor = Fraction(record["minor"])
            normalized = Fraction(record["normalized"])
            assert (minor > 0) - (minor < 0) == int(record["sign"])
            assert (normalized > 0) - (normalized < 0) == int(record["sign"])

    for sequence in ("B_U", "B_V", "H_U", "H_V"):
        for kind in ("ordinary", "shifted"):
            selected = [
                record
                for record in hankel
                if record["sequence"] == sequence and record["matrix_kind"] == kind
            ]
            assert [int(record["order"]) for record in selected] == list(range(1, 13))
            for record in selected:
                determinant = Fraction(record["determinant"])
                assert (determinant > 0) - (determinant < 0) == int(record["sign"])
    print(
        "validated 96 exact Turan records, 96 exact Hankel signs, and four "
        "negative theorem witnesses"
    )


if __name__ == "__main__":
    main()
