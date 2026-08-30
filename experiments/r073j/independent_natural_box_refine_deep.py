#!/usr/bin/env python3
"""Adaptive full-cover refinement of the 96 unresolved depth-two leaves.

Starting from the frozen ``natural_box_refinement.json``, every unresolved
leaf is split into all four exact rational ``(d,s)`` children.  Passing
branches stop; every unresolved branch is completely split again, through a
maximum total additional depth of six relative to its original natural box.
No sampling, threshold relaxation, or region deletion is permitted.

This remains an independent raw-ODE corroboration of selected natural boxes,
not a replacement for the parameter-uniform contour certificate.
"""

from __future__ import annotations

import argparse
import copy
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
import threading
import time
from typing import Any, Sequence

import flint
from flint import arb, ctx

import independent_natural_box_validate as natural
import independent_natural_box_refine as shallow


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SCHEMA_VERSION = "r073j-independent-natural-box-refinement-deep-v1"
PRECISION_DPS = 120
ORDER = 14
WORKERS = 16
STARTING_DEPTH = 2
MAXIMUM_ADDITIONAL_DEPTH = 6
LEAF_FORECAST_LIMIT = 30000
EXPECTED_STARTING_FAILURES = 96
EXPECTED_SHALLOW_PASSED_LEAVES = 16
EXPECTED_ROOTS = 7
RESOURCE_INTERVAL_SECONDS = 5


class DeepRefinementFailure(RuntimeError):
    """Fail-closed input, geometry, or orchestration failure."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise DeepRefinementFailure(message)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def compact_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True)


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2,
                      ensure_ascii=True) + "\n"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def file_digest(path: Path) -> str:
    require(path.is_file(), f"required file missing: {path}")
    return sha256_bytes(path.read_bytes())


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(canonical_json(value), encoding="utf-8")
    os.replace(temporary, path)


def append_ndjson(path: Path, value: object) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(compact_json(value) + "\n")


def initialize_ndjson(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(compact_json(value) + "\n", encoding="utf-8")


def parse_ndjson(path: Path) -> list[dict[str, Any]]:
    require(path.is_file(), f"required NDJSON missing: {path}")
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        require(line != "", f"blank NDJSON record at {path}:{line_number}")
        value = json.loads(line)
        require(type(value) is dict,
                f"NDJSON record is not an object at {path}:{line_number}")
        rows.append(value)
    return rows


def parse_fraction(value: Any, label: str) -> Fraction:
    require(type(value) is str and value != "", f"{label} is not a rational string")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise DeepRefinementFailure(f"{label} is not a rational") from error


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def interval_tuple(record: dict[str, Any], label: str) -> tuple[Fraction, Fraction]:
    require(type(record) is dict and set(record) == {"lower", "upper"},
            f"{label} is not an exact interval record")
    lower = parse_fraction(record["lower"], f"{label}.lower")
    upper = parse_fraction(record["upper"], f"{label}.upper")
    require(lower < upper, f"{label} must have positive width")
    return lower, upper


def interval_record(lower: Fraction, upper: Fraction) -> dict[str, str]:
    require(lower < upper, "refinement interval must have positive width")
    return {"lower": fraction_text(lower), "upper": fraction_text(upper)}


def split_bounds(lower: Fraction, upper: Fraction, side: int) -> tuple[Fraction, Fraction]:
    require(side in (0, 1), "dyadic side must be zero or one")
    midpoint = (lower + upper) / 2
    return (lower, midpoint) if side == 0 else (midpoint, upper)


def split_case(parent: dict[str, Any], depth: int) -> list[dict[str, Any]]:
    require(STARTING_DEPTH < depth <= MAXIMUM_ADDITIONAL_DEPTH,
            "deep refinement depth is outside the frozen range")
    require(parent.get("refinementDepth") == depth - 1,
            "parent depth is inconsistent with requested child depth")
    spec = parent["parameterSpec"]
    require(spec.get("kind") == "panel-cell",
            "deep refinement parent is not a panel cell")
    root_id = parent["rootOriginalId"]
    parent_path = parent["refinementPath"]
    d_lower, d_upper = interval_tuple(spec["d"], f"{parent['id']}.d")
    s_lower, s_upper = interval_tuple(spec["s"], f"{parent['id']}.s")
    children: list[dict[str, Any]] = []
    for d_side in (0, 1):
        child_d = split_bounds(d_lower, d_upper, d_side)
        for s_side in (0, 1):
            child_s = split_bounds(s_lower, s_upper, s_side)
            child_spec = copy.deepcopy(spec)
            child_spec["d"] = interval_record(*child_d)
            child_spec["s"] = interval_record(*child_s)
            child_spec["dDepth"] = int(spec["dDepth"]) + 1
            child_spec["dIndex"] = 2 * int(spec["dIndex"]) + d_side
            child_spec["sDepth"] = int(spec["sDepth"]) + 1
            child_spec["sIndex"] = 2 * int(spec["sIndex"]) + s_side
            path = f"{parent_path}d{d_side}s{s_side}"
            children.append({
                "id": f"DEEP-{root_id}-z{depth}-{path}",
                "category": "adaptive-deep-full-cover-refinement",
                "family": parent["family"],
                "steps": parent["steps"],
                "parameterSpec": child_spec,
                "rootOriginalId": root_id,
                "parentBoxId": parent["id"],
                "refinementDepth": depth,
                "refinementPath": path,
                "splitIndices": {"d": d_side, "s": s_side},
            })
    validate_partition(parent, children)
    return children


def validate_partition(parent: dict[str, Any], children: Sequence[dict[str, Any]]) -> None:
    require(len(children) == 4, "a 2-by-2 partition must have four children")
    parent_d = interval_tuple(parent["parameterSpec"]["d"], f"{parent['id']}.d")
    parent_s = interval_tuple(parent["parameterSpec"]["s"], f"{parent['id']}.s")
    expected: set[tuple[Fraction, Fraction, Fraction, Fraction]] = set()
    for d_side in (0, 1):
        d_bounds = split_bounds(*parent_d, d_side)
        for s_side in (0, 1):
            s_bounds = split_bounds(*parent_s, s_side)
            expected.add((*d_bounds, *s_bounds))
    actual = {
        (*interval_tuple(child["parameterSpec"]["d"], f"{child['id']}.d"),
         *interval_tuple(child["parameterSpec"]["s"], f"{child['id']}.s"))
        for child in children
    }
    require(actual == expected,
            f"children do not exactly partition parent {parent['id']}")
    require(len({child["id"] for child in children}) == 4,
            f"child IDs are not unique for parent {parent['id']}")


def exact_grid_cover(
    parent: dict[str, Any], leaves: Sequence[dict[str, Any]], divisions: int
) -> bool:
    parent_d = interval_tuple(parent["parameterSpec"]["d"], f"{parent['id']}.d")
    parent_s = interval_tuple(parent["parameterSpec"]["s"], f"{parent['id']}.s")
    d_points = [
        parent_d[0] + (parent_d[1] - parent_d[0]) * Fraction(i, divisions)
        for i in range(divisions + 1)
    ]
    s_points = [
        parent_s[0] + (parent_s[1] - parent_s[0]) * Fraction(i, divisions)
        for i in range(divisions + 1)
    ]
    expected = {
        (d_points[i], d_points[i + 1], s_points[j], s_points[j + 1])
        for i in range(divisions) for j in range(divisions)
    }
    actual = {
        (*interval_tuple(leaf["parameterSpec"]["d"], f"{leaf['id']}.d"),
         *interval_tuple(leaf["parameterSpec"]["s"], f"{leaf['id']}.s"))
        for leaf in leaves
    }
    return actual == expected


def verify_inputs(
    shallow_output_path: Path,
    shallow_progress_path: Path,
    shallow_resources_path: Path,
    baseline_path: Path,
    baseline_progress_path: Path,
    baseline_resources_path: Path,
    config_path: Path,
    design_path: Path,
    kernel_path: Path,
    shallow_script_path: Path,
) -> tuple[
    dict[str, Any], dict[str, Any], list[dict[str, Any]],
    list[dict[str, Any]], list[dict[str, Any]], dict[str, str]
]:
    paths = {
        "naturalBoxKernel": kernel_path,
        "naturalBoxBaseline": baseline_path,
        "naturalBoxBaselineProgress": baseline_progress_path,
        "naturalBoxBaselineResources": baseline_resources_path,
        "shallowRefinementScript": shallow_script_path,
        "shallowRefinement": shallow_output_path,
        "shallowRefinementProgress": shallow_progress_path,
        "shallowRefinementResources": shallow_resources_path,
        "config": config_path,
        "design": design_path,
    }
    digests = {name: file_digest(path) for name, path in paths.items()}

    baseline, original_failures, baseline_digests, _ = shallow.verify_frozen_baseline(
        baseline_path, baseline_progress_path, baseline_resources_path,
        config_path, design_path, kernel_path,
    )
    baseline_key_map = {
        "baseline": "naturalBoxBaseline",
        "baselineProgress": "naturalBoxBaselineProgress",
        "baselineResources": "naturalBoxBaselineResources",
        "config": "config",
        "design": "design",
        "independentOdeKernel": "naturalBoxKernel",
    }
    require(all(digests[baseline_key_map[name]] == digest
                for name, digest in baseline_digests.items()),
            "baseline digest verification disagrees with shallow verifier")

    refinement = json.loads(shallow_output_path.read_text(encoding="utf-8"))
    require(refinement.get("schemaVersion") == shallow.SCHEMA_VERSION
            and refinement.get("status") == "inconclusive",
            "shallow refinement is not the frozen inconclusive result")
    provenance = refinement.get("provenance", {})
    require(provenance.get("scriptSha256") == digests["shallowRefinementScript"],
            "shallow refinement source digest mismatch")
    require(provenance.get("frozenArtifactSha256") == baseline_digests,
            "shallow refinement baseline digest ledger mismatch")
    decisions = refinement.get("decisions", {})
    require(decisions.get("firstLevelBoxCount") == 28
            and decisions.get("firstLevelFailedBoxCount") == 28
            and decisions.get("secondLevelBoxCount") == 112
            and decisions.get("secondLevelPassedBoxCount")
            == EXPECTED_SHALLOW_PASSED_LEAVES
            and decisions.get("secondLevelFailedBoxCount")
            == EXPECTED_STARTING_FAILURES,
            "shallow refinement counts differ from 28 then 16/96")
    computations = refinement.get("computations")
    require(type(computations) is list and len(computations) == 140,
            "shallow refinement computation list is incomplete")
    require(len({result["id"] for result in computations}) == len(computations),
            "shallow refinement computation IDs are not unique")
    depth_two = [
        result for result in computations if result.get("refinementDepth") == 2
    ]
    shallow_passed = [result for result in depth_two if result["status"] == "passed"]
    starting_failures = [result for result in depth_two if result["status"] != "passed"]
    require(len(depth_two) == 112
            and len(shallow_passed) == EXPECTED_SHALLOW_PASSED_LEAVES
            and len(starting_failures) == EXPECTED_STARTING_FAILURES,
            "shallow depth-two leaf split is not 16 passed and 96 failed")
    require(set(decisions.get("finalInconclusiveLeafBoxIds", []))
            == {result["id"] for result in starting_failures},
            "shallow unresolved leaf list differs from its failed depth-two cases")
    for result in starting_failures:
        require(result.get("error") == "final Evans enclosure contains zero"
                and result.get("evansAbsoluteLower") == "0",
                f"unexpected shallow failure mode: {result['id']}")
        require(arb(result["minimumRayleighDenominatorLower"]).lower() > 0
                and arb(result["minimumPicardTubeSlack"]).lower() > 0,
                f"nonpositive shallow audit margin: {result['id']}")

    progress = parse_ndjson(shallow_progress_path)
    progress_events = [row.get("event") for row in progress]
    require(progress_events.count("refinement-run-started") == 1
            and progress_events.count("refinement-box-planned") == 140
            and progress_events.count("refinement-box-complete") == 140
            and progress_events.count("refinement-run-complete") == 1,
            "shallow refinement progress ledger is incomplete")
    require(all(row.get("runId") == refinement["runId"] for row in progress),
            "shallow refinement progress ledger mixes run IDs")
    resources = parse_ndjson(shallow_resources_path)
    require(resources[0].get("event") == "resource-start"
            and resources[-1].get("event") == "resource-stop",
            "shallow refinement resource ledger lacks start/stop")

    original_by_id = {result["id"]: result for result in original_failures}
    depth_two_by_root: dict[str, list[dict[str, Any]]] = {}
    for result in depth_two:
        depth_two_by_root.setdefault(result["rootOriginalId"], []).append(result)
    require(set(depth_two_by_root) == set(original_by_id),
            "shallow depth-two roots differ from original failed parents")
    for root_id, root_leaves in depth_two_by_root.items():
        require(len(root_leaves) == 16
                and exact_grid_cover(original_by_id[root_id], root_leaves, 4),
                f"shallow depth-two leaves do not exactly cover {root_id}")
    return (
        baseline, refinement, original_failures, shallow_passed,
        starting_failures, digests,
    )


def worker_initialize(settings: dict[str, Any]) -> None:
    natural.worker_initialize(settings)


def worker_case(case: dict[str, Any]) -> dict[str, Any]:
    result = natural.worker_case(case)
    result.update({
        "rootOriginalId": case["rootOriginalId"],
        "parentBoxId": case["parentBoxId"],
        "refinementDepth": case["refinementDepth"],
        "refinementPath": case["refinementPath"],
        "splitIndices": case["splitIndices"],
    })
    return result


def resource_snapshot(started: float, event: str) -> dict[str, Any]:
    own = resource.getrusage(resource.RUSAGE_SELF)
    children = resource.getrusage(resource.RUSAGE_CHILDREN)
    return {
        "time": utc_now(),
        "event": event,
        "elapsedSeconds": time.perf_counter() - started,
        "loadAverage": list(os.getloadavg()),
        "selfUserSeconds": own.ru_utime,
        "selfSystemSeconds": own.ru_stime,
        "childrenUserSeconds": children.ru_utime,
        "childrenSystemSeconds": children.ru_stime,
        "selfMaxRssRaw": own.ru_maxrss,
        "childrenMaxRssRaw": children.ru_maxrss,
        "diskFreeBytes": shutil.disk_usage(HERE).free,
    }


def resource_monitor(stop: threading.Event, path: Path, started: float) -> None:
    while not stop.wait(RESOURCE_INTERVAL_SECONDS):
        append_ndjson(path, resource_snapshot(started, "resource-sample"))


def plan_layer(
    path: Path, run_id: str, depth: int, cases: Sequence[dict[str, Any]]
) -> None:
    append_ndjson(path, {
        "time": utc_now(),
        "event": "deep-layer-started",
        "runId": run_id,
        "depth": depth,
        "boxCount": len(cases),
        "parentCount": len(cases) // 4,
    })
    for ordinal, case in enumerate(cases):
        append_ndjson(path, {
            "time": utc_now(),
            "event": "deep-box-planned",
            "runId": run_id,
            "depth": depth,
            "ordinalWithinLayer": ordinal,
            "caseId": case["id"],
            "rootOriginalId": case["rootOriginalId"],
            "parentBoxId": case["parentBoxId"],
            "family": case["family"],
            "steps": case["steps"],
        })


def execute_layer(
    pool: Any,
    path: Path,
    run_id: str,
    depth: int,
    cases: Sequence[dict[str, Any]],
    completed_before: int,
) -> tuple[list[dict[str, Any]], float]:
    layer_started = time.perf_counter()
    results: list[dict[str, Any]] = []
    for result in pool.imap_unordered(worker_case, cases, chunksize=1):
        results.append(result)
        append_ndjson(path, {
            "time": utc_now(),
            "event": "deep-box-complete",
            "runId": run_id,
            "depth": depth,
            "completedWithinLayer": len(results),
            "layerTotal": len(cases),
            "completedOverall": completed_before + len(results),
            "caseId": result["id"],
            "rootOriginalId": result["rootOriginalId"],
            "parentBoxId": result["parentBoxId"],
            "status": result["status"],
            "elapsedSeconds": result["elapsedSeconds"],
            "evansAbsoluteLower": result.get("evansAbsoluteLower"),
            "minimumRayleighDenominatorLower": result.get(
                "minimumRayleighDenominatorLower"
            ),
            "minimumPicardTubeSlack": result.get("minimumPicardTubeSlack"),
            "error": result.get("error"),
        })
    order = {case["id"]: index for index, case in enumerate(cases)}
    results.sort(key=lambda result: order[result["id"]])
    require(len(results) == len(cases), f"depth-{depth} result count is incomplete")
    return results, time.perf_counter() - layer_started


def result_minimum(
    results: Sequence[dict[str, Any]], key: str, passed_only: bool = False
) -> dict[str, str] | None:
    available: list[tuple[arb, dict[str, Any]]] = []
    for result in results:
        if passed_only and result.get("status") != "passed":
            continue
        value = result.get(key)
        if value is None:
            continue
        parsed = arb(value)
        require(parsed.is_finite(), f"nonfinite {key} in {result['id']}")
        available.append((parsed, result))
    if not available:
        return None
    value, result = min(available, key=lambda item: item[0].lower())
    return {"caseId": result["id"], "value": natural.arb_text(value)}


def checkpoint(
    output_path: Path,
    run_id: str,
    source_hash: str,
    frozen_digests: dict[str, str],
    layers: Sequence[dict[str, Any]],
    computations: Sequence[dict[str, Any]],
    current_failures: Sequence[dict[str, Any]],
    elapsed: float,
) -> None:
    atomic_json(output_path, {
        "schemaVersion": SCHEMA_VERSION,
        "status": "running",
        "updatedAt": utc_now(),
        "runId": run_id,
        "provenance": {
            "scriptSha256": source_hash,
            "frozenArtifactSha256": frozen_digests,
        },
        "completedLayers": list(layers),
        "completedComputationCount": len(computations),
        "currentInconclusiveLeafBoxIds": [
            result["id"] for result in current_failures
        ],
        "computations": list(computations),
        "elapsedSeconds": elapsed,
        "interpretation": "atomic layer-boundary recovery checkpoint; no final decision",
    })


def construct_final_leaf_cover(
    original_parents: Sequence[dict[str, Any]],
    shallow_depth_two: Sequence[dict[str, Any]],
    deep_results: Sequence[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    original_by_id = {result["id"]: result for result in original_parents}
    shallow_by_root: dict[str, list[dict[str, Any]]] = {}
    children_by_parent: dict[str, list[dict[str, Any]]] = {}
    for result in shallow_depth_two:
        shallow_by_root.setdefault(result["rootOriginalId"], []).append(result)
    for result in deep_results:
        children_by_parent.setdefault(result["parentBoxId"], []).append(result)

    all_leaves: list[dict[str, Any]] = []
    root_decisions: list[dict[str, Any]] = []

    def visit(node: dict[str, Any]) -> list[dict[str, Any]]:
        children = children_by_parent.get(node["id"], [])
        if not children:
            return [node]
        require(node["status"] != "passed",
                f"passed branch was incorrectly subdivided: {node['id']}")
        require(len(children) == 4,
                f"expanded node does not have four children: {node['id']}")
        validate_partition(node, children)
        descendants: list[dict[str, Any]] = []
        for child in children:
            descendants.extend(visit(child))
        return descendants

    for parent in original_parents:
        first = shallow_by_root.get(parent["id"], [])
        require(len(first) == 16 and exact_grid_cover(parent, first, 4),
                f"shallow leaves do not exactly cover original parent {parent['id']}")
        leaves: list[dict[str, Any]] = []
        for node in first:
            leaves.extend(visit(node))
        unresolved = [leaf["id"] for leaf in leaves if leaf["status"] != "passed"]
        depth_counts: dict[str, int] = {}
        for leaf in leaves:
            depth = str(leaf["refinementDepth"])
            depth_counts[depth] = depth_counts.get(depth, 0) + 1
        root_decisions.append({
            "rootOriginalId": parent["id"],
            "family": parent["family"],
            "leafBoxCount": len(leaves),
            "leafCountByDepth": depth_counts,
            "passedLeafBoxCount": len(leaves) - len(unresolved),
            "inconclusiveLeafBoxIds": unresolved,
            "fullRegionStructurallyCovered": True,
            "coveredByStrictlyPassingLeaves": not unresolved,
        })
        all_leaves.extend(leaves)
    require(len(root_decisions) == EXPECTED_ROOTS,
            "final root coverage decision count is incomplete")
    return all_leaves, root_decisions


def run(
    shallow_output_path: Path,
    shallow_progress_path: Path,
    shallow_resources_path: Path,
    baseline_path: Path,
    baseline_progress_path: Path,
    baseline_resources_path: Path,
    config_path: Path,
    design_path: Path,
    output_path: Path,
    progress_path: Path,
    resources_path: Path,
) -> dict[str, Any]:
    require(flint.__version__ == natural.EXPECTED_PYTHON_FLINT,
            "runtime python-flint version differs from the frozen kernel")
    require(ORDER == natural.ORDER and PRECISION_DPS == natural.PRECISION_DPS,
            "deep-refinement arithmetic differs from the frozen kernel")
    ctx.dps = PRECISION_DPS
    ctx.threads = 1
    script_path = Path(__file__).resolve()
    script_bytes = script_path.read_bytes()
    source_hash = sha256_bytes(script_bytes)
    kernel_path = Path(natural.__file__).resolve()
    shallow_script_path = Path(shallow.__file__).resolve()
    require(kernel_path == HERE / "independent_natural_box_validate.py"
            and shallow_script_path == HERE / "independent_natural_box_refine.py",
            "independent refinement dependencies did not resolve to sibling files")

    (
        baseline, refinement, original_parents, shallow_passed,
        starting_failures, frozen_digests,
    ) = verify_inputs(
        shallow_output_path, shallow_progress_path, shallow_resources_path,
        baseline_path, baseline_progress_path, baseline_resources_path,
        config_path, design_path, kernel_path, shallow_script_path,
    )
    shallow_depth_two = [
        result for result in refinement["computations"]
        if result["refinementDepth"] == 2
    ]
    run_id = sha256_bytes(
        (source_hash + frozen_digests["shallowRefinement"]
         + utc_now()).encode("ascii")
    )[:20]
    started = time.perf_counter()
    initialize_ndjson(progress_path, {
        "time": utc_now(),
        "event": "deep-run-started",
        "runId": run_id,
        "startingFailedDepthTwoLeaves": len(starting_failures),
        "startingPassedDepthTwoLeaves": len(shallow_passed),
        "startingDepth": STARTING_DEPTH,
        "maximumAdditionalDepth": MAXIMUM_ADDITIONAL_DEPTH,
        "leafForecastLimit": LEAF_FORECAST_LIMIT,
        "workers": WORKERS,
        "order": ORDER,
        "precisionDecimalDigits": PRECISION_DPS,
        "globalSteps": natural.GLOBAL_STEPS,
        "localSteps": natural.LOCAL_STEPS,
    })
    initialize_ndjson(resources_path, resource_snapshot(started, "resource-start"))
    stop = threading.Event()
    monitor = threading.Thread(
        target=resource_monitor,
        args=(stop, resources_path, started), daemon=True,
    )
    monitor.start()

    current_failures = list(starting_failures)
    stopped_passes: list[dict[str, Any]] = []
    all_results: list[dict[str, Any]] = []
    layer_records: list[dict[str, Any]] = []
    completed_depth = STARTING_DEPTH
    stop_reason = "all-branches-passed"
    context = mp.get_context("spawn")
    try:
        with context.Pool(
            processes=WORKERS,
            initializer=worker_initialize,
            initargs=({"dps": PRECISION_DPS, "order": ORDER},),
            maxtasksperchild=32,
        ) as pool:
            for depth in range(STARTING_DEPTH + 1,
                               MAXIMUM_ADDITIONAL_DEPTH + 1):
                if not current_failures:
                    stop_reason = "all-branches-passed"
                    break
                cases = [
                    child for parent in current_failures
                    for child in split_case(parent, depth)
                ]
                require(len(cases) == 4 * len(current_failures),
                        f"depth-{depth} is not a complete 2-by-2 expansion")
                require(len({case["id"] for case in cases}) == len(cases),
                        f"depth-{depth} case IDs are not unique")
                plan_layer(progress_path, run_id, depth, cases)
                results, layer_seconds = execute_layer(
                    pool, progress_path, run_id, depth, cases,
                    len(all_results),
                )
                passed = [result for result in results if result["status"] == "passed"]
                failed = [result for result in results if result["status"] != "passed"]
                stopped_passes.extend(passed)
                all_results.extend(results)
                current_failures = failed
                completed_depth = depth
                current_leaf_count = (
                    len(shallow_passed) + len(stopped_passes)
                    + len(current_failures)
                )
                projected_next_leaf_count = (
                    len(shallow_passed) + len(stopped_passes)
                    + 4 * len(current_failures)
                )
                layer_record = {
                    "depth": depth,
                    "inputFailedParentCount": len(cases) // 4,
                    "boxCount": len(results),
                    "passedBoxCount": len(passed),
                    "failedBoxCount": len(failed),
                    "currentAdaptiveLeafCountIncludingShallowPasses": current_leaf_count,
                    "projectedNextAdaptiveLeafCount": projected_next_leaf_count,
                    "elapsedSeconds": layer_seconds,
                }
                layer_records.append(layer_record)
                append_ndjson(progress_path, {
                    "time": utc_now(),
                    "event": "deep-layer-complete",
                    "runId": run_id,
                    **layer_record,
                })
                checkpoint(
                    output_path, run_id, source_hash, frozen_digests,
                    layer_records, all_results, current_failures,
                    time.perf_counter() - started,
                )
                if not failed:
                    stop_reason = "all-branches-passed"
                    break
                if depth == MAXIMUM_ADDITIONAL_DEPTH:
                    stop_reason = "maximum-depth-reached"
                    break
                if projected_next_leaf_count > LEAF_FORECAST_LIMIT:
                    stop_reason = "next-layer-leaf-forecast-exceeds-limit"
                    break
    finally:
        stop.set()
        monitor.join(timeout=10)
        append_ndjson(resources_path, resource_snapshot(started, "resource-stop"))

    final_leaves, root_decisions = construct_final_leaf_cover(
        original_parents, shallow_depth_two, all_results
    )
    final_unresolved = [
        leaf for leaf in final_leaves if leaf["status"] != "passed"
    ]
    all_roots_resolved = all(
        decision["coveredByStrictlyPassingLeaves"]
        for decision in root_decisions
    )
    require({leaf["id"] for leaf in final_unresolved}
            == {leaf["id"] for leaf in current_failures},
            "final tree leaves differ from the adaptive frontier")

    paths_for_recheck = {
        "naturalBoxKernel": kernel_path,
        "naturalBoxBaseline": baseline_path,
        "naturalBoxBaselineProgress": baseline_progress_path,
        "naturalBoxBaselineResources": baseline_resources_path,
        "shallowRefinementScript": shallow_script_path,
        "shallowRefinement": shallow_output_path,
        "shallowRefinementProgress": shallow_progress_path,
        "shallowRefinementResources": shallow_resources_path,
        "config": config_path,
        "design": design_path,
    }
    require({name: file_digest(path) for name, path in paths_for_recheck.items()}
            == frozen_digests,
            "a frozen natural-box artifact changed during deep refinement")
    require(script_path.read_bytes() == script_bytes,
            "deep-refinement source changed during its run")

    combined_audited = shallow_depth_two + all_results
    decisions = {
        "startingInconclusiveDepthTwoLeafCount": len(starting_failures),
        "completedDepth": completed_depth,
        "stopReason": stop_reason,
        "layers": layer_records,
        "deepComputationCount": len(all_results),
        "deepPassedComputationCount": sum(
            result["status"] == "passed" for result in all_results
        ),
        "deepFailedComputationCountIncludingExpandedInternalNodes": sum(
            result["status"] != "passed" for result in all_results
        ),
        "finalLeafBoxCountAcrossSevenParents": len(final_leaves),
        "finalPassedLeafBoxCount": sum(
            result["status"] == "passed" for result in final_leaves
        ),
        "finalInconclusiveLeafBoxCount": len(final_unresolved),
        "finalInconclusiveLeafBoxIds": [leaf["id"] for leaf in final_unresolved],
        "resolvedOriginalParentCount": sum(
            decision["coveredByStrictlyPassingLeaves"]
            for decision in root_decisions
        ),
        "allSevenParentsCoveredByPassingLeaves": all_roots_resolved,
        "allOriginal83NaturalBoxesCoveredDirectlyOrByPassingRefinedLeaves": (
            all_roots_resolved
        ),
        "minimumFinalPassedLeafEvansAbsoluteLower": result_minimum(
            final_leaves, "evansAbsoluteLower", passed_only=True
        ),
        "minimumDeepPassedEvansAbsoluteLower": result_minimum(
            all_results, "evansAbsoluteLower", passed_only=True
        ),
        "minimumDeepRayleighDenominatorLower": result_minimum(
            all_results, "minimumRayleighDenominatorLower"
        ),
        "minimumDeepPicardTubeSlack": result_minimum(
            all_results, "minimumPicardTubeSlack"
        ),
        "minimumCombinedRefinementRayleighDenominatorLower": result_minimum(
            combined_audited, "minimumRayleighDenominatorLower"
        ),
        "minimumCombinedRefinementPicardTubeSlack": result_minimum(
            combined_audited, "minimumPicardTubeSlack"
        ),
        "rootCoverage": root_decisions,
    }
    output = {
        "schemaVersion": SCHEMA_VERSION,
        "status": "passed" if all_roots_resolved else "inconclusive",
        "completedAt": utc_now(),
        "runId": run_id,
        "classification": "adaptive-full-cover-deep-refinement-of-natural-boxes",
        "provenance": {
            "scriptSha256": source_hash,
            "frozenArtifactSha256": frozen_digests,
            "naturalBoxBaselineRunId": baseline["runId"],
            "shallowRefinementRunId": refinement["runId"],
            "pythonFlintVersion": flint.__version__,
            "python": platform.python_version(),
            "pythonImplementation": platform.python_implementation(),
        },
        "method": {
            "arithmetic": "python-flint Arb/Acb outward-rounded ball arithmetic",
            "precisionDecimalDigits": PRECISION_DPS,
            "TaylorOrder": ORDER,
            "globalSteps": natural.GLOBAL_STEPS,
            "localSteps": natural.LOCAL_STEPS,
            "workers": WORKERS,
            "flintThreadsPerWorker": 1,
            "partition": "complete adaptive 2-by-2 dyadic splits in exact rational (d,s)",
            "startingAdditionalDepth": STARTING_DEPTH,
            "maximumAdditionalDepth": MAXIMUM_ADDITIONAL_DEPTH,
            "leafForecastLimit": LEAF_FORECAST_LIMIT,
            "branchPolicy": (
                "passed branches stop; every failed branch is fully split unless the "
                "maximum depth or post-layer leaf-forecast limit is reached"
            ),
            "decisionPolicy": (
                "Evans box must exclude zero and every Rayleigh-denominator and "
                "Picard-tube margin must be strictly positive"
            ),
        },
        "decisions": decisions,
        "computations": all_results,
        "interpretation": {
            "coverageMeaning": (
                "the adaptive leaves, including previously passed shallow leaves, "
                "form an exact full cover of all seven original failed natural boxes"
            ),
            "failurePolicy": (
                "unresolved leaves at the frozen stopping rule remain inconclusive; "
                "no sampling, box deletion, or relaxed threshold is used"
            ),
            "limitation": (
                "this audit covers seven selected natural boxes only and remains "
                "corroborative; it cannot replace the uniform Clenshaw contour certificate"
            ),
        },
        "artifacts": {
            "progress": str(progress_path.relative_to(ROOT)),
            "resources": str(resources_path.relative_to(ROOT)),
        },
        "elapsedSeconds": time.perf_counter() - started,
    }
    atomic_json(output_path, output)
    append_ndjson(progress_path, {
        "time": utc_now(),
        "event": "deep-run-complete",
        "runId": run_id,
        "status": output["status"],
        "elapsedSeconds": output["elapsedSeconds"],
        "summary": {
            key: value for key, value in decisions.items()
            if key not in ("rootCoverage", "finalInconclusiveLeafBoxIds")
        },
        "output": str(output_path.relative_to(ROOT)),
    })
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shallow", type=Path,
                        default=HERE / "natural_box_refinement.json")
    parser.add_argument("--shallow-progress", type=Path,
                        default=HERE / "natural_box_refinement_progress.ndjson")
    parser.add_argument("--shallow-resources", type=Path,
                        default=HERE / "natural_box_refinement_resources.ndjson")
    parser.add_argument("--baseline", type=Path,
                        default=HERE / "natural_box_validation.json")
    parser.add_argument("--baseline-progress", type=Path,
                        default=HERE / "natural_box_progress.ndjson")
    parser.add_argument("--baseline-resources", type=Path,
                        default=HERE / "natural_box_resources.ndjson")
    parser.add_argument("--config", type=Path, default=HERE / "config.json")
    parser.add_argument("--design", type=Path,
                        default=HERE / "independent_validation.json")
    parser.add_argument("--output", type=Path,
                        default=HERE / "natural_box_refinement_deep.json")
    parser.add_argument("--progress", type=Path,
                        default=HERE / "natural_box_refinement_deep_progress.ndjson")
    parser.add_argument("--resources", type=Path,
                        default=HERE / "natural_box_refinement_deep_resources.ndjson")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        output = run(
            args.shallow.resolve(), args.shallow_progress.resolve(),
            args.shallow_resources.resolve(), args.baseline.resolve(),
            args.baseline_progress.resolve(), args.baseline_resources.resolve(),
            args.config.resolve(), args.design.resolve(), args.output.resolve(),
            args.progress.resolve(), args.resources.resolve(),
        )
    except Exception as error:
        failure = {
            "schemaVersion": SCHEMA_VERSION,
            "status": "failed",
            "completedAt": utc_now(),
            "errorType": type(error).__name__,
            "error": str(error),
            "interpretation": (
                "setup or orchestration failed; progress and any atomic layer "
                "checkpoint remain available for audit"
            ),
        }
        atomic_json(args.output.resolve(), failure)
        print(canonical_json(failure), end="")
        raise SystemExit(1)
    summary = {
        "status": output["status"],
        "output": str(args.output.resolve()),
        "elapsedSeconds": output["elapsedSeconds"],
        "decisions": {
            key: value for key, value in output["decisions"].items()
            if key not in ("rootCoverage", "finalInconclusiveLeafBoxIds")
        },
    }
    print(canonical_json(summary), end="")
    if output["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
