#!/usr/bin/env python3
"""Extract exact R0.44 journal-figure tables from the pinned certificate."""

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

import edge_common_slope_tail_audit as r044  # noqa: E402
import edge_charge_degree_floor_audit as r043  # noqa: E402
import edge_charge_resolved_audit as r039  # noqa: E402
import edge_rational_asymptotic_audit as r028  # noqa: E402
import edge_short_continuation_audit as r036  # noqa: E402
import edge_weighted_restart_audit as r037  # noqa: E402


Q = gmpy2.mpq
HERE = Path(__file__).resolve().parent
CERTIFICATE = RESEARCH / "certificates/r044/edge-common-slope-tail.json"
EXPECTED_CERTIFICATE_SHA256 = (
    "7966771f25305211907e11e1a7ab7b6d784b1a14e3db92b3cbec37b96382bb1f"
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


def record(value: Q) -> tuple[str, str]:
    return str(value), decimal(value)


def main() -> None:
    if sha256(CERTIFICATE) != EXPECTED_CERTIFICATE_SHA256:
        raise SystemExit("R0.44 certificate hash mismatch")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if not all(certificate["checks"].values()):
        raise SystemExit("R0.44 certificate contains a failed check")

    started = time.perf_counter()
    active, _, _, _ = r028.rational_edge_recurrence(80, False, started)
    polynomial = r036.field_to_polynomial(active, 80)
    if r037.polynomial_digest(polynomial) != certificate["restartCertificate"][
        "degreeEightyPolynomialSha256"
    ]:
        raise SystemExit("reconstructed polynomial digest mismatch")

    radius = Q(certificate["restartCertificate"]["radius"]["exact"])
    terms = r039.weighted_base_terms(polynomial, radius)
    slopes = {Q(0), Q(2)}
    for base_degree, base_charge, _weight in terms:
        if 0 <= base_charge <= 2 * base_degree:
            slopes.add(Q(base_charge, base_degree))
    envelope_rows: list[dict[str, object]] = []
    for slope in sorted(slopes):
        value = r044.common_slope_value(terms, slope, 80, 241)
        slope_exact, slope_decimal = record(slope)
        value_exact, value_decimal = record(value)
        envelope_rows.append(
            {
                "slopeExact": slope_exact,
                "slopeDecimal": slope_decimal,
                "boundExact": value_exact,
                "boundDecimal": value_decimal,
                "isEndpoint": str(slope in {Q(0), Q(2)}).lower(),
                "isMaximum": str(
                    value
                    == Q(
                        certificate["restartCertificate"][
                            "commonSlopeLargeSector"
                        ]["bound"]["exact"]
                    )
                ).lower(),
            }
        )
    write_csv(
        HERE / "common-slope-envelope.csv",
        [
            "slopeExact",
            "slopeDecimal",
            "boundExact",
            "boundDecimal",
            "isEndpoint",
            "isMaximum",
        ],
        envelope_rows,
    )

    groups = (
        ("q=-1", lambda q: q == -1),
        ("q=0", lambda q: q == 0),
        ("q=1", lambda q: q == 1),
        ("q=2", lambda q: q == 2),
        ("q>=3", lambda q: q >= 3),
    )
    bridge_rows: list[dict[str, object]] = []
    for label, predicate in groups:
        legacy = Q(0)
        common = Q(0)
        for base_degree, base_charge, weight in terms:
            if not predicate(base_charge):
                continue
            legacy += weight * r043.large_charge_degree_floor_factor(
                base_degree,
                base_charge,
                80,
                241,
            )
            common += (
                weight
                * Q(base_degree + 121, base_degree + 120)
                * r044.charge_factor_upper(base_charge, 241)
                * abs(2 * base_degree - base_charge)
                / 3
            )
        reduction = legacy - common
        bridge_rows.append(
            {
                "baseChargeGroup": label,
                "legacyExact": str(legacy),
                "legacyDecimal": decimal(legacy),
                "commonExact": str(common),
                "commonDecimal": decimal(common),
                "reductionExact": str(reduction),
                "reductionDecimal": decimal(reduction),
            }
        )
    write_csv(
        HERE / "slope-loss-bridge.csv",
        [
            "baseChargeGroup",
            "legacyExact",
            "legacyDecimal",
            "commonExact",
            "commonDecimal",
            "reductionExact",
            "reductionDecimal",
        ],
        bridge_rows,
    )

    controls = (
        ("entry", certificate["entryControl"]),
        ("target", certificate["restartCertificate"]),
        ("failureProbe", certificate["negativeControl"]),
    )
    radius_rows: list[dict[str, object]] = []
    for label, block in controls:
        common = Q(block["commonSlopeLargeSector"]["bound"]["exact"])
        complete = Q(block["tailLinearizationBound"]["exact"])
        finite_minus_one = complete
        stretch = Q(block["stretchOperatorBound"]["exact"])
        radius_value = Q(block["radius"]["exact"])
        for series, value in (
            ("common large sector", common),
            ("finite s=-1 / complete tail", finite_minus_one),
            ("canonical stretch", stretch),
        ):
            radius_rows.append(
                {
                    "control": label,
                    "radiusExact": str(radius_value),
                    "radiusDecimal": decimal(radius_value),
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
        radius_rows,
    )

    target = certificate["restartCertificate"]
    ball = Q(target["chosenBallRadius"]["exact"])
    proof_rows = []
    for gate, value, classification in (
        (
            "active tail",
            Q(target["tailLinearizationBound"]["exact"]),
            "formal gate",
        ),
        (
            "ball mapping / radius",
            Q(target["mappingUpperBound"]["exact"]) / ball,
            "formal gate",
        ),
        (
            "Lipschitz",
            Q(target["lipschitzUpperBound"]["exact"]),
            "formal gate",
        ),
        (
            "canonical stretch",
            Q(target["stretchOperatorBound"]["exact"]),
            "formal gate",
        ),
        (
            "old direct transport",
            Q(target["directTransportBound"]["exact"]),
            "diagnostic, not a construction gate",
        ),
    ):
        proof_rows.append(
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
        proof_rows,
    )

    shutil.copy2(RESEARCH / "certificates/r044/progress.ndjson", HERE / "progress.ndjson")
    shutil.copy2(RESEARCH / "certificates/r044/resources.csv", HERE / "resources.csv")
    print(
        json.dumps(
            {
                "envelopeRows": len(envelope_rows),
                "bridgeRows": len(bridge_rows),
                "radiusRows": len(radius_rows),
                "proofRows": len(proof_rows),
                "certificateSha256": EXPECTED_CERTIFICATE_SHA256,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
