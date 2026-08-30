#!/usr/bin/env python3
"""Build the primary R0.73J parameter-uniform Evans contour certificate.

The formal run has two stages:

1. validated Arb monodromy solves on tensor Chebyshev grids;
2. an analysis-only conversion to tensor Bernstein form, complete boundary
   nonvanishing checks, and an exact rational polygon winding computation.

Every completed panel is checkpointed atomically.  A stopped run resumes only
when the source/configuration digest is identical.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
from datetime import datetime, timezone
from decimal import Decimal
from fractions import Fraction
import hashlib
import json
import math
import multiprocessing as mp
import os
from pathlib import Path
import platform
import resource
import shutil
import sys
import threading
import time
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from flint import acb, arb, ctx  # noqa: E402

from research.r073j_chebyshev import (  # noqa: E402
    chebyshev_lebesgue_bound,
    chebyshev_to_bernstein,
    complex_d_evans_majorant,
    complex_hull,
    inflate_by_modulus_error,
    interpolation_error,
    real_d_evans_majorant,
    restrict_first_chebyshev_variable,
    subdivide_bernstein,
    subdivide_tensor_bernstein,
    tensor_bernstein_hull,
    tensor_chebyshev_coefficients,
    tensor_chebyshev_to_bernstein,
)
from research.r073j_interval_core import evans  # noqa: E402


SCHEMA_VERSION = "r073j-parameter-uniform-contours-v1"
SOURCE_PATHS = (
    ROOT / "research/r073j_interval_core.py",
    ROOT / "research/r073j_chebyshev.py",
    HERE / "certify_contours.py",
    HERE / "config.json",
    HERE / "requirements.txt",
)
WORKER_CONFIG: dict[str, Any] = {}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def compact_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_ledger() -> list[dict[str, object]]:
    return [
        {
            "path": str(path.relative_to(ROOT)),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        for path in SOURCE_PATHS
    ]


def source_digest(ledger: Sequence[dict[str, object]]) -> str:
    return hashlib.sha256(compact_json(list(ledger)).encode()).hexdigest()


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(canonical_json(value))
    os.replace(temporary, path)


def append_ndjson(path: Path, value: object) -> None:
    with path.open("a") as handle:
        handle.write(compact_json(value) + "\n")


def parse_fraction(text: str) -> Fraction:
    return Fraction(text)


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def arb_fraction(text: str) -> arb:
    value = parse_fraction(text)
    return arb(value.numerator) / value.denominator


def arb_text(value: arb, digits: int = 80) -> str:
    return value.str(digits, more=True)


def acb_record(value: acb) -> dict[str, str]:
    return {
        "real": arb_text(value.real),
        "imag": arb_text(value.imag),
    }


def acb_from_record(value: dict[str, str]) -> acb:
    return acb(arb(value["real"]), arb(value["imag"]))


def midpoint_record(value: acb, digits: int = 50) -> dict[str, str]:
    return {
        "real": value.real.mid().str(digits, radius=False, more=True),
        "imag": value.imag.mid().str(digits, radius=False, more=True),
    }


def panel_definitions(config: dict[str, Any]) -> list[dict[str, Any]]:
    boundary = config["global"]["boundary"]
    left = Fraction(boundary["left"])
    radius = Fraction(boundary["outer"])
    vertical_count = config["global"]["verticalPanelsPerEdge"]
    horizontal_count = config["global"]["horizontalPanelsPerEdge"]
    horizontal_length = (radius - left) / horizontal_count
    vertical_length = 2 * radius / vertical_count
    panels: list[dict[str, Any]] = []

    def line_panel(
        panel_id: str,
        edge: str,
        center: complex | tuple[Fraction, Fraction],
        half: complex | tuple[Fraction, Fraction],
    ) -> dict[str, Any]:
        center_pair = center if isinstance(center, tuple) else (
            Fraction(center.real), Fraction(center.imag)
        )
        half_pair = half if isinstance(half, tuple) else (
            Fraction(half.real), Fraction(half.imag)
        )
        return {
            "id": panel_id,
            "family": "global",
            "kind": "line",
            "edge": edge,
            "centerReal": fraction_text(center_pair[0]),
            "centerImag": fraction_text(center_pair[1]),
            "halfReal": fraction_text(half_pair[0]),
            "halfImag": fraction_text(half_pair[1]),
            "degreeS": config["global"]["degreeS"],
            "steps": config["global"]["steps"],
        }

    for index in range(horizontal_count):
        center_x = left + (Fraction(2 * index + 1, 2) * horizontal_length)
        panels.append(line_panel(
            f"G-bottom-{index:02d}", "bottom",
            (center_x, -radius), (horizontal_length / 2, Fraction(0)),
        ))
    for index in range(vertical_count):
        center_y = -radius + Fraction(2 * index + 1, 2) * vertical_length
        panels.append(line_panel(
            f"G-right-{index:02d}", "right",
            (radius, center_y), (Fraction(0), vertical_length / 2),
        ))
    for index in range(horizontal_count):
        center_x = radius - Fraction(2 * index + 1, 2) * horizontal_length
        panels.append(line_panel(
            f"G-top-{index:02d}", "top",
            (center_x, radius), (-horizontal_length / 2, Fraction(0)),
        ))
    for index in range(vertical_count):
        center_y = radius - Fraction(2 * index + 1, 2) * vertical_length
        panels.append(line_panel(
            f"G-left-{index:02d}", "left",
            (left, center_y), (Fraction(0), -vertical_length / 2),
        ))

    local_count = config["local"]["panels"]
    for index in range(local_count):
        panels.append({
            "id": f"L-circle-{index:02d}",
            "family": "local",
            "kind": "circle",
            "thetaCenterPi": fraction_text(Fraction(2 * index + 1, local_count)),
            "thetaHalfPi": fraction_text(Fraction(1, local_count)),
            "degreeS": config["local"]["degreeS"],
            "steps": config["local"]["steps"],
        })
    return panels


def worker_initialize(config: dict[str, Any]) -> None:
    global WORKER_CONFIG
    WORKER_CONFIG = config
    ctx.dps = config["dps"]


def chebyshev_node(index: int, count: int) -> arb:
    return ((2 * index + 1) * arb.pi() / (2 * count)).cos()


def worker_point(task: dict[str, Any]) -> dict[str, Any]:
    config = WORKER_CONFIG
    d_count = config["degreeD"] + 1
    d_coordinate = chebyshev_node(task["dIndex"], d_count)
    d_value = (arb(1) / 450) * (1 + d_coordinate) / 2
    s_count = task["panel"]["degreeS"] + 1
    s_value = chebyshev_node(task["sIndex"], s_count)
    panel = task["panel"]
    if panel["kind"] == "line":
        spectral = acb(
            arb_fraction(panel["centerReal"])
            + arb_fraction(panel["halfReal"]) * s_value,
            arb_fraction(panel["centerImag"])
            + arb_fraction(panel["halfImag"]) * s_value,
        )
    elif panel["kind"] == "circle":
        theta = arb.pi() * (
            arb_fraction(panel["thetaCenterPi"])
            + arb_fraction(panel["thetaHalfPi"]) * s_value
        )
        spectral = acb(
            arb(17) / 100 + arb(3) / 1000 * theta.cos(),
            arb(3) / 1000 * theta.sin(),
        )
    else:
        raise ValueError(f"unknown panel kind {panel['kind']}")
    value, audit = evans(
        d_value,
        spectral,
        panel["steps"],
        config["order"],
    )
    return {
        "panelId": panel["id"],
        "dIndex": task["dIndex"],
        "sIndex": task["sIndex"],
        "evans": acb_record(value),
        "audit": {
            "minimumDenominatorLower": arb_text(
                audit.minimum_denominator_lower or arb(0)
            ),
            "minimumComponentSlack": arb_text(
                audit.minimum_component_slack or arb(0)
            ),
            "maximumPicardAttempt": audit.maximum_picard_attempt,
            "steps": audit.step_count,
        },
    }


class Progress:
    def __init__(self, path: Path) -> None:
        self.path = path

    def emit(self, event: str, **payload: object) -> None:
        record = {"time": utc_now(), "event": event, **payload}
        append_ndjson(self.path, record)
        print(compact_json(record), flush=True)


def resource_monitor(
    stop: threading.Event,
    path: Path,
    interval_seconds: int,
    started: float,
) -> None:
    while not stop.wait(interval_seconds):
        usage = resource.getrusage(resource.RUSAGE_SELF)
        children = resource.getrusage(resource.RUSAGE_CHILDREN)
        append_ndjson(path, {
            "time": utc_now(),
            "elapsedSeconds": time.monotonic() - started,
            "loadAverage": list(os.getloadavg()),
            "selfUserSeconds": usage.ru_utime,
            "selfSystemSeconds": usage.ru_stime,
            "childrenUserSeconds": children.ru_utime,
            "childrenSystemSeconds": children.ru_stime,
            "selfMaxRss": usage.ru_maxrss,
            "childrenMaxRss": children.ru_maxrss,
            "diskFreeBytes": shutil.disk_usage(HERE).free,
        })


def checkpoint_template(
    config: dict[str, Any],
    ledger: list[dict[str, object]],
) -> dict[str, Any]:
    return {
        "schemaVersion": SCHEMA_VERSION,
        "status": "running",
        "createdAt": utc_now(),
        "updatedAt": utc_now(),
        "sourceLedger": ledger,
        "sourceDigest": source_digest(ledger),
        "configuration": config,
        "panels": {},
    }


def load_or_create_checkpoint(
    path: Path,
    config: dict[str, Any],
    ledger: list[dict[str, object]],
) -> dict[str, Any]:
    expected = source_digest(ledger)
    if not path.exists():
        result = checkpoint_template(config, ledger)
        atomic_json(path, result)
        return result
    result = json.loads(path.read_text())
    if result.get("sourceDigest") != expected:
        raise RuntimeError(
            "checkpoint source digest differs; preserve or remove it explicitly"
        )
    if result.get("configuration") != config:
        raise RuntimeError(
            "checkpoint configuration differs; preserve or remove it explicitly"
        )
    return result


def run_grids(
    config: dict[str, Any],
    panels: list[dict[str, Any]],
    checkpoint_path: Path,
    progress: Progress,
) -> dict[str, Any]:
    ledger = source_ledger()
    checkpoint = load_or_create_checkpoint(checkpoint_path, config, ledger)
    pending = [panel for panel in panels if panel["id"] not in checkpoint["panels"]]
    total_points = sum(
        (config["degreeD"] + 1) * (panel["degreeS"] + 1)
        for panel in pending
    )
    progress.emit(
        "grid-start",
        pendingPanels=len(pending),
        pendingPoints=total_points,
        workers=config["workers"],
    )
    context = mp.get_context("spawn")
    with context.Pool(
        processes=config["workers"],
        initializer=worker_initialize,
        initargs=(config,),
    ) as pool:
        completed_points = 0
        for panel_number, panel in enumerate(pending, start=1):
            tasks = [
                {"panel": panel, "dIndex": d_index, "sIndex": s_index}
                for d_index in range(config["degreeD"] + 1)
                for s_index in range(panel["degreeS"] + 1)
            ]
            started = time.monotonic()
            values = list(pool.imap_unordered(worker_point, tasks, chunksize=1))
            values.sort(key=lambda item: (item["dIndex"], item["sIndex"]))
            completed_points += len(values)
            checkpoint["panels"][panel["id"]] = {
                "definition": panel,
                "shape": [config["degreeD"] + 1, panel["degreeS"] + 1],
                "values": values,
            }
            checkpoint["updatedAt"] = utc_now()
            atomic_json(checkpoint_path, checkpoint)
            progress.emit(
                "panel-complete",
                panelId=panel["id"],
                panelIndex=panel_number,
                pendingPanelCount=len(pending),
                points=len(values),
                completedPendingPoints=completed_points,
                pendingPoints=total_points,
                elapsedSeconds=time.monotonic() - started,
            )
    checkpoint["status"] = "grids-complete"
    checkpoint["updatedAt"] = utc_now()
    atomic_json(checkpoint_path, checkpoint)
    progress.emit("grid-complete", panelCount=len(panels))
    return checkpoint


def panel_minimum_real_on_real_path(panel: dict[str, Any]) -> arb:
    if panel["kind"] == "line":
        return (
            arb_fraction(panel["centerReal"])
            - abs(arb_fraction(panel["halfReal"]))
        )
    if panel["kind"] == "circle":
        return arb(167) / 1000
    raise ValueError("unknown panel kind")


def panel_minimum_real_on_parameter_ellipse(
    panel: dict[str, Any],
    rho: arb,
) -> arb:
    real_semiaxis = (rho + 1 / rho) / 2
    imag_semiaxis = (rho - 1 / rho) / 2
    if panel["kind"] == "line":
        return (
            arb_fraction(panel["centerReal"])
            - abs(arb_fraction(panel["halfReal"])) * real_semiaxis
            - abs(arb_fraction(panel["halfImag"])) * imag_semiaxis
        )
    if panel["kind"] == "circle":
        theta_half = arb.pi() * abs(arb_fraction(panel["thetaHalfPi"]))
        return (
            arb(17) / 100
            - arb(3) / 1000 * (theta_half * imag_semiaxis).exp()
        )
    raise ValueError("unknown panel kind")


def matrix_from_panel(
    panel_record: dict[str, Any],
) -> list[list[acb]]:
    rows, columns = panel_record["shape"]
    result = [[acb(0) for _ in range(columns)] for _ in range(rows)]
    seen: set[tuple[int, int]] = set()
    for value in panel_record["values"]:
        index = (value["dIndex"], value["sIndex"])
        if index in seen:
            raise RuntimeError(f"duplicate grid index {index}")
        seen.add(index)
        result[index[0]][index[1]] = acb_from_record(value["evans"])
    if len(seen) != rows * columns:
        raise RuntimeError("incomplete panel grid")
    return result


def interval_decision_record(value: acb) -> dict[str, Any]:
    return {
        "box": acb_record(value),
        "absoluteLower": arb_text(value.abs_lower()),
    }


def axis_half_plane_witness(value: acb) -> dict[str, str] | None:
    if value.real.lower() > 0:
        return {"axis": "real", "sign": "+", "margin": arb_text(value.real.lower())}
    if value.real.upper() < 0:
        return {"axis": "real", "sign": "-", "margin": arb_text(-value.real.upper())}
    if value.imag.lower() > 0:
        return {"axis": "imag", "sign": "+", "margin": arb_text(value.imag.lower())}
    if value.imag.upper() < 0:
        return {"axis": "imag", "sign": "-", "margin": arb_text(-value.imag.upper())}
    return None


def hull_with_vertices(
    value: acb,
    vertices: Sequence[dict[str, str]],
) -> acb:
    real = value.real
    imag = value.imag
    for vertex in vertices:
        real = real.union(arb(vertex["real"]))
        imag = imag.union(arb(vertex["imag"]))
    return acb(real, imag)


def exact_polygon_winding(vertices: Sequence[dict[str, str]]) -> dict[str, int]:
    rational = [
        (Fraction(Decimal(vertex["real"])), Fraction(Decimal(vertex["imag"])))
        for vertex in vertices
    ]
    if any(x == 0 and y == 0 for x, y in rational):
        raise RuntimeError("polygon has the origin as a vertex")
    rotation = None
    transformed: list[tuple[Fraction, Fraction]] = []
    for candidate in range(0, 257):
        trial = [(x - candidate * y, candidate * x + y) for x, y in rational]
        if all(y != 0 for _, y in trial):
            rotation = candidate
            transformed = trial
            break
    if rotation is None:
        raise RuntimeError("failed to choose an exact rational ray rotation")
    winding = 0
    for index, first in enumerate(transformed):
        second = transformed[(index + 1) % len(transformed)]
        x1, y1 = first
        x2, y2 = second
        determinant = x1 * y2 - x2 * y1
        if y1 <= 0 < y2 and determinant > 0:
            winding += 1
        elif y2 <= 0 < y1 and determinant < 0:
            winding -= 1
    return {"rotationImaginaryMultiplier": rotation, "winding": winding}


def analyze_checkpoint(
    config: dict[str, Any],
    panels: list[dict[str, Any]],
    checkpoint: dict[str, Any],
    progress: Progress,
) -> dict[str, Any]:
    if checkpoint.get("status") not in ("grids-complete", "passed"):
        raise RuntimeError("all grid panels must be complete before analysis")
    ctx.dps = config["dps"]
    rho_d = arb(config["rhoD"])
    rho_s = arb(config["rhoS"])
    lebesgue_limit = arb(config["lebesgueLimit"])
    if chebyshev_lebesgue_bound(config["degreeD"]) >= lebesgue_limit:
        raise RuntimeError("degree-d Lebesgue bound exceeds the configured limit")

    panel_results: list[dict[str, Any]] = []
    base_cells: list[dict[str, Any]] = []
    uniform_minimum: arb | None = None
    local_minimum: arb | None = None
    global_minimum: arb | None = None
    for panel_index, panel in enumerate(panels):
        record = checkpoint["panels"].get(panel["id"])
        if record is None:
            raise RuntimeError(f"missing panel {panel['id']}")
        degree_s = panel["degreeS"]
        lebesgue_s = chebyshev_lebesgue_bound(degree_s)
        if lebesgue_s >= lebesgue_limit:
            raise RuntimeError(f"Lebesgue bound failed for {panel['id']}")
        values = matrix_from_panel(record)
        coefficients = tensor_chebyshev_coefficients(values)
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
        bernstein = tensor_chebyshev_to_bernstein(coefficients)
        subdivision = config[panel["family"]]["subdivision"]
        cells = subdivide_tensor_bernstein(
            bernstein,
            subdivision["dDepth"],
            subdivision["sDepth"],
        )
        cell_records = []
        panel_minimum: arb | None = None
        for d_index, s_index, cell in cells:
            image = inflate_by_modulus_error(
                tensor_bernstein_hull(cell), tensor_error
            )
            lower = image.abs_lower()
            if lower <= 0:
                raise RuntimeError(
                    f"uniform contour enclosure contains zero: {panel['id']} "
                    f"d={d_index} s={s_index} box={image}"
                )
            if panel_minimum is None or lower < panel_minimum:
                panel_minimum = lower
            cell_records.append({
                "dIndex": d_index,
                "sIndex": s_index,
                **interval_decision_record(image),
            })

        if panel_minimum is None:
            raise RuntimeError("empty Bernstein subdivision")
        if uniform_minimum is None or panel_minimum < uniform_minimum:
            uniform_minimum = panel_minimum
        if panel["family"] == "global":
            if global_minimum is None or panel_minimum < global_minimum:
                global_minimum = panel_minimum
            restricted = restrict_first_chebyshev_variable(coefficients, arb(-1))
            restricted_bernstein = chebyshev_to_bernstein(restricted)
            for cell_index, cell in enumerate(subdivide_bernstein(
                restricted_bernstein, subdivision["sDepth"]
            )):
                image = inflate_by_modulus_error(complex_hull(cell), tensor_error)
                base_cells.append({
                    "panelId": panel["id"],
                    "panelIndex": panel_index,
                    "cellIndex": cell_index,
                    "image": image,
                    "startCandidate": midpoint_record(cell[0]),
                    "endCandidate": midpoint_record(cell[-1]),
                })
        else:
            if local_minimum is None or panel_minimum < local_minimum:
                local_minimum = panel_minimum

        panel_results.append({
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
            "cells": cell_records,
        })
        progress.emit(
            "panel-analyzed",
            panelId=panel["id"],
            minimumAbsoluteLower=arb_text(panel_minimum),
            cellCount=len(cells),
        )

    if not base_cells or global_minimum is None or local_minimum is None:
        raise RuntimeError("missing global or local analysis cells")

    vertices = [base_cells[0]["startCandidate"]]
    vertices.extend(cell["endCandidate"] for cell in base_cells[:-1])
    winding_cells = []
    homotopy_minimum: arb | None = None
    for index, cell in enumerate(base_cells):
        endpoints = (vertices[index], vertices[(index + 1) % len(vertices)])
        homotopy_box = hull_with_vertices(cell["image"], endpoints)
        witness = axis_half_plane_witness(homotopy_box)
        if witness is None:
            raise RuntimeError(
                f"base homotopy cell has no axis half-plane witness: {index}"
            )
        lower = homotopy_box.abs_lower()
        if homotopy_minimum is None or lower < homotopy_minimum:
            homotopy_minimum = lower
        winding_cells.append({
            "index": index,
            "panelId": cell["panelId"],
            "cellIndex": cell["cellIndex"],
            "imageWithChord": acb_record(homotopy_box),
            "absoluteLower": arb_text(lower),
            "halfPlaneWitness": witness,
        })
    winding = exact_polygon_winding(vertices)
    if winding["winding"] != 1:
        raise RuntimeError(f"unexpected exact base winding: {winding}")

    audit_minimum_denominator: arb | None = None
    audit_minimum_slack: arb | None = None
    audit_max_attempt = 0
    point_count = 0
    for record in checkpoint["panels"].values():
        for value in record["values"]:
            point_count += 1
            denominator = arb(value["audit"]["minimumDenominatorLower"])
            slack = arb(value["audit"]["minimumComponentSlack"])
            if audit_minimum_denominator is None or denominator < audit_minimum_denominator:
                audit_minimum_denominator = denominator
            if audit_minimum_slack is None or slack < audit_minimum_slack:
                audit_minimum_slack = slack
            audit_max_attempt = max(
                audit_max_attempt,
                value["audit"]["maximumPicardAttempt"],
            )

    result = {
        "schemaVersion": SCHEMA_VERSION,
        "status": "passed",
        "completedAt": utc_now(),
        "sourceLedger": checkpoint["sourceLedger"],
        "sourceDigest": checkpoint["sourceDigest"],
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
            "maximumPicardInflationAttempt": audit_max_attempt,
        },
        "interpolation": {
            "nodes": "roots of T_(degree+1)",
            "remainderFormula": "4*M*rho^(-degree)/(rho-1)",
            "tensorDecomposition": "epsilon_s + Lambda_s*epsilon_d",
            "lebesgueLimit": config["lebesgueLimit"],
            "degreeDLebesgueBound": arb_text(
                chebyshev_lebesgue_bound(config["degreeD"])
            ),
        },
        "decisions": {
            "globalBoundaryNonzeroForAllD": True,
            "globalMinimumAbsoluteLower": arb_text(global_minimum),
            "localBoundaryNonzeroForAllD": True,
            "localMinimumAbsoluteLower": arb_text(local_minimum),
            "basePositiveOrientationWinding": winding["winding"],
            "baseHomotopyMinimumAbsoluteLower": arb_text(
                homotopy_minimum or arb(0)
            ),
        },
        "exactPolygon": {
            **winding,
            "vertexCount": len(vertices),
            "vertices": vertices,
            "cells": winding_cells,
        },
        "panels": panel_results,
    }
    return result


def smoke(config: dict[str, Any], panels: list[dict[str, Any]]) -> None:
    worker_initialize(config)
    selected = [
        next(panel for panel in panels if panel["id"].startswith("G-left")),
        next(panel for panel in panels if panel["id"].startswith("G-bottom")),
        next(panel for panel in panels if panel["id"].startswith("L-circle")),
    ]
    for panel in selected:
        result = worker_point({
            "panel": panel,
            "dIndex": config["degreeD"] // 2,
            "sIndex": panel["degreeS"] // 2,
        })
        print(canonical_json(result), end="")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=HERE / "config.json")
    parser.add_argument("--checkpoint", type=Path, default=HERE / "contour_grid_checkpoint.json")
    parser.add_argument("--output", type=Path, default=HERE / "contour_certificate.json")
    parser.add_argument("--progress", type=Path, default=HERE / "progress.ndjson")
    parser.add_argument("--resource-log", type=Path, default=HERE / "resources.ndjson")
    parser.add_argument("--analyze-only", action="store_true")
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = json.loads(args.config.read_text())
    if config["schemaVersion"] != SCHEMA_VERSION:
        raise RuntimeError("configuration schema mismatch")
    ctx.dps = config["dps"]
    panels = panel_definitions(config)
    if args.smoke:
        smoke(config, panels)
        return
    progress = Progress(args.progress)
    started = time.monotonic()
    stop = threading.Event()
    monitor = threading.Thread(
        target=resource_monitor,
        args=(stop, args.resource_log, config["resourceIntervalSeconds"], started),
        daemon=True,
    )
    monitor.start()
    try:
        if args.analyze_only:
            checkpoint = json.loads(args.checkpoint.read_text())
        else:
            checkpoint = run_grids(
                config, panels, args.checkpoint, progress
            )
        certificate = analyze_checkpoint(config, panels, checkpoint, progress)
        atomic_json(args.output, certificate)
        checkpoint["status"] = "passed"
        checkpoint["updatedAt"] = utc_now()
        atomic_json(args.checkpoint, checkpoint)
        progress.emit(
            "certificate-passed",
            output=str(args.output.relative_to(ROOT)),
            elapsedSeconds=time.monotonic() - started,
            decisions=certificate["decisions"],
        )
    finally:
        stop.set()
        monitor.join(timeout=5)


if __name__ == "__main__":
    main()
