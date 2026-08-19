#!/usr/bin/env python3
"""Validate every plotted R0.36 value against the formal exact certificate."""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
CERTIFICATE = (
    REPOSITORY / "research/certificates/r036/edge-short-continuation.json"
)
EXPECTED_CERTIFICATE_SHA256 = (
    "dfe0395df8b9654f235207c71dda5a0de8a70a54908b76b92dca00ad83c38e48"
)
EXPECTED_SOURCE_COMMIT = "e8685f41005a3149ebff91e9f4d537b02dbacb00"


def read_rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def main() -> None:
    actual_hash = hashlib.sha256(CERTIFICATE.read_bytes()).hexdigest()
    if actual_hash != EXPECTED_CERTIFICATE_SHA256:
        raise AssertionError("R0.36 certificate hash mismatch")
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if payload["git"] != {"commit": EXPECTED_SOURCE_COMMIT, "dirty": False}:
        raise AssertionError("R0.36 source state mismatch")
    if len(payload["checks"]) != 12 or not all(payload["checks"].values()):
        raise AssertionError("R0.36 formal checks are incomplete")

    geometry = {row["name"]: row for row in read_rows("geometry.csv")}
    expected_normalized = {
        "r031_radius": Fraction(1),
        "center_modulus": Fraction(1, 7),
        "inner_local_radius": Fraction(1, 7),
        "inner_affine_orbit_extent": Fraction(3, 7),
        "outer_local_radius": Fraction(5, 7),
        "outer_disc_origin_extent": Fraction(6, 7),
        "origin_inner_after_conjugacy": Fraction(2, 7),
        "origin_outer_after_conjugacy": Fraction(4, 7),
        "r031_containment_margin": Fraction(1, 7),
        "affine_orbit_margin": Fraction(2, 7),
    }
    rho = Fraction(4, 81)
    for name, normalized in expected_normalized.items():
        row = geometry[name]
        if Fraction(row["normalized_by_r031"]) != normalized:
            raise AssertionError(f"normalized geometry mismatch: {name}")
        if Fraction(row["exact"]) != rho * normalized:
            raise AssertionError(f"exact geometry mismatch: {name}")

    scales = {row["name"]: row for row in read_rows("certificate-scales.csv")}
    inclusion = payload["inclusionCertificate"]
    expected_scales = {
        "all_order_residual_upper_bound": inclusion[
            "allOrderResidualUpperBound"
        ]["exact"],
        "outer_tail_bound": inclusion["outerTailBound"]["exact"],
        "inner_inclusion_radius": inclusion["innerInclusionRadius"]["exact"],
        "finite_exact_residual_norm": inclusion[
            "exactConjugatedResidualNorm"
        ]["exact"],
    }
    for name, expected in expected_scales.items():
        if Fraction(scales[name]["exact"]) != Fraction(expected):
            raise AssertionError(f"certificate scale mismatch: {name}")
        decimal = float(scales[name]["decimal"])
        if decimal <= 0:
            raise AssertionError(f"nonpositive plotted scale: {name}")

    residual = Fraction(expected_scales["finite_exact_residual_norm"])
    residual_bound = Fraction(expected_scales["all_order_residual_upper_bound"])
    if residual > residual_bound:
        raise AssertionError("finite residual exceeds its all-order upper bound")

    jacobian = {row["name"]: row["exact_or_text"] for row in read_rows("jacobian.csv")}
    formal_jacobian = payload["finiteRegression"]["jacobian"]
    if int(jacobian["dimension"]) != 42:
        raise AssertionError("finite Jacobian dimension mismatch")
    if formal_jacobian["leftInverseExact"] is not True:
        raise AssertionError("left inverse check failed")
    if formal_jacobian["rightInverseExact"] is not True:
        raise AssertionError("right inverse check failed")
    if jacobian["jacobian_sha256"] != formal_jacobian["jacobianSha256"]:
        raise AssertionError("Jacobian hash mismatch")
    if jacobian["inverse_sha256"] != formal_jacobian["inverseSha256"]:
        raise AssertionError("inverse hash mismatch")

    print(
        "validated ten exact geometry values, four certified scales, "
        "twelve formal flags, and the 42-dimensional finite inverse metadata"
    )


if __name__ == "__main__":
    main()
