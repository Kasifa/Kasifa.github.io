#!/usr/bin/env python3
"""Prepare certificate-backed tables for the R0.54 journal figure."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from decimal import Decimal, getcontext
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import time


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CERTIFICATE = ROOT / "research/certificates/r054/edge-product-affine-family-global.json"
DIAGNOSTIC = ROOT / "research/certificates/r054/product-family-diagnostic.json"
EXPECTED_SHA256 = {
    "certificate": "130e954c3f8b711c28664f6f1d2aeb589942f69773ac9c839d98cc8f71b3006b",
    "diagnostic": "0553525f77aeffbe74eb64eda300d5673159022776aa15a6d963d5e7f45618bf",
}
getcontext().prec = 100


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decimal_fraction(value: Fraction, digits: int = 28) -> str:
    result = Decimal(value.numerator) / Decimal(value.denominator)
    return format(result, f".{digits}g")


def fraction_record(value: Fraction) -> tuple[str, str]:
    return str(value), decimal_fraction(value)


def write_csv(name: str, rows: list[dict[str, object]]) -> None:
    with (HERE / name).open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def basin(record: dict[str, object]) -> str:
    alpha = float(record["scaledAlpha"])
    beta = float(record["scaledBeta"])
    lower = min(alpha, beta)
    upper = max(alpha, beta)
    if lower > 0.8 and abs(alpha - beta) < 0.05:
        return "symmetric product interior"
    if lower < 0.1 and upper > 0.8:
        return "single-factor boundary"
    if upper < 0.1:
        return "near character-only boundary"
    return "other"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-commit", required=True)
    arguments = parser.parse_args()
    if re.fullmatch(r"[0-9a-f]{40}", arguments.source_commit) is None:
        raise SystemExit("--source-commit must be a full lowercase Git commit")
    started = time.perf_counter()
    if sha256(CERTIFICATE) != EXPECTED_SHA256["certificate"]:
        raise SystemExit("R0.54 exact certificate hash mismatch")
    if sha256(DIAGNOSTIC) != EXPECTED_SHA256["diagnostic"]:
        raise SystemExit("R0.54 diagnostic hash mismatch")
    exact = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    diagnostic = json.loads(DIAGNOSTIC.read_text(encoding="utf-8"))
    if len(exact["checks"]) != 16 or not all(exact["checks"].values()):
        raise SystemExit("R0.54 exact checks are incomplete")

    print("[R0.54 figure] sampling the exact invariant boundary", flush=True)
    domain_rows: list[dict[str, object]] = []
    for index in range(201):
        scaled_a = Fraction(index, 100)
        lower = max(Fraction(0), scaled_a - 1)
        upper = scaled_a * scaled_a / 4
        x_exact, x_decimal = fraction_record(scaled_a)
        lower_exact, lower_decimal = fraction_record(lower)
        upper_exact, upper_decimal = fraction_record(upper)
        domain_rows.append(
            {
                "sampleIndex": index,
                "scaledAExact": x_exact,
                "scaledADecimal": x_decimal,
                "scaledBLowerExact": lower_exact,
                "scaledBLowerDecimal": lower_decimal,
                "scaledBUpperExact": upper_exact,
                "scaledBUpperDecimal": upper_decimal,
                "classification": "exact invariant-domain presentation sample",
            }
        )
    write_csv("invariant-domain.csv", domain_rows)

    print("[R0.54 figure] reconstructing all 14 exact cover leaves", flush=True)
    cover = exact["continuousDomainCover"]
    c_lower = Fraction(cover["characterInterval"][0]["exact"])
    c_upper = Fraction(cover["characterInterval"][1]["exact"])
    c_width = c_upper - c_lower
    leaf_rows: list[dict[str, object]] = []
    for order, leaf in enumerate(cover["leafRecords"], start=1):
        c_denominator = 2 ** int(leaf["cDepth"])
        c_left = c_lower + c_width * Fraction(int(leaf["cIndex"]), c_denominator)
        c_right = c_lower + c_width * Fraction(int(leaf["cIndex"]) + 1, c_denominator)
        a_base = 0 if leaf["region"] == "A<=h" else 1
        a_denominator = 2 ** int(leaf["aDepth"])
        a_left = Fraction(a_base) + Fraction(int(leaf["aIndex"]), a_denominator)
        a_right = Fraction(a_base) + Fraction(int(leaf["aIndex"]) + 1, a_denominator)
        leaf_rows.append(
            {
                "order": order,
                "region": leaf["region"],
                "characterDepth": leaf["cDepth"],
                "characterIndex": leaf["cIndex"],
                "invariantDepth": leaf["aDepth"],
                "invariantIndex": leaf["aIndex"],
                "characterLowerExact": str(c_left),
                "characterLowerDecimal": decimal_fraction(c_left),
                "characterUpperExact": str(c_right),
                "characterUpperDecimal": decimal_fraction(c_right),
                "scaledALowerExact": str(a_left),
                "scaledALowerDecimal": decimal_fraction(a_left),
                "scaledAUpperExact": str(a_right),
                "scaledAUpperDecimal": decimal_fraction(a_right),
                "excludedBy": leaf["excludedBy"],
                "minimumCoefficientDecimal": leaf["minimumBernsteinCoefficient"]["decimal"],
                "minimumCoefficientSha256": leaf["minimumBernsteinCoefficient"]["sha256"],
                "classification": "formal exact continuous-cover leaf",
            }
        )
    write_csv("cover-leaves.csv", leaf_rows)

    print("[R0.54 figure] deriving the formal enclosure and diagnostic point", flush=True)
    comparison = exact["comparisonWithCompleteAffineFamily"]
    global_bound = exact["globalProductAffineFamilyBound"]
    affine = Fraction(comparison["completeAffineUpper"]["exact"])
    lower = Fraction(global_bound["optimalRadiusLower"]["exact"])
    upper = Fraction(global_bound["optimalRadiusUpper"]["exact"])
    candidate_decimal = Decimal(diagnostic["symmetricCandidate"]["radius"])
    affine_decimal = Decimal(affine.numerator) / Decimal(affine.denominator)
    enclosure_rows = []
    for order, label, kind, radius, status in (
        (1, "R0.53 witness lower", "formal lower", lower, "certified"),
        (2, "100-digit symmetric candidate", "diagnostic point", None, "not proof"),
        (3, "R0.54 complete-family upper", "formal upper", upper, "certified"),
    ):
        if radius is None:
            radius_exact = ""
            radius_decimal = format(candidate_decimal, ".48g")
            gain_exact = ""
            gain_decimal = format((candidate_decimal / affine_decimal - 1) * Decimal(1_000_000), ".32g")
        else:
            radius_exact = str(radius)
            radius_decimal = decimal_fraction(radius, 48)
            gain = (radius / affine - 1) * 1_000_000
            gain_exact = str(gain)
            gain_decimal = decimal_fraction(gain, 32)
        enclosure_rows.append(
            {
                "order": order,
                "label": label,
                "kind": kind,
                "status": status,
                "radiusExact": radius_exact,
                "radiusDecimal": radius_decimal,
                "gainPpmExact": gain_exact,
                "gainPpmDecimal": gain_decimal,
                "classification": (
                    "formal exact comparison" if radius is not None else "100-digit diagnostic; not used by theorem"
                ),
            }
        )
    write_csv("global-enclosure.csv", enclosure_rows)

    print("[R0.54 figure] retaining all 64 diagnostic optimizer records", flush=True)
    diagnostic_rows = []
    for record in diagnostic["multistart"]["allRecords"]:
        radius = Decimal(str(record["radius"]))
        diagnostic_rows.append(
            {
                "index": record["index"],
                "success": str(record["success"]).lower(),
                "status": record["status"],
                "radiusDecimal": record["radius"],
                "gainPpmDecimal": format((radius / affine_decimal - 1) * Decimal(1_000_000), ".20g"),
                "characterDecimal": record["character"],
                "scaledAlphaDecimal": record["scaledAlpha"],
                "scaledBetaDecimal": record["scaledBeta"],
                "symmetryDefectDecimal": abs(float(record["scaledAlpha"]) - float(record["scaledBeta"])),
                "activeMarginDecimal": record["activeMargin"],
                "zeroMarginDecimal": record["zeroMargin"],
                "basin": basin(record),
                "classification": "finite deterministic floating-point reconnaissance",
            }
        )
    write_csv("diagnostic-starts.csv", diagnostic_rows)

    candidate_u = Decimal(diagnostic["symmetricCandidate"]["scaledAlpha"])
    metadata = {
        "schemaVersion": "1.0",
        "createdUtc": datetime.now(timezone.utc).isoformat(),
        "figureSourceCommit": arguments.source_commit,
        "certificateSha256": EXPECTED_SHA256,
        "formalSourceCommit": exact["git"]["commit"],
        "certificateChecks": len(exact["checks"]),
        "coverLeafCount": len(leaf_rows),
        "coverExclusionCounts": cover["exclusionCounts"],
        "coverLeafSetSha256": cover["leafSetSha256"],
        "domainRows": len(domain_rows),
        "enclosureRows": len(enclosure_rows),
        "diagnosticRows": len(diagnostic_rows),
        "diagnosticConvergedFeasibleRuns": diagnostic["multistart"]["convergedFeasibleRuns"],
        "candidate": {
            "radius": diagnostic["symmetricCandidate"]["radius"],
            "character": diagnostic["symmetricCandidate"]["character"],
            "scaledA": format(2 * candidate_u, ".60g"),
            "scaledB": format(candidate_u * candidate_u, ".60g"),
            "antisymmetricSecondDerivative": diagnostic["symmetricCandidate"]["antisymmetricSecondDerivative"],
            "classification": "100-digit diagnostic only",
        },
        "formalArithmetic": "gmpy2.mpq over GMP in the pinned certificate",
        "decimalDecisionUse": False,
        "diagnosticFloatingPointUse": True,
        "randomSeed": diagnostic["multistart"]["seed"],
        "displaySamplesAreProof": False,
        "wallSeconds": time.perf_counter() - started,
    }
    (HERE / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "domainRows": len(domain_rows),
                "coverLeaves": len(leaf_rows),
                "diagnosticRows": len(diagnostic_rows),
                "wallSeconds": metadata["wallSeconds"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
