#!/usr/bin/env python3
"""Validate every plotted R0.38 value against the pinned exact certificate."""

from __future__ import annotations

import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
CERTIFICATE = REPOSITORY / "research/certificates/r038/edge-tail-newton.json"
EXPECTED_CERTIFICATE_SHA256 = (
    "3eb320e8cef0289c7fa2fef00a38c3c66b6b4c5006375bf6386d784f6b95dbf4"
)
EXPECTED_SOURCE_COMMIT = "bc230622aeac611966c091c4beca734c783f65ac"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def by_key(name: str, key: str) -> dict[str, dict[str, str]]:
    return {row[key]: row for row in rows(name)}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    require(
        sha256(CERTIFICATE) == EXPECTED_CERTIFICATE_SHA256,
        "R0.38 certificate hash changed",
    )
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    require(payload["git"]["commit"] == EXPECTED_SOURCE_COMMIT, "source commit changed")
    require(payload["git"]["dirty"] is False, "formal source was dirty")
    require(len(payload["checks"]) == 17, "unexpected formal check count")
    require(all(payload["checks"].values()), "a formal R0.38 check failed")

    restart = payload["restartCertificate"]
    radius_rows = {
        (row["quantity"], row["version"]): row for row in rows("radius-gain.csv")
    }
    expected_radii = {
        ("bivariate_radius", "R0.31"): Fraction(
            restart["r031Radius"]["exact"]
        ),
        ("bivariate_radius", "R0.37"): Fraction(
            restart["r037Radius"]["exact"]
        ),
        ("bivariate_radius", "R0.38"): Fraction(
            restart["targetRadius"]["exact"]
        ),
    }
    expected_radii.update(
        {
            ("fixed_charge_radius", version): value**3
            for (quantity, version), value in list(expected_radii.items())
            if quantity == "bivariate_radius"
        }
    )
    require(set(radius_rows) == set(expected_radii), "radius row set changed")
    for key, expected in expected_radii.items():
        row = radius_rows[key]
        require(Fraction(row["exact"]) == expected, f"radius mismatch: {key}")
        baseline_key = (key[0], "R0.31")
        baseline = expected_radii[baseline_key]
        require(
            Fraction(row["normalized_to_r031"]) == expected / baseline,
            f"normalized radius mismatch: {key}",
        )
    require(
        Fraction(radius_rows[("bivariate_radius", "R0.38")]["normalized_to_r031"])
        == Fraction(4779, 2000),
        "R0.38 bivariate gain changed",
    )
    require(
        Fraction(radius_rows[("fixed_charge_radius", "R0.38")]["normalized_to_r031"])
        == Fraction(restart["fixedChargeGainFromR031"]["exact"]),
        "R0.38 fixed-charge gain changed",
    )

    contraction = by_key("contraction.csv", "metric")
    expected_contraction = {
        "old_full_space_bound": Fraction(
            restart["oldFullSpaceLinearizationBound"]["exact"]
        ),
        "tail_linearization": Fraction(
            restart["tailLinearizationBound"]["exact"]
        ),
        "ball_mapping_ratio": Fraction(restart["mappingUpperBound"]["exact"])
        / Fraction(restart["chosenBallRadius"]["exact"]),
        "ball_lipschitz": Fraction(restart["lipschitzUpperBound"]["exact"]),
        "transport_operator": Fraction(
            restart["transportOperatorNormUpperBound"]["exact"]
        ),
        "nearby_failure_probe": Fraction(
            restart["nearbyFailureProbe"]["tailLinearizationBound"]["exact"]
        ),
        "finite_tail_column": Fraction(
            payload["finiteRegression"]["tailColumns"][
                "maximumWeightedColumnRatio"
            ]["exact"]
        ),
    }
    require(set(contraction) == set(expected_contraction), "contraction row set changed")
    for key, expected in expected_contraction.items():
        require(
            Fraction(contraction[key]["exact"]) == expected,
            f"contraction mismatch: {key}",
        )
        require(Fraction(contraction[key]["threshold"]) == 1, "threshold changed")
    require(expected_contraction["old_full_space_bound"] > 1, "old bound must fail")
    require(expected_contraction["tail_linearization"] < 1, "tail bound must close")
    require(expected_contraction["ball_mapping_ratio"] < 1, "ball map must close")
    require(expected_contraction["ball_lipschitz"] < 1, "Lipschitz must close")
    require(expected_contraction["transport_operator"] < 1, "transport must close")
    require(expected_contraction["nearby_failure_probe"] > 1, "probe must fail")
    require(
        expected_contraction["finite_tail_column"]
        < expected_contraction["tail_linearization"],
        "finite column must remain below the all-order bound",
    )

    residual = by_key("residual-scales.csv", "metric")
    require(
        Fraction(residual["exact_residual_norm"]["exact"])
        == Fraction(restart["exactResidualNorm"]["exact"]),
        "residual norm changed",
    )
    require(
        Fraction(residual["residual_allowance"]["exact"])
        == Fraction(restart["residualAllowance"]["exact"]),
        "residual allowance changed",
    )
    require(
        Fraction(residual["exact_residual_norm"]["exact"])
        < Fraction(residual["residual_allowance"]["exact"]),
        "residual no longer fits",
    )

    metadata = by_key("preconditioner-metadata.csv", "name")
    low_block = payload["lowBlockPreconditionerAudit"]["finiteBlock"]
    tail_columns = payload["finiteRegression"]["tailColumns"]
    require(metadata["finite_low_block_dimension"]["exact_or_text"] == "62", "low dimension changed")
    require(metadata["tail_low_projection_terms"]["exact_or_text"] == "0", "low projection changed")
    require(
        metadata["tail_defect_factor_after_low_preconditioner"]["exact_or_text"]
        == "1",
        "tail defect identity changed",
    )
    require(metadata["finite_tail_columns"]["exact_or_text"] == "55", "column count changed")
    require(
        Fraction(metadata["candidate_gap_factor_lower"]["exact_or_text"])
        == Fraction(payload["candidateComparison"]["candidateGapFactorLower"]["exact"]),
        "candidate gap changed",
    )
    require(
        metadata["jacobian_sha256"]["exact_or_text"] == low_block["jacobianSha256"],
        "Jacobian hash changed",
    )
    require(
        metadata["inverse_sha256"]["exact_or_text"] == low_block["inverseSha256"],
        "inverse hash changed",
    )
    require(tail_columns["lowProjectionTerms"] == 0, "tail left the high block")

    progress_records = [
        json.loads(line)
        for line in (PACKAGE / "progress.ndjson").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    require(len(progress_records) == 7, "progress stage count changed")
    require(progress_records[-1]["passed"] is True, "progress did not complete")
    resource_rows = rows("resources.csv")
    require(len(resource_rows) == 253, "resource sample count changed")
    require(resource_rows[-1]["status"] == "exited:0", "resource monitor did not exit cleanly")

    print(
        "validated six radius values, seven contraction metrics, two residual "
        "scales, seven preconditioner fields, seventeen formal flags, and "
        "the monitored source records"
    )


if __name__ == "__main__":
    main()
