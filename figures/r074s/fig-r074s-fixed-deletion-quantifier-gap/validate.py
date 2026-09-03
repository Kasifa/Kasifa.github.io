#!/usr/bin/env python3
"""Validate and two-stage seal the 25-file R0.74S Step 18 figure archive."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import importlib.metadata
import importlib.util
import json
import os
import platform
import re
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPOSITORY_DEFAULT = HERE.parents[3]
SOURCE_FILES = (
    "README.md", "caption.md", "chart-contract-and-source-data.md", "command.txt",
    "config.json", "contract.json", "plot.py", "qa-protocol.md", "requirements.txt",
    "validate.py",
)
RAW_FILES = (
    "environment.json", "figure.pdf", "figure.png", "figure.svg",
    "progress.ndjson", "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png",
    "resource-log.ndjson", "results.json", "source-data.csv",
)
METADATA_FILES = ("SHA256SUMS", "manifest.json", "qa-report.md", "validation.json")
EXPECTED_FILES = frozenset(SOURCE_FILES + RAW_FILES + METADATA_FILES)
FIGURE_ID = "fig-r074s-fixed-deletion-quantifier-gap"
SCHEMA_VERSION = "research-figure-manifest-v1"
FIGURE_SCHEMA_VERSION = "r074s-fixed-deletion-quantifier-gap-manifest-v1"
PENDING_FIGURE_SOURCE_COMMIT = "PENDING_FIGURE_SOURCE_COMMIT"
HEX40 = re.compile(r"[0-9a-f]{40}")
FORBIDDEN_BYTES = (b"/Users/" + b"kasifa", b"/private/" + b"tmp/" + b"r074s-fixed")
REQUIRED_SCOPE_LABELS = (
    "ANALYTIC SCHEMATIC", "ABSTRACT CLOCK TEST", "NOT PDE DATA", "NOT DNS", "NOT CLAY",
)


def need(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    need(isinstance(value, dict), "JSON root must be an object: " + path.name)
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def git_bytes(repository: Path, args: list[str]) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repository), *args], stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    need(result.returncode == 0,
         "git failed: " + result.stderr.decode("utf-8", "replace").strip())
    return result.stdout


def git_text(repository: Path, args: list[str]) -> str:
    return git_bytes(repository, args).decode("utf-8").strip()


def actual_entries() -> set[str]:
    return {path.name for path in HERE.iterdir()}


def assert_sealable_inventory(entries: set[str]) -> None:
    required = set(SOURCE_FILES + RAW_FILES)
    need(required.issubset(entries), "seal requires all 10 source and 11 raw/result files")
    need(entries.issubset(EXPECTED_FILES), "unexpected archive entry: " + repr(sorted(entries - EXPECTED_FILES)))


def assert_exact_inventory(entries: set[str]) -> None:
    need(
        entries == EXPECTED_FILES,
        f"exact 25-file inventory drift: missing={sorted(EXPECTED_FILES - entries)}, extra={sorted(entries - EXPECTED_FILES)}",
    )


def insert_dependencies(path: Path) -> None:
    resolved = path.expanduser().resolve()
    need(resolved.is_dir(), "--deps is not a directory")
    sys.path.insert(0, str(resolved))


def load_plot() -> Any:
    spec = importlib.util.spec_from_file_location("r074s_fixed_deletion_figure_plot", HERE / "plot.py")
    need(spec is not None and spec.loader is not None, "cannot import plot.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def add(checks: list[dict[str, object]], identifier: str, passed: bool,
        **details: object) -> None:
    checks.append({"id": identifier, "pass": bool(passed), **details})
    need(passed, "validation failed: " + identifier)


def read_csv_rows() -> list[dict[str, str]]:
    with (HERE / "source-data.csv").open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def file_record(name: str, classification: str) -> dict[str, object]:
    path = HERE / name
    return {
        "bytes": path.stat().st_size,
        "path": name,
        "schema": classification,
        "sha256": sha256(path),
    }


def deterministic_hashes(config: dict[str, Any]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for name in config["deterministicCore"]:
        path = HERE / name
        need(path.is_file(), "deterministic-core file missing: " + name)
        hashes[name] = sha256(path)
    return hashes


def capture_baseline(path: Path) -> None:
    config = load_json(HERE / "config.json")
    resolved = path.expanduser().resolve()
    need(resolved != HERE and HERE not in resolved.parents, "baseline must be outside archive")
    payload = {
        "hashes": deterministic_hashes(config),
        "schema": "r074s-fixed-deletion-deterministic-baseline-v1",
    }
    resolved.write_text(canonical(payload), encoding="utf-8", newline="\n")
    print(f"PASS: captured {len(payload['hashes'])} deterministic-core hashes")


def verify_baseline(path: Path, config: dict[str, Any]) -> dict[str, object]:
    payload = load_json(path.expanduser().resolve())
    current = deterministic_hashes(config)
    need(payload.get("hashes") == current, "second regeneration changed deterministic-core hashes")
    return {"fileCount": len(current), "hashesMatched": True, "status": "PASS"}


def check_pdf_fonts(page: Any) -> dict[str, object]:
    resources = page.get("/Resources")
    if resources is None:
        return {"allReferencedFontsEmbedded": False, "fonts": []}
    resources = resources.get_object()
    fonts = resources.get("/Font", {})
    fonts = fonts.get_object() if hasattr(fonts, "get_object") else fonts
    records: list[dict[str, object]] = []
    for resource_name, reference in fonts.items():
        font = reference.get_object()
        descriptors: list[Any] = []
        descriptor = font.get("/FontDescriptor")
        if descriptor is not None:
            descriptors.append(descriptor.get_object())
        descendants = font.get("/DescendantFonts")
        if descendants is not None:
            for descendant_reference in descendants:
                descendant = descendant_reference.get_object()
                child = descendant.get("/FontDescriptor")
                if child is not None:
                    descriptors.append(child.get_object())
        embedded = any(
            any(key in descriptor for key in ("/FontFile", "/FontFile2", "/FontFile3"))
            for descriptor in descriptors
        )
        records.append({
            "baseFont": str(font.get("/BaseFont", "")),
            "embedded": embedded,
            "resource": str(resource_name),
            "subtype": str(font.get("/Subtype", "")),
        })
    return {
        "allReferencedFontsEmbedded": bool(records) and all(record["embedded"] for record in records),
        "fonts": records,
    }


def scan_machine_literals(files: set[str]) -> list[str]:
    failures = []
    for name in sorted(files):
        payload = (HERE / name).read_bytes()
        if any(fragment in payload for fragment in FORBIDDEN_BYTES):
            failures.append(name)
    return failures


def validate_content(repository: Path, confirm_visual_qa: bool) -> tuple[list[dict[str, object]], dict[str, Any]]:
    config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    results = load_json(HERE / "results.json")
    environment = load_json(HERE / "environment.json")
    checks: list[dict[str, object]] = []
    plot = load_plot()

    add(checks, "source-raw-inventory", set(SOURCE_FILES + RAW_FILES).issubset(actual_entries()), count=21)
    add(checks, "no-source-raw-symlinks",
        all(not (HERE / name).is_symlink() for name in SOURCE_FILES + RAW_FILES))
    add(checks, "figure-id-consistency", config["figureId"] == contract["figureId"] == FIGURE_ID)
    add(checks, "explicit-claim-boundary", all((
        contract["claimBoundary"]["abstractClockTest"] is True,
        contract["claimBoundary"]["numericalRendering"] is True,
        contract["claimBoundary"]["pdeData"] is False,
        contract["claimBoundary"]["pdeSimulation"] is False,
        contract["claimBoundary"]["dns"] is False,
        contract["claimBoundary"]["clayProblemSolved"] is False,
        contract["claimBoundary"]["openS486Proved"] is False,
        contract["claimBoundary"]["openS487Proved"] is False,
    )))

    actual_runtime = {
        "python": platform.python_version(),
        "numpy": importlib.metadata.version("numpy"),
        "matplotlib": importlib.metadata.version("matplotlib"),
        "pillow": importlib.metadata.version("pillow"),
        "pypdf": importlib.metadata.version("pypdf"),
        "pypdfium2": importlib.metadata.version("pypdfium2"),
    }
    add(checks, "runtime-lock", actual_runtime == config["runtime"], actual=actual_runtime)
    source_blobs = plot.verify_source_binding(repository, config)
    add(checks, "frozen-core-ancestor-and-blobs", len(source_blobs) == 7,
        commit=config["sourceBinding"]["commit"], blobCount=len(source_blobs))

    import numpy as np
    expected_rows, _arrays, expected_audit = plot.generate_payload(config, np)
    actual_rows = read_csv_rows()
    add(checks, "csv-exact-regeneration", actual_rows == expected_rows,
        rows=len(actual_rows), expectedRows=len(expected_rows))
    panel_a = [row for row in actual_rows if row["panel"] == "A"]
    add(checks, "panel-a-node-edge-encoding",
        len(panel_a) == 13
        and sum(row["record"].startswith("node-") for row in panel_a) == 6
        and sum(row["record"].startswith("edge-") for row in panel_a) == 7
        and sum(row["method"] == "literal-inequality" for row in panel_a) == 4
        and sum(row["method"] == "known-payment-estimate" for row in panel_a) == 3)
    add(checks, "results-status", results.get("status") == "PASS")
    add(checks, "results-source-binding",
        results.get("sourceBinding", {}).get("commit") == config["sourceBinding"]["commit"]
        and results.get("sourceBinding", {}).get("fileCount") == 7)
    add(checks, "formula-audit-exact-regeneration",
        results.get("formulaAudit") == expected_audit and expected_audit["checksPassed"] is True,
        audit=expected_audit)
    add(checks, "disjoint-clock-supports",
        expected_audit["maximumSimultaneouslyPositiveClocks"] == 1
        and max(abs(value - 1.0) for value in expected_audit["clockPeaks"])
        <= expected_audit["tolerances"]["clockPeakError"])
    add(checks, "exact-functional-values", expected_audit["exactFunctionalValues"] == {
        "H_hyb": 0.0, "H_fix": 1.0, "L_K": 1.0,
        "O_F_plus": 3.0, "M_K": 3.0, "H1_F": 6.0,
    })
    add(checks, "fixed-budget-ledger", expected_audit["panelDFixedN"] == 2
        and expected_audit["panelDFixedM"] == 4
        and expected_audit["panelDExpectedCheckpointRatios"] == [0.25, 0.5, 1.0, 2.0, 4.0])
    add(checks, "one-third-log-slope",
        expected_audit["panelDMaximumSlopeError"] <= expected_audit["tolerances"]["slopeError"],
        actual=expected_audit["panelDLogSlope"], expected=1.0 / 3.0)

    from PIL import Image, ImageChops, ImageOps, ImageStat
    from pypdf import PdfReader
    import pypdfium2 as pdfium

    width_mm = float(config["widthMillimetres"])
    height_mm = float(config["heightMillimetres"])
    master_expected = (
        int(width_mm / 25.4 * int(config["pngDpi"])),
        int(height_mm / 25.4 * int(config["pngDpi"])),
    )
    qa_expected = (
        int(width_mm / 25.4 * int(config["qaDpi"])),
        int(height_mm / 25.4 * int(config["qaDpi"])),
    )
    add(checks, "locked-pixel-contract", master_expected == (4204, 2740) and qa_expected == (2102, 1370),
        master=list(master_expected), qa=list(qa_expected))
    with Image.open(HERE / "figure.png") as opened:
        master_info = dict(opened.info)
        master = opened.convert("RGB")
    add(checks, "png-physical-pixel-size", master.size == master_expected,
        actual=list(master.size), expected=list(master_expected))
    reported_dpi = master_info.get("dpi", (0.0, 0.0))
    add(checks, "png-600-dpi-metadata",
        len(reported_dpi) == 2 and all(abs(float(value) - config["pngDpi"]) < 0.2 for value in reported_dpi),
        actual=list(reported_dpi))
    expected_final = master.resize(qa_expected, Image.Resampling.LANCZOS)
    with Image.open(HERE / "qa-final-size.png") as opened:
        final_size = opened.convert("RGB")
    add(checks, "qa-final-size-exact",
        final_size.size == qa_expected and ImageChops.difference(final_size, expected_final).getbbox() is None,
        pixels=list(final_size.size))
    expected_gray = ImageOps.grayscale(final_size).convert("RGB")
    with Image.open(HERE / "qa-grayscale.png") as opened:
        grayscale = opened.convert("RGB")
    add(checks, "qa-grayscale-exact",
        grayscale.size == qa_expected and ImageChops.difference(grayscale, expected_gray).getbbox() is None,
        standardDeviation=sum(ImageStat.Stat(grayscale).stddev) / 3.0)
    add(checks, "qa-grayscale-dynamic-range", sum(ImageStat.Stat(grayscale).stddev) / 3.0 > 15.0)

    reader = PdfReader(str(HERE / "figure.pdf"))
    add(checks, "pdf-one-page", len(reader.pages) == 1)
    page = reader.pages[0]
    expected_points = (width_mm / 25.4 * 72.0, height_mm / 25.4 * 72.0)
    actual_points = (float(page.mediabox.width), float(page.mediabox.height))
    add(checks, "pdf-physical-size",
        max(abs(actual_points[index] - expected_points[index]) for index in (0, 1)) < 0.1,
        actual=list(actual_points), expected=list(expected_points))
    font_audit = check_pdf_fonts(page)
    add(checks, "pdf-fonts-embedded", font_audit["allReferencedFontsEmbedded"] is True,
        fonts=font_audit["fonts"])
    extracted = page.extract_text() or ""
    add(checks, "pdf-scope-labels", all(label in extracted for label in REQUIRED_SCOPE_LABELS),
        labels=list(REQUIRED_SCOPE_LABELS))

    document = pdfium.PdfDocument(str(HERE / "figure.pdf"))
    pdf_page = document[0]
    width_points, _ = pdf_page.get_size()
    rerendered = pdf_page.render(scale=qa_expected[0] / float(width_points)).to_pil().convert("RGB")
    pdf_page.close()
    document.close()
    if rerendered.size != qa_expected:
        rerendered = rerendered.resize(qa_expected, Image.Resampling.LANCZOS)
    with Image.open(HERE / "qa-pdf.png") as opened:
        stored_pdf = opened.convert("RGB")
    add(checks, "qa-pdf-exact-rerender",
        stored_pdf.size == qa_expected and ImageChops.difference(stored_pdf, rerendered).getbbox() is None)
    difference = ImageChops.difference(stored_pdf, final_size)
    mean_difference = sum(ImageStat.Stat(difference).mean) / 3.0
    add(checks, "qa-pdf-vs-png", mean_difference < 15.0,
        meanAbsoluteRgbDifference=mean_difference, threshold=15.0)

    svg_root = ET.parse(HERE / "figure.svg").getroot()
    width_match = re.fullmatch(r"([0-9.]+)pt", svg_root.attrib.get("width", ""))
    height_match = re.fullmatch(r"([0-9.]+)pt", svg_root.attrib.get("height", ""))
    svg_size = bool(width_match and height_match)
    if width_match and height_match:
        svg_size = (
            abs(float(width_match.group(1)) - expected_points[0]) < 0.1
            and abs(float(height_match.group(1)) - expected_points[1]) < 0.1
        )
    add(checks, "svg-physical-size", svg_size,
        width=svg_root.attrib.get("width"), height=svg_root.attrib.get("height"))
    svg_text = (HERE / "figure.svg").read_text(encoding="utf-8")
    add(checks, "svg-scope-labels", all(label in svg_text for label in REQUIRED_SCOPE_LABELS),
        labels=list(REQUIRED_SCOPE_LABELS))
    add(checks, "renderer-artist-bounds", results["render"]["artistBoundsPass"] is True)

    progress = [json.loads(line) for line in (HERE / "progress.ndjson").read_text(encoding="utf-8").splitlines() if line]
    resources = [json.loads(line) for line in (HERE / "resource-log.ndjson").read_text(encoding="utf-8").splitlines() if line]
    add(checks, "progress-monitor",
        len(progress) >= 8 and all({"utc", "pid", "elapsedSeconds", "event"}.issubset(row) for row in progress),
        events=[row["event"] for row in progress])
    add(checks, "resource-monitor",
        len(resources) == 1 and {"utc", "pid", "wallSeconds", "cpuSeconds", "maximumResidentSetSizeRaw"}.issubset(resources[0]))
    add(checks, "environment-observation",
        environment["python"] == config["runtime"]["python"]
        and environment["matplotlibConfigPolicy"] == "system temporary directory removed after render")
    machine_failures = scan_machine_literals(set(SOURCE_FILES + RAW_FILES))
    add(checks, "machine-specific-literals-absent", not machine_failures, failures=machine_failures)
    add(checks, "owner-visual-qa-confirmed", confirm_visual_qa is True,
        assets=contract["ownerVisualReview"]["requiredAssets"])
    return checks, {
        "config": config,
        "contract": contract,
        "environment": environment,
        "fontAudit": font_audit,
        "meanDifference": mean_difference,
        "plot": plot,
        "repository": repository,
        "sourceBlobs": source_blobs,
    }


def figure_source_bindings(repository: Path, commit: str) -> list[dict[str, object]]:
    need(bool(HEX40.fullmatch(commit)), "figure source commit must be lowercase full 40-hex")
    git_text(repository, ["cat-file", "-e", commit + "^{commit}"])
    ancestor = subprocess.run(
        ["git", "-C", str(repository), "merge-base", "--is-ancestor", commit, "HEAD"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    need(ancestor.returncode == 0, "figure source commit is not an ancestor of HEAD")
    records: list[dict[str, object]] = []
    scoped: list[str] = []
    for name in SOURCE_FILES + RAW_FILES:
        path = (HERE / name).resolve()
        relative = path.relative_to(repository.resolve()).as_posix()
        payload = git_bytes(repository, ["cat-file", "blob", commit + ":" + relative])
        need(payload == path.read_bytes(), "committed Git blob differs from working file: " + name)
        records.append({
            "bytes": len(payload),
            "gitBlobObjectId": git_text(repository, ["rev-parse", commit + ":" + relative]),
            "path": name,
            "repositoryPath": relative,
            "sha256": sha256_bytes(payload),
        })
        scoped.append(relative)
    status = git_text(repository, ["status", "--porcelain", "--", *scoped])
    need(not status, "21-file source/raw scope is not clean: " + status)
    return records


def run_negative_tests(plot: Any, config: dict[str, Any]) -> dict[str, object]:
    drifted_runtime = json.loads(json.dumps(config))
    drifted_runtime["runtime"]["python"] = "0.0.0"
    runtime_failed = False
    try:
        plot.live_runtime_versions(drifted_runtime)
    except RuntimeError:
        runtime_failed = True
    need(runtime_failed, "runtime drift negative test failed open")

    inventory_failed = False
    try:
        assert_exact_inventory(set(EXPECTED_FILES) | {"unexpected.file"})
    except RuntimeError:
        inventory_failed = True
    need(inventory_failed, "inventory drift negative test failed open")

    import numpy as np
    drifted_formula = json.loads(json.dumps(config))
    drifted_formula["panelD"]["m"] = 5
    _rows, _arrays, audit = plot.generate_payload(drifted_formula, np)
    formula_failed = audit["checksPassed"] is False
    need(formula_failed, "formula-parameter drift negative test failed open")
    return {
        "formulaParameterDriftFailedClosed": formula_failed,
        "inventoryDriftFailedClosed": inventory_failed,
        "runtimeDriftFailedClosed": runtime_failed,
        "status": "PASS",
    }


def make_qa_report(checks: list[dict[str, object]], context: dict[str, Any],
                   generated_at: str, determinism: dict[str, object],
                   final_commit: str | None) -> str:
    audit = next(check["audit"] for check in checks if check["id"] == "formula-audit-exact-regeneration")
    resource_row = json.loads((HERE / "resource-log.ndjson").read_text(encoding="utf-8").splitlines()[0])
    seal = final_commit or PENDING_FIGURE_SOURCE_COMMIT
    return f"""# R0.74S fixed-deletion formal figure QA report

Status: **PASS**

- generated at UTC: `{generated_at}`
- frozen mathematical core: `{context['config']['sourceBinding']['commit']}`
- bound frozen evidence blobs: `7`
- figure-source seal: `{seal}`
- exact inventory: 25 files = 10 source + 11 raw/result + 4 metadata
- deterministic-core regeneration: PASS, `{determinism['fileCount']}` hashes unchanged
- validation checks: `{len(checks)}` passed
- Panel A records: `6` nodes + `7` edges
- maximum simultaneously positive triangular clocks: `{audit['maximumSimultaneouslyPositiveClocks']}`
- exact values: `0, 1, 1, 3, 3, 6`
- fixed Panel D parameters: `N={audit['panelDFixedN']}`, `M={audit['panelDFixedM']}`
- audited log--log slope: `{audit['panelDLogSlope']:.15f}`
- maximum slope error: `{audit['panelDMaximumSlopeError']:.3e}`
- PDF-versus-PNG mean absolute RGB difference: `{context['meanDifference']:.6f}`
- render wall time: `{resource_row['wallSeconds']:.6f}` seconds
- render CPU time: `{resource_row['cpuSeconds']:.6f}` seconds

## Visual QA

The 178 mm by 116 mm final-size image, grayscale conversion, and independent
PDF render were inspected.  The four panel titles, direct labels, markers,
axes, legends, scope badges, footer, and top-right research blossom are
legible.  No clipping or collision was accepted.  Line styles, marker shapes,
and tones preserve every comparison in grayscale.

## Scope

ANALYTIC SCHEMATIC · ABSTRACT CLOCK TEST · NOT PDE DATA · NOT DNS · NOT CLAY.
The package does not prove the open estimates (S.486)--(S.487), global
regularity, or the Navier--Stokes Millennium problem.
"""


def build_manifest(checks: list[dict[str, object]], context: dict[str, Any],
                   generated_at: str, figure_commit: str | None,
                   bindings: list[dict[str, object]]) -> dict[str, Any]:
    config = context["config"]
    contract = context["contract"]
    environment = context["environment"]
    resource_row = json.loads((HERE / "resource-log.ndjson").read_text(encoding="utf-8").splitlines()[0])
    data_names = (
        "source-data.csv", "results.json", "environment.json", "progress.ndjson",
        "resource-log.ndjson", "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png",
        "validation.json", "qa-report.md",
    )
    source_data = []
    for relative, lock in config["sourceBinding"]["files"].items():
        source_data.append({
            "bytes": len(context["sourceBlobs"][relative]),
            "extractionCommand": "git show " + config["sourceBinding"]["commit"] + ":" + relative,
            "fileName": relative,
            "gitBlobObjectId": lock["gitBlobObjectId"],
            "location": "Git core commit " + config["sourceBinding"]["commit"],
            "sha256": lock["sha256"],
        })
    return {
        "analyticalQuestion": contract["analyticalQuestion"],
        "caption": {"english": "caption.md"},
        "claimBoundary": contract["claimBoundary"],
        "computation": {
            "configuration": "config.json",
            "formalCommand": "python plot.py --render; python validate.py --confirm-visual-qa",
            "kind": "exact-formula-audit",
            "monitoring": {"enabled": True, "progressLog": "progress.ndjson", "resourceLog": "resource-log.ndjson"},
            "precision": "exact finite formulas with deterministic IEEE-754 binary64 rendering",
            "solver": "none",
            "wallTimeSeconds": resource_row["wallSeconds"],
        },
        "compute": {
            "cpu": f"{environment['machine']} / {environment['logicalCpuCount']} logical CPUs",
            "dgxUsed": False,
            "gpu": "not used",
            "host": "local workstation (hostname omitted)",
            "memoryGiB": environment["memoryBytes"] / 1073741824,
            "network": "not used",
            "operatingSystem": environment["operatingSystem"],
            "processes": 1,
            "threadsPerProcess": 1,
        },
        "createdAt": environment["createdAtUtc"],
        "data": [file_record(name, "r074s-figure-package-record-v1") for name in data_names],
        "deterministicCore": config["deterministicCore"],
        "environment": {
            "packages": environment["packages"],
            "packagesLock": "requirements.txt",
            "python": environment["python"],
            "runtime": {"provenance": "version-bound; absolute paths omitted"},
        },
        "figure": {
            "heightMillimetres": config["heightMillimetres"],
            "outputs": [
                file_record("figure.svg", "svg-journal-master"),
                file_record("figure.pdf", "one-page-pdf-journal-master"),
                {**file_record("figure.png", "png-journal-master"), "dpi": 600},
            ],
            "widthMillimetres": config["widthMillimetres"],
        },
        "figureId": FIGURE_ID,
        "figureSchemaVersion": FIGURE_SCHEMA_VERSION,
        "git": {
            "certificateCommit": config["sourceBinding"]["commit"],
            "dirtyAtCertifiedRun": False,
            "figureSourceCommit": figure_commit or PENDING_FIGURE_SOURCE_COMMIT,
            "figureSourceCommitBound": figure_commit is not None,
            "repository": config["repositoryUrl"],
            "sourceCommit": figure_commit or config["sourceBinding"]["commit"],
            "sourceEvidenceCommit": config["sourceBinding"]["commit"],
        },
        "inventory": {
            "count": 25,
            "files": sorted(EXPECTED_FILES),
            "metadataCount": 4,
            "rawAndResultCount": 11,
            "sourceCount": 10,
        },
        "notClay": True,
        "nondeterministic_observability": {
            "excludedFromDeterministicCore": True,
            "files": config["nondeterministicObservability"],
        },
        "publicationStatus": "staged",
        "qa": {
            "dataCrossChecked": True,
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "pdfInspected": True,
            "report": "qa-report.md",
            "scalesAndUnitsInspected": True,
            "status": "passed",
            "validationChecks": len(checks),
            "visualQaConfirmed": True,
        },
        "release": config["release"],
        "schemaVersion": SCHEMA_VERSION,
        "seal": {
            "figureSourceBindings": bindings,
            "figureSourceCommit": figure_commit or PENDING_FIGURE_SOURCE_COMMIT,
            "figureSourceCommitAssigned": figure_commit is not None,
            "requiresFigureSourceCommitFinalReseal": figure_commit is None,
            "state": "formal-figure-source-seal" if figure_commit else PENDING_FIGURE_SOURCE_COMMIT,
        },
        "sourceData": source_data,
        "status": "formal",
        "supportedClaim": contract["supportedClaim"],
    }


def verify_checksums() -> None:
    rows = (HERE / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    expected_names = sorted(EXPECTED_FILES - {"SHA256SUMS"})
    actual_names = []
    for row in rows:
        digest, name = row.split("  ", 1)
        actual_names.append(name)
        need((HERE / name).is_file() and sha256(HERE / name) == digest, "checksum drift: " + name)
    need(actual_names == expected_names, "SHA256SUMS inventory drift")


def write_seal(repository: Path, baseline: Path | None, confirm_visual_qa: bool,
               figure_commit: str | None) -> None:
    started = time.perf_counter()
    assert_sealable_inventory(actual_entries())
    checks, context = validate_content(repository, confirm_visual_qa)
    if figure_commit:
        previous = load_json(HERE / "validation.json")
        stored_hashes = previous.get("deterministicCoreHashes")
        need(stored_hashes == deterministic_hashes(context["config"]), "preseal deterministic core drift")
        determinism = {"fileCount": len(stored_hashes), "hashesMatched": True, "status": "PASS"}
        bindings = figure_source_bindings(repository, figure_commit)
        add(checks, "figure-source-commit-bound", len(bindings) == 21,
            commit=figure_commit, boundFiles=len(bindings))
    else:
        need(baseline is not None, "preseal requires --determinism-baseline")
        determinism = verify_baseline(baseline, context["config"])
        bindings = []
    add(checks, "deterministic-core-second-regeneration", True, **determinism)
    negatives = run_negative_tests(context["plot"], context["config"])
    add(checks, "negative-drift-tests", True, **negatives)
    add(checks, "exact-25-file-inventory", True, count=25)
    generated_at = dt.datetime.now(dt.timezone.utc).isoformat(timespec="microseconds")
    validation = {
        "checkCount": len(checks),
        "checks": checks,
        "deterministicCoreHashes": deterministic_hashes(context["config"]),
        "deterministicCoreRegeneration": determinism,
        "generatedAtUtc": generated_at,
        "inventory": {"count": 25, "files": sorted(EXPECTED_FILES), "status": "PASS"},
        "negativeTests": negatives,
        "passCount": len(checks),
        "pid": os.getpid(),
        "schemaVersion": "r074s-fixed-deletion-validation-v1",
        "sealState": "formal-figure-source-seal" if figure_commit else PENDING_FIGURE_SOURCE_COMMIT,
        "status": "PASS",
        "validationElapsedSeconds": time.perf_counter() - started,
        "visualQaConfirmed": True,
    }
    qa_report = make_qa_report(checks, context, generated_at, determinism, figure_commit)
    with tempfile.TemporaryDirectory(prefix="r074s-figure-seal-") as temporary:
        stage = Path(temporary)
        (stage / "validation.json").write_text(canonical(validation), encoding="utf-8", newline="\n")
        (stage / "qa-report.md").write_text(qa_report, encoding="utf-8", newline="\n")
        for name in ("validation.json", "qa-report.md"):
            os.replace(stage / name, HERE / name)
        manifest = build_manifest(checks, context, generated_at, figure_commit, bindings)
        (stage / "manifest.json").write_text(canonical(manifest), encoding="utf-8", newline="\n")
        os.replace(stage / "manifest.json", HERE / "manifest.json")
        checksum_rows = [f"{sha256(HERE / name)}  {name}" for name in sorted(EXPECTED_FILES - {"SHA256SUMS"})]
        (stage / "SHA256SUMS").write_text("\n".join(checksum_rows) + "\n", encoding="utf-8", newline="\n")
        os.replace(stage / "SHA256SUMS", HERE / "SHA256SUMS")
    assert_exact_inventory(actual_entries())
    verify_checksums()
    need(not scan_machine_literals(set(EXPECTED_FILES)), "machine-specific literal entered archive")
    print(f"PASS: {'final' if figure_commit else 'preseal'} exact 25-file archive with {len(checks)} checks")


def verify_only(repository: Path) -> None:
    assert_exact_inventory(actual_entries())
    verify_checksums()
    need(not scan_machine_literals(set(EXPECTED_FILES)), "machine-specific literal entered archive")
    config = load_json(HERE / "config.json")
    manifest = load_json(HERE / "manifest.json")
    validation = load_json(HERE / "validation.json")
    need(manifest["schemaVersion"] == SCHEMA_VERSION, "manifest schema drift")
    need(manifest["figureSchemaVersion"] == FIGURE_SCHEMA_VERSION, "figure schema drift")
    need(manifest["inventory"]["count"] == 25 and set(manifest["inventory"]["files"]) == EXPECTED_FILES,
         "manifest inventory drift")
    need(validation["inventory"]["count"] == 25 and set(validation["inventory"]["files"]) == EXPECTED_FILES,
         "validation inventory drift")
    need(validation["deterministicCoreHashes"] == deterministic_hashes(config), "deterministic core drift")
    plot = load_plot()
    plot.verify_source_binding(repository, config)
    seal = manifest["seal"]
    if seal["figureSourceCommitAssigned"]:
        reconstructed = figure_source_bindings(repository, seal["figureSourceCommit"])
        need(reconstructed == seal["figureSourceBindings"], "reconstructed figure Git binding drift")
    else:
        need(seal["figureSourceCommit"] == PENDING_FIGURE_SOURCE_COMMIT, "pending seal sentinel drift")
    print("PASS: exact inventory, checksums, core evidence, deterministic hashes, and seal verified")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deps", required=True, type=Path)
    parser.add_argument("--repository", type=Path, default=REPOSITORY_DEFAULT)
    parser.add_argument("--capture-deterministic-core", type=Path)
    parser.add_argument("--confirm-visual-qa", action="store_true")
    parser.add_argument("--determinism-baseline", type=Path)
    parser.add_argument("--figure-source-commit", default="")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    insert_dependencies(args.deps)
    modes = sum((bool(args.capture_deterministic_core), bool(args.confirm_visual_qa), bool(args.verify_only)))
    need(modes == 1, "choose exactly one of capture, confirm-visual-qa, or verify-only")
    repository = args.repository.expanduser().resolve()
    if args.capture_deterministic_core:
        capture_baseline(args.capture_deterministic_core)
    elif args.verify_only:
        need(not args.figure_source_commit, "verify-only uses the stored seal")
        verify_only(repository)
    else:
        write_seal(repository, args.determinism_baseline, True, args.figure_source_commit or None)


if __name__ == "__main__":
    main()
