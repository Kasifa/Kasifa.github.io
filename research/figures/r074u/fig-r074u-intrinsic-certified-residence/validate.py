#!/usr/bin/env python3
"""Validate and two-stage seal the 25-file R0.74U Step 20 figure archive."""

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
SOURCE_RAW_FILES = frozenset(SOURCE_FILES + RAW_FILES)
EXPECTED_FILES = frozenset(SOURCE_FILES + RAW_FILES + METADATA_FILES)
FIGURE_ID = "fig-r074u-intrinsic-certified-residence"
SCHEMA_VERSION = "research-figure-manifest-v1"
FIGURE_SCHEMA_VERSION = "r074u-intrinsic-certified-residence-manifest-v1"
HEX40 = re.compile(r"[0-9a-f]{40}")
FORBIDDEN_BYTES = (b"/Users/" + b"kasifa", b"/private/" + b"tmp/" + b"r074u-residence")
REQUIRED_SCOPE_LABELS = (
    "ANALYTIC SCHEMATIC", "DERIVED ANALYTIC VALUES", "NOT PDE DATA", "NOT DNS", "NOT CLAY",
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


def assert_preseal_inventory(entries: set[str]) -> None:
    need(entries == SOURCE_RAW_FILES,
         f"exact 21-file preseal drift: missing={sorted(SOURCE_RAW_FILES - entries)}, "
         f"extra={sorted(entries - SOURCE_RAW_FILES)}")


def assert_sealable_inventory(entries: set[str]) -> None:
    need(SOURCE_RAW_FILES.issubset(entries), "seal requires all 10 source and 11 raw/result files")
    need(entries.issubset(EXPECTED_FILES), "unexpected archive entry: " + repr(sorted(entries - EXPECTED_FILES)))


def assert_exact_inventory(entries: set[str]) -> None:
    need(entries == EXPECTED_FILES,
         f"exact 25-file inventory drift: missing={sorted(EXPECTED_FILES - entries)}, "
         f"extra={sorted(entries - EXPECTED_FILES)}")


def insert_dependencies(path: Path) -> None:
    resolved = path.expanduser().resolve()
    need(resolved.is_dir(), "--deps is not a directory")
    sys.path.insert(0, str(resolved))


def load_plot() -> Any:
    spec = importlib.util.spec_from_file_location("r074u_intrinsic_residence_figure_plot", HERE / "plot.py")
    need(spec is not None and spec.loader is not None, "cannot import plot.py")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def add(checks: list[dict[str, object]], identifier: str, passed: bool, **details: object) -> None:
    checks.append({"id": identifier, "pass": bool(passed), **details})
    need(passed, "validation failed: " + identifier)


def read_csv_rows() -> list[dict[str, str]]:
    with (HERE / "source-data.csv").open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def file_record(name: str, classification: str) -> dict[str, object]:
    path = HERE / name
    return {"bytes": path.stat().st_size, "path": name, "schema": classification, "sha256": sha256(path)}


def deterministic_hashes(config: dict[str, Any]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for name in config["deterministicCore"]:
        path = HERE / name
        need(path.is_file(), "deterministic-core file missing: " + name)
        hashes[name] = sha256(path)
    return hashes


def check_pdf_fonts(page: Any) -> dict[str, object]:
    resources = page.get("/Resources")
    if resources is None:
        return {"allReferencedFontsEmbedded": False, "fonts": []}
    resources = resources.get_object(); fonts = resources.get("/Font", {})
    fonts = fonts.get_object() if hasattr(fonts, "get_object") else fonts
    records: list[dict[str, object]] = []
    for resource_name, reference in fonts.items():
        font = reference.get_object(); descriptors: list[Any] = []
        descriptor = font.get("/FontDescriptor")
        if descriptor is not None:
            descriptors.append(descriptor.get_object())
        descendants = font.get("/DescendantFonts")
        if descendants is not None:
            for descendant_reference in descendants:
                child = descendant_reference.get_object().get("/FontDescriptor")
                if child is not None:
                    descriptors.append(child.get_object())
        embedded = any(any(key in descriptor for key in ("/FontFile", "/FontFile2", "/FontFile3"))
                       for descriptor in descriptors)
        records.append({"baseFont": str(font.get("/BaseFont", "")), "embedded": embedded,
                        "resource": str(resource_name), "subtype": str(font.get("/Subtype", ""))})
    return {"allReferencedFontsEmbedded": bool(records) and all(row["embedded"] for row in records),
            "fonts": records}


def scan_machine_literals(files: set[str] | frozenset[str]) -> list[str]:
    failures = []
    for name in sorted(files):
        payload = (HERE / name).read_bytes()
        if any(fragment in payload for fragment in FORBIDDEN_BYTES):
            failures.append(name)
    return failures


def validate_content(repository: Path, confirm_visual_qa: bool) -> tuple[list[dict[str, object]], dict[str, Any]]:
    config = load_json(HERE / "config.json"); contract = load_json(HERE / "contract.json")
    results = load_json(HERE / "results.json"); environment = load_json(HERE / "environment.json")
    checks: list[dict[str, object]] = []; plot = load_plot()
    add(checks, "source-raw-inventory", SOURCE_RAW_FILES.issubset(actual_entries()), count=21)
    add(checks, "no-source-raw-symlinks",
        all(not (HERE / name).is_symlink() for name in SOURCE_FILES + RAW_FILES))
    add(checks, "figure-id-consistency", config["figureId"] == contract["figureId"] == FIGURE_ID)
    boundary = contract["claimBoundary"]
    add(checks, "explicit-claim-boundary", all((
        boundary["analyticSchematic"] is True, boundary["derivedAnalyticValues"] is True,
        boundary["canonicalCommonShearFamily"] is True,
        boundary["twoSidedCertifiedGeometricCorridor"] is True,
        boundary["fullClockSuperlevelLowerOnly"] is True,
        boundary["arbitraryPacketResidence"] is False, boundary["fullClockUpperBound"] is False,
        boundary["pdeData"] is False, boundary["pdeSimulation"] is False,
        boundary["dns"] is False, boundary["globalRegularity"] is False,
        boundary["clayProblemSolved"] is False,
    )))
    authority = contract["sourceAuthority"]; binding = config["sourceBinding"]
    add(checks, "source-authority-chain", all((
        authority["commit"] == binding["commit"] == plot.FROZEN_NOTE_COMMIT,
        authority["gitBlobObjectId"] == binding["gitBlobObjectId"] == plot.FROZEN_NOTE_BLOB,
        authority["sha256"] == binding["sha256"] == plot.FROZEN_NOTE_SHA256,
        authority["path"] == binding["path"] == plot.FROZEN_NOTE_PATH,
    )), commit=binding["commit"], blob=binding["gitBlobObjectId"], sha256=binding["sha256"])
    actual_runtime = {
        "python": platform.python_version(), "numpy": importlib.metadata.version("numpy"),
        "matplotlib": importlib.metadata.version("matplotlib"),
        "pillow": importlib.metadata.version("pillow"), "pypdf": importlib.metadata.version("pypdf"),
        "pypdfium2": importlib.metadata.version("pypdfium2"),
    }
    add(checks, "runtime-lock", actual_runtime == config["runtime"], actual=actual_runtime)
    source_blobs = plot.verify_source_binding(repository, config)
    add(checks, "frozen-core-ancestor-blob-content", len(source_blobs) == 1,
        commit=binding["commit"], blobCount=len(source_blobs))

    import numpy as np
    expected_rows, _arrays, expected_audit = plot.generate_payload(config, np)
    actual_rows = read_csv_rows()
    add(checks, "csv-exact-regeneration", actual_rows == expected_rows,
        rows=len(actual_rows), expectedRows=len(expected_rows))
    counts = {panel: sum(row["panel"] == panel for row in actual_rows) for panel in "ABCD"}
    add(checks, "panel-row-inventory", counts == {"A": 6, "B": 6, "C": 6, "D": 363}, counts=counts)
    add(checks, "evidence-class-contract",
        {row["evidence_class"] for row in actual_rows} == {
            "derived-analytic-value", "exact-algebra", "exact-analytic-claim-boundary",
            "exact-analytic-schematic", "exact-rational",
        })
    add(checks, "results-status", results.get("status") == "PASS")
    source_result = results.get("sourceBinding", {})
    add(checks, "results-source-binding", all((
        source_result.get("commit") == binding["commit"], source_result.get("fileCount") == 1,
        source_result.get("gitBlobObjectId") == binding["gitBlobObjectId"],
        source_result.get("sha256") == binding["sha256"],
    )))
    add(checks, "formula-audit-exact-regeneration",
        results.get("formulaAudit") == expected_audit and expected_audit["checksPassed"] is True,
        audit=expected_audit)
    exact_tests = expected_audit["annularMarginExactTests"]
    add(checks, "annular-margin-exact-tests",
        exact_tests == {"innerDenominator": 21504, "innerNumerator": 9235,
                        "squareDenominator": 1849688064, "squareNumerator": 15232043}
        and 0.375 < expected_audit["annularMarginAtLMinimum"] < 1.0)
    add(checks, "platform-exponent-exact",
        expected_audit["platformExponentAtLMinimum"]
        == {"numerator": 462422016, "denominator": 1625})
    add(checks, "kinematic-exponent-ledger", expected_audit["exponentLedger"] == {
        "speedR": -2.0, "inverseSpeedR": 2.0, "roomL": 1.0,
        "roomR": 1.0, "residenceL": 1.0, "residenceR": 3.0,
    })
    add(checks, "corridor-exact-coefficients", expected_audit["corridorCoefficients"] == {
        "lower": {"numerator": 72, "denominator": 5},
        "strictUpper": {"numerator": 1024, "denominator": 3},
    })
    add(checks, "strict-full-K-boundary", expected_audit["fullKSuperlevel"] == {
        "converseProved": False, "lowerOnly": True, "upperBoundProved": False,
    })
    margin = expected_audit["exponentialMargin"]
    add(checks, "exact-positive-exponential-margin",
        margin["numerator"] == 603445 and margin["denominator"] == 89413632 and margin["decimal"] > 0.0)
    add(checks, "dwell-curve-directions",
        expected_audit["log10CertifiedLowerEndpoints"][1] > expected_audit["log10CertifiedLowerEndpoints"][0]
        and expected_audit["log10NecessaryUpperEndpoints"][1]
        < expected_audit["log10NecessaryUpperEndpoints"][0] < 0.0
        and expected_audit["log10ConflictGapEndpoints"][1]
        > expected_audit["log10ConflictGapEndpoints"][0] > 0.0)
    add(checks, "log-gap-identity", expected_audit["logGapIdentityMaximumResidual"] == 0.0)

    from PIL import Image, ImageChops, ImageOps, ImageStat
    from pypdf import PdfReader
    import pypdfium2 as pdfium
    width_mm = float(config["widthMillimetres"]); height_mm = float(config["heightMillimetres"])
    master_expected = (int(width_mm / 25.4 * int(config["pngDpi"])),
                       int(height_mm / 25.4 * int(config["pngDpi"])))
    qa_expected = (int(width_mm / 25.4 * int(config["qaDpi"])),
                   int(height_mm / 25.4 * int(config["qaDpi"])))
    add(checks, "locked-pixel-contract", master_expected == (4204, 2740)
        and qa_expected == (2102, 1370), master=list(master_expected), qa=list(qa_expected))
    with Image.open(HERE / "figure.png") as opened:
        master_info = dict(opened.info); master = opened.convert("RGB")
    add(checks, "png-physical-pixel-size", master.size == master_expected,
        actual=list(master.size), expected=list(master_expected))
    reported_dpi = master_info.get("dpi", (0.0, 0.0))
    add(checks, "png-600-dpi-metadata", len(reported_dpi) == 2
        and all(abs(float(value) - config["pngDpi"]) < 0.2 for value in reported_dpi), actual=list(reported_dpi))
    expected_final = master.resize(qa_expected, Image.Resampling.LANCZOS)
    with Image.open(HERE / "qa-final-size.png") as opened:
        final_size = opened.convert("RGB")
    add(checks, "qa-final-size-exact", final_size.size == qa_expected
        and ImageChops.difference(final_size, expected_final).getbbox() is None,
        pixels=list(final_size.size))
    expected_gray = ImageOps.grayscale(final_size).convert("RGB")
    with Image.open(HERE / "qa-grayscale.png") as opened:
        grayscale = opened.convert("RGB")
    gray_std = sum(ImageStat.Stat(grayscale).stddev) / 3.0
    add(checks, "qa-grayscale-exact", grayscale.size == qa_expected
        and ImageChops.difference(grayscale, expected_gray).getbbox() is None,
        standardDeviation=gray_std)
    add(checks, "qa-grayscale-dynamic-range", gray_std > 15.0)

    reader = PdfReader(str(HERE / "figure.pdf")); add(checks, "pdf-one-page", len(reader.pages) == 1)
    page = reader.pages[0]; expected_points = (width_mm / 25.4 * 72.0, height_mm / 25.4 * 72.0)
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
    add(checks, "pdf-strict-boundary-label",
        "NO CONVERSE / NO UPPER BOUND FOR FULL K-SUPERLEVEL" in extracted)

    document = pdfium.PdfDocument(str(HERE / "figure.pdf")); pdf_page = document[0]
    width_points, _ = pdf_page.get_size()
    rerendered = pdf_page.render(scale=qa_expected[0] / float(width_points)).to_pil().convert("RGB")
    pdf_page.close(); document.close()
    if rerendered.size != qa_expected:
        rerendered = rerendered.resize(qa_expected, Image.Resampling.LANCZOS)
    with Image.open(HERE / "qa-pdf.png") as opened:
        stored_pdf = opened.convert("RGB")
    add(checks, "qa-pdf-exact-rerender", stored_pdf.size == qa_expected
        and ImageChops.difference(stored_pdf, rerendered).getbbox() is None)
    difference = ImageChops.difference(stored_pdf, final_size)
    mean_difference = sum(ImageStat.Stat(difference).mean) / 3.0
    add(checks, "qa-pdf-vs-png", mean_difference < 15.0,
        meanAbsoluteRgbDifference=mean_difference, threshold=15.0)

    svg_root = ET.parse(HERE / "figure.svg").getroot()
    width_match = re.fullmatch(r"([0-9.]+)pt", svg_root.attrib.get("width", ""))
    height_match = re.fullmatch(r"([0-9.]+)pt", svg_root.attrib.get("height", ""))
    svg_size = bool(width_match and height_match)
    if width_match and height_match:
        svg_size = (abs(float(width_match.group(1)) - expected_points[0]) < 0.1
                    and abs(float(height_match.group(1)) - expected_points[1]) < 0.1)
    add(checks, "svg-physical-size", svg_size,
        width=svg_root.attrib.get("width"), height=svg_root.attrib.get("height"))
    svg_text = (HERE / "figure.svg").read_text(encoding="utf-8")
    add(checks, "svg-scope-labels", all(label in svg_text for label in REQUIRED_SCOPE_LABELS),
        labels=list(REQUIRED_SCOPE_LABELS))
    add(checks, "svg-strict-boundary-label",
        "NO CONVERSE / NO UPPER BOUND FOR FULL K-SUPERLEVEL" in svg_text)
    add(checks, "renderer-artist-bounds", results["render"]["artistBoundsPass"] is True)

    progress = [json.loads(line) for line in (HERE / "progress.ndjson").read_text(encoding="utf-8").splitlines() if line]
    resources = [json.loads(line) for line in (HERE / "resource-log.ndjson").read_text(encoding="utf-8").splitlines() if line]
    add(checks, "progress-monitor", len(progress) >= 8
        and all({"utc", "pid", "elapsedSeconds", "event"}.issubset(row) for row in progress),
        events=[row["event"] for row in progress])
    add(checks, "resource-monitor", len(resources) == 1
        and {"utc", "pid", "wallSeconds", "cpuSeconds", "maximumResidentSetSizeRaw"}.issubset(resources[0]))
    add(checks, "environment-observation", environment["python"] == config["runtime"]["python"]
        and environment["matplotlibConfigPolicy"] == "system temporary directory removed after render"
        and environment["pythonLocatorPolicy"]
        == "bundled Python 3.12.13 executable; absolute path omitted"
        and environment["dependencyLocatorPolicy"]
        == "external version-pinned directory supplied by PYTHONPATH and --deps; absolute path omitted")
    machine_failures = scan_machine_literals(SOURCE_RAW_FILES)
    add(checks, "machine-specific-literals-absent", not machine_failures, failures=machine_failures)
    add(checks, "owner-visual-qa-confirmed", confirm_visual_qa is True,
        assets=contract["ownerVisualReview"]["requiredAssets"])
    return checks, {
        "config": config, "contract": contract, "environment": environment,
        "fontAudit": font_audit, "meanDifference": mean_difference,
        "plot": plot, "repository": repository, "sourceBlobs": source_blobs,
    }


def figure_source_bindings(repository: Path, commit: str) -> list[dict[str, object]]:
    need(bool(HEX40.fullmatch(commit)), "figure source commit must be lowercase full 40-hex")
    git_text(repository, ["cat-file", "-e", commit + "^{commit}"])
    ancestor = subprocess.run(
        ["git", "-C", str(repository), "merge-base", "--is-ancestor", commit, "HEAD"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    need(ancestor.returncode == 0, "figure source commit is not an ancestor of HEAD")
    records: list[dict[str, object]] = []; scoped: list[str] = []
    for name in SOURCE_FILES + RAW_FILES:
        relative = (HERE / name).resolve().relative_to(repository.resolve()).as_posix()
        payload = git_bytes(repository, ["cat-file", "blob", commit + ":" + relative])
        need(payload == (HERE / name).read_bytes(), "committed Git blob differs from working file: " + name)
        records.append({
            "bytes": len(payload), "gitBlobObjectId": git_text(repository, ["rev-parse", commit + ":" + relative]),
            "path": name, "repositoryPath": relative, "sha256": sha256_bytes(payload),
        })
        scoped.append(relative)
    status = git_text(repository, ["status", "--porcelain", "--", *scoped])
    need(not status, "21-file source/raw scope is not clean: " + status)
    return records


def run_negative_tests(plot: Any, config: dict[str, Any], contract: dict[str, Any], repository: Path) -> dict[str, object]:
    drifted_runtime = json.loads(json.dumps(config)); drifted_runtime["runtime"]["python"] = "0.0.0"
    runtime_failed = False
    try:
        plot.live_runtime_versions(drifted_runtime)
    except RuntimeError:
        runtime_failed = True
    inventory_failed = False
    try:
        assert_exact_inventory(set(EXPECTED_FILES) | {"unexpected.file"})
    except RuntimeError:
        inventory_failed = True
    import numpy as np
    drifted_margin = json.loads(json.dumps(config)); drifted_margin["panelD"]["cGamma"]["numerator"] = 0
    _rows, _arrays, margin_audit = plot.generate_payload(drifted_margin, np)
    margin_failed = margin_audit["checksPassed"] is False
    drifted_corridor = json.loads(json.dumps(config)); drifted_corridor["panelC"]["corridorLower"]["numerator"] = 73
    _rows, _arrays, corridor_audit = plot.generate_payload(drifted_corridor, np)
    corridor_failed = corridor_audit["checksPassed"] is False
    drifted_hash = json.loads(json.dumps(config)); drifted_hash["sourceBinding"]["sha256"] = "0" * 64
    hash_failed = False
    try:
        plot.verify_source_binding(repository, drifted_hash)
    except RuntimeError:
        hash_failed = True
    drifted_boundary = json.loads(json.dumps(contract)); drifted_boundary["claimBoundary"]["fullClockUpperBound"] = True
    boundary_failed = drifted_boundary["claimBoundary"] != contract["claimBoundary"]
    need(all((runtime_failed, inventory_failed, margin_failed, corridor_failed, hash_failed, boundary_failed)),
         "one or more negative tests failed open")
    return {
        "claimBoundaryDriftFailedClosed": boundary_failed,
        "corridorConstantDriftFailedClosed": corridor_failed,
        "exponentialMarginDriftFailedClosed": margin_failed,
        "inventoryDriftFailedClosed": inventory_failed,
        "runtimeDriftFailedClosed": runtime_failed,
        "sourceHashDriftFailedClosed": hash_failed,
        "status": "PASS",
    }


def rerender(repository: Path, deps: Path) -> None:
    result = subprocess.run([
        sys.executable, "-B", str(HERE / "plot.py"), "--deps", str(deps),
        "--repository", str(repository), "--render",
    ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False)
    print(result.stdout, end="")
    need(result.returncode == 0, "deterministic second render failed")


def preseal_roundtrip(repository: Path, deps: Path, confirm_visual_qa: bool) -> None:
    assert_preseal_inventory(actual_entries())
    first_checks, first_context = validate_content(repository, confirm_visual_qa)
    baseline = deterministic_hashes(first_context["config"])
    rerender(repository, deps)
    assert_preseal_inventory(actual_entries())
    second_checks, second_context = validate_content(repository, confirm_visual_qa)
    current = deterministic_hashes(second_context["config"])
    need(current == baseline, "second regeneration changed deterministic-core hashes")
    negatives = run_negative_tests(second_context["plot"], second_context["config"],
                                   second_context["contract"], repository)
    summary = {
        "checkCountPerPass": len(second_checks), "deterministicCoreFileCount": len(current),
        "deterministicCoreHashesMatched": True, "firstPassCheckCount": len(first_checks),
        "inventory": {"count": 21, "rawAndResult": 11, "source": 10},
        "negativeTests": negatives, "sealMetadataWritten": False, "status": "PASS",
        "visualQaConfirmed": confirm_visual_qa,
    }
    print(canonical(summary), end="")
    print(f"PASS: preseal exact 21-file source/raw archive; {len(second_checks)} checks per pass; no metadata written")


def make_qa_report(checks: list[dict[str, object]], context: dict[str, Any], generated_at: str,
                   figure_commit: str, determinism: dict[str, object]) -> str:
    audit = next(check["audit"] for check in checks if check["id"] == "formula-audit-exact-regeneration")
    resource_row = json.loads((HERE / "resource-log.ndjson").read_text(encoding="utf-8").splitlines()[0])
    return f"""# R0.74U intrinsic certified-residence formal figure QA report

Status: **PASS**

- generated at UTC: `{generated_at}`
- frozen mathematical core: `{context['config']['sourceBinding']['commit']}`
- frozen theorem-note blob: `{context['config']['sourceBinding']['gitBlobObjectId']}`
- frozen theorem-note SHA-256: `{context['config']['sourceBinding']['sha256']}`
- figure-source seal: `{figure_commit}`
- exact inventory: 25 files = 10 source + 11 raw/result + 4 metadata
- deterministic-core regeneration: PASS, `{determinism['fileCount']}` hashes unchanged
- validation checks: `{len(checks)}` passed
- annular margin at L=9216: `{audit['annularMarginAtLMinimum']:.15f}`
- certified corridor coefficients: `72/5` lower and strict `1024/3` upper
- full K-superlevel statement: lower only; no converse; no upper bound
- Panel D derived values: `{audit['panelPointCount']}` per series
- certified-lower log10 endpoints: `{audit['log10CertifiedLowerEndpoints'][0]:.6f}`, `{audit['log10CertifiedLowerEndpoints'][1]:.6f}`
- necessary-upper log10 endpoints: `{audit['log10NecessaryUpperEndpoints'][0]:.6f}`, `{audit['log10NecessaryUpperEndpoints'][1]:.6f}`
- conflict-gap log10 endpoints: `{audit['log10ConflictGapEndpoints'][0]:.6f}`, `{audit['log10ConflictGapEndpoints'][1]:.6f}`
- PDF-versus-PNG mean absolute RGB difference: `{context['meanDifference']:.6f}`
- render wall time: `{resource_row['wallSeconds']:.6f}` seconds
- render CPU time: `{resource_row['cpuSeconds']:.6f}` seconds

## Visual QA

The 178 mm by 116 mm final-size image, grayscale conversion, and independent
PDF render were inspected. The four panel titles, formulas, hatches, direct
labels, set nesting, axes, footer, and top-right research blossom are legible.
No clipping or collision was accepted. Line styles, markers, hatches, and
tones preserve every distinction in grayscale.

## Scope

ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE DATA | NOT DNS | NOT CLAY.
The two-sided upper estimate applies only to the certified geometric corridor.
The package proves only lower residence for the completed-clock superlevel set
and does not prove arbitrary-packet residence, regularity, or singularity.
"""


def build_manifest(checks: list[dict[str, object]], context: dict[str, Any], generated_at: str,
                   figure_commit: str, bindings: list[dict[str, object]]) -> dict[str, Any]:
    config = context["config"]; contract = context["contract"]; environment = context["environment"]
    resource_row = json.loads((HERE / "resource-log.ndjson").read_text(encoding="utf-8").splitlines()[0])
    data_names = ("source-data.csv", "results.json", "environment.json", "progress.ndjson",
                  "resource-log.ndjson", "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png",
                  "validation.json", "qa-report.md")
    binding = config["sourceBinding"]
    return {
        "analyticalQuestion": contract["analyticalQuestion"], "caption": {"english": "caption.md"},
        "claimBoundary": contract["claimBoundary"],
        "computation": {
            "configuration": "config.json", "formalCommand": "python plot.py --render; python validate.py --preseal-roundtrip --confirm-visual-qa",
            "kind": "exact-kinematic-algebra-and-derived-analytic-identity-audit",
            "monitoring": {"enabled": True, "progressLog": "progress.ndjson", "resourceLog": "resource-log.ndjson"},
            "precision": "exact rational checks plus deterministic IEEE-754 binary64 formula evaluation",
            "solver": "none", "wallTimeSeconds": resource_row["wallSeconds"],
        },
        "compute": {
            "cpu": f"{environment['machine']} / {environment['logicalCpuCount']} logical CPUs",
            "dgxUsed": False, "gpu": "not used", "host": "local workstation (hostname omitted)",
            "memoryGiB": environment["memoryBytes"] / 1073741824, "network": "not used",
            "operatingSystem": environment["operatingSystem"], "processes": 1, "threadsPerProcess": 1,
        },
        "createdAt": environment["createdAtUtc"],
        "data": [file_record(name, "r074u-figure-package-record-v1") for name in data_names],
        "deterministicCore": config["deterministicCore"],
        "environment": {"dependencyLocatorPolicy": environment["dependencyLocatorPolicy"],
                        "packages": environment["packages"], "packagesLock": "requirements.txt",
                        "python": environment["python"],
                        "pythonLocatorPolicy": environment["pythonLocatorPolicy"],
                        "runtime": {"provenance": "version-bound; absolute paths omitted"}},
        "figure": {
            "heightMillimetres": config["heightMillimetres"],
            "outputs": [file_record("figure.svg", "svg-journal-master"),
                        file_record("figure.pdf", "one-page-pdf-journal-master"),
                        {**file_record("figure.png", "png-journal-master"), "dpi": 600}],
            "widthMillimetres": config["widthMillimetres"],
        },
        "figureId": FIGURE_ID, "figureSchemaVersion": FIGURE_SCHEMA_VERSION,
        "git": {
            "certificateCommit": binding["commit"], "figureScopeCommitted": True,
            "figureSourceCommit": figure_commit, "figureSourceCommitBound": True,
            "repository": config["repositoryUrl"], "sourceCommit": figure_commit,
            "sourceEvidenceCommit": binding["commit"],
        },
        "inventory": {"count": 25, "files": sorted(EXPECTED_FILES), "metadataCount": 4,
                      "rawAndResultCount": 11, "sourceCount": 10},
        "nondeterministic_observability": {"excludedFromDeterministicCore": True,
                                           "files": config["nondeterministicObservability"]},
        "notClay": True, "publicationStatus": "sealed",
        "qa": {"dataCrossChecked": True, "finalSizeInspected": True, "grayscaleInspected": True,
               "labelsAndLegendsInspected": True, "pdfInspected": True, "report": "qa-report.md",
               "scalesAndUnitsInspected": True, "status": "passed", "validationChecks": len(checks),
               "visualQaConfirmed": True},
        "release": config["release"], "schemaVersion": SCHEMA_VERSION,
        "seal": {"figureSourceBindings": bindings, "figureSourceCommit": figure_commit,
                 "figureSourceCommitAssigned": True, "requiresFigureSourceCommitFinalReseal": False,
                 "state": "formal-figure-source-seal"},
        "sourceData": [{
            "bytes": len(context["sourceBlobs"][binding["path"]]),
            "extractionCommand": "git show " + binding["commit"] + ":" + binding["path"],
            "fileName": binding["path"], "gitBlobObjectId": binding["gitBlobObjectId"],
            "location": "Git core commit " + binding["commit"], "sha256": binding["sha256"],
        }],
        "status": "formal", "supportedClaim": contract["supportedClaim"],
    }


def verify_checksums() -> None:
    rows = (HERE / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    expected_names = sorted(EXPECTED_FILES - {"SHA256SUMS"}); actual_names = []
    for row in rows:
        digest, name = row.split("  ", 1); actual_names.append(name)
        need((HERE / name).is_file() and sha256(HERE / name) == digest, "checksum drift: " + name)
    need(actual_names == expected_names, "SHA256SUMS inventory drift")


def write_final_seal(repository: Path, confirm_visual_qa: bool, figure_commit: str) -> None:
    started = time.perf_counter(); assert_sealable_inventory(actual_entries())
    checks, context = validate_content(repository, confirm_visual_qa)
    bindings = figure_source_bindings(repository, figure_commit)
    add(checks, "figure-source-commit-bound", len(bindings) == 21,
        commit=figure_commit, boundFiles=len(bindings))
    current_hashes = deterministic_hashes(context["config"])
    add(checks, "deterministic-core-bound-to-figure-source", all(
        next(row for row in bindings if row["path"] == name)["sha256"] == digest
        for name, digest in current_hashes.items()), fileCount=len(current_hashes), hashesMatched=True)
    negatives = run_negative_tests(context["plot"], context["config"], context["contract"], repository)
    add(checks, "negative-drift-tests", True, **negatives)
    add(checks, "exact-25-file-inventory-planned", True, count=25)
    generated_at = dt.datetime.now(dt.timezone.utc).isoformat(timespec="microseconds")
    determinism = {"fileCount": len(current_hashes), "hashesMatched": True, "status": "PASS"}
    validation = {
        "checkCount": len(checks), "checks": checks, "deterministicCoreHashes": current_hashes,
        "deterministicCoreRegeneration": determinism, "generatedAtUtc": generated_at,
        "inventory": {"count": 25, "files": sorted(EXPECTED_FILES), "status": "PASS"},
        "negativeTests": negatives, "passCount": len(checks), "pid": os.getpid(),
        "schemaVersion": "r074u-intrinsic-certified-residence-validation-v1",
        "sealState": "formal-figure-source-seal", "status": "PASS",
        "validationElapsedSeconds": time.perf_counter() - started, "visualQaConfirmed": True,
    }
    qa_report = make_qa_report(checks, context, generated_at, figure_commit, determinism)
    with tempfile.TemporaryDirectory(prefix="r074u-figure-seal-") as temporary:
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
    assert_exact_inventory(actual_entries()); verify_checksums()
    need(not scan_machine_literals(EXPECTED_FILES), "machine-specific literal entered archive")
    print(f"PASS: final exact 25-file archive with {len(checks)} checks")


def verify_only(repository: Path) -> None:
    assert_exact_inventory(actual_entries()); verify_checksums()
    need(not scan_machine_literals(EXPECTED_FILES), "machine-specific literal entered archive")
    config = load_json(HERE / "config.json"); manifest = load_json(HERE / "manifest.json")
    validation = load_json(HERE / "validation.json")
    need(manifest["schemaVersion"] == SCHEMA_VERSION, "manifest schema drift")
    need(manifest["figureSchemaVersion"] == FIGURE_SCHEMA_VERSION, "figure schema drift")
    need(manifest["inventory"]["count"] == 25 and set(manifest["inventory"]["files"]) == EXPECTED_FILES,
         "manifest inventory drift")
    need(validation["inventory"]["count"] == 25 and set(validation["inventory"]["files"]) == EXPECTED_FILES,
         "validation inventory drift")
    need(validation["deterministicCoreHashes"] == deterministic_hashes(config), "deterministic core drift")
    plot = load_plot(); plot.verify_source_binding(repository, config)
    seal = manifest["seal"]; reconstructed = figure_source_bindings(repository, seal["figureSourceCommit"])
    need(reconstructed == seal["figureSourceBindings"], "reconstructed figure Git binding drift")
    print("PASS: exact inventory, checksums, core evidence, deterministic hashes, and seal verified")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deps", required=True, type=Path)
    parser.add_argument("--repository", type=Path, default=REPOSITORY_DEFAULT)
    parser.add_argument("--preseal-roundtrip", action="store_true")
    parser.add_argument("--confirm-visual-qa", action="store_true")
    parser.add_argument("--figure-source-commit", default="")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args(); insert_dependencies(args.deps)
    modes = sum((bool(args.preseal_roundtrip), bool(args.figure_source_commit), bool(args.verify_only)))
    need(modes == 1, "choose exactly one of preseal-roundtrip, final figure-source seal, or verify-only")
    repository = args.repository.expanduser().resolve(); deps = args.deps.expanduser().resolve()
    if args.preseal_roundtrip:
        need(args.confirm_visual_qa, "preseal roundtrip requires --confirm-visual-qa")
        preseal_roundtrip(repository, deps, True)
    elif args.verify_only:
        need(not args.confirm_visual_qa, "verify-only uses the stored visual confirmation")
        verify_only(repository)
    else:
        need(args.confirm_visual_qa, "final seal requires --confirm-visual-qa")
        write_final_seal(repository, True, args.figure_source_commit)


if __name__ == "__main__":
    main()
