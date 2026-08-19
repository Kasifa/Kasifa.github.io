#!/usr/bin/env python3
"""Extract exact R0.41 radius, charge, degree, and proof-gate data."""

from __future__ import annotations

import csv
from fractions import Fraction
import json
from pathlib import Path
import shutil


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
CERTIFICATE_DIRECTORY = REPOSITORY / "research/certificates/r041"
CERTIFICATE = CERTIFICATE_DIRECTORY / "edge-degree-resolved-tail.json"
R040_CERTIFICATE = (
    REPOSITORY / "research/certificates/r040/edge-slope-resolved-transport.json"
)
R039_CERTIFICATE = (
    REPOSITORY / "research/certificates/r039/edge-charge-resolved.json"
)
R038_CERTIFICATE = (
    REPOSITORY / "research/certificates/r038/edge-tail-newton.json"
)


def write_rows(
    path: Path,
    fieldnames: tuple[str, ...],
    rows: list[dict[str, object]],
) -> None:
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def decimal(value: Fraction) -> str:
    return format(float(value), ".20g")


def main() -> None:
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    r040_payload = json.loads(R040_CERTIFICATE.read_text(encoding="utf-8"))
    r039_payload = json.loads(R039_CERTIFICATE.read_text(encoding="utf-8"))
    r038_payload = json.loads(R038_CERTIFICATE.read_text(encoding="utf-8"))
    restart = payload["restartCertificate"]
    r040_restart = r040_payload["restartCertificate"]

    radii = (
        ("R0.31", Fraction(r040_restart["r031Radius"]["exact"])),
        (
            "R0.37",
            Fraction(r038_payload["restartCertificate"]["r037Radius"]["exact"]),
        ),
        (
            "R0.38",
            Fraction(r039_payload["restartCertificate"]["r038Radius"]["exact"]),
        ),
        ("R0.39", Fraction(r040_restart["r039Radius"]["exact"])),
        ("R0.40", Fraction(restart["previousRadius"]["exact"])),
        ("R0.41", Fraction(restart["radius"]["exact"])),
    )
    radius_rows: list[dict[str, object]] = []
    for quantity, power in (("common_radius", 1), ("fixed_charge_radius", 3)):
        baseline = radii[0][1] ** power
        for version, radius in radii:
            value = radius**power
            radius_rows.append(
                {
                    "quantity": quantity,
                    "version": version,
                    "exact": str(value),
                    "decimal": decimal(value),
                    "normalized_to_r031": str(value / baseline),
                }
            )
    write_rows(
        PACKAGE / "radius-gain.csv",
        ("quantity", "version", "exact", "decimal", "normalized_to_r031"),
        radius_rows,
    )

    charge_rows: list[dict[str, object]] = []
    for record in payload["activeTailKernel"]["finiteColumns"]:
        value = Fraction(record["bound"]["exact"])
        charge = int(record["inputCharge"])
        charge_rows.append(
            {
                "sector": str(charge),
                "plot_charge": charge,
                "input_charge": charge,
                "minimum_tail_degree": record["minimumTailDegree"],
                "exact": str(value),
                "decimal": decimal(value),
                "kind": "exceptional" if charge <= 1 else "common_endpoint",
                "highlight": charge in {-1, 162},
                "classification": record["classification"],
            }
        )
    large = payload["activeTailKernel"]["largeChargeSector"]
    large_value = Fraction(large["bound"]["exact"])
    charge_rows.append(
        {
            "sector": ">=241",
            "plot_charge": 241,
            "input_charge": "",
            "minimum_tail_degree": "",
            "exact": str(large_value),
            "decimal": decimal(large_value),
            "kind": "large_charge",
            "highlight": True,
            "classification": large["classification"],
        }
    )
    write_rows(
        PACKAGE / "charge-columns.csv",
        (
            "sector",
            "plot_charge",
            "input_charge",
            "minimum_tail_degree",
            "exact",
            "decimal",
            "kind",
            "highlight",
            "classification",
        ),
        charge_rows,
    )

    sector_162 = next(
        record
        for record in payload["activeTailKernel"]["finiteColumns"]
        if record["inputCharge"] == 162
    )
    infinity = Fraction(sector_162["coreEndpointAtInfinity"]["exact"])
    sector_bound = Fraction(sector_162["bound"]["exact"])
    degree_rows: list[dict[str, object]] = []
    for record in payload["finiteRegression"]["degreeColumnsAtCharge162"][
        "records"
    ]:
        value = Fraction(record["exactColumn"]["exact"])
        degree_rows.append(
            {
                "input_degree": record["inputDegree"],
                "input_charge": record["inputCharge"],
                "exact": str(value),
                "decimal": decimal(value),
                "all_order_bound_exact": str(sector_bound),
                "all_order_bound_decimal": decimal(sector_bound),
                "infinite_core_exact": str(infinity),
                "infinite_core_decimal": decimal(infinity),
                "classification": record["classification"],
            }
        )
    write_rows(
        PACKAGE / "degree-columns.csv",
        (
            "input_degree",
            "input_charge",
            "exact",
            "decimal",
            "all_order_bound_exact",
            "all_order_bound_decimal",
            "infinite_core_exact",
            "infinite_core_decimal",
            "classification",
        ),
        degree_rows,
    )

    gates = (
        (
            "acceptance_legacy_tail",
            "0.257",
            "legacy tail",
            Fraction(payload["legacyComparison"]["legacyAcceptanceTail"]["exact"]),
        ),
        (
            "acceptance_resolved_tail",
            "0.257",
            "resolved tail",
            Fraction(payload["acceptanceTest"]["tailLinearizationBound"]["exact"]),
        ),
        (
            "acceptance_transport",
            "0.257",
            "transport",
            Fraction(payload["acceptanceTest"]["transportBound"]["exact"]),
        ),
        (
            "target_legacy_tail",
            "0.28125",
            "legacy tail",
            Fraction(payload["legacyComparison"]["legacyTargetTail"]["exact"]),
        ),
        (
            "target_resolved_tail",
            "0.28125",
            "resolved tail",
            Fraction(restart["tailLinearizationBound"]["exact"]),
        ),
        (
            "target_transport",
            "0.28125",
            "transport",
            Fraction(restart["transportBound"]["exact"]),
        ),
        (
            "probe_resolved_tail",
            "0.282",
            "resolved tail",
            Fraction(payload["negativeControl"]["tailLinearizationBound"]["exact"]),
        ),
        (
            "probe_transport",
            "0.282",
            "transport",
            Fraction(payload["negativeControl"]["transportBound"]["exact"]),
        ),
    )
    write_rows(
        PACKAGE / "proof-gates.csv",
        (
            "metric",
            "radius",
            "gate",
            "exact",
            "decimal",
            "threshold",
            "status",
            "classification",
        ),
        [
            {
                "metric": metric,
                "radius": radius,
                "gate": gate,
                "exact": str(value),
                "decimal": decimal(value),
                "threshold": "1",
                "status": "passes" if value < 1 else "fails",
                "classification": (
                    "all-order sufficient inequality; failure does not imply "
                    "singularity or loss of analyticity"
                ),
            }
            for metric, radius, gate, value in gates
        ],
    )

    shutil.copyfile(
        CERTIFICATE_DIRECTORY / "progress.ndjson",
        PACKAGE / "progress.ndjson",
    )
    shutil.copyfile(
        CERTIFICATE_DIRECTORY / "resources.csv",
        PACKAGE / "resources.csv",
    )


if __name__ == "__main__":
    main()
