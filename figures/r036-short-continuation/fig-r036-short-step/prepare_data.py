#!/usr/bin/env python3
"""Extract exact R0.36 geometry, enclosures, and finite inverse metadata."""

from __future__ import annotations

import csv
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
CERTIFICATE = (
    REPOSITORY / "research/certificates/r036/edge-short-continuation.json"
)


def write_rows(
    path: Path, fieldnames: tuple[str, ...], rows: list[dict[str, object]]
) -> None:
    with path.open("w", newline="", encoding="utf-8") as target:
        writer = csv.DictWriter(target, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    step = payload["shortStep"]
    radii = step["localRadii"]
    margins = step["strictMargins"]
    inclusion = payload["inclusionCertificate"]
    jacobian = payload["finiteRegression"]["jacobian"]

    geometry_rows = [
        {
            "name": "r031_radius",
            "exact": step["r031Radius"]["exact"],
            "decimal": step["r031Radius"]["decimal"],
            "normalized_by_r031": "1",
        },
        {
            "name": "center_modulus",
            "exact": step["center"]["Z"]["exact"],
            "decimal": step["center"]["Z"]["decimal"],
            "normalized_by_r031": "1/7",
        },
        {
            "name": "inner_local_radius",
            "exact": radii["inner"]["exact"],
            "decimal": radii["inner"]["decimal"],
            "normalized_by_r031": "1/7",
        },
        {
            "name": "inner_affine_orbit_extent",
            "exact": radii["innerAffineOrbitExtent"]["exact"],
            "decimal": radii["innerAffineOrbitExtent"]["decimal"],
            "normalized_by_r031": "3/7",
        },
        {
            "name": "outer_local_radius",
            "exact": radii["outer"]["exact"],
            "decimal": radii["outer"]["decimal"],
            "normalized_by_r031": "5/7",
        },
        {
            "name": "outer_disc_origin_extent",
            "exact": radii["outerDiscOriginExtent"]["exact"],
            "decimal": radii["outerDiscOriginExtent"]["decimal"],
            "normalized_by_r031": "6/7",
        },
        {
            "name": "origin_inner_after_conjugacy",
            "exact": radii["originInnerAfterConjugacy"]["exact"],
            "decimal": radii["originInnerAfterConjugacy"]["decimal"],
            "normalized_by_r031": "2/7",
        },
        {
            "name": "origin_outer_after_conjugacy",
            "exact": radii["originOuterAfterConjugacy"]["exact"],
            "decimal": radii["originOuterAfterConjugacy"]["decimal"],
            "normalized_by_r031": "4/7",
        },
        {
            "name": "r031_containment_margin",
            "exact": margins["r031Containment"]["exact"],
            "decimal": margins["r031Containment"]["decimal"],
            "normalized_by_r031": "1/7",
        },
        {
            "name": "affine_orbit_margin",
            "exact": margins["affineOrbitContainment"]["exact"],
            "decimal": margins["affineOrbitContainment"]["decimal"],
            "normalized_by_r031": "2/7",
        },
    ]
    write_rows(
        PACKAGE / "geometry.csv",
        ("name", "exact", "decimal", "normalized_by_r031"),
        geometry_rows,
    )

    scale_rows = [
        {
            "name": "all_order_residual_upper_bound",
            "classification": "all-order upper bound",
            "exact": inclusion["allOrderResidualUpperBound"]["exact"],
            "decimal": inclusion["allOrderResidualUpperBound"]["decimal"],
        },
        {
            "name": "outer_tail_bound",
            "classification": "all-order upper bound",
            "exact": inclusion["outerTailBound"]["exact"],
            "decimal": inclusion["outerTailBound"]["decimal"],
        },
        {
            "name": "inner_inclusion_radius",
            "classification": "all-order inclusion radius",
            "exact": inclusion["innerInclusionRadius"]["exact"],
            "decimal": inclusion["innerInclusionRadius"]["decimal"],
        },
        {
            "name": "finite_exact_residual_norm",
            "classification": "finite exact polynomial residual",
            "exact": inclusion["exactConjugatedResidualNorm"]["exact"],
            "decimal": inclusion["exactConjugatedResidualNorm"]["decimal"],
        },
    ]
    write_rows(
        PACKAGE / "certificate-scales.csv",
        ("name", "classification", "exact", "decimal"),
        scale_rows,
    )

    write_rows(
        PACKAGE / "jacobian.csv",
        ("name", "exact_or_text"),
        [
            {"name": "dimension", "exact_or_text": jacobian["dimension"]},
            {
                "name": "maximum_total_degree",
                "exact_or_text": jacobian["maximumTotalDegree"],
            },
            {
                "name": "jacobian_nonzero_entries",
                "exact_or_text": jacobian["jacobianNonzeroEntries"],
            },
            {
                "name": "inverse_nonzero_entries",
                "exact_or_text": jacobian["inverseNonzeroEntries"],
            },
            {
                "name": "maximum_unweighted_column_l1_norm",
                "exact_or_text": jacobian["maximumUnweightedColumnL1Norm"]["exact"],
            },
            {
                "name": "jacobian_sha256",
                "exact_or_text": jacobian["jacobianSha256"],
            },
            {
                "name": "inverse_sha256",
                "exact_or_text": jacobian["inverseSha256"],
            },
        ],
    )


if __name__ == "__main__":
    main()
