#!/usr/bin/env python3
"""Validate R0.42 figure data against pinned exact sources."""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "research"))

import gmpy2

import edge_rational_asymptotic_audit as r028
import edge_short_continuation_audit as r036
import edge_charge_resolved_audit as r039


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
CERTIFICATE = REPOSITORY / "research/certificates/r042/edge-stretch-transport.json"
EXPECTED_CERTIFICATE_SHA256 = (
    "0c426070c47afb519fc9c705cbe11ed59b82ee6b28e766696280379b15e5dfa5"
)
EXPECTED_SOURCE_COMMIT = "5ff24eae1cb9f73a1aac6965b07f0c1f12c62477"
Rational = gmpy2.mpq


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def exact_endpoint(polynomial, radius: Rational, slope: int) -> Rational:
    return sum(
        (
            abs(coefficient)
            * radius ** r039.degree(exponent)
            * Rational(
                abs(r039.degree(exponent) * slope - r039.charge(exponent)),
                3,
            )
            for exponent, coefficient in polynomial.items()
        ),
        Rational(0),
    )


def main() -> None:
    actual_hash = hashlib.sha256(CERTIFICATE.read_bytes()).hexdigest()
    if actual_hash != EXPECTED_CERTIFICATE_SHA256:
        raise AssertionError("R0.42 certificate hash mismatch")
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if payload["git"] != {"commit": EXPECTED_SOURCE_COMMIT, "dirty": False}:
        raise AssertionError("R0.42 source provenance mismatch")
    if len(payload["checks"]) != 26 or not all(payload["checks"].values()):
        raise AssertionError("R0.42 formal checks are incomplete")

    radius_data = rows("radius-gain.csv")
    gate_data = rows("proof-gates.csv")
    endpoint_data = rows("endpoint-decomposition.csv")
    finite_data = rows("finite-columns.csv")
    if len(radius_data) != 14 or len(gate_data) != 9:
        raise AssertionError("unexpected radius or gate row count")
    if len(endpoint_data) != 12 or len(finite_data) != 5:
        raise AssertionError("unexpected endpoint or finite row count")

    active, _, _, _ = r028.rational_edge_recurrence(80, False, 0.0)
    polynomial = r036.field_to_polynomial(active, 80)
    if r036.polynomial_digest(polynomial) != payload["restartCertificate"][
        "degreeEightyPolynomialSha256"
    ]:
        raise AssertionError("independent polynomial digest mismatch")

    stage_records = {
        "acceptance": payload["acceptanceTest"],
        "target": payload["restartCertificate"],
        "failure": payload["negativeControl"],
    }
    radii = {
        stage: Rational(record["radius"]["exact"])
        for stage, record in stage_records.items()
    }
    for stage, record in stage_records.items():
        plus = exact_endpoint(polynomial, radii[stage], 2)
        minus = exact_endpoint(polynomial, radii[stage], -1)
        stretch = record["stretchOperator"]
        archived_plus = next(
            item for item in stretch["endpointColumns"] if item["label"] == "x=2"
        )
        archived_minus = next(
            item for item in stretch["endpointColumns"] if item["label"] == "x=-1"
        )
        if plus != Rational(archived_plus["bound"]["exact"]):
            raise AssertionError(f"independent x=2 endpoint mismatch at {stage}")
        if minus != Rational(archived_minus["bound"]["exact"]):
            raise AssertionError(f"independent x=-1 endpoint mismatch at {stage}")

    for row in endpoint_data:
        record = stage_records[row["stage"]]
        operator_key = (
            "directTransportComparison"
            if row["operator"] == "direct transport"
            else "stretchOperator"
        )
        endpoint = next(
            item
            for item in record[operator_key]["endpointColumns"]
            if item["label"] == "x=2"
        )
        field = {
            "polynomial": "bound",
            "tail": "tailContributionUpperBound",
            "total": "totalBound",
        }[row["component"]]
        if Fraction(row["exact"]) != Fraction(endpoint[field]["exact"]):
            raise AssertionError("endpoint extraction mismatch")

    target_theorem = Fraction(
        payload["restartCertificate"]["stretchOperator"][
            "maximumPolynomialBound"
        ]["exact"]
    )
    for row in finite_data:
        if Fraction(row["exact"]) != target_theorem:
            raise AssertionError("finite column does not attain endpoint theorem")
        if row["maximum_slope_exact"] != "2" or row["equals_theorem"] != "True":
            raise AssertionError("finite endpoint classification mismatch")

    progress_rows = [
        json.loads(line)
        for line in (PACKAGE / "progress.ndjson").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    resource_data = rows("resources.csv")
    if progress_rows[-1]["stage"] != "all exact checks passed":
        raise AssertionError("progress log lacks successful completion")
    if resource_data[-1]["status"] != "exited:0" or len(resource_data) != 244:
        raise AssertionError("resource log does not match the successful run")

    print(
        "validated 14 radius rows, nine proof gates, 12 endpoint components, "
        "five finite columns, all 26 formal flags, independent polynomial "
        "endpoint reconstructions, and archived progress/resource records"
    )


if __name__ == "__main__":
    main()
