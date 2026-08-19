#!/usr/bin/env python3
"""Independently validate the R0.49 figure tables against exact sources."""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[2]
CERTIFICATE = ROOT / "research/certificates/r049/edge-charge-character-weight.json"
EXPECTED_CERTIFICATE_SHA256 = (
    "b60405d395a4b927ab674af8cec1aef8f3b42e4962fd7118425851e075a49e44"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    assert sha256(CERTIFICATE) == EXPECTED_CERTIFICATE_SHA256
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    assert len(certificate["checks"]) == 31
    assert all(certificate["checks"].values())
    theorem = certificate["thresholdTheorem"]

    curve = rows("threshold-curve.csv")
    assert len(curve) == 101
    assert [int(row["sampleIndex"]) for row in curve] == list(range(101))
    assert Fraction(curve[0]["radiusExact"]) == Fraction(
        theorem["window"]["lower"]["exact"]
    )
    assert Fraction(curve[-1]["radiusExact"]) == Fraction(
        theorem["window"]["upper"]["exact"]
    )
    assert Fraction(curve[0]["activeMarginExact"]) == Fraction(
        theorem["activeColumn"]["valueAtWindowLower"]["exact"]
    ) - 1
    assert Fraction(curve[-1]["activeMarginExact"]) == Fraction(
        theorem["activeColumn"]["valueAtWindowUpper"]["exact"]
    ) - 1
    margins = [Fraction(row["activeMarginExact"]) for row in curve]
    assert all(left < right for left, right in zip(margins, margins[1:]))
    assert margins[0] < 0 < margins[-1]

    roots = rows("root-endpoints.csv")
    assert len(roots) == 2
    assert [row["side"] for row in roots] == ["lower", "upper"]
    assert Fraction(roots[0]["polynomialValueExact"]) < 0
    assert Fraction(roots[1]["polynomialValueExact"]) > 0
    assert Fraction(roots[1]["radiusExact"]) - Fraction(
        roots[0]["radiusExact"]
    ) == Fraction(1, 10**18)
    assert [int(row["sturmVariations"]) for row in roots] == [40, 39]
    assert [int(row["zeroSturmValues"]) for row in roots] == [0, 0]
    assert theorem["sturmCertificate"]["sequenceLength"] == 81
    assert theorem["sturmCertificate"]["rootCount"] == 1

    contributions = rows("charge-contributions.csv")
    source_contributions = theorem["activeColumn"]["chargeDistribution"]["records"]
    assert len(contributions) == len(source_contributions) == 158
    contribution_charges = [int(row["centerCharge"]) for row in contributions]
    assert contribution_charges == sorted(set(contribution_charges))
    assert contribution_charges[0] == -1 and contribution_charges[-1] == 157
    for row, source in zip(contributions, source_contributions, strict=True):
        assert int(row["centerCharge"]) == source["centerCharge"]
        assert Fraction(row["contributionExact"]) == Fraction(
            source["contribution"]["exact"]
        )
        assert Fraction(row["shareExact"]) == Fraction(
            source["shareOfActiveColumn"]["exact"]
        )
    assert sum((Fraction(row["shareExact"]) for row in contributions), Fraction(0)) == 1

    competitors = rows("competitor-gaps.csv")
    assert len(competitors) == 243
    assert [int(row["rankByGap"]) for row in competitors] == list(range(1, 244))
    gaps = [Fraction(row["gapBelowActiveAtWindowLeftExact"]) for row in competitors]
    assert all(gap > 0 for gap in gaps)
    assert all(left <= right for left, right in zip(gaps, gaps[1:]))
    assert competitors[0]["label"] == "fixed s=164"
    assert competitors[0]["isNearest"] == "true"
    assert Fraction(competitors[0]["gapBelowActiveAtWindowLeftExact"]) == Fraction(
        theorem["fullWindowDominance"]["minimumDominanceGap"]["exact"]
    )

    geometry = rows("anisotropic-geometry.csv")
    assert len(geometry) == 3
    old_radius = Fraction(certificate["input"]["r048"]["previousRootUpper"]["exact"])
    target = Fraction(theorem["window"]["lower"]["exact"])
    expected_ratios = [
        Fraction(certificate["anisotropicGeometry"]["rhoZ"]["exact"]) / old_radius,
        Fraction(certificate["anisotropicGeometry"]["rhoW"]["exact"]) / old_radius,
        target**3 / old_radius**3,
    ]
    assert [Fraction(row["ratioExact"]) for row in geometry] == expected_ratios
    assert expected_ratios[0] > 1
    assert expected_ratios[1] < 1
    assert expected_ratios[2] == Fraction(
        certificate["anisotropicGeometry"][
            "certifiedFixedChargeRadiusGainLowerFactor"
        ]["exact"]
    ) > 1

    progress = (PACKAGE / "progress.ndjson").read_text(encoding="utf-8").splitlines()
    assert len(progress) == 11
    assert json.loads(progress[-1])["checks"] == 31
    resources = rows("resources.csv")
    assert len(resources) == 807
    assert resources[-1]["status"] == "exited:0"

    print(
        "validated R0.49 figure data: 101 exact polynomial samples, 2 exact "
        "root endpoints, 158 charge contributions, 243 formal competitors, "
        "3 exact geometry ratios, and monitored provenance"
    )


if __name__ == "__main__":
    main()
