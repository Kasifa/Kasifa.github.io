#!/usr/bin/env python3
"""Extract R0.46 journal-figure tables from the pinned GMP certificate."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import shutil

import gmpy2


Q = gmpy2.mpq
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RESEARCH = ROOT / "research"
CERTIFICATE = RESEARCH / "certificates/r046/edge-two-block-weight.json"
EXPECTED_CERTIFICATE_SHA256 = (
    "9310267b894c32b61034ec5e8f34b7d49144028830713a5e86b59d5be00109d1"
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
        raise SystemExit("R0.46 certificate hash mismatch")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if not all(certificate["checks"].values()):
        raise SystemExit("R0.46 certificate contains a failed check")

    target = certificate["restartCertificate"]
    tail = target["tail"]
    zero_nonzero = Q(
        tail["zeroInputColumn"]["nonzeroOutputAtMinimumDegree"]["exact"]
    )
    minus_zero = Q(tail["minusOneColumn"]["zeroOutputAtMinimumDegree"]["exact"])
    minus_nonzero = Q(
        tail["minusOneColumn"]["nonzeroOutputAtMinimumDegree"]["exact"]
    )
    plus_zero = Q(tail["plusOneColumn"]["zeroOutputTermwiseBound"]["exact"])
    plus_nonzero = Q(
        tail["plusOneColumn"]["nonzeroOutputTermwiseBound"]["exact"]
    )
    finite = Q(tail["finitePositiveChargeMaximum"]["bound"]["exact"])
    large = Q(tail["commonSlopeLargeSector"]["bound"]["exact"])

    envelope_rows = []
    for index in range(101):
        weight = Q(1, 2) + Q(index, 200)
        values = {
            "s=0 endpoint": zero_nonzero / weight,
            "s=-1 endpoint": minus_nonzero + weight * minus_zero,
            "s=1 bound": plus_nonzero + weight * plus_zero,
            "finite s=162": finite,
            "large s>=241": large,
        }
        envelope = max(values.values())
        for series, value in (*values.items(), ("complete envelope", envelope)):
            envelope_rows.append(
                {
                    "sampleIndex": index,
                    "zeroChargeWeightExact": str(weight),
                    "zeroChargeWeightDecimal": decimal(weight),
                    "series": series,
                    "boundExact": str(value),
                    "boundDecimal": decimal(value),
                    "isCertifiedWeight": str(weight == Q(3, 4)).lower(),
                    "classification": "presentation sample of explicit rational formula",
                }
            )
    write_csv(
        HERE / "weight-envelope.csv",
        [
            "sampleIndex",
            "zeroChargeWeightExact",
            "zeroChargeWeightDecimal",
            "series",
            "boundExact",
            "boundDecimal",
            "isCertifiedWeight",
            "classification",
        ],
        envelope_rows,
    )

    radius_rows = []
    for label, block in (
        ("entry", certificate["entryControl"]),
        ("rescued", certificate["rescuedControl"]),
        ("target", certificate["restartCertificate"]),
        ("probe", certificate["negativeControl"]),
    ):
        for series, record in (
            ("two-block tail", block["tailLinearizationBound"]),
            ("unweighted R0.45", block["tail"]["unweightedR045Bound"]),
            ("canonical stretch", block["stretchOperatorBound"]),
        ):
            value = Q(record["exact"])
            radius_rows.append(
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
        radius_rows,
    )

    sector_rows = []
    for sector, record in (
        ("s=0", tail["zeroInputColumn"]),
        ("s=-1", tail["minusOneColumn"]),
        ("s=1", tail["plusOneColumn"]),
        ("s=162", tail["finitePositiveChargeMaximum"]),
        ("s>=241", tail["commonSlopeLargeSector"]),
    ):
        value = Q(record["bound"]["exact"])
        sector_rows.append(
            {
                "sector": sector,
                "boundExact": str(value),
                "boundDecimal": decimal(value),
                "passes": str(value < 1).lower(),
                "classification": "formal all-order sector",
            }
        )
    write_csv(
        HERE / "sector-bounds.csv",
        ["sector", "boundExact", "boundDecimal", "passes", "classification"],
        sector_rows,
    )

    ball = Q(target["chosenTwoBlockBallRadius"]["exact"])
    matrix = tail["coarseSeparateBlockMatrix"]
    proof_rows = [
        {
            "gate": "coarse block Perron",
            "valueExact": "",
            "valueDecimal": matrix["perronRootDisplayOnly"],
            "passes": "false",
            "classification": "display-only diagnostic; exact failure uses D+BC-1>0",
        },
        {
            "gate": "unweighted s=-1",
            "valueExact": tail["unweightedR045Bound"]["exact"],
            "valueDecimal": tail["unweightedR045Bound"]["decimal"],
            "passes": "false",
            "classification": "exact unweighted comparison",
        },
        {
            "gate": "correlated tail",
            "valueExact": target["tailLinearizationBound"]["exact"],
            "valueDecimal": target["tailLinearizationBound"]["decimal"],
            "passes": "true",
            "classification": "formal gate",
        },
        {
            "gate": "mapping / ball",
            "valueExact": str(Q(target["mappingUpperBound"]["exact"]) / ball),
            "valueDecimal": decimal(Q(target["mappingUpperBound"]["exact"]) / ball),
            "passes": "true",
            "classification": "formal gate",
        },
        {
            "gate": "Lipschitz",
            "valueExact": target["lipschitzUpperBound"]["exact"],
            "valueDecimal": target["lipschitzUpperBound"]["decimal"],
            "passes": "true",
            "classification": "formal gate",
        },
        {
            "gate": "canonical stretch",
            "valueExact": target["stretchOperatorBound"]["exact"],
            "valueDecimal": target["stretchOperatorBound"]["decimal"],
            "passes": "true",
            "classification": "formal gate",
        },
    ]
    write_csv(
        HERE / "proof-gates.csv",
        ["gate", "valueExact", "valueDecimal", "passes", "classification"],
        proof_rows,
    )

    shutil.copyfile(RESEARCH / "certificates/r046/progress.ndjson", HERE / "progress.ndjson")
    shutil.copyfile(RESEARCH / "certificates/r046/resources.csv", HERE / "resources.csv")


if __name__ == "__main__":
    main()
