#!/usr/bin/env python3
"""Extract exact R0.45 journal-figure tables from the pinned certificate."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import shutil
import sys
import time

import gmpy2


ROOT = Path(__file__).resolve().parents[3]
RESEARCH = ROOT / "research"
if str(RESEARCH) not in sys.path:
    sys.path.insert(0, str(RESEARCH))

import edge_charge_resolved_audit as r039  # noqa: E402
import edge_fixed_negative_charge_audit as r045  # noqa: E402
import edge_rational_asymptotic_audit as r028  # noqa: E402
import edge_short_continuation_audit as r036  # noqa: E402
import edge_weighted_restart_audit as r037  # noqa: E402


Q = gmpy2.mpq
HERE = Path(__file__).resolve().parent
CERTIFICATE = RESEARCH / "certificates/r045/edge-fixed-negative-charge.json"
EXPECTED_CERTIFICATE_SHA256 = (
    "abc588fb80a140cf78f0558119f50e7a15dce9b2d3fa5219a8b0f9456c8d0b7b"
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
        raise SystemExit("R0.45 certificate hash mismatch")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if not all(certificate["checks"].values()):
        raise SystemExit("R0.45 certificate contains a failed check")

    started = time.perf_counter()
    active, _, _, _ = r028.rational_edge_recurrence(80, False, started)
    polynomial = r036.field_to_polynomial(active, 80)
    if r037.polynomial_digest(polynomial) != certificate["restartCertificate"][
        "degreeEightyPolynomialSha256"
    ]:
        raise SystemExit("reconstructed polynomial digest mismatch")

    curve_rows: list[dict[str, object]] = []
    for radius_label, radius in (("target 0.371", Q(371, 1000)), ("probe 0.372", Q(372, 1000))):
        terms = r039.weighted_base_terms(polynomial, radius)
        for index in range(101):
            inverse_degree = Q(index, 8200)
            value = r045.exact_negative_charge_value(terms, inverse_degree)
            curve_rows.append(
                {
                    "radiusLabel": radius_label,
                    "radiusExact": str(radius),
                    "sampleIndex": index,
                    "inverseDegreeExact": str(inverse_degree),
                    "inverseDegreeDecimal": decimal(inverse_degree),
                    "columnExact": str(value),
                    "columnDecimal": decimal(value),
                    "isLatticeEndpoint": str(index == 100).lower(),
                    "classification": "presentation sample; not used in proof",
                }
            )
    write_csv(
        HERE / "negative-charge-curve.csv",
        [
            "radiusLabel",
            "radiusExact",
            "sampleIndex",
            "inverseDegreeExact",
            "inverseDegreeDecimal",
            "columnExact",
            "columnDecimal",
            "isLatticeEndpoint",
            "classification",
        ],
        curve_rows,
    )

    derivative_rows: list[dict[str, object]] = []
    for label, block in (
        ("entry 0.370", certificate["entryControl"]),
        ("target 0.371", certificate["restartCertificate"]),
        ("probe 0.372", certificate["negativeControl"]),
    ):
        theorem = block["exactNegativeChargeColumn"]
        for component, field in (
            ("q=1 obstruction", "qOneNegativeDerivativeUpperBound"),
            ("q=2 seed", "seedDerivativeLowerBound"),
            ("certified margin", "fullDerivativeLowerBound"),
        ):
            value = Q(theorem[field]["exact"])
            derivative_rows.append(
                {
                    "control": label,
                    "component": component,
                    "valueExact": str(value),
                    "valueDecimal": decimal(value),
                }
            )
    write_csv(
        HERE / "derivative-certificate.csv",
        ["control", "component", "valueExact", "valueDecimal"],
        derivative_rows,
    )

    control_rows: list[dict[str, object]] = []
    for label, block in (
        ("entry", certificate["entryControl"]),
        ("target", certificate["restartCertificate"]),
        ("probe", certificate["negativeControl"]),
    ):
        values = (
            ("exact s=-1", Q(block["exactNegativeChargeColumn"]["bound"]["exact"])),
            ("common large sector", Q(block["commonSlopeLargeSector"]["bound"]["exact"])),
            ("canonical stretch", Q(block["stretchOperatorBound"]["exact"])),
        )
        for series, value in values:
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
    old = certificate["restartCertificate"]["r044InheritedNegativeChargeBound"]
    control_rows.append(
        {
            "control": "target",
            "radiusExact": "371/1000",
            "radiusDecimal": "0.371",
            "series": "R0.44 inherited s=-1",
            "boundExact": old["exact"],
            "boundDecimal": old["decimal"],
            "passes": "false",
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

    target = certificate["restartCertificate"]
    ball = Q(target["chosenBallRadius"]["exact"])
    gate_rows = []
    for gate, value, classification in (
        ("active tail", Q(target["tailLinearizationBound"]["exact"]), "formal gate"),
        ("ball mapping / radius", Q(target["mappingUpperBound"]["exact"]) / ball, "formal gate"),
        ("Lipschitz", Q(target["lipschitzUpperBound"]["exact"]), "formal gate"),
        ("canonical stretch", Q(target["stretchOperatorBound"]["exact"]), "formal gate"),
        ("old direct transport", Q(target["directTransportBound"]["exact"]), "diagnostic, not a construction gate"),
    ):
        gate_rows.append(
            {
                "gate": gate,
                "boundExact": str(value),
                "boundDecimal": decimal(value),
                "thresholdExact": "1",
                "passes": str(value < 1).lower(),
                "classification": classification,
            }
        )
    write_csv(
        HERE / "proof-gates.csv",
        [
            "gate",
            "boundExact",
            "boundDecimal",
            "thresholdExact",
            "passes",
            "classification",
        ],
        gate_rows,
    )

    shutil.copyfile(RESEARCH / "certificates/r045/progress.ndjson", HERE / "progress.ndjson")
    shutil.copyfile(RESEARCH / "certificates/r045/resources.csv", HERE / "resources.csv")


if __name__ == "__main__":
    main()
