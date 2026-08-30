#!/usr/bin/env python3
"""Certify the R0.73J kinetic left/right overlap and phase anchor."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import multiprocessing as mp
import os
from pathlib import Path
import platform
import resource
import shutil
import sys
import threading
import time
from typing import Any, Sequence


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from flint import acb, arb, ctx  # noqa: E402

from research.r073j_chebyshev import (  # noqa: E402
    chebyshev_evaluate,
    chebyshev_lebesgue_bound,
    inflate_by_modulus_error,
    interpolation_error,
    tensor_chebyshev_coefficients,
)
from research.r073j_overlap_core import integrate_overlap  # noqa: E402


SCHEMA_VERSION = "r073j-kinetic-overlap-v1"
OUTPUT_NAMES = ("anchor", "numerator", "rightEnergy", "leftEnergy")
SOURCE_PATHS = (
    ROOT / "research/r073j_interval_core.py",
    ROOT / "research/r073j_overlap_core.py",
    ROOT / "research/r073j_overlap_analytic_proof.md",
    ROOT / "research/r073j_chebyshev.py",
    HERE / "certify_overlap.py",
    HERE / "overlap_config.json",
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


def ledger() -> list[dict[str, object]]:
    return [
        {
            "path": str(path.relative_to(ROOT)),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        for path in SOURCE_PATHS
    ]


def ledger_digest(value: Sequence[dict[str, object]]) -> str:
    return hashlib.sha256(compact_json(list(value)).encode()).hexdigest()


def atomic_json(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(canonical_json(value))
    os.replace(temporary, path)


def append_ndjson(path: Path, value: object) -> None:
    with path.open("a") as handle:
        handle.write(compact_json(value) + "\n")


def arb_text(value: arb, digits: int = 80) -> str:
    return value.str(digits, more=True)


def arb_rational(text: str) -> arb:
    value = Fraction(text)
    return arb(value.numerator) / value.denominator


def acb_record(value: acb) -> dict[str, str]:
    return {"real": arb_text(value.real), "imag": arb_text(value.imag)}


def acb_from_record(value: dict[str, str]) -> acb:
    return acb(arb(value["real"]), arb(value["imag"]))


def chebyshev_node(index: int, count: int) -> arb:
    return ((2 * index + 1) * arb.pi() / (2 * count)).cos()


def dyadic_interval(index: int, depth: int) -> arb:
    if depth < 0 or not 0 <= index < 2**depth:
        raise ValueError("invalid dyadic cell")
    denominator = 2**depth
    lower = Fraction(-1) + Fraction(2 * index, denominator)
    upper = Fraction(-1) + Fraction(2 * (index + 1), denominator)
    lo = arb(lower.numerator) / lower.denominator
    hi = arb(upper.numerator) / upper.denominator
    return lo.union(hi)


def tensor_interval_clenshaw(
    coefficients: Sequence[Sequence[acb]], d_box: arb, lambda_box: arb
) -> acb:
    lambda_evaluated = [
        chebyshev_evaluate(row, lambda_box) for row in coefficients
    ]
    return chebyshev_evaluate(lambda_evaluated, d_box)


def contour_prerequisite() -> dict[str, object]:
    path = HERE / "contour_certificate.json"
    certificate = json.loads(path.read_text())
    decisions = certificate.get("decisions", {})
    required = {
        "globalBoundaryNonzeroForAllD": True,
        "localBoundaryNonzeroForAllD": True,
        "globalBasePositiveOrientationWinding": 1,
        "localBasePositiveOrientationWinding": 1,
    }
    if certificate.get("status") != "passed":
        raise RuntimeError("the prerequisite contour certificate did not pass")
    if any(decisions.get(key) != value for key, value in required.items()):
        raise RuntimeError("the prerequisite contour decisions are incomplete")
    return {
        "path": str(path.relative_to(ROOT)),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "schemaVersion": certificate.get("schemaVersion"),
        "sourceDigest": certificate.get("sourceDigest"),
        "verifiedDecisions": required,
    }


def worker_initialize(config: dict[str, Any]) -> None:
    global WORKER_CONFIG
    WORKER_CONFIG = config
    ctx.dps = config["dps"]


def worker_point(task: tuple[int, int]) -> dict[str, Any]:
    config = WORKER_CONFIG
    d_index, lambda_index = task
    d_coordinate = chebyshev_node(d_index, config["degreeD"] + 1)
    lambda_coordinate = chebyshev_node(
        lambda_index, config["degreeLambda"] + 1
    )
    d_value = (arb(1) / 450) * (1 + d_coordinate) / 2
    eigenvalue = (
        arb_rational(config["lambdaCenter"])
        + arb_rational(config["lambdaRadius"]) * lambda_coordinate
    )
    values, audit, monodromy_audit = integrate_overlap(
        d_value,
        eigenvalue,
        config["steps"],
        config["order"],
    )
    return {
        "dIndex": d_index,
        "lambdaIndex": lambda_index,
        "values": {name: acb_record(values[name]) for name in OUTPUT_NAMES},
        "audit": {
            "minimumDenominatorLower": arb_text(
                min(
                    audit.minimum_denominator_lower or arb(0),
                    monodromy_audit.minimum_denominator_lower or arb(0),
                )
            ),
            "minimumComponentSlack": arb_text(
                min(
                    audit.minimum_component_slack or arb(0),
                    monodromy_audit.minimum_component_slack or arb(0),
                )
            ),
            "maximumPicardAttempt": max(
                audit.maximum_picard_attempt,
                monodromy_audit.maximum_picard_attempt,
            ),
        },
    }


def overlap_majorant(
    minimum_lambda_real: arb,
    *,
    complex_d: bool,
    rho_d: arb,
) -> dict[str, arb]:
    if minimum_lambda_real <= 0:
        raise ValueError("analytic ellipse reaches Re lambda <= 0")
    if complex_d:
        maximum_d = arb(1) / 450
        real_semiaxis = (rho_d + 1 / rho_d) / 2
        imag_semiaxis = (rho_d - 1 / rho_d) / 2
        d_real_minimum = maximum_d * (1 - real_semiaxis) / 2
        d_imag_maximum = maximum_d * imag_semiaxis / 2
        exp_one = (-d_real_minimum).exp()
        exp_four = (-4 * d_real_minimum).exp()
        imaginary_velocity = (
            exp_one * d_imag_maximum / 2
            + exp_four * d_imag_maximum
        )
        denominator = 2 * minimum_lambda_real - imaginary_velocity
        velocity_xx = exp_one / 2 + exp_four
        velocity_x = exp_one / 2 + exp_four / 2
    else:
        d_real_minimum = arb(0)
        d_imag_maximum = arb(0)
        imaginary_velocity = arb(0)
        denominator = 2 * minimum_lambda_real
        velocity_xx = arb(3) / 2
        velocity_x = arb(1)
    if denominator <= 0:
        raise ValueError("analytic ellipse reaches a Rayleigh pole")
    potential = arb(1) / 4 + velocity_xx / denominator
    root_potential = potential.sqrt()
    fundamental = (2 * arb.pi() * root_potential).exp()
    scaled_solution = fundamental * (1 + fundamental)
    phi = scaled_solution / root_potential
    phi_x = scaled_solution
    anchor = fundamental / root_potential
    numerator = (
        2 * arb.pi() * velocity_xx * phi ** 2 / denominator ** 2
    )
    right_energy = 2 * arb.pi() * (phi_x ** 2 + phi ** 2 / 4)
    left_potential = phi / denominator
    left_potential_x = (
        phi_x / denominator
        + phi * velocity_x / denominator ** 2
    )
    left_energy = 2 * arb.pi() * (
        left_potential_x ** 2 + left_potential ** 2 / 4
    )
    return {
        "minimumLambdaReal": minimum_lambda_real,
        "dRealMinimum": d_real_minimum,
        "dImagMaximum": d_imag_maximum,
        "imaginaryVelocityUpper": imaginary_velocity,
        "denominatorLower": denominator,
        "velocityXXUpper": velocity_xx,
        "velocityXUpper": velocity_x,
        "potentialUpper": potential,
        "fundamentalUpper": fundamental,
        "scaledSolutionUpper": scaled_solution,
        "anchor": anchor,
        "numerator": numerator,
        "rightEnergy": right_energy,
        "leftEnergy": left_energy,
    }


def resource_monitor(
    stop: threading.Event,
    path: Path,
    interval: int,
    started: float,
) -> None:
    while not stop.wait(interval):
        usage = resource.getrusage(resource.RUSAGE_SELF)
        children = resource.getrusage(resource.RUSAGE_CHILDREN)
        append_ndjson(path, {
            "time": utc_now(),
            "elapsedSeconds": time.monotonic() - started,
            "loadAverage": list(os.getloadavg()),
            "selfUserSeconds": usage.ru_utime,
            "childrenUserSeconds": children.ru_utime,
            "selfMaxRss": usage.ru_maxrss,
            "childrenMaxRss": children.ru_maxrss,
            "diskFreeBytes": shutil.disk_usage(HERE).free,
        })


def run_grid(
    config: dict[str, Any],
    checkpoint_path: Path,
    progress_path: Path,
) -> dict[str, Any]:
    source_ledger = ledger()
    digest = ledger_digest(source_ledger)
    if checkpoint_path.exists():
        checkpoint = json.loads(checkpoint_path.read_text())
        if checkpoint.get("sourceDigest") != digest:
            raise RuntimeError("overlap checkpoint source digest mismatch")
        if checkpoint.get("configuration") != config:
            raise RuntimeError("overlap checkpoint configuration mismatch")
        if checkpoint.get("status") == "grid-complete":
            return checkpoint
    tasks = [
        (d_index, lambda_index)
        for d_index in range(config["degreeD"] + 1)
        for lambda_index in range(config["degreeLambda"] + 1)
    ]
    append_ndjson(progress_path, {
        "time": utc_now(),
        "event": "overlap-grid-start",
        "pointCount": len(tasks),
        "workers": config["workers"],
    })
    started = time.monotonic()
    context = mp.get_context("spawn")
    values: list[dict[str, Any]] = []
    with context.Pool(
        processes=config["workers"],
        initializer=worker_initialize,
        initargs=(config,),
    ) as pool:
        for completed, value in enumerate(
            pool.imap_unordered(worker_point, tasks, chunksize=1), start=1
        ):
            values.append(value)
            if completed % 50 == 0 or completed == len(tasks):
                record = {
                    "time": utc_now(),
                    "event": "overlap-grid-progress",
                    "completed": completed,
                    "pointCount": len(tasks),
                    "elapsedSeconds": time.monotonic() - started,
                }
                append_ndjson(progress_path, record)
                print(compact_json(record), flush=True)
    values.sort(key=lambda item: (item["dIndex"], item["lambdaIndex"]))
    checkpoint = {
        "schemaVersion": SCHEMA_VERSION,
        "status": "grid-complete",
        "completedAt": utc_now(),
        "sourceLedger": source_ledger,
        "sourceDigest": digest,
        "configuration": config,
        "shape": [config["degreeD"] + 1, config["degreeLambda"] + 1],
        "values": values,
    }
    atomic_json(checkpoint_path, checkpoint)
    return checkpoint


def analyze(config: dict[str, Any], checkpoint: dict[str, Any]) -> dict[str, Any]:
    ctx.dps = config["dps"]
    rows, columns = checkpoint["shape"]
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
        seen.add(index)
        for name in OUTPUT_NAMES:
            grids[name][index[0]][index[1]] = acb_from_record(
                item["values"][name]
            )
        denominator = arb(item["audit"]["minimumDenominatorLower"])
        slack = arb(item["audit"]["minimumComponentSlack"])
        if minimum_denominator is None or denominator < minimum_denominator:
            minimum_denominator = denominator
        if minimum_slack is None or slack < minimum_slack:
            minimum_slack = slack
        maximum_attempt = max(
            maximum_attempt, item["audit"]["maximumPicardAttempt"]
        )
    if len(seen) != rows * columns:
        raise RuntimeError("incomplete overlap grid")

    rho_d = arb(config["rhoD"])
    rho_lambda = arb(config["rhoLambda"])
    lebesgue_limit = arb(config["lebesgueLimit"])
    if chebyshev_lebesgue_bound(config["degreeLambda"]) >= lebesgue_limit:
        raise RuntimeError("overlap Lebesgue limit failed")
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

    coefficients: dict[str, list[list[acb]]] = {}
    errors: dict[str, arb] = {}
    for name in OUTPUT_NAMES:
        coefficients[name] = tensor_chebyshev_coefficients(grids[name])
        d_error = interpolation_error(
            d_majorant[name], config["degreeD"], rho_d
        )
        lambda_error = interpolation_error(
            lambda_majorant[name],
            config["degreeLambda"],
            rho_lambda,
        )
        errors[name] = lambda_error + lebesgue_limit * d_error

    d_depth = config["subdivision"]["dDepth"]
    lambda_depth = config["subdivision"]["lambdaDepth"]
    result_cells = []
    minimum_anchor: arb | None = None
    minimum_overlap: arb | None = None
    minimum_right_energy: arb | None = None
    minimum_left_energy: arb | None = None
    for d_index in range(2**d_depth):
        d_box = dyadic_interval(d_index, d_depth)
        for lambda_index in range(2**lambda_depth):
            lambda_box = dyadic_interval(lambda_index, lambda_depth)
            boxes = {
                name: inflate_by_modulus_error(
                    tensor_interval_clenshaw(
                        coefficients[name], d_box, lambda_box
                    ),
                    errors[name],
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
                raise RuntimeError(
                    "overlap cell has a nonpositive factor: "
                    f"d={d_index} lambda={lambda_index}"
                )
            overlap_lower = numerator_lower / (
                right_upper * left_upper
            ).sqrt()
            if overlap_lower <= arb(1) / 2:
                raise RuntimeError(
                    "overlap cell misses one-half target: "
                    f"d={d_index} lambda={lambda_index} {overlap_lower}"
                )
            if minimum_anchor is None or anchor_lower < minimum_anchor:
                minimum_anchor = anchor_lower
            if minimum_overlap is None or overlap_lower < minimum_overlap:
                minimum_overlap = overlap_lower
            if (
                minimum_right_energy is None
                or right_lower < minimum_right_energy
            ):
                minimum_right_energy = right_lower
            if minimum_left_energy is None or left_lower < minimum_left_energy:
                minimum_left_energy = left_lower
            result_cells.append({
                "dIndex": d_index,
                "lambdaIndex": lambda_index,
                "dDepth": d_depth,
                "lambdaDepth": lambda_depth,
                "anchor": acb_record(boxes["anchor"]),
                "numerator": acb_record(boxes["numerator"]),
                "rightEnergy": acb_record(boxes["rightEnergy"]),
                "leftEnergy": acb_record(boxes["leftEnergy"]),
                "anchorAbsoluteLower": arb_text(anchor_lower),
                "overlapLower": arb_text(overlap_lower),
            })

    prerequisite = contour_prerequisite()

    return {
        "schemaVersion": SCHEMA_VERSION,
        "status": "passed",
        "completedAt": utc_now(),
        "sourceLedger": checkpoint["sourceLedger"],
        "sourceDigest": checkpoint["sourceDigest"],
        "configuration": config,
        "prerequisiteEvidence": prerequisite,
        "arithmetic": {
            "engine": "python-flint Arb/Acb ball arithmetic",
            "python": platform.python_version(),
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
            "remainderFormula": "epsilon_lambda + Lambda_lambda*epsilon_d",
            "rangeMethod": (
                "direct outward-rounded interval Clenshaw on a complete "
                "dyadic real-box cover"
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
    parser.add_argument("--config", type=Path, default=HERE / "overlap_config.json")
    parser.add_argument("--checkpoint", type=Path, default=HERE / "overlap_grid_checkpoint.json")
    parser.add_argument("--output", type=Path, default=HERE / "overlap_certificate.json")
    parser.add_argument("--progress", type=Path, default=HERE / "overlap_progress.ndjson")
    parser.add_argument("--resources", type=Path, default=HERE / "overlap_resources.ndjson")
    parser.add_argument("--analyze-only", action="store_true")
    parser.add_argument("--smoke", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = json.loads(args.config.read_text())
    if config["schemaVersion"] != SCHEMA_VERSION:
        raise RuntimeError("overlap configuration schema mismatch")
    ctx.dps = config["dps"]
    if args.smoke:
        worker_initialize(config)
        print(canonical_json(worker_point((
            config["degreeD"] // 2,
            config["degreeLambda"] // 2,
        ))), end="")
        return
    started = time.monotonic()
    stop = threading.Event()
    monitor = threading.Thread(
        target=resource_monitor,
        args=(stop, args.resources, config["resourceIntervalSeconds"], started),
        daemon=True,
    )
    monitor.start()
    try:
        checkpoint = (
            json.loads(args.checkpoint.read_text())
            if args.analyze_only
            else run_grid(config, args.checkpoint, args.progress)
        )
        certificate = analyze(config, checkpoint)
        atomic_json(args.output, certificate)
        record = {
            "time": utc_now(),
            "event": "overlap-certificate-passed",
            "elapsedSeconds": time.monotonic() - started,
            "decisions": certificate["decisions"],
        }
        append_ndjson(args.progress, record)
        print(compact_json(record), flush=True)
    finally:
        stop.set()
        monitor.join(timeout=5)


if __name__ == "__main__":
    main()
