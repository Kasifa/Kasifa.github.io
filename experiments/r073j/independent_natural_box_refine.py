#!/usr/bin/env python3
"""Full-cover dyadic refinement of the seven inconclusive natural boxes.

This driver reads the frozen 76/83 natural-box audit and reuses only its
independent Arb/Acb ODE kernel.  Each of the seven failed ``(d,s)`` rectangles
is split into all four 2-by-2 children.  A failed first-level child is split
into all four children once more.  No region is discarded, and no box is made
narrower than this frozen maximum additional depth of two.

The result is still corroborative: it refines seven selected natural boxes,
not a cover of either complete spectral contour.
"""

from __future__ import annotations

import argparse
import ast
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
from typing import Any, Iterable, Sequence

import flint
from flint import arb, ctx

import independent_natural_box_validate as natural


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SCHEMA_VERSION = "r073j-independent-natural-box-refinement-v1"
PRECISION_DPS = 120
ORDER = 14
WORKERS = 16
MAXIMUM_ADDITIONAL_DEPTH = 2
EXPECTED_PARENT_COUNT = 7
EXPECTED_BASELINE_PASSED = 76
RESOURCE_INTERVAL_SECONDS = 5
WORKER_SETTINGS: dict[str, Any] = {}


class RefinementFailure(RuntimeError):
    """Fail-closed baseline, geometry, or orchestration failure."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RefinementFailure(message)


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


def parse_fraction(value: Any, label: str) -> Fraction:
    require(type(value) is str and value != "", f"{label} is not a rational string")
    try:
        return Fraction(value)
    except (ValueError, ZeroDivisionError) as error:
        raise RefinementFailure(f"{label} is not a rational") from error


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def interval_record(lower: Fraction, upper: Fraction) -> dict[str, str]:
    require(lower <= upper, "reversed rational interval")
    return {"lower": fraction_text(lower), "upper": fraction_text(upper)}


def interval_tuple(record: dict[str, Any], label: str) -> tuple[Fraction, Fraction]:
    require(type(record) is dict and set(record) == {"lower", "upper"},
            f"{label} is not an exact interval record")
    lower = parse_fraction(record["lower"], f"{label}.lower")
    upper = parse_fraction(record["upper"], f"{label}.upper")
    require(lower < upper, f"{label} must have positive width")
    return lower, upper


def file_digest(path: Path) -> str:
    require(path.is_file(), f"required file missing: {path}")
    return sha256_bytes(path.read_bytes())


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


def audit_base_imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            modules.append(node.module or "")
    forbidden = (
        "r073j_interval_core", "r073j_chebyshev", "certify_contours",
        "research", "driver", "analyzer",
    )
    require(not [module for module in modules
                 if any(token in module for token in forbidden)],
            "frozen independent ODE kernel imports a primary module")
    return modules


def verify_frozen_baseline(
    baseline_path: Path,
    progress_path: Path,
    resources_path: Path,
    config_path: Path,
    design_path: Path,
    kernel_path: Path,
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, str], list[str]]:
    paths = {
        "baseline": baseline_path,
        "baselineProgress": progress_path,
        "baselineResources": resources_path,
        "config": config_path,
        "design": design_path,
        "independentOdeKernel": kernel_path,
    }
    digests = {name: file_digest(path) for name, path in paths.items()}
    imported_modules = audit_base_imports(kernel_path)

    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    require(baseline.get("schemaVersion") == natural.SCHEMA_VERSION,
            "baseline natural-box schema mismatch")
    require(baseline.get("status") == "failed",
            "baseline must preserve the original 76/83 failed status")
    decisions = baseline.get("decisions", {})
    require(decisions.get("expectedBoxCount") == natural.EXPECTED_BOX_COUNT
            and decisions.get("passedBoxCount") == EXPECTED_BASELINE_PASSED
            and decisions.get("failedBoxCount") == EXPECTED_PARENT_COUNT
            and decisions.get("all83BoxesPassed") is False,
            "baseline decisions are not the frozen 76/83 result")
    cases = baseline.get("cases")
    require(type(cases) is list and len(cases) == natural.EXPECTED_BOX_COUNT,
            "baseline case list is incomplete")
    require(len({case.get("id") for case in cases}) == len(cases),
            "baseline case IDs are not unique")

    provenance = baseline.get("provenance", {})
    require(provenance.get("scriptSha256") == digests["independentOdeKernel"]
            and provenance.get("configSha256") == digests["config"]
            and provenance.get("frozenIndependentValidationSha256")
            == digests["design"],
            "baseline provenance does not match current frozen inputs")

    config = json.loads(config_path.read_text(encoding="utf-8"))
    design_audit = json.loads(design_path.read_text(encoding="utf-8"))
    require(design_audit.get("status") == "passed",
            "frozen shared-grid audit is not passed")
    expected_cases = natural.build_cases(
        config, design_audit["naturalBoxSpotCheck"]
    )
    expected_by_id = {case["id"]: case for case in expected_cases}
    require(set(expected_by_id) == {case["id"] for case in cases},
            "baseline IDs differ from the frozen 83-box design")
    for case in cases:
        expected = expected_by_id[case["id"]]
        require(case["parameterSpec"] == expected["parameterSpec"]
                and case["family"] == expected["family"]
                and case["steps"] == expected["steps"],
                f"baseline geometry differs for {case['id']}")

    failures = [case for case in cases if case.get("status") != "passed"]
    require(len(failures) == EXPECTED_PARENT_COUNT,
            "baseline does not contain exactly seven failed cases")
    for case in failures:
        require(case.get("category") == "hash-selected-primary-cell"
                and case.get("parameterSpec", {}).get("kind") == "panel-cell",
                f"failed parent is not a hash-selected (d,s) cell: {case.get('id')}")
        require(case.get("error") == "final Evans enclosure contains zero"
                and case.get("evansAbsoluteLower") == "0",
                f"failed parent has an unexpected failure mode: {case['id']}")
        require(case.get("minimumRayleighDenominatorLower") is not None
                and case.get("minimumPicardTubeSlack") is not None,
                f"failed parent lacks denominator/tube evidence: {case['id']}")

    progress = parse_ndjson(progress_path)
    events = [row.get("event") for row in progress]
    require(events.count("natural-box-run-started") == 1
            and events.count("natural-box-planned") == natural.EXPECTED_BOX_COUNT
            and events.count("natural-box-complete") == natural.EXPECTED_BOX_COUNT
            and events.count("natural-box-run-complete") == 1,
            "baseline progress ledger is incomplete")
    completed_ids = {
        row["caseId"] for row in progress
        if row.get("event") == "natural-box-complete"
    }
    require(completed_ids == set(expected_by_id),
            "baseline progress ledger does not complete the frozen 83 boxes")
    require(all(row.get("runId") == baseline["runId"] for row in progress),
            "baseline progress ledger mixes run IDs")

    resources = parse_ndjson(resources_path)
    resource_events = [row.get("event") for row in resources]
    require(resource_events[0] == "resource-start"
            and resource_events[-1] == "resource-stop",
            "baseline resource ledger lacks start/stop records")
    return baseline, failures, digests, imported_modules


def split_bounds(lower: Fraction, upper: Fraction, side: int) -> tuple[Fraction, Fraction]:
    require(side in (0, 1), "dyadic side must be zero or one")
    midpoint = (lower + upper) / 2
    return (lower, midpoint) if side == 0 else (midpoint, upper)


def split_case(parent: dict[str, Any], depth: int) -> list[dict[str, Any]]:
    require(1 <= depth <= MAXIMUM_ADDITIONAL_DEPTH,
            "refinement depth is outside the frozen range")
    root_id = parent.get("rootOriginalId", parent["id"])
    parent_path = parent.get("refinementPath", "")
    spec = parent["parameterSpec"]
    require(spec.get("kind") == "panel-cell",
            "refinement parent is not a panel cell")
    d_lower, d_upper = interval_tuple(spec["d"], f"{parent['id']}.d")
    s_lower, s_upper = interval_tuple(spec["s"], f"{parent['id']}.s")
    children: list[dict[str, Any]] = []
    for d_side in (0, 1):
        child_d_lower, child_d_upper = split_bounds(d_lower, d_upper, d_side)
        for s_side in (0, 1):
            child_s_lower, child_s_upper = split_bounds(s_lower, s_upper, s_side)
            child_spec = copy.deepcopy(spec)
            child_spec["d"] = interval_record(child_d_lower, child_d_upper)
            child_spec["s"] = interval_record(child_s_lower, child_s_upper)
            child_spec["dDepth"] = int(spec["dDepth"]) + 1
            child_spec["dIndex"] = 2 * int(spec["dIndex"]) + d_side
            child_spec["sDepth"] = int(spec["sDepth"]) + 1
            child_spec["sIndex"] = 2 * int(spec["sIndex"]) + s_side
            path = f"{parent_path}d{d_side}s{s_side}"
            children.append({
                "id": f"REFINE-{root_id}-z{depth}-{path}",
                "category": "failed-parent-full-cover-refinement",
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


def worker_initialize(settings: dict[str, Any]) -> None:
    global WORKER_SETTINGS
    WORKER_SETTINGS = dict(settings)
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


def plan_stage(
    path: Path,
    run_id: str,
    stage: int,
    cases: Sequence[dict[str, Any]],
) -> None:
    for ordinal, case in enumerate(cases):
        append_ndjson(path, {
            "time": utc_now(),
            "event": "refinement-box-planned",
            "runId": run_id,
            "stage": stage,
            "ordinalWithinStage": ordinal,
            "caseId": case["id"],
            "rootOriginalId": case["rootOriginalId"],
            "parentBoxId": case["parentBoxId"],
            "family": case["family"],
            "steps": case["steps"],
        })


def execute_stage(
    pool: Any,
    path: Path,
    run_id: str,
    stage: int,
    cases: Sequence[dict[str, Any]],
    completed_before: int,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for result in pool.imap_unordered(worker_case, cases, chunksize=1):
        results.append(result)
        append_ndjson(path, {
            "time": utc_now(),
            "event": "refinement-box-complete",
            "runId": run_id,
            "stage": stage,
            "completedWithinStage": len(results),
            "stageTotal": len(cases),
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
    require(len(results) == len(cases), f"stage {stage} result count is incomplete")
    return results


def result_minimum(
    results: Sequence[dict[str, Any]], key: str, passed_only: bool = False
) -> dict[str, str] | None:
    available: list[tuple[arb, dict[str, Any]]] = []
    for result in results:
        if passed_only and result.get("status") != "passed":
            continue
        value = result.get(key)
        if value is not None:
            parsed = arb(value)
            require(parsed.is_finite(), f"nonfinite {key} in {result['id']}")
            available.append((parsed, result))
    if not available:
        return None
    value, result = min(available, key=lambda item: item[0].lower())
    return {"caseId": result["id"], "value": natural.arb_text(value)}


def build_root_decisions(
    parents: Sequence[dict[str, Any]],
    stage_one: Sequence[dict[str, Any]],
    stage_two: Sequence[dict[str, Any]],
) -> list[dict[str, Any]]:
    stage_one_by_root: dict[str, list[dict[str, Any]]] = {}
    stage_two_by_parent: dict[str, list[dict[str, Any]]] = {}
    for result in stage_one:
        stage_one_by_root.setdefault(result["rootOriginalId"], []).append(result)
    for result in stage_two:
        stage_two_by_parent.setdefault(result["parentBoxId"], []).append(result)

    decisions: list[dict[str, Any]] = []
    for parent in parents:
        first = stage_one_by_root.get(parent["id"], [])
        require(len(first) == 4,
                f"root {parent['id']} does not have four first-level children")
        leaves: list[dict[str, Any]] = []
        refined_first_level: list[str] = []
        for child in first:
            if child["status"] == "passed":
                require(child["id"] not in stage_two_by_parent,
                        "a passed first-level child was unexpectedly subdivided")
                leaves.append(child)
            else:
                grandchildren = stage_two_by_parent.get(child["id"], [])
                require(len(grandchildren) == 4,
                        f"failed first-level child {child['id']} lacks four grandchildren")
                validate_partition(child, grandchildren)
                refined_first_level.append(child["id"])
                leaves.extend(grandchildren)
        unresolved = [leaf["id"] for leaf in leaves if leaf["status"] != "passed"]
        decisions.append({
            "rootOriginalId": parent["id"],
            "family": parent["family"],
            "firstLevelBoxCount": len(first),
            "refinedFirstLevelBoxIds": refined_first_level,
            "leafBoxCount": len(leaves),
            "passedLeafBoxCount": len(leaves) - len(unresolved),
            "inconclusiveLeafBoxIds": unresolved,
            "fullRegionStructurallyCovered": True,
            "coveredByStrictlyPassingLeaves": not unresolved,
        })
    require(len(decisions) == EXPECTED_PARENT_COUNT,
            "root refinement decision count is incomplete")
    return decisions


def run(
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
            "refinement arithmetic differs from the frozen kernel")
    ctx.dps = PRECISION_DPS
    ctx.threads = 1
    kernel_path = Path(natural.__file__).resolve()
    script_path = Path(__file__).resolve()
    script_bytes = script_path.read_bytes()
    baseline, parents, frozen_digests, imported_modules = verify_frozen_baseline(
        baseline_path, baseline_progress_path, baseline_resources_path,
        config_path, design_path, kernel_path,
    )
    stage_one_cases = [
        child for parent in parents for child in split_case(parent, 1)
    ]
    require(len(stage_one_cases) == 4 * EXPECTED_PARENT_COUNT,
            "first refinement level does not contain 28 boxes")
    require(len({case["id"] for case in stage_one_cases})
            == len(stage_one_cases), "first-level IDs are not unique")

    run_id = sha256_bytes(
        (sha256_bytes(script_bytes) + frozen_digests["baseline"]
         + utc_now()).encode("ascii")
    )[:20]
    started = time.perf_counter()
    initialize_ndjson(progress_path, {
        "time": utc_now(),
        "event": "refinement-run-started",
        "runId": run_id,
        "failedParentCount": len(parents),
        "maximumAdditionalDepth": MAXIMUM_ADDITIONAL_DEPTH,
        "workers": WORKERS,
        "order": ORDER,
        "precisionDecimalDigits": PRECISION_DPS,
        "globalSteps": natural.GLOBAL_STEPS,
        "localSteps": natural.LOCAL_STEPS,
    })
    initialize_ndjson(resources_path, resource_snapshot(started, "resource-start"))
    plan_stage(progress_path, run_id, 1, stage_one_cases)

    stop = threading.Event()
    monitor = threading.Thread(
        target=resource_monitor,
        args=(stop, resources_path, started), daemon=True,
    )
    monitor.start()
    settings = {"dps": PRECISION_DPS, "order": ORDER}
    context = mp.get_context("spawn")
    stage_one_results: list[dict[str, Any]] = []
    stage_two_results: list[dict[str, Any]] = []
    try:
        with context.Pool(
            processes=WORKERS,
            initializer=worker_initialize,
            initargs=(settings,),
            maxtasksperchild=8,
        ) as pool:
            stage_one_results = execute_stage(
                pool, progress_path, run_id, 1, stage_one_cases, 0
            )
            failed_first_level = [
                result for result in stage_one_results
                if result["status"] != "passed"
            ]
            stage_two_cases = [
                child for parent in failed_first_level
                for child in split_case(parent, 2)
            ]
            require(len({case["id"] for case in stage_two_cases})
                    == len(stage_two_cases), "second-level IDs are not unique")
            plan_stage(progress_path, run_id, 2, stage_two_cases)
            if stage_two_cases:
                stage_two_results = execute_stage(
                    pool, progress_path, run_id, 2, stage_two_cases,
                    len(stage_one_results),
                )
    finally:
        stop.set()
        monitor.join(timeout=10)
        append_ndjson(resources_path, resource_snapshot(started, "resource-stop"))

    root_decisions = build_root_decisions(
        parents, stage_one_results, stage_two_results
    )
    all_results = stage_one_results + stage_two_results
    all_seven_covered = all(
        decision["coveredByStrictlyPassingLeaves"]
        for decision in root_decisions
    )
    unresolved = [
        leaf_id for decision in root_decisions
        for leaf_id in decision["inconclusiveLeafBoxIds"]
    ]
    leaf_ids: set[str] = set()
    stage_two_parent_ids = {result["parentBoxId"] for result in stage_two_results}
    for result in stage_one_results:
        if result["id"] not in stage_two_parent_ids:
            leaf_ids.add(result["id"])
    leaf_ids.update(result["id"] for result in stage_two_results)
    leaves = [result for result in all_results if result["id"] in leaf_ids]

    current_digests = {
        "baseline": file_digest(baseline_path),
        "baselineProgress": file_digest(baseline_progress_path),
        "baselineResources": file_digest(baseline_resources_path),
        "config": file_digest(config_path),
        "design": file_digest(design_path),
        "independentOdeKernel": file_digest(kernel_path),
    }
    require(current_digests == frozen_digests,
            "a frozen baseline artifact changed during refinement")
    require(script_path.read_bytes() == script_bytes,
            "refinement source changed during its run")

    decisions = {
        "originalPassedBoxCount": EXPECTED_BASELINE_PASSED,
        "originalFailedParentCount": EXPECTED_PARENT_COUNT,
        "firstLevelBoxCount": len(stage_one_results),
        "firstLevelPassedBoxCount": sum(
            result["status"] == "passed" for result in stage_one_results
        ),
        "firstLevelFailedBoxCount": sum(
            result["status"] != "passed" for result in stage_one_results
        ),
        "secondLevelBoxCount": len(stage_two_results),
        "secondLevelPassedBoxCount": sum(
            result["status"] == "passed" for result in stage_two_results
        ),
        "secondLevelFailedBoxCount": sum(
            result["status"] != "passed" for result in stage_two_results
        ),
        "finalLeafBoxCount": len(leaves),
        "finalPassedLeafBoxCount": sum(
            result["status"] == "passed" for result in leaves
        ),
        "finalInconclusiveLeafBoxIds": unresolved,
        "allSevenFailedParentsCoveredByPassingLeaves": all_seven_covered,
        "allOriginal83NaturalBoxesCoveredDirectlyOrByPassingRefinedLeaves": (
            all_seven_covered
        ),
        "minimumPassedLeafEvansAbsoluteLower": result_minimum(
            leaves, "evansAbsoluteLower", passed_only=True
        ),
        "minimumRefinementRayleighDenominatorLower": result_minimum(
            all_results, "minimumRayleighDenominatorLower"
        ),
        "minimumRefinementPicardTubeSlack": result_minimum(
            all_results, "minimumPicardTubeSlack"
        ),
        "rootCoverage": root_decisions,
    }
    output = {
        "schemaVersion": SCHEMA_VERSION,
        "status": "passed" if all_seven_covered else "inconclusive",
        "completedAt": utc_now(),
        "runId": run_id,
        "classification": "full-cover-refinement-of-seven-natural-boxes",
        "provenance": {
            "scriptSha256": sha256_bytes(script_bytes),
            "frozenArtifactSha256": frozen_digests,
            "baselineRunId": baseline["runId"],
            "pythonFlintVersion": flint.__version__,
            "python": platform.python_version(),
            "pythonImplementation": platform.python_implementation(),
            "independentKernelImportedModules": imported_modules,
        },
        "method": {
            "arithmetic": "python-flint Arb/Acb outward-rounded ball arithmetic",
            "precisionDecimalDigits": PRECISION_DPS,
            "TaylorOrder": ORDER,
            "globalSteps": natural.GLOBAL_STEPS,
            "localSteps": natural.LOCAL_STEPS,
            "workers": WORKERS,
            "flintThreadsPerWorker": 1,
            "partition": "complete 2-by-2 dyadic split in exact rational (d,s)",
            "maximumAdditionalDepth": MAXIMUM_ADDITIONAL_DEPTH,
            "failurePolicy": (
                "refine every failed level-one child once; preserve every failed "
                "level-two child as inconclusive without shrinking or relaxed criteria"
            ),
        },
        "originalFailedParents": [parent["id"] for parent in parents],
        "decisions": decisions,
        "computations": all_results,
        "interpretation": {
            "coverageMeaning": (
                "the final leaf boxes form an exact full cover of each of the seven "
                "original failed (d,s) parent boxes"
            ),
            "successMeaning": (
                "a parent is resolved only when every leaf in its full-cover dyadic "
                "partition has a nonzero Evans box and positive denominator/tube margins"
            ),
            "limitation": (
                "this is full-cover refinement only inside seven selected natural boxes; "
                "it remains corroborative and cannot replace the uniform Clenshaw contour certificate"
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
        "event": "refinement-run-complete",
        "runId": run_id,
        "status": output["status"],
        "elapsedSeconds": output["elapsedSeconds"],
        "decisions": {
            key: value for key, value in decisions.items()
            if key != "rootCoverage"
        },
        "output": str(output_path.relative_to(ROOT)),
    })
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
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
                        default=HERE / "natural_box_refinement.json")
    parser.add_argument("--progress", type=Path,
                        default=HERE / "natural_box_refinement_progress.ndjson")
    parser.add_argument("--resources", type=Path,
                        default=HERE / "natural_box_refinement_resources.ndjson")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        output = run(
            args.baseline.resolve(), args.baseline_progress.resolve(),
            args.baseline_resources.resolve(), args.config.resolve(),
            args.design.resolve(), args.output.resolve(),
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
                "setup or orchestration failed before a complete refinement decision"
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
            if key != "rootCoverage"
        },
    }
    print(canonical_json(summary), end="")
    if output["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
