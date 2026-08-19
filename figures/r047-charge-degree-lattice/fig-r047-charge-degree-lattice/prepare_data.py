#!/usr/bin/env python3
"""Extract R0.47 journal-figure tables from the pinned GMP certificate."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import shutil
import sys

import gmpy2


Q = gmpy2.mpq
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESEARCH = ROOT / "research"
sys.path.insert(0, str(RESEARCH))

import edge_charge_degree_lattice_audit as r047  # noqa: E402
import edge_charge_resolved_audit as r039  # noqa: E402
import edge_rational_asymptotic_audit as r028  # noqa: E402
import edge_short_continuation_audit as r036  # noqa: E402
import edge_weighted_restart_audit as r037  # noqa: E402


CERTIFICATE = RESEARCH / "certificates/r047/edge-charge-degree-lattice.json"
EXPECTED_CERTIFICATE_SHA256 = (
    "e45bc20ddeab9efde83dafefc84514df0260f8831c102c4621f0fdcd43dea6c9"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decimal(value: Q, digits: int = 20) -> str:
    return format(float(value), f".{digits}g")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    if sha256(CERTIFICATE) != EXPECTED_CERTIFICATE_SHA256:
        raise SystemExit("R0.47 certificate hash mismatch")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if not all(certificate["checks"].values()):
        raise SystemExit("R0.47 certificate contains a failed check")

    target = certificate["restartCertificate"]
    target_tail = target["tail"]

    fixed_rows = []
    for record in target_tail["fixedPositiveChargeColumns"]:
        bound = Q(record["bound"]["exact"])
        fixed_rows.append(
            {
                "inputCharge": record["inputCharge"],
                "minimumTailDegree": record["minimumTailDegree"],
                "maximumEndpoint": record["maximumEndpoint"],
                "endpointAtInfinityExact": record["endpointAtInfinity"]["exact"],
                "endpointAtMinimumDegreeExact": record["endpointAtMinimumDegree"]["exact"],
                "boundExact": str(bound),
                "boundDecimal": decimal(bound),
                "isMaximum": str(record["inputCharge"] == 162).lower(),
                "classification": record["classification"],
            }
        )
    write_csv(
        HERE / "fixed-charge-bounds.csv",
        [
            "inputCharge",
            "minimumTailDegree",
            "maximumEndpoint",
            "endpointAtInfinityExact",
            "endpointAtMinimumDegreeExact",
            "boundExact",
            "boundDecimal",
            "isMaximum",
            "classification",
        ],
        fixed_rows,
    )

    active, _, _, _ = r028.rational_edge_recurrence(80, False, 0.0)
    polynomial = r036.field_to_polynomial(active, 80)
    if r037.polynomial_digest(polynomial) != target["degreeEightyPolynomialSha256"]:
        raise SystemExit("reconstructed polynomial hash mismatch")
    terms = r039.weighted_base_terms(polynomial, Q(target["radius"]["exact"]))
    parity_rows = []
    for branch, denominator in (("even", 242), ("odd", 241)):
        numerator, rational_denominator, _ = r047.endpoint_rational_function(
            terms, branch
        )
        for sample_index in range(81):
            y = Q(sample_index, 80 * denominator)
            value = r047.rational_function_value(
                numerator,
                rational_denominator,
                y,
            )
            parity_rows.append(
                {
                    "branch": branch,
                    "sampleIndex": sample_index,
                    "yExact": str(y),
                    "yDecimal": decimal(y),
                    "boundExact": str(value),
                    "boundDecimal": decimal(value),
                    "endpointLabel": (
                        "infinity"
                        if sample_index == 0
                        else (f"s={denominator}" if sample_index == 80 else "")
                    ),
                    "classification": (
                        "exact rational presentation sample; derivative sign, "
                        "not sampling, proves the continuous branch bound"
                    ),
                }
            )
    write_csv(
        HERE / "parity-endpoints.csv",
        [
            "branch",
            "sampleIndex",
            "yExact",
            "yDecimal",
            "boundExact",
            "boundDecimal",
            "endpointLabel",
            "classification",
        ],
        parity_rows,
    )

    control_rows = []
    for label, block in (
        ("entry", certificate["entryControl"]),
        ("target", certificate["restartCertificate"]),
        ("probe", certificate["negativeControl"]),
    ):
        for series, record in (
            ("lattice-sharp tail", block["tailLinearizationBound"]),
            ("R0.46 separated tail", block["tail"]["r046Bound"]),
            ("canonical stretch", block["stretchOperatorBound"]),
        ):
            value = Q(record["exact"])
            control_rows.append(
                {
                    "control": label,
                    "radiusExact": block["radius"]["exact"],
                    "radiusDecimal": block["radius"]["decimal"],
                    "series": series,
                    "boundExact": str(value),
                    "boundDecimal": decimal(value),
                    "passes": str(value < 1).lower(),
                }
            )
    write_csv(
        HERE / "radius-controls.csv",
        [
            "control",
            "radiusExact",
            "radiusDecimal",
            "series",
            "boundExact",
            "boundDecimal",
            "passes",
        ],
        control_rows,
    )

    sector_rows = []
    for sector, record in (
        ("s=0", target_tail["zeroInputColumn"]),
        ("s=-1", target_tail["minusOneColumn"]),
        ("s=1", target_tail["plusOneColumn"]),
        ("s=162", target_tail["fixedPositiveChargeMaximum"]),
        ("s>=241", target_tail["largeChargeLatticeSector"]),
    ):
        value = Q(record["bound"]["exact"])
        sector_rows.append(
            {
                "sector": sector,
                "boundExact": str(value),
                "boundDecimal": decimal(value),
                "passes": str(value < 1).lower(),
                "isMaximum": str(sector == "s=162").lower(),
                "classification": "formal all-order sector",
            }
        )
    write_csv(
        HERE / "sector-bounds.csv",
        [
            "sector",
            "boundExact",
            "boundDecimal",
            "passes",
            "isMaximum",
            "classification",
        ],
        sector_rows,
    )

    large = target_tail["largeChargeLatticeSector"]
    derivative_rows = []
    for branch, endpoint in (
        ("even", large["evenEndpoint"]),
        ("odd", large["oddEndpoint"]),
    ):
        derivative = endpoint["derivativeCertificate"]
        derivative_rows.append(
            {
                "branch": branch,
                "expectedDerivativeSign": derivative["expectedDerivativeSign"],
                "interval": endpoint["interval"],
                "bernsteinDegree": derivative["bernsteinDegree"],
                "bernsteinCoefficientCount": derivative["bernsteinCoefficientCount"],
                "minimumSignedBernsteinCoefficientExact": derivative[
                    "minimumSignedBernsteinCoefficient"
                ]["exact"],
                "minimumSignedBernsteinCoefficientDecimal": derivative[
                    "minimumSignedBernsteinCoefficient"
                ]["decimal"],
                "allPositive": str(
                    derivative["allSignedBernsteinCoefficientsPositive"]
                ).lower(),
                "subdivisionCount": derivative["subdivisionCount"],
            }
        )
    write_csv(
        HERE / "derivative-certificates.csv",
        [
            "branch",
            "expectedDerivativeSign",
            "interval",
            "bernsteinDegree",
            "bernsteinCoefficientCount",
            "minimumSignedBernsteinCoefficientExact",
            "minimumSignedBernsteinCoefficientDecimal",
            "allPositive",
            "subdivisionCount",
        ],
        derivative_rows,
    )

    shutil.copyfile(
        RESEARCH / "certificates/r047/progress.ndjson",
        HERE / "progress.ndjson",
    )
    shutil.copyfile(
        RESEARCH / "certificates/r047/resources.csv",
        HERE / "resources.csv",
    )


if __name__ == "__main__":
    main()
