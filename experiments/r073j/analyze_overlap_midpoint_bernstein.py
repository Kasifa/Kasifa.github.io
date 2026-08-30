#!/usr/bin/env python3
"""Analyze the frozen R0.73J overlap grid by midpoint Bernstein ranges.

The exact interpolation coefficients are Acb balls.  Converting those full
balls to power/Bernstein form magnifies coefficient radii unnecessarily.
This analysis separates each coefficient into a zero-radius midpoint and a
rigorous residual.  The midpoint polynomial is ranged in tensor Bernstein
form; the residual is bounded directly in the Chebyshev basis using
``|T_k(t)| <= 1`` on every real parameter box.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from flint import acb, arb, ctx  # noqa: E402

from experiments.r073j.certify_overlap import (  # noqa: E402
    OUTPUT_NAMES,
    acb_from_record,
    acb_record,
    arb_rational,
    arb_text,
    contour_prerequisite,
    ledger_digest,
    overlap_majorant,
)
from research.r073j_chebyshev import (  # noqa: E402
    chebyshev_lebesgue_bound,
    inflate_by_modulus_error,
    interpolation_error,
    subdivide_tensor_bernstein,
    tensor_bernstein_hull,
    tensor_chebyshev_coefficients,
    tensor_chebyshev_to_bernstein,
)


SCHEMA_VERSION = "r073j-kinetic-overlap-midpoint-bernstein-v2"
ANALYSIS_SOURCE_PATHS = (Path(__file__).resolve(),)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def compact_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_ledger(paths: Sequence[Path]) -> list[dict[str, object]]:
    return [
        {
            "path": str(path.relative_to(ROOT)),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        for path in paths
    ]


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(canonical_json(value))
    os.replace(temporary, path)


def append_ndjson(path: Path, value: object) -> None:
    with path.open("a") as handle:
        handle.write(compact_json(value) + "\n")


def emit(progress: Path, event: str, **fields: object) -> None:
    append_ndjson(progress, {"time": utc_now(), "event": event, **fields})


def verify_frozen_grid(
    config: dict[str, Any], checkpoint: dict[str, Any]
) -> None:
    if checkpoint.get("status") not in ("grid-complete", "passed"):
        raise RuntimeError("the overlap ODE grid is not complete")
    if checkpoint.get("configuration") != config:
        raise RuntimeError("overlap checkpoint configuration mismatch")
    recorded = checkpoint.get("sourceLedger")
    if not isinstance(recorded, list):
        raise RuntimeError("overlap checkpoint has no source ledger")
    current: list[dict[str, object]] = []
    for entry in recorded:
        path = ROOT / str(entry["path"])
        if not path.is_file():
            raise RuntimeError(f"missing frozen overlap source: {entry['path']}")
        current.append({
            "path": entry["path"],
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    if current != recorded:
        raise RuntimeError("a frozen overlap source no longer matches its ledger")
    if ledger_digest(current) != checkpoint.get("sourceDigest"):
        raise RuntimeError("frozen overlap source digest mismatch")


def midpoint_coefficients(
    coefficients: Sequence[Sequence[acb]],
) -> tuple[list[list[acb]], arb]:
    midpoint: list[list[acb]] = []
    residual_upper = arb(0)
    for row in coefficients:
        midpoint_row: list[acb] = []
        for coefficient in row:
            center = acb(coefficient.real.mid(), coefficient.imag.mid())
            midpoint_row.append(center)
            residual_upper += (coefficient - center).abs_upper()
        midpoint.append(midpoint_row)
    return midpoint, residual_upper


def analyze(
    config: dict[str, Any],
    checkpoint: dict[str, Any],
    progress: Path,
) -> dict[str, Any]:
    verify_frozen_grid(config, checkpoint)
    ctx.dps = config["dps"]
    rows, columns = checkpoint["shape"]
    if rows != config["degreeD"] + 1 or columns != config["degreeLambda"] + 1:
        raise RuntimeError("overlap grid shape mismatch")
    grids = {
        name: [[acb(0) for _ in range(columns)] for _ in range(rows)]
        for name in OUTPUT_NAMES
    }
    seen: set[tuple[int, int]] = set()
    minimum_denominator: arb | None = None
    minimum_slack: arb | None = None
    maximum_attempt = 0
    for item in checkpoint["values"]:
        index = (item["dIndex"], item["lambdaIndex"])
        if index in seen:
            raise RuntimeError("duplicate overlap grid point")
        if not 0 <= index[0] < rows or not 0 <= index[1] < columns:
            raise RuntimeError("overlap grid index out of range")
        seen.add(index)
        for name in OUTPUT_NAMES:
            grids[name][index[0]][index[1]] = acb_from_record(
                item["values"][name]
            )
        denominator = arb(item["audit"]["minimumDenominatorLower"])
        slack = arb(item["audit"]["minimumComponentSlack"])
        minimum_denominator = (
            denominator
            if minimum_denominator is None or denominator < minimum_denominator
            else minimum_denominator
        )
        minimum_slack = (
            slack if minimum_slack is None or slack < minimum_slack else minimum_slack
        )
        maximum_attempt = max(
            maximum_attempt, item["audit"]["maximumPicardAttempt"]
        )
    if len(seen) != rows * columns:
        raise RuntimeError("incomplete overlap grid")

    rho_d = arb(config["rhoD"])
    rho_lambda = arb(config["rhoLambda"])
    lebesgue_limit = arb(config["lebesgueLimit"])
    if chebyshev_lebesgue_bound(config["degreeD"]) >= lebesgue_limit:
        raise RuntimeError("degree-d overlap Lebesgue limit failed")
    if chebyshev_lebesgue_bound(config["degreeLambda"]) >= lebesgue_limit:
        raise RuntimeError("degree-lambda overlap Lebesgue limit failed")

    d_majorant = overlap_majorant(
        arb(167) / 1000, complex_d=True, rho_d=rho_d
    )
    lambda_semiaxis = (rho_lambda + 1 / rho_lambda) / 2
    lambda_minimum = (
        arb_rational(config["lambdaCenter"])
        - arb_rational(config["lambdaRadius"]) * lambda_semiaxis
    )
    lambda_majorant = overlap_majorant(
        lambda_minimum, complex_d=False, rho_d=rho_d
    )

    errors: dict[str, arb] = {}
    coefficient_residuals: dict[str, arb] = {}
    cells_by_name: dict[str, list[tuple[int, int, list[list[acb]]]]] = {}
    for name in OUTPUT_NAMES:
        coefficients = tensor_chebyshev_coefficients(grids[name])
        midpoint, residual = midpoint_coefficients(coefficients)
        coefficient_residuals[name] = residual
        d_error = interpolation_error(
            d_majorant[name], config["degreeD"], rho_d
        )
        lambda_error = interpolation_error(
            lambda_majorant[name], config["degreeLambda"], rho_lambda
        )
        errors[name] = lambda_error + lebesgue_limit * d_error
        midpoint_bernstein = tensor_chebyshev_to_bernstein(midpoint)
        cells_by_name[name] = subdivide_tensor_bernstein(
            midpoint_bernstein,
            config["subdivision"]["dDepth"],
            config["subdivision"]["lambdaDepth"],
        )

    cell_count = len(cells_by_name["anchor"])
    if any(len(cells_by_name[name]) != cell_count for name in OUTPUT_NAMES):
        raise RuntimeError("overlap subdivision mismatch")
    result_cells: list[dict[str, Any]] = []
    minimum_anchor: arb | None = None
    minimum_overlap: arb | None = None
    minimum_right_energy: arb | None = None
    minimum_left_energy: arb | None = None
    for index in range(cell_count):
        indices = {name: cells_by_name[name][index][:2] for name in OUTPUT_NAMES}
        if len(set(indices.values())) != 1:
            raise RuntimeError("overlap cell index mismatch")
        boxes = {
            name: inflate_by_modulus_error(
                tensor_bernstein_hull(cells_by_name[name][index][2]),
                errors[name] + coefficient_residuals[name],
            )
            for name in OUTPUT_NAMES
        }
        anchor_lower = boxes["anchor"].abs_lower()
        numerator_lower = boxes["numerator"].abs_lower()
        right_lower = boxes["rightEnergy"].real.lower()
        left_lower = boxes["leftEnergy"].real.lower()
        right_upper = boxes["rightEnergy"].real.upper()
        left_upper = boxes["leftEnergy"].real.upper()
        if min(anchor_lower, numerator_lower, right_lower, left_lower) <= 0:
            raise RuntimeError(f"overlap cell has a nonpositive factor: {index}")
        overlap_lower = numerator_lower / (right_upper * left_upper).sqrt()
        if overlap_lower <= arb(1) / 2:
            raise RuntimeError(
                f"overlap cell misses one-half target: {index} {overlap_lower}"
            )
        minimum_anchor = (
            anchor_lower
            if minimum_anchor is None or anchor_lower < minimum_anchor
            else minimum_anchor
        )
        minimum_overlap = (
            overlap_lower
            if minimum_overlap is None or overlap_lower < minimum_overlap
            else minimum_overlap
        )
        minimum_right_energy = (
            right_lower
            if minimum_right_energy is None or right_lower < minimum_right_energy
            else minimum_right_energy
        )
        minimum_left_energy = (
            left_lower
            if minimum_left_energy is None or left_lower < minimum_left_energy
            else minimum_left_energy
        )
        result_cells.append({
            "dIndex": indices["anchor"][0],
            "lambdaIndex": indices["anchor"][1],
            "dDepth": config["subdivision"]["dDepth"],
            "lambdaDepth": config["subdivision"]["lambdaDepth"],
            "anchor": acb_record(boxes["anchor"]),
            "numerator": acb_record(boxes["numerator"]),
            "rightEnergy": acb_record(boxes["rightEnergy"]),
            "leftEnergy": acb_record(boxes["leftEnergy"]),
            "anchorAbsoluteLower": arb_text(anchor_lower),
            "overlapLower": arb_text(overlap_lower),
        })

    prerequisite = contour_prerequisite()
    analysis_ledger = source_ledger(ANALYSIS_SOURCE_PATHS)
    combined_ledger = list(checkpoint["sourceLedger"]) + analysis_ledger
    emit(
        progress,
        "midpoint-bernstein-analysis-complete",
        cellCount=cell_count,
        minimumAnchorAbsoluteLower=arb_text(minimum_anchor or arb(0)),
        minimumKineticOverlapLower=arb_text(minimum_overlap or arb(0)),
    )
    return {
        "schemaVersion": SCHEMA_VERSION,
        "status": "passed",
        "completedAt": utc_now(),
        "sourceLedger": combined_ledger,
        "sourceDigest": ledger_digest(combined_ledger),
        "gridEvidence": {
            "checkpoint": str(
                (HERE / "overlap_grid_checkpoint.json").relative_to(ROOT)
            ),
            "sourceLedger": checkpoint["sourceLedger"],
            "sourceDigest": checkpoint["sourceDigest"],
            "status": checkpoint["status"],
        },
        "analysisEvidence": {
            "sourceLedger": analysis_ledger,
            "sourceDigest": ledger_digest(analysis_ledger),
        },
        "configuration": config,
        "prerequisiteEvidence": prerequisite,
        "arithmetic": {
            "engine": "python-flint Arb/Acb ball arithmetic",
            "python": platform.python_version(),
            "pythonImplementation": platform.python_implementation(),
            "precisionDecimalDigits": config["dps"],
            "pointCount": len(checkpoint["values"]),
            "minimumRayleighDenominatorLower": arb_text(
                minimum_denominator or arb(0)
            ),
            "minimumPicardComponentSlack": arb_text(minimum_slack or arb(0)),
            "maximumPicardInflationAttempt": maximum_attempt,
        },
        "analyticMajorants": {
            "complexD": {key: arb_text(value) for key, value in d_majorant.items()},
            "complexLambda": {
                key: arb_text(value) for key, value in lambda_majorant.items()
            },
            "totalInterpolationErrors": {
                key: arb_text(value) for key, value in errors.items()
            },
            "coefficientResidualModulusUpper": {
                key: arb_text(value) for key, value in coefficient_residuals.items()
            },
            "remainderFormula": "epsilon_lambda + Lambda_lambda*epsilon_d",
            "rangeMethod": (
                "tensor Bernstein hull of zero-radius midpoint coefficients, "
                "inflated by the direct Chebyshev-basis coefficient residual "
                "sum and analytic interpolation error"
            ),
        },
        "decisions": {
            "auxiliaryRectanglePhaseAnchorNonzero": True,
            "minimumAnchorAbsoluteLower": arb_text(minimum_anchor or arb(0)),
            "auxiliaryRectangleKineticQuotientAtLeastOneHalf": True,
            "minimumKineticOverlapLower": arb_text(minimum_overlap or arb(0)),
            "minimumRightEnergyLower": arb_text(minimum_right_energy or arb(0)),
            "minimumLeftEnergyLower": arb_text(minimum_left_energy or arb(0)),
            "conditionalBranchImplications": {
                "conditionalOn": (
                    "J8: the unique algebraically simple real root lies in "
                    "the certified local disk for every d in [0,1/450]"
                ),
                "phaseAnchorNonzeroAlongBranch": True,
                "kineticOverlapAtLeastOneHalfAlongBranch": True,
            },
        },
        "cells": result_cells,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--config", type=Path, default=HERE / "overlap_config.json"
    )
    parser.add_argument(
        "--checkpoint", type=Path, default=HERE / "overlap_grid_checkpoint.json"
    )
    parser.add_argument(
        "--output", type=Path, default=HERE / "overlap_certificate.json"
    )
    parser.add_argument(
        "--progress", type=Path, default=HERE / "overlap_analysis_progress.ndjson"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = json.loads(args.config.read_text())
    checkpoint = json.loads(args.checkpoint.read_text())
    emit(
        args.progress,
        "midpoint-bernstein-analysis-started",
        checkpoint=str(args.checkpoint.relative_to(ROOT)),
    )
    result = analyze(config, checkpoint, args.progress)
    atomic_json(args.output, result)
    emit(
        args.progress,
        "overlap-certificate-passed",
        output=str(args.output.relative_to(ROOT)),
        decisions=result["decisions"],
    )


if __name__ == "__main__":
    main()
