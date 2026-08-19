#!/usr/bin/env python3
"""Prepare exact certificate-backed data for the R0.53 journal figure."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys
import time

import gmpy2


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESEARCH = ROOT / "research"
sys.path.insert(0, str(RESEARCH))

import edge_affine_charge_weight_audit as r051  # noqa: E402
import edge_charge_degree_lattice_audit as r047  # noqa: E402
import edge_rational_asymptotic_audit as r028  # noqa: E402
import edge_short_continuation_audit as r036  # noqa: E402
import edge_product_affine_charge_weight_audit as r053  # noqa: E402


Q = gmpy2.mpq
R052_CERTIFICATE = RESEARCH / "certificates/r052/edge-affine-family-global.json"
R053_CERTIFICATE = RESEARCH / "certificates/r053/edge-product-affine-charge-weight.json"
EXPECTED_SHA256 = {
    "r052": "b79e59ec327bc02b64e23ad3f903b6d61860a075d59ff75a43d82f5684590def",
    "r053": "5d6486dfcc6f2c016380a29698ed986213701b9441dd007d95acce4fc0ea67a5",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decimal(value: Q, digits: int = 24) -> str:
    return r053.r037.rational_decimal(value, digits)


def write_csv(name: str, rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-commit", required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    started = time.perf_counter()
    if re.fullmatch(r"[0-9a-f]{40}", args.source_commit) is None:
        raise SystemExit("--source-commit must be a full lowercase Git commit")
    if sha256(R052_CERTIFICATE) != EXPECTED_SHA256["r052"]:
        raise SystemExit("R0.52 certificate hash mismatch")
    if sha256(R053_CERTIFICATE) != EXPECTED_SHA256["r053"]:
        raise SystemExit("R0.53 certificate hash mismatch")
    old = json.loads(R052_CERTIFICATE.read_text(encoding="utf-8"))
    new = json.loads(R053_CERTIFICATE.read_text(encoding="utf-8"))
    if len(new["checks"]) != 28 or not all(new["checks"].values()):
        raise SystemExit("R0.53 certificate checks are incomplete")

    print("[R0.53 figure] reconstructing the exact degree-80 center", flush=True)
    active_field, _, _, interactions = r028.rational_edge_recurrence(
        80, False, started
    )
    polynomial = r036.field_to_polynomial(active_field, 80)
    polynomial_digest = r053.r037.polynomial_digest(polynomial)
    if polynomial_digest != new["finiteConstruction"]["degreeEightyPolynomialSha256"]:
        raise SystemExit("degree-80 polynomial hash mismatch")

    character = Q(new["input"]["character"]["exact"])
    lam = Q(new["input"]["lambda"]["exact"])
    mu = Q(new["input"]["mu"]["exact"])
    terms = r051.charge_scaled_terms(polynomial, character)
    zero_poly = r053.product_zero_sector_polynomial(terms, 80, lam, mu)
    active_poly = r053.exact_product_column_polynomial(
        terms, 80, 81, 162, lam, mu
    )

    print("[R0.53 figure] evaluating 121 exact threshold samples", flush=True)
    profile_rows: list[dict[str, object]] = []
    radius_start = Q(382624, 1_000_000)
    radius_step = Q(1, 20_000_000)
    root_lower = Q(new["input"]["rootBox"][0]["exact"])
    root_upper = Q(new["input"]["rootBox"][1]["exact"])
    old_upper = Q(new["comparisonWithR052"]["r052CompleteAffineUpper"]["exact"])
    for index in range(121):
        radius = radius_start + index * radius_step
        zero_deficit = 1 - r047.poly_evaluate(zero_poly, radius)
        active_deficit = 1 - r047.poly_evaluate(active_poly, radius)
        profile_rows.append(
            {
                "sampleIndex": index,
                "radiusExact": str(radius),
                "radiusDecimal": decimal(radius, 18),
                "zeroDeficitPpmExact": str(zero_deficit * 1_000_000),
                "zeroDeficitPpmDecimal": decimal(zero_deficit * 1_000_000, 24),
                "active162DeficitPpmExact": str(active_deficit * 1_000_000),
                "active162DeficitPpmDecimal": decimal(active_deficit * 1_000_000, 24),
                "sideOfCertifiedRoot": (
                    "left" if radius < root_lower else "right" if radius > root_upper else "root box"
                ),
                "classification": "exact-rational presentation sample; not root-isolation evidence",
            }
        )
    write_csv("threshold-profile.csv", profile_rows)

    print("[R0.53 figure] deriving strict comparison factors", flush=True)
    gains = []
    for order, (key, label, bound_kind) in enumerate(
        (
            ("restartGainFactor", "fixed restart", "certified lower factor"),
            ("rootRadiusGainLowerFactor", "sharp threshold", "strict lower factor"),
        ),
        start=1,
    ):
        factor = Q(new["comparisonWithR052"][key]["exact"])
        gains.append(
            {
                "order": order,
                "label": label,
                "comparison": "R0.53 product-affine / R0.52 complete-affine upper",
                "factorExact": str(factor),
                "factorDecimal": decimal(factor, 24),
                "gainPpmExact": str((factor - 1) * 1_000_000),
                "gainPpmDecimal": decimal((factor - 1) * 1_000_000, 24),
                "boundKind": bound_kind,
                "classification": "formal exact certificate comparison",
            }
        )
    write_csv("strict-gains.csv", gains)

    print("[R0.53 figure] retaining all 281 exact competitor gaps", flush=True)
    records = sorted(
        new["competitorDominance"]["records"],
        key=lambda record: Q(record["gapBelowZeroEquality"]["exact"]),
    )
    gap_rows = []
    for rank, record in enumerate(records, start=1):
        gap = Q(record["gapBelowZeroEquality"]["exact"])
        gap_rows.append(
            {
                "rankByGap": rank,
                "label": record["label"],
                "sector": record["sector"],
                "gapExact": str(gap),
                "gapDecimal": decimal(gap, 24),
                "gapSha256": record["gapBelowZeroEquality"]["sha256"],
                "isNearest": str(rank == 1).lower(),
                "isLargeChargeTail": str(record["label"] == "s>=280").lower(),
                "classification": "formal exact all-order competitor gap at the root-box right endpoint",
            }
        )
    write_csv("competitor-gaps.csv", gap_rows)

    metadata = {
        "schemaVersion": "1.0",
        "createdUtc": datetime.now(timezone.utc).isoformat(),
        "figureSourceCommit": args.source_commit,
        "certificateSha256": EXPECTED_SHA256,
        "certificateSourceCommit": new["git"]["commit"],
        "degreeEightyPolynomialSha256": polynomial_digest,
        "centerTerms": len(polynomial),
        "recurrenceOrderedInteractions": interactions,
        "profileRows": len(profile_rows),
        "profileRadiusStart": str(radius_start),
        "profileRadiusStep": str(radius_step),
        "profileRadiusEnd": str(radius_start + 120 * radius_step),
        "rootBox": [str(root_lower), str(root_upper)],
        "r052CompleteAffineUpper": str(old_upper),
        "gainRows": len(gains),
        "competitorRows": len(gap_rows),
        "nearestCompetitor": records[0]["label"],
        "minimumGapExact": gap_rows[0]["gapExact"],
        "formalArithmetic": "gmpy2.mpq over GMP",
        "decimalDecisionUse": False,
        "randomness": False,
        "displaySamplesAreProof": False,
        "wallSeconds": time.perf_counter() - started,
    }
    (HERE / "sampling-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"profileRows": len(profile_rows), "gainRows": len(gains), "competitorRows": len(gap_rows), "wallSeconds": metadata["wallSeconds"]}, sort_keys=True))


if __name__ == "__main__":
    main()
