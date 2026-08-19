#!/usr/bin/env python3
"""Validate every plotted R0.37 value against the formal certificate."""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
CERTIFICATE = REPOSITORY / "research/certificates/r037/edge-weighted-restart.json"
EXPECTED_CERTIFICATE_SHA256 = (
    "a4fe36192b80112c282b9388da65ffca625f7a84d0b64f294b24352f92870eda"
)
EXPECTED_SOURCE_COMMIT = "04e62468f383d5e07c572ffd89561ee46dc249b8"


def read_rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    actual_hash = hashlib.sha256(CERTIFICATE.read_bytes()).hexdigest()
    if actual_hash != EXPECTED_CERTIFICATE_SHA256:
        raise AssertionError("R0.37 certificate hash mismatch")
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if payload["git"] != {"commit": EXPECTED_SOURCE_COMMIT, "dirty": False}:
        raise AssertionError("R0.37 source state mismatch")
    if len(payload["checks"]) != 13 or not all(payload["checks"].values()):
        raise AssertionError("R0.37 formal checks are incomplete")

    restart = payload["restartCertificate"]
    radius_rows = {
        (row["quantity"], row["version"]): row
        for row in read_rows("radius-gain.csv")
    }
    old_radius = Fraction(restart["r031Radius"]["exact"])
    new_radius = Fraction(restart["targetRadius"]["exact"])
    expected_radii = {
        ("bivariate_radius", "R0.31"): old_radius,
        ("bivariate_radius", "R0.37"): new_radius,
        ("fixed_charge_radius", "R0.31"): old_radius**3,
        ("fixed_charge_radius", "R0.37"): new_radius**3,
    }
    for key, expected in expected_radii.items():
        row = radius_rows[key]
        if Fraction(row["exact"]) != expected:
            raise AssertionError(f"radius value mismatch: {key}")
        baseline = old_radius if key[0] == "bivariate_radius" else old_radius**3
        if Fraction(row["normalized_to_r031"]) != expected / baseline:
            raise AssertionError(f"normalized radius mismatch: {key}")
    if new_radius / old_radius != Fraction(4, 3):
        raise AssertionError("bivariate radius gain mismatch")
    if (new_radius / old_radius) ** 3 != Fraction(64, 27):
        raise AssertionError("fixed-charge radius gain mismatch")

    contraction = {row["metric"]: row for row in read_rows("contraction.csv")}
    mapping_ratio = Fraction(restart["mappingUpperBound"]["exact"]) / Fraction(
        restart["chosenBallRadius"]["exact"]
    )
    expected_contraction = {
        "active_linearization": Fraction(
            restart["linearizationNormUpperBound"]["exact"]
        ),
        "ball_mapping_ratio": mapping_ratio,
        "ball_lipschitz": Fraction(restart["lipschitzUpperBound"]["exact"]),
        "transport_operator": Fraction(
            restart["transportOperatorNormUpperBound"]["exact"]
        ),
    }
    for name, expected in expected_contraction.items():
        row = contraction[name]
        if Fraction(row["exact"]) != expected:
            raise AssertionError(f"contraction value mismatch: {name}")
        if expected >= Fraction(row["threshold"]):
            raise AssertionError(f"contraction threshold failed: {name}")

    residual = {row["metric"]: row for row in read_rows("residual-scales.csv")}
    expected_residual = {
        "exact_residual_norm": Fraction(restart["exactResidualNorm"]["exact"]),
        "residual_allowance": Fraction(restart["residualAllowance"]["exact"]),
    }
    for name, expected in expected_residual.items():
        if Fraction(residual[name]["exact"]) != expected:
            raise AssertionError(f"residual scale mismatch: {name}")
    if expected_residual["exact_residual_norm"] >= expected_residual[
        "residual_allowance"
    ]:
        raise AssertionError("exact residual does not fit the allowance")

    inverse = {
        row["name"]: row["exact_or_text"]
        for row in read_rows("inverse-metadata.csv")
    }
    jacobian = payload["finiteRegression"]["jacobian"]
    if int(inverse["finite_jacobian_dimension"]) != 62:
        raise AssertionError("finite Jacobian dimension mismatch")
    if inverse["jacobian_sha256"] != jacobian["jacobianSha256"]:
        raise AssertionError("Jacobian hash mismatch")
    if inverse["inverse_sha256"] != jacobian["inverseSha256"]:
        raise AssertionError("inverse hash mismatch")

    print(
        "validated four radius values, four contraction ratios, two residual "
        "scales, thirteen formal flags, and the 62-dimensional finite inverse"
    )


if __name__ == "__main__":
    main()
