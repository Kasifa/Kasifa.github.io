#!/usr/bin/env python3
"""Analyze the frozen R0.73J contour grids by interval Clenshaw evaluation.

The validated ODE grid is immutable evidence with its own source ledger.  This
analysis stage reconstructs the tensor Chebyshev interpolants and evaluates
them directly on a dyadic cover of each real parameter panel.  Direct interval
Clenshaw evaluation avoids the coefficient wrapping introduced by converting
an entire complex ball polynomial to power and then Bernstein form.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
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

from experiments.r073j.certify_contours import (  # noqa: E402
    acb_record,
    arb_text,
    axis_half_plane_witness,
    exact_polygon_winding,
    hull_with_vertices,
    interval_decision_record,
    matrix_from_panel,
    midpoint_record,
    panel_definitions,
    panel_minimum_real_on_parameter_ellipse,
    panel_minimum_real_on_real_path,
    source_digest,
)
from research.r073j_chebyshev import (  # noqa: E402
    chebyshev_evaluate,
    chebyshev_lebesgue_bound,
    complex_d_evans_majorant,
    inflate_by_modulus_error,
    interpolation_error,
    real_d_evans_majorant,
    restrict_first_chebyshev_variable,
    tensor_chebyshev_coefficients,
)


SCHEMA_VERSION = "r073j-parameter-uniform-contours-clenshaw-v2"
ANALYSIS_SOURCE_PATHS = (Path(__file__).resolve(),)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def compact_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ledger(paths: Sequence[Path]) -> list[dict[str, object]]:
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
    if checkpoint.get("status") not in ("grids-complete", "passed"):
        raise RuntimeError("the ODE grid is not complete")
    if checkpoint.get("configuration") != config:
        raise RuntimeError("checkpoint configuration differs from config.json")
    recorded = checkpoint.get("sourceLedger")
    if not isinstance(recorded, list):
        raise RuntimeError("checkpoint has no source ledger")
    current: list[dict[str, object]] = []
    for entry in recorded:
        path = ROOT / str(entry["path"])
        if not path.is_file():
            raise RuntimeError(f"missing frozen grid source: {entry['path']}")
        current.append({
            "path": entry["path"],
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    if current != recorded:
        raise RuntimeError("a frozen grid source no longer matches its ledger")
    if source_digest(current) != checkpoint.get("sourceDigest"):
        raise RuntimeError("frozen grid source digest mismatch")


def dyadic_interval(index: int, depth: int) -> arb:
    if depth < 0 or not 0 <= index < 2**depth:
        raise ValueError("invalid dyadic cell")
    denominator = 2**depth
    lower = Fraction(-1) + Fraction(2 * index, denominator)
    upper = Fraction(-1) + Fraction(2 * (index + 1), denominator)
    lo = arb(lower.numerator) / lower.denominator
    hi = arb(upper.numerator) / upper.denominator
    return lo.union(hi)


def dyadic_point(index: int, depth: int) -> arb:
    if depth < 0 or not 0 <= index <= 2**depth:
        raise ValueError("invalid dyadic endpoint")
    value = Fraction(-1) + Fraction(2 * index, 2**depth)
    return arb(value.numerator) / value.denominator


def tensor_interval_clenshaw(
    coefficients: Sequence[Sequence[acb]], d_box: arb, s_box: arb
) -> acb:
    """Enclose a tensor Chebyshev polynomial on a real parameter box."""
    if not coefficients or not coefficients[0]:
        raise ValueError("empty tensor coefficient array")
    if any(len(row) != len(coefficients[0]) for row in coefficients):
        raise ValueError("ragged tensor coefficient array")
    s_evaluated = [chebyshev_evaluate(row, s_box) for row in coefficients]
    return chebyshev_evaluate(s_evaluated, d_box)


def certify_base_polygon(
    family: str, base_cells: list[dict[str, Any]]
) -> dict[str, Any]:
    if not base_cells:
        raise RuntimeError(f"empty {family} base contour")
    vertices = [base_cells[0]["startCandidate"]]
    vertices.extend(cell["endCandidate"] for cell in base_cells[:-1])
    homotopy_cells: list[dict[str, Any]] = []
    homotopy_minimum: arb | None = None
    for index, cell in enumerate(base_cells):
        endpoints = (vertices[index], vertices[(index + 1) % len(vertices)])
        homotopy_box = hull_with_vertices(cell["image"], endpoints)
        witness = axis_half_plane_witness(homotopy_box)
        if witness is None:
            raise RuntimeError(
                f"{family} base homotopy cell has no axis half-plane witness: "
                f"{index}"
            )
        lower = homotopy_box.abs_lower()
        homotopy_minimum = (
            lower
            if homotopy_minimum is None or lower < homotopy_minimum
            else homotopy_minimum
        )
        homotopy_cells.append({
            "index": index,
            "panelId": cell["panelId"],
            "cellIndex": cell["cellIndex"],
            "imageWithChord": acb_record(homotopy_box),
            "absoluteLower": arb_text(lower),
            "halfPlaneWitness": witness,
        })
    winding = exact_polygon_winding(vertices)
    if winding["winding"] != 1:
        raise RuntimeError(f"unexpected exact {family} base winding: {winding}")
    return {
        **winding,
        "homotopyMinimumAbsoluteLower": arb_text(homotopy_minimum or arb(0)),
        "vertexCount": len(vertices),
        "vertices": vertices,
        "cells": homotopy_cells,
    }


def analyze(
    config: dict[str, Any],
    panels: list[dict[str, Any]],
    checkpoint: dict[str, Any],
    progress: Path,
) -> dict[str, Any]:
    verify_frozen_grid(config, checkpoint)
    ctx.dps = config["dps"]
    rho_d = arb(config["rhoD"])
    rho_s = arb(config["rhoS"])
    lebesgue_limit = arb(config["lebesgueLimit"])
    degree_d_bound = chebyshev_lebesgue_bound(config["degreeD"])
    if degree_d_bound >= lebesgue_limit:
        raise RuntimeError("degree-d Lebesgue bound exceeds its configured limit")

    results: list[dict[str, Any]] = []
    base_cells: dict[str, list[dict[str, Any]]] = {"global": [], "local": []}
    uniform_minimum: arb | None = None
    global_minimum: arb | None = None
    local_minimum: arb | None = None

    for panel_index, panel in enumerate(panels):
        record = checkpoint["panels"].get(panel["id"])
        if record is None:
            raise RuntimeError(f"missing panel {panel['id']}")
        values = matrix_from_panel(record)
        coefficients = tensor_chebyshev_coefficients(values)
        degree_s = panel["degreeS"]
        lebesgue_s = chebyshev_lebesgue_bound(degree_s)
        if lebesgue_s >= lebesgue_limit:
            raise RuntimeError(f"Lebesgue bound failed for {panel['id']}")

        real_path_minimum = panel_minimum_real_on_real_path(panel)
        ellipse_minimum = panel_minimum_real_on_parameter_ellipse(panel, rho_s)
        d_majorant = complex_d_evans_majorant(real_path_minimum, rho_d)
        s_majorant = real_d_evans_majorant(ellipse_minimum)
        d_error = interpolation_error(
            d_majorant["evansUpper"], config["degreeD"], rho_d
        )
        s_error = interpolation_error(
            s_majorant["evansUpper"], degree_s, rho_s
        )
        tensor_error = s_error + lebesgue_limit * d_error
        subdivision = config[panel["family"]]["subdivision"]
        d_depth = subdivision["dDepth"]
        s_depth = subdivision["sDepth"]

        panel_cells: list[dict[str, Any]] = []
        panel_minimum: arb | None = None
        for d_index in range(2**d_depth):
            d_box = dyadic_interval(d_index, d_depth)
            for s_index in range(2**s_depth):
                s_box = dyadic_interval(s_index, s_depth)
                image = inflate_by_modulus_error(
                    tensor_interval_clenshaw(coefficients, d_box, s_box),
                    tensor_error,
                )
                lower = image.abs_lower()
                if lower <= 0:
                    raise RuntimeError(
                        "interval-Clenshaw contour enclosure contains zero: "
                        f"{panel['id']} d={d_index} s={s_index} box={image}"
                    )
                panel_minimum = (
                    lower if panel_minimum is None or lower < panel_minimum
                    else panel_minimum
                )
                panel_cells.append({
                    "dIndex": d_index,
                    "sIndex": s_index,
                    "dDepth": d_depth,
                    "sDepth": s_depth,
                    **interval_decision_record(image),
                })

        if panel_minimum is None:
            raise RuntimeError("empty dyadic panel cover")
        uniform_minimum = (
            panel_minimum
            if uniform_minimum is None or panel_minimum < uniform_minimum
            else uniform_minimum
        )

        family = panel["family"]
        if family == "global":
            global_minimum = (
                panel_minimum
                if global_minimum is None or panel_minimum < global_minimum
                else global_minimum
            )
        else:
            local_minimum = (
                panel_minimum
                if local_minimum is None or panel_minimum < local_minimum
                else local_minimum
            )

        restricted = restrict_first_chebyshev_variable(coefficients, arb(-1))
        for cell_index in range(2**s_depth):
            s_box = dyadic_interval(cell_index, s_depth)
            image = inflate_by_modulus_error(
                chebyshev_evaluate(restricted, s_box), tensor_error
            )
            if image.abs_lower() <= 0:
                raise RuntimeError(
                    f"{family} base contour enclosure contains zero: "
                    f"{panel['id']} s={cell_index} box={image}"
                )
            start = chebyshev_evaluate(
                restricted, dyadic_point(cell_index, s_depth)
            )
            end = chebyshev_evaluate(
                restricted, dyadic_point(cell_index + 1, s_depth)
            )
            base_cells[family].append({
                "panelId": panel["id"],
                "panelIndex": panel_index,
                "cellIndex": cell_index,
                "image": image,
                "startCandidate": midpoint_record(start),
                "endCandidate": midpoint_record(end),
            })

        results.append({
            "id": panel["id"],
            "family": panel["family"],
            "definition": panel,
            "realPathMinimumLambdaReal": arb_text(real_path_minimum),
            "ellipseMinimumLambdaReal": arb_text(ellipse_minimum),
            "dMajorant": {key: arb_text(value) for key, value in d_majorant.items()},
            "sMajorant": {key: arb_text(value) for key, value in s_majorant.items()},
            "dInterpolationError": arb_text(d_error),
            "sInterpolationError": arb_text(s_error),
            "tensorInterpolationError": arb_text(tensor_error),
            "lebesgueBound": arb_text(lebesgue_s),
            "minimumAbsoluteLower": arb_text(panel_minimum),
            "cells": panel_cells,
        })
        emit(
            progress,
            "clenshaw-panel-analyzed",
            panelId=panel["id"],
            minimumAbsoluteLower=arb_text(panel_minimum),
            cellCount=len(panel_cells),
        )

    if (
        not base_cells["global"]
        or not base_cells["local"]
        or global_minimum is None
        or local_minimum is None
    ):
        raise RuntimeError("missing global or local analysis cells")
    global_polygon = certify_base_polygon("global", base_cells["global"])
    local_polygon = certify_base_polygon("local", base_cells["local"])

    audit_minimum_denominator: arb | None = None
    audit_minimum_slack: arb | None = None
    audit_maximum_attempt = 0
    point_count = 0
    for record in checkpoint["panels"].values():
        for value in record["values"]:
            point_count += 1
            denominator = arb(value["audit"]["minimumDenominatorLower"])
            slack = arb(value["audit"]["minimumComponentSlack"])
            audit_minimum_denominator = (
                denominator
                if audit_minimum_denominator is None
                or denominator < audit_minimum_denominator
                else audit_minimum_denominator
            )
            audit_minimum_slack = (
                slack
                if audit_minimum_slack is None or slack < audit_minimum_slack
                else audit_minimum_slack
            )
            audit_maximum_attempt = max(
                audit_maximum_attempt, value["audit"]["maximumPicardAttempt"]
            )

    analysis_ledger = ledger(ANALYSIS_SOURCE_PATHS)
    combined_ledger = list(checkpoint["sourceLedger"]) + analysis_ledger
    return {
        "schemaVersion": SCHEMA_VERSION,
        "status": "passed",
        "completedAt": utc_now(),
        "sourceLedger": combined_ledger,
        "sourceDigest": source_digest(combined_ledger),
        "gridEvidence": {
            "checkpoint": str(
                (HERE / "contour_grid_checkpoint.json").relative_to(ROOT)
            ),
            "sourceLedger": checkpoint["sourceLedger"],
            "sourceDigest": checkpoint["sourceDigest"],
            "status": checkpoint["status"],
        },
        "analysisEvidence": {
            "sourceLedger": analysis_ledger,
            "sourceDigest": source_digest(analysis_ledger),
        },
        "configuration": config,
        "arithmetic": {
            "engine": "python-flint Arb/Acb ball arithmetic",
            "python": platform.python_version(),
            "pythonImplementation": platform.python_implementation(),
            "precisionDecimalDigits": config["dps"],
            "odePointCount": point_count,
            "minimumRayleighDenominatorLower": arb_text(
                audit_minimum_denominator or arb(0)
            ),
            "minimumPicardComponentSlack": arb_text(
                audit_minimum_slack or arb(0)
            ),
            "maximumPicardInflationAttempt": audit_maximum_attempt,
        },
        "interpolation": {
            "nodes": "roots of T_(degree+1)",
            "remainderFormula": "4*M*rho^(-degree)/(rho-1)",
            "tensorDecomposition": "epsilon_s + Lambda_s*epsilon_d",
            "rangeMethod": (
                "direct outward-rounded interval Clenshaw on a complete "
                "dyadic real-box cover"
            ),
            "lebesgueLimit": config["lebesgueLimit"],
            "degreeDLebesgueBound": arb_text(degree_d_bound),
        },
        "decisions": {
            "globalBoundaryNonzeroForAllD": True,
            "globalMinimumAbsoluteLower": arb_text(global_minimum),
            "localBoundaryNonzeroForAllD": True,
            "localMinimumAbsoluteLower": arb_text(local_minimum),
            "globalBasePositiveOrientationWinding": global_polygon["winding"],
            "globalBaseHomotopyMinimumAbsoluteLower": global_polygon[
                "homotopyMinimumAbsoluteLower"
            ],
            "localBasePositiveOrientationWinding": local_polygon["winding"],
            "localBaseHomotopyMinimumAbsoluteLower": local_polygon[
                "homotopyMinimumAbsoluteLower"
            ],
        },
        "exactPolygons": {
            "global": global_polygon,
            "local": local_polygon,
        },
        "panels": results,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=HERE / "config.json")
    parser.add_argument(
        "--checkpoint", type=Path, default=HERE / "contour_grid_checkpoint.json"
    )
    parser.add_argument(
        "--output", type=Path, default=HERE / "contour_certificate.json"
    )
    parser.add_argument(
        "--progress", type=Path, default=HERE / "analysis_progress.ndjson"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = json.loads(args.config.read_text())
    checkpoint = json.loads(args.checkpoint.read_text())
    ctx.dps = config["dps"]
    panels = panel_definitions(config)
    emit(
        args.progress,
        "clenshaw-analysis-started",
        checkpoint=str(args.checkpoint.relative_to(ROOT)),
        panelCount=len(panels),
    )
    result = analyze(config, panels, checkpoint, args.progress)
    atomic_json(args.output, result)
    emit(
        args.progress,
        "clenshaw-certificate-passed",
        output=str(args.output.relative_to(ROOT)),
        decisions=result["decisions"],
    )


if __name__ == "__main__":
    main()
