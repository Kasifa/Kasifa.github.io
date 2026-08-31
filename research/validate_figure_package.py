#!/usr/bin/env python3
"""Validate one archived, paper-ready figure package.

The validator is deliberately independent of Matplotlib.  It checks provenance,
required assets, hashes, and the final visual-QA declarations recorded in the
manifest.  It does not replace looking at the exported figure at final size.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from typing import Any


FINAL_STATUSES = {"formal", "published"}
FINAL_QA_KEYS = (
    "finalSizeInspected",
    "grayscaleInspected",
    "labelsAndLegendsInspected",
    "scalesAndUnitsInspected",
    "dataCrossChecked",
)
COMPUTATION_KINDS = {
    "simulation",
    "exact-audit",
    "exact-formula-audit",
    "data-analysis",
    "exact-audit plus high-precision presentation sampling",
    "closed-form sampling plus validated finite CSV ingestion",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(mapping: dict[str, Any], key: str, where: str, errors: list[str]) -> Any:
    value = mapping.get(key)
    if value in (None, "", [], {}):
        errors.append(f"{where}.{key} is required")
    return value


def validate(package: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    manifest_path = package / "manifest.json"
    if not manifest_path.is_file():
        return {"package": str(package), "errors": ["manifest.json is missing"], "warnings": []}

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {"package": str(package), "errors": [f"manifest.json is invalid: {exc}"], "warnings": []}

    for key in ("schemaVersion", "figureId", "status", "analyticalQuestion", "supportedClaim", "createdAt"):
        require(manifest, key, "manifest", errors)

    final = manifest.get("status") in FINAL_STATUSES
    if not final:
        warnings.append("package is a draft; final-asset and QA requirements are not enforced")

    git = manifest.get("git", {})
    if not isinstance(git, dict):
        errors.append("manifest.git must be an object")
        git = {}
    require(git, "repository", "manifest.git", errors if final else warnings)
    if "commit" in git or "dirty" in git:
        commit = require(git, "commit", "manifest.git", errors if final else warnings)
        dirty = require(git, "dirty", "manifest.git", errors if final else warnings)
        if final and not re.fullmatch(r"[0-9a-fA-F]{40}", str(commit or "")):
            errors.append("manifest.git.commit must be a full 40-character commit hash")
        if final and dirty is not False:
            errors.append("manifest.git.dirty must be false for a formal figure")
    else:
        source_commit = require(
            git, "sourceCommit", "manifest.git", errors if final else warnings
        )
        certificate_commit = require(
            git, "certificateCommit", "manifest.git", errors if final else warnings
        )
        dirty = require(
            git, "dirtyAtCertifiedRun", "manifest.git", errors if final else warnings
        )
        if final:
            for key, commit in (
                ("sourceCommit", source_commit),
                ("certificateCommit", certificate_commit),
            ):
                if not re.fullmatch(r"[0-9a-fA-F]{40}", str(commit or "")):
                    errors.append(
                        f"manifest.git.{key} must be a full 40-character commit hash"
                    )
            if dirty is not False:
                errors.append(
                    "manifest.git.dirtyAtCertifiedRun must be false for a formal figure"
                )

    for relative in ("caption.md", "plot.py"):
        path = package / relative
        if not path.is_file():
            (errors if final else warnings).append(f"{relative} is missing")

    computation_key = "simulation" if "simulation" in manifest else "computation"
    simulation = manifest.get(computation_key, {})
    where = f"manifest.{computation_key}"
    if not isinstance(simulation, dict):
        errors.append(f"{where} must be an object")
        simulation = {}
    for key in ("kind", "configuration", "precision", "solver"):
        require(simulation, key, where, errors if final else warnings)
    command = simulation.get("command") or simulation.get("formalCommand")
    if not command:
        (errors if final else warnings).append(
            f"{where}.command or {where}.formalCommand is required"
        )
    wall_time = simulation.get("wallTimeSeconds")
    if wall_time is None:
        wall_time = simulation.get("scientificWallTimeSeconds")
    if wall_time in (None, ""):
        (errors if final else warnings).append(
            f"{where}.wallTimeSeconds or {where}.scientificWallTimeSeconds is required"
        )
    simulation_kind = simulation.get("kind")
    if simulation_kind not in COMPUTATION_KINDS:
        errors.append(
            f"{where}.kind must be one of {sorted(COMPUTATION_KINDS)}"
        )

    compute = manifest.get("compute", {})
    if not isinstance(compute, dict):
        errors.append("manifest.compute must be an object")
        compute = {}
    for key in ("host", "operatingSystem", "cpu", "memoryGiB", "processes", "threadsPerProcess"):
        require(compute, key, "manifest.compute", errors if final else warnings)

    environment = manifest.get("environment", {})
    if not isinstance(environment, dict):
        errors.append("manifest.environment must be an object")
        environment = {}
    for key in ("python", "packagesLock"):
        require(environment, key, "manifest.environment", errors if final else warnings)
    packages_lock = environment.get("packagesLock")
    if packages_lock and not (package / packages_lock).is_file() and not (package.parent.parent.parent / packages_lock).is_file():
        (errors if final else warnings).append(
            f"manifest.environment.packagesLock does not resolve: {packages_lock}"
        )

    records: list[tuple[str, Path, str]] = []
    data_paths: set[str] = set()
    data = manifest.get("data", [])
    if not isinstance(data, list) or not data:
        (errors if final else warnings).append("manifest.data must contain at least one data record")
    else:
        for index, record in enumerate(data):
            if not isinstance(record, dict):
                errors.append(f"manifest.data[{index}] must be an object")
                continue
            relative = require(record, "path", f"manifest.data[{index}]", errors)
            require(record, "schema", f"manifest.data[{index}]", errors if final else warnings)
            expected = record.get("sha256", "")
            if relative:
                data_paths.add(relative)
                records.append((f"data[{index}]", package / relative, expected))

    monitoring = simulation.get("monitoring", {})
    if not isinstance(monitoring, dict):
        errors.append(f"{where}.monitoring must be an object")
        monitoring = {}
    if simulation_kind == "simulation":
        if final and monitoring.get("enabled") is not True:
            errors.append("formal simulations require monitoring.enabled=true")
        interval = monitoring.get("reportIntervalSeconds")
        if not isinstance(interval, (int, float)) or interval <= 0:
            (errors if final else warnings).append(
                f"{where}.monitoring.reportIntervalSeconds must be positive"
            )
        tracked = monitoring.get("trackedFields")
        if not isinstance(tracked, list) or not tracked:
            (errors if final else warnings).append(
                f"{where}.monitoring.trackedFields must not be empty"
            )
        for key in ("progressLog", "resourceLog"):
            relative = require(
                monitoring,
                key,
                f"{where}.monitoring",
                errors if final else warnings,
            )
            if relative and relative not in data_paths:
                (errors if final else warnings).append(
                    f"{where}.monitoring.{key} must also appear in manifest.data"
                )

    source_data = manifest.get("sourceData", [])
    if not isinstance(source_data, list):
        errors.append("manifest.sourceData must be an array")
    else:
        for index, record in enumerate(source_data):
            if not isinstance(record, dict):
                errors.append(f"manifest.sourceData[{index}] must be an object")
                continue
            if "path" in record:
                relative = require(
                    record,
                    "path",
                    f"manifest.sourceData[{index}]",
                    errors if final else warnings,
                )
                expected = require(
                    record,
                    "sha256",
                    f"manifest.sourceData[{index}]",
                    errors if final else warnings,
                )
                if relative:
                    records.append(
                        (
                            f"sourceData[{index}]",
                            package.parents[2] / relative,
                            expected or "",
                        )
                    )
                continue
            for key in ("location", "fileName", "bytes", "sha256", "extractionCommand"):
                require(
                    record,
                    key,
                    f"manifest.sourceData[{index}]",
                    errors if final else warnings,
                )

    figure = manifest.get("figure", {})
    if not isinstance(figure, dict):
        errors.append("manifest.figure must be an object")
        figure = {}
    outputs = figure.get("outputs", [])
    if not isinstance(outputs, list):
        errors.append("manifest.figure.outputs must be an array")
        outputs = []
    output_extensions: set[str] = set()
    for index, record in enumerate(outputs):
        if not isinstance(record, dict):
            errors.append(f"manifest.figure.outputs[{index}] must be an object")
            continue
        relative = require(record, "path", f"manifest.figure.outputs[{index}]", errors)
        expected = record.get("sha256", "")
        if relative:
            path = package / relative
            output_extensions.add(path.suffix.lower())
            records.append((f"figure.outputs[{index}]", path, expected))
            if path.suffix.lower() == ".png" and final and record.get("dpi") != 600:
                errors.append(f"manifest.figure.outputs[{index}].dpi must be 600")
    if final and not {".pdf", ".svg", ".png"}.issubset(output_extensions):
        errors.append("formal figures require PDF, SVG, and PNG outputs")

    caption = manifest.get("caption", {})
    if not isinstance(caption, dict):
        errors.append("manifest.caption must be an object")
        caption = {}
    english_caption = require(caption, "english", "manifest.caption", errors if final else warnings)
    if english_caption and not (package / english_caption).is_file():
        (errors if final else warnings).append(
            f"manifest.caption.english does not resolve: {english_caption}"
        )

    for label, path, expected in records:
        if not path.is_file():
            (errors if final else warnings).append(f"{label}: {path.name} is missing")
            continue
        actual = sha256(path)
        if not expected:
            (errors if final else warnings).append(f"{label}: sha256 is empty")
        elif expected.lower() != actual:
            errors.append(f"{label}: sha256 mismatch (actual {actual})")

    qa = manifest.get("qa", {})
    if not isinstance(qa, dict):
        errors.append("manifest.qa must be an object")
        qa = {}
    if final:
        if qa.get("status") != "passed":
            errors.append("manifest.qa.status must be passed for a formal figure")
        for key in FINAL_QA_KEYS:
            if qa.get(key) is not True:
                errors.append(f"manifest.qa.{key} must be true for a formal figure")

    return {"package": str(package), "errors": errors, "warnings": warnings}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path, help="figure package directory")
    args = parser.parse_args()
    report = validate(args.package.resolve())
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
