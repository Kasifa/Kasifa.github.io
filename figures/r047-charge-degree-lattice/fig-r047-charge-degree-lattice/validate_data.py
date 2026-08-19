#!/usr/bin/env python3
"""Independently validate the R0.47 figure tables against exact sources."""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[2]
CERTIFICATE = ROOT / "research/certificates/r047/edge-charge-degree-lattice.json"
EXPECTED_CERTIFICATE_SHA256 = (
    "e45bc20ddeab9efde83dafefc84514df0260f8831c102c4621f0fdcd43dea6c9"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    assert sha256(CERTIFICATE) == EXPECTED_CERTIFICATE_SHA256
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert all(certificate["checks"].values())
    assert len(certificate["checks"]) == 39
    target = certificate["restartCertificate"]
    target_tail = target["tail"]

    fixed = rows("fixed-charge-bounds.csv")
    assert len(fixed) == 239
    assert [int(row["inputCharge"]) for row in fixed] == list(range(2, 241))
    source_fixed = target_tail["fixedPositiveChargeColumns"]
    for row, source in zip(fixed, source_fixed, strict=True):
        assert int(row["minimumTailDegree"]) == source["minimumTailDegree"]
        assert Fraction(row["boundExact"]) == Fraction(source["bound"]["exact"])
        assert row["maximumEndpoint"] == source["maximumEndpoint"]
    fixed_maximum = max(fixed, key=lambda row: Fraction(row["boundExact"]))
    assert fixed_maximum["inputCharge"] == "162"
    assert fixed_maximum["minimumTailDegree"] == "81"
    assert fixed_maximum["isMaximum"] == "true"
    assert Fraction(fixed_maximum["boundExact"]) < 1

    parity = rows("parity-endpoints.csv")
    assert len(parity) == 162
    for branch, denominator in (("even", 242), ("odd", 241)):
        selected = [row for row in parity if row["branch"] == branch]
        assert len(selected) == 81
        assert Fraction(selected[0]["yExact"]) == 0
        assert Fraction(selected[-1]["yExact"]) == Fraction(1, denominator)
    large = target_tail["largeChargeLatticeSector"]
    even = [row for row in parity if row["branch"] == "even"]
    odd = [row for row in parity if row["branch"] == "odd"]
    assert Fraction(even[-1]["boundExact"]) == Fraction(
        large["evenEndpoint"]["valueAtS242"]["exact"]
    )
    assert Fraction(odd[-1]["boundExact"]) == Fraction(
        large["oddEndpoint"]["valueAtS241"]["exact"]
    )
    assert Fraction(even[0]["boundExact"]) == Fraction(
        large["evenEndpoint"]["valueAtInfinity"]["exact"]
    )
    assert Fraction(odd[0]["boundExact"]) == Fraction(
        large["oddEndpoint"]["valueAtInfinity"]["exact"]
    )
    assert all(
        Fraction(left["boundExact"]) < Fraction(right["boundExact"])
        for left, right in zip(even, even[1:])
    )
    assert all(
        Fraction(left["boundExact"]) > Fraction(right["boundExact"])
        for left, right in zip(odd, odd[1:])
    )

    derivatives = rows("derivative-certificates.csv")
    assert len(derivatives) == 2
    for row in derivatives:
        assert row["allPositive"] == "true"
        assert row["bernsteinDegree"] == "318"
        assert row["bernsteinCoefficientCount"] == "319"
        assert row["subdivisionCount"] == "1"
        assert Fraction(row["minimumSignedBernsteinCoefficientExact"]) > 0

    controls = rows("radius-controls.csv")
    assert len(controls) == 9
    block_by_control = {
        "entry": certificate["entryControl"],
        "target": certificate["restartCertificate"],
        "probe": certificate["negativeControl"],
    }
    for row in controls:
        block = block_by_control[row["control"]]
        expected = {
            "lattice-sharp tail": block["tailLinearizationBound"],
            "R0.46 separated tail": block["tail"]["r046Bound"],
            "canonical stretch": block["stretchOperatorBound"],
        }[row["series"]]
        assert Fraction(row["boundExact"]) == Fraction(expected["exact"])
        assert (Fraction(row["boundExact"]) < 1) == (row["passes"] == "true")

    probe_tail = next(
        row
        for row in controls
        if row["control"] == "probe" and row["series"] == "lattice-sharp tail"
    )
    target_tail_row = next(
        row
        for row in controls
        if row["control"] == "target" and row["series"] == "lattice-sharp tail"
    )
    assert Fraction(target_tail_row["boundExact"]) < 1
    assert Fraction(probe_tail["boundExact"]) > 1

    sectors = rows("sector-bounds.csv")
    assert len(sectors) == 5
    assert {row["sector"] for row in sectors} == {
        "s=0",
        "s=-1",
        "s=1",
        "s=162",
        "s>=241",
    }
    sector_maximum = max(sectors, key=lambda row: Fraction(row["boundExact"]))
    assert sector_maximum["sector"] == "s=162"
    assert sector_maximum["isMaximum"] == "true"

    progress = (PACKAGE / "progress.ndjson").read_text(encoding="utf-8").splitlines()
    assert len(progress) == 8
    assert json.loads(progress[-1])["checks"] == 39
    resources = rows("resources.csv")
    assert len(resources) == 458
    assert resources[-1]["status"] == "exited:0"

    print(
        "validated R0.47 figure data: 239 fixed-charge theorems, "
        "162 rational parity samples, 2 continuous sign certificates, "
        "9 radius controls, 5 exhaustive sectors, and monitored provenance"
    )


if __name__ == "__main__":
    main()
