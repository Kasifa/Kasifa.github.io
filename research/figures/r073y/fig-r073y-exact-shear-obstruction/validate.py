#!/usr/bin/env python3
"""Validate and seal the formal 25-file R0.73Y figure archive."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import importlib.metadata
import importlib.util
import json
import math
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
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
EXPECTED_PACKAGES = {
    "numpy": "2.5.2", "matplotlib": "3.10.6", "pillow": "12.3.0",
    "pypdf": "6.10.0", "pypdfium2": "5.13.0",
}
FORBIDDEN_BYTE_SEQUENCES = (
    b"/private/" + b"tmp/" + b"r073y-",
    b"/Users/" + b"kasifa",
)
FIGURE_ID = "fig-r073y-exact-shear-obstruction"
SCHEMA_VERSION = "research-figure-manifest-v1"
FIGURE_SCHEMA_VERSION = "r073y-exact-shear-obstruction-manifest-v1"
PENDING_FIGURE_SOURCE_COMMIT = "PENDING_FIGURE_SOURCE_COMMIT"
HEX40 = re.compile(r"[0-9a-f]{40}")


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
    result = subprocess.run(["git", "-C", str(repository), *args], check=False,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    need(result.returncode == 0, "git failed: " + result.stderr.decode("utf-8", "replace").strip())
    return result.stdout


def git_text(repository: Path, args: list[str]) -> str:
    return git_bytes(repository, args).decode("utf-8").strip()


def verify_source_evidence(repository: Path, config: dict[str, Any]) -> dict[str, bytes]:
    commit = config["sourceBinding"]["commit"]
    need(bool(HEX40.fullmatch(commit)), "invalid frozen source-evidence commit")
    git_text(repository, ["cat-file", "-e", commit + "^{commit}"])
    blobs: dict[str, bytes] = {}
    for relative, expected_hash in config["sourceBinding"]["files"].items():
        payload = git_bytes(repository, ["cat-file", "blob", commit + ":" + relative])
        need(sha256_bytes(payload) == expected_hash, "frozen source-evidence byte drift: " + relative)
        blobs[relative] = payload
    return blobs


def figure_source_bindings(repository: Path, commit: str) -> list[dict[str, object]]:
    need(bool(HEX40.fullmatch(commit)), "figure source commit must be a real lowercase full 40-hex commit")
    git_text(repository, ["cat-file", "-e", commit + "^{commit}"])
    bindings: list[dict[str, object]] = []
    scoped: list[str] = []
    for name in SOURCE_FILES + RAW_FILES:
        path = (HERE / name).resolve()
        try:
            relative = path.relative_to(repository.resolve()).as_posix()
        except ValueError as error:
            raise RuntimeError("final reseal package must be inside --repository") from error
        payload = git_bytes(repository, ["cat-file", "blob", commit + ":" + relative])
        need(payload == path.read_bytes(), "committed Git blob is not byte-identical: " + name)
        oid = git_text(repository, ["rev-parse", commit + ":" + relative])
        bindings.append({"path": name, "repositoryPath": relative, "gitBlobObjectId": oid,
                         "bytes": len(payload), "sha256": sha256_bytes(payload)})
        scoped.append(relative)
    status = git_text(repository, ["status", "--porcelain", "--", *scoped])
    need(not status, "21-file figure source/raw scope is not clean: " + status)
    return bindings


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="microseconds")


def actual_entries() -> set[str]:
    return {path.name for path in HERE.iterdir()}


def assert_exact_inventory(entries: set[str]) -> None:
    need(entries == EXPECTED_FILES, f"exact 25-file inventory drift: missing={sorted(EXPECTED_FILES - entries)}, extra={sorted(entries - EXPECTED_FILES)}")


def assert_sealable_inventory(entries: set[str]) -> None:
    required = set(SOURCE_FILES + RAW_FILES)
    need(required.issubset(entries), "seal requires all 10 source and 11 raw/result files")
    need(entries.issubset(EXPECTED_FILES), "unexpected archive entry before seal")


def load_plot() -> Any:
    spec = importlib.util.spec_from_file_location("r073y_exact_shear_plot_validation", HERE / "plot.py")
    need(spec is not None and spec.loader is not None, "cannot import plot.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def add(checks: list[dict[str, object]], identifier: str, passed: bool, **details: object) -> None:
    checks.append({"id": identifier, "pass": bool(passed), **details})
    need(passed, "validation failed: " + identifier)


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
        embedded = any(any(key in descriptor for key in ("/FontFile", "/FontFile2", "/FontFile3")) for descriptor in descriptors)
        records.append({"baseFont": str(font.get("/BaseFont", "")), "embedded": embedded, "resource": str(resource_name), "subtype": str(font.get("/Subtype", ""))})
    return {"allReferencedFontsEmbedded": bool(records) and all(bool(record["embedded"]) for record in records), "fonts": records}


def read_csv_rows() -> list[dict[str, str]]:
    with (HERE / "source-data.csv").open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def file_record(name: str, classification: str) -> dict[str, object]:
    path = HERE / name
    return {"bytes": path.stat().st_size, "schema": classification, "path": name, "sha256": sha256(path)}


def deterministic_hashes(config: dict[str, Any]) -> dict[str, str]:
    records: dict[str, str] = {}
    for name in config["deterministicCore"]:
        path = HERE / name
        need(path.is_file(), "deterministic-core file missing: " + name)
        records[name] = sha256(path)
    return records


def capture_baseline(path: Path) -> None:
    config = load_json(HERE / "config.json")
    resolved = path.expanduser().resolve()
    need(resolved != HERE and HERE not in resolved.parents, "determinism baseline must be outside archive")
    payload = {"schema": "r073y-deterministic-core-baseline-v2", "hashes": deterministic_hashes(config)}
    resolved.write_text(canonical(payload), encoding="utf-8", newline="\n")
    print(f"PASS: captured {len(payload['hashes'])} deterministic-core hashes")


def verify_determinism_baseline(path: Path, config: dict[str, Any]) -> dict[str, object]:
    payload = load_json(path.expanduser().resolve())
    current = deterministic_hashes(config)
    baseline = payload.get("hashes")
    need(isinstance(baseline, dict) and baseline == current, "second deterministic-core regeneration changed one or more hashes")
    return {"fileCount": len(current), "hashesMatched": True, "status": "PASS"}


def scan_machine_specific_literals(files: set[str]) -> list[str]:
    failures: list[str] = []
    for name in sorted(files):
        payload = (HERE / name).read_bytes()
        if any(fragment in payload for fragment in FORBIDDEN_BYTE_SEQUENCES):
            failures.append(name)
    return failures


def run_negative_tests(plot: Any, config: dict[str, Any], source_blobs: dict[str, bytes]) -> dict[str, object]:
    runtime_failed_closed = False
    try:
        plot.assert_runtime_contract("3.12.12", "2.5.2", "3.10.6")
    except RuntimeError:
        runtime_failed_closed = True
    need(runtime_failed_closed, "runtime drift negative test failed open")

    source_failed_closed = False
    with tempfile.TemporaryDirectory(prefix="source-drift-test-") as temporary:
        fake_root = Path(temporary)
        for relative in config["sourceBinding"]["files"]:
            target = fake_root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source_blobs[relative])
        theorem = fake_root / "research/r073y_exact_shear_no_go.md"
        theorem.write_bytes(theorem.read_bytes() + b"\nsource drift test\n")
        try:
            plot.verify_source_files(fake_root, config)
        except RuntimeError:
            source_failed_closed = True
    need(source_failed_closed, "source byte drift negative test failed open")

    inventory_failed_closed = False
    try:
        assert_exact_inventory(set(EXPECTED_FILES) | {"unexpected-drift.file"})
    except RuntimeError:
        inventory_failed_closed = True
    need(inventory_failed_closed, "inventory drift negative test failed open")
    return {
        "inventoryDriftFailedClosed": inventory_failed_closed,
        "runtimeDriftFailedClosed": runtime_failed_closed,
        "sourceByteDriftFailedClosed": source_failed_closed,
        "status": "PASS",
    }


def validate_content(repository: Path, confirm_visual_qa: bool) -> tuple[list[dict[str, object]], dict[str, Any]]:
    checks: list[dict[str, object]] = []
    config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    results = load_json(HERE / "results.json")
    environment = load_json(HERE / "environment.json")
    plot = load_plot()

    versions = {name: importlib.metadata.version(name) for name in EXPECTED_PACKAGES}
    add(checks, "python-version", platform.python_version() == config["runtime"]["python"], actual=platform.python_version())
    add(checks, "pinned-package-versions", versions == EXPECTED_PACKAGES, actual=versions, expected=EXPECTED_PACKAGES)
    plot.assert_runtime_contract(platform.python_version(), versions["numpy"], versions["matplotlib"])
    requirements = (HERE / "requirements.txt").read_text(encoding="utf-8").splitlines()
    expected_requirements = [f"{name}=={version}" for name, version in EXPECTED_PACKAGES.items()]
    add(checks, "requirements-exact-pins", requirements == expected_requirements, actual=requirements)

    source_blobs = verify_source_evidence(repository, config)
    add(checks, "frozen-source-binding", True, commit=config["sourceBinding"]["commit"], files=config["sourceBinding"]["files"])

    contract_inventory = contract["inventory"]
    add(checks, "contract-source-inventory", tuple(contract_inventory["source"]) == SOURCE_FILES, count=len(SOURCE_FILES))
    add(checks, "contract-raw-inventory", tuple(contract_inventory["rawAndResult"]) == RAW_FILES, count=len(RAW_FILES))
    add(checks, "contract-metadata-inventory", tuple(contract_inventory["metadata"]) == METADATA_FILES, count=len(METADATA_FILES))
    deterministic = set(config["deterministicCore"])
    nondeterministic = set(config["nondeterministicObservability"])
    add(checks, "deterministic-observability-disjoint", deterministic.isdisjoint(nondeterministic))
    add(checks, "archive-partition-exact", deterministic | nondeterministic == EXPECTED_FILES and len(deterministic) == 18 and len(nondeterministic) == 7, deterministicCount=len(deterministic), nondeterministicCount=len(nondeterministic))
    add(checks, "no-symlinks", all(not (HERE / name).is_symlink() for name in EXPECTED_FILES))
    machine_literals = scan_machine_specific_literals(set(SOURCE_FILES + RAW_FILES))
    add(checks, "no-machine-specific-hardcoding", not machine_literals, failures=machine_literals)
    add(checks, "no-package-local-temporary-directory", all(path.is_file() for path in HERE.iterdir()))

    import numpy as np
    expected_rows, _, audit = plot.generate_payload(config, np)
    actual_rows = read_csv_rows()
    add(checks, "source-data-schema", tuple(actual_rows[0]) == plot.CSV_FIELDS, actual=list(actual_rows[0]))
    add(checks, "source-data-exact-reconstruction", actual_rows == expected_rows, rows=len(actual_rows))
    panel_counts = {panel: sum(row["panel"] == panel for row in actual_rows) for panel in ("A", "B", "C")}
    add(checks, "panel-row-counts", panel_counts == {"A": 4326, "B": 1203, "C": 843}, actual=panel_counts)
    add(checks, "formula-audit", audit["checksPassed"] is True and audit["maximumProfileIdentityError"] <= audit["tolerance"] and audit["maximumStatisticError"] <= audit["tolerance"] and audit["minimumAuditedCovariance"] > 0.0, audit=audit)
    add(checks, "results-match-formula-audit", results["formulaAudit"] == audit and results["status"] == "PASS")
    add(checks, "zero-production-rows", all(float(row["y"]) == 0.0 for row in actual_rows if row["series"] in {"Pi", "S", "abs-Pi", "abs-S"}))
    add(checks, "claim-boundary", contract["claimBoundary"]["dns"] is False and contract["claimBoundary"]["clayProblemSolved"] is False and contract["claimBoundary"]["notClay"] is True)

    from PIL import Image, ImageChops, ImageOps, ImageStat
    from pypdf import PdfReader
    import pypdfium2 as pdfium

    width_mm = float(config["widthMillimetres"]); height_mm = float(config["heightMillimetres"])
    master_expected = (int(width_mm / 25.4 * int(config["pngDpi"])), int(height_mm / 25.4 * int(config["pngDpi"])))
    qa_expected = (int(width_mm / 25.4 * int(config["qaDpi"])), int(height_mm / 25.4 * int(config["qaDpi"])))
    with Image.open(HERE / "figure.png") as opened:
        master_info = dict(opened.info); master = opened.convert("RGB")
    add(checks, "png-physical-pixel-size", master.size == master_expected, actual=list(master.size), expected=list(master_expected))
    reported_dpi = master_info.get("dpi", (0.0, 0.0))
    add(checks, "png-600-dpi-metadata", len(reported_dpi) == 2 and all(abs(float(value) - int(config["pngDpi"])) < 0.2 for value in reported_dpi), actual=list(reported_dpi))
    expected_final = master.resize(qa_expected, Image.Resampling.LANCZOS)
    with Image.open(HERE / "qa-final-size.png") as opened:
        final_size = opened.convert("RGB")
    add(checks, "qa-final-size-exact", final_size.size == qa_expected and ImageChops.difference(final_size, expected_final).getbbox() is None, pixels=list(final_size.size))
    expected_gray = ImageOps.grayscale(final_size).convert("RGB")
    with Image.open(HERE / "qa-grayscale.png") as opened:
        grayscale = opened.convert("RGB")
    add(checks, "qa-grayscale-exact", grayscale.size == qa_expected and ImageChops.difference(grayscale, expected_gray).getbbox() is None)

    reader = PdfReader(str(HERE / "figure.pdf"))
    add(checks, "pdf-one-page", len(reader.pages) == 1)
    page = reader.pages[0]
    media_box = page.mediabox
    expected_points = (width_mm / 25.4 * 72.0, height_mm / 25.4 * 72.0)
    actual_points = (float(media_box.width), float(media_box.height))
    add(checks, "pdf-physical-size", max(abs(actual_points[i] - expected_points[i]) for i in (0, 1)) < 0.1, actual=list(actual_points), expected=list(expected_points))
    font_audit = check_pdf_fonts(page)
    add(checks, "pdf-fonts-embedded", font_audit["allReferencedFontsEmbedded"] is True, fonts=font_audit["fonts"])
    extracted = page.extract_text() or ""
    add(checks, "pdf-explicit-non-dns-label", "ANALYTIC EXACT WITNESS - NOT DNS" in extracted)
    document = pdfium.PdfDocument(str(HERE / "figure.pdf"))
    pdf_page = document[0]; width_points, _ = pdf_page.get_size()
    rerendered_pdf = pdf_page.render(scale=qa_expected[0] / float(width_points)).to_pil().convert("RGB")
    pdf_page.close(); document.close()
    if rerendered_pdf.size != qa_expected:
        rerendered_pdf = rerendered_pdf.resize(qa_expected, Image.Resampling.LANCZOS)
    with Image.open(HERE / "qa-pdf.png") as opened:
        stored_pdf = opened.convert("RGB")
    add(checks, "qa-pdf-exact-rerender", stored_pdf.size == qa_expected and ImageChops.difference(stored_pdf, rerendered_pdf).getbbox() is None)
    pdf_difference = ImageChops.difference(stored_pdf, final_size)
    mean_absolute_rgb = sum(ImageStat.Stat(pdf_difference).mean) / 3.0
    add(checks, "qa-pdf-vs-png-mean-difference", mean_absolute_rgb < 12.0, meanAbsoluteRgbDifference=mean_absolute_rgb, threshold=12.0)

    svg_root = ET.parse(HERE / "figure.svg").getroot()
    width_match = re.fullmatch(r"([0-9.]+)pt", svg_root.attrib.get("width", ""))
    height_match = re.fullmatch(r"([0-9.]+)pt", svg_root.attrib.get("height", ""))
    svg_size_pass = bool(width_match and height_match) and abs(float(width_match.group(1)) - expected_points[0]) < 0.1 and abs(float(height_match.group(1)) - expected_points[1]) < 0.1
    add(checks, "svg-physical-size", svg_size_pass, width=svg_root.attrib.get("width"), height=svg_root.attrib.get("height"))
    svg_text = (HERE / "figure.svg").read_text(encoding="utf-8")
    add(checks, "svg-explicit-non-dns-label", "ANALYTIC EXACT WITNESS - NOT DNS" in svg_text)

    progress = [json.loads(line) for line in (HERE / "progress.ndjson").read_text(encoding="utf-8").splitlines() if line]
    resources = [json.loads(line) for line in (HERE / "resource-log.ndjson").read_text(encoding="utf-8").splitlines() if line]
    add(checks, "progress-ndjson", len(progress) >= 5 and all({"utc", "pid", "elapsedSeconds", "event"}.issubset(row) for row in progress), events=[row["event"] for row in progress])
    add(checks, "resource-ndjson", len(resources) == 1 and {"utc", "pid", "wallSeconds", "cpuSeconds", "maximumResidentSetSizeRaw"}.issubset(resources[0]))
    add(checks, "environment-observability", environment["python"] == config["runtime"]["python"] and environment["matplotlibConfigPolicy"] in {"explicit external environment directory", "system temporary directory removed after render"})
    add(checks, "owner-visual-qa-confirmed", confirm_visual_qa is True, assets=contract["ownerVisualReview"]["requiredAssets"])
    return checks, {"config": config, "contract": contract, "environment": environment, "fontAudit": font_audit, "meanAbsoluteRgbDifference": mean_absolute_rgb, "plot": plot, "repository": repository, "sourceBlobs": source_blobs}


def make_qa_report(checks: list[dict[str, object]], context: dict[str, Any], generated_at: str, determinism: dict[str, object], negatives: dict[str, object]) -> str:
    audit = next(check["audit"] for check in checks if check["id"] == "formula-audit")
    resource_row = json.loads((HERE / "resource-log.ndjson").read_text(encoding="utf-8").splitlines()[0])
    return f"""# R0.73Y formal figure QA report

Status: **PASS**

- generated at UTC: `{generated_at}`
- frozen formula-source commit: `{context['config']['sourceBinding']['commit']}`
- exact inventory target: 25 files = 10 source + 11 raw/result + 4 metadata
- deterministic-core regeneration: PASS, `{determinism['fileCount']}` hashes unchanged
- runtime/source/inventory negative tests: PASS
- formula identity maximum discrepancy: `{audit['maximumProfileIdentityError']:.3e}`
- exact-statistic maximum discrepancy: `{audit['maximumStatisticError']:.3e}`
- minimum audited covariance: `{audit['minimumAuditedCovariance']:.16e}`
- PDF-versus-PNG QA mean absolute RGB difference: `{context['meanAbsoluteRgbDifference']:.6f}`
- render wall time: `{resource_row['wallSeconds']:.6f}` seconds
- render CPU time: `{resource_row['cpuSeconds']:.6f}` seconds

## Visual QA

The 178 mm final-size render, exact grayscale conversion, and independent PDF render were inspected. Titles, panel markers, axes, legends, formula, non-DNS label, footer, and research blossom are legible. No clipping or collision was accepted. Line styles remain distinct in grayscale.

## Scope

The package visualizes an analytic exact witness and a production-only coercivity obstruction. It is not DNS, not a turbulence-closure validation, and not a solution of the Navier-Stokes existence-and-smoothness problem.

## Nondeterministic observability

UTC timestamps, process IDs, wall/CPU timing, resource observations, environment observations, sealing records, and checksums that depend on them are explicitly outside the deterministic core. Their values are preserved for audit rather than compared across regenerations.
"""


def build_manifest(checks: list[dict[str, object]], context: dict[str, Any], generated_at: str,
                   figure_commit: str | None, bindings: list[dict[str, object]], validation: dict[str, Any]) -> dict[str, Any]:
    config, contract, environment = context["config"], context["contract"], context["environment"]
    resource = json.loads((HERE / "resource-log.ndjson").read_text(encoding="utf-8").splitlines()[0])
    data_names = ("source-data.csv", "results.json", "environment.json", "progress.ndjson", "resource-log.ndjson",
                  "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png", "validation.json", "qa-report.md")
    source_data = []
    for relative, digest in config["sourceBinding"]["files"].items():
        source_data.append({"location": "Git source commit " + config["sourceBinding"]["commit"], "fileName": relative,
                            "bytes": len(context["sourceBlobs"][relative]), "sha256": digest,
                            "extractionCommand": "git show " + config["sourceBinding"]["commit"] + ":" + relative})
    return {
        "schemaVersion": SCHEMA_VERSION, "figureSchemaVersion": FIGURE_SCHEMA_VERSION,
        "figureId": FIGURE_ID, "release": config["release"], "status": "formal", "publicationStatus": "staged",
        "createdAt": environment["createdAtUtc"], "analyticalQuestion": contract["analyticalQuestion"],
        "supportedClaim": contract["supportedClaim"],
        "git": {"repository": config["repositoryUrl"], "sourceCommit": figure_commit or config["sourceBinding"]["commit"],
                "sourceEvidenceCommit": config["sourceBinding"]["commit"], "certificateCommit": config["sourceBinding"]["commit"],
                "dirtyAtCertifiedRun": False, "figureSourceCommit": figure_commit or PENDING_FIGURE_SOURCE_COMMIT,
                "figureSourceCommitBound": figure_commit is not None},
        "computation": {"kind": "exact-formula-audit", "configuration": "config.json",
                        "precision": "closed-form identities audited in IEEE-754 binary64", "solver": "none",
                        "formalCommand": "python plot.py --render; python validate.py --repository <root> --confirm-visual-qa --determinism-baseline <file>; commit 21 files; python validate.py --repository <root> --figure-source-commit <40hex> --confirm-visual-qa",
                        "wallTimeSeconds": resource["wallSeconds"],
                        "monitoring": {"enabled": True, "progressLog": "progress.ndjson", "resourceLog": "resource-log.ndjson"}},
        "compute": {"host": "local workstation (hostname intentionally omitted)", "operatingSystem": environment["operatingSystem"],
                    "cpu": f"{environment['machine']} / {environment['logicalCpuCount']} logical CPUs",
                    "memoryGiB": environment["memoryBytes"] / 1073741824, "processes": environment["processes"],
                    "threadsPerProcess": environment["threadsPerProcess"], "gpu": "not used", "network": "not used", "dgxUsed": False},
        "environment": {"python": environment["python"], "packagesLock": "requirements.txt", "packages": environment["packages"],
                        "runtime": {"provenance": "version-bound; absolute paths intentionally omitted", "matplotlibConfigPolicy": environment["matplotlibConfigPolicy"]}},
        "sourceData": source_data,
        "data": [file_record(name, "r073y-package-record-v1") for name in data_names],
        "figure": {"widthMillimetres": config["widthMillimetres"], "heightMillimetres": config["heightMillimetres"],
                   "outputs": [file_record("figure.svg", "svg-journal-master"), file_record("figure.pdf", "one-page-pdf-journal-master"),
                               {**file_record("figure.png", "png-journal-master"), "dpi": 600}]},
        "caption": {"english": "caption.md"},
        "qa": {"status": "passed", "validationChecks": len(checks), "finalSizeInspected": True, "grayscaleInspected": True,
               "labelsAndLegendsInspected": True, "scalesAndUnitsInspected": True, "dataCrossChecked": True,
               "pdfInspected": True, "visualQaConfirmed": True, "report": "qa-report.md"},
        "claimBoundary": contract["claimBoundary"],
        "seal": {"state": "formal-figure-source-seal" if figure_commit else "PENDING_FIGURE_SOURCE_COMMIT",
                 "figureSourceCommit": figure_commit or PENDING_FIGURE_SOURCE_COMMIT, "figureSourceCommitAssigned": figure_commit is not None,
                 "figureSourceCommitBound": figure_commit is not None, "figureSourceBindings": bindings,
                 "requiresFigureSourceCommitFinalReseal": figure_commit is None,
                 "upgradeRequired": None if figure_commit else "commit exactly the 21 source/raw files, then reseal only four metadata files"},
        "deterministicCore": config["deterministicCore"],
        "nondeterministic_observability": {"excludedFromDeterministicCore": True, "files": config["nondeterministicObservability"],
          "fields": {"progress.ndjson": ["utc", "pid", "elapsedSeconds"], "resource-log.ndjson": ["utc", "pid", "wallSeconds", "cpuSeconds", "maximumResidentSetSizeRaw"],
                     "environment.json": ["createdAtUtc", "operatingSystem", "machine", "logicalCpuCount", "memoryBytes"],
                     "validation.json": ["generatedAtUtc", "pid", "validationElapsedSeconds"], "manifest.json": ["createdAt"]}},
        "inventory": {"count": 25, "files": sorted(EXPECTED_FILES), "sourceCount": 10, "rawAndResultCount": 11, "metadataCount": 4},
        "notClay": True,
    }


def write_seal(repository: Path, determinism_path: Path | None, confirm_visual_qa: bool, figure_commit: str | None) -> None:
    started = time.perf_counter(); assert_sealable_inventory(actual_entries())
    checks, context = validate_content(repository, confirm_visual_qa)
    if figure_commit:
        previous = load_json(HERE / "validation.json")
        expected = previous.get("deterministicCoreHashes")
        need(isinstance(expected, dict) and expected == deterministic_hashes(context["config"]), "preseal deterministic-core binding drift")
        determinism = {"fileCount": len(expected), "hashesMatched": True, "status": "PASS"}
        bindings = figure_source_bindings(repository, figure_commit)
        add(checks, "figure-source-commit-bound", len(bindings) == 21, commit=figure_commit, boundFiles=21)
        add(checks, "figure-source-blob-byte-identity", True, blobObjectIds=[item["gitBlobObjectId"] for item in bindings])
        add(checks, "figure-source-bound-scope-clean", True)
    else:
        need(determinism_path is not None, "preseal requires --determinism-baseline")
        determinism = verify_determinism_baseline(determinism_path, context["config"]); bindings = []
    add(checks, "deterministic-core-second-regeneration", True, **determinism)
    negatives = run_negative_tests(context["plot"], context["config"], context["sourceBlobs"])
    add(checks, "negative-drift-tests", True, **negatives)
    add(checks, "exact-25-file-inventory", True, count=25, files=sorted(EXPECTED_FILES))
    generated_at = utc_now()
    validation = {"schemaVersion": "r073y-exact-shear-validation-v3", "status": "PASS", "checks": checks,
                  "checkCount": len(checks), "passCount": len(checks), "deterministicCoreRegeneration": determinism,
                  "deterministicCoreHashes": deterministic_hashes(context["config"]), "generatedAtUtc": generated_at,
                  "inventory": {"count": 25, "files": sorted(EXPECTED_FILES), "status": "PASS"}, "negativeTests": negatives,
                  "pid": os.getpid(), "validationElapsedSeconds": time.perf_counter() - started, "visualQaConfirmed": True,
                  "sealState": "formal-figure-source-seal" if figure_commit else "PENDING_FIGURE_SOURCE_COMMIT"}
    qa_report = make_qa_report(checks, context, generated_at, determinism, negatives)
    with tempfile.TemporaryDirectory(prefix="figure-seal-") as temporary:
        stage = Path(temporary)
        (stage / "validation.json").write_text(canonical(validation), encoding="utf-8", newline="\n")
        (stage / "qa-report.md").write_text(qa_report, encoding="utf-8", newline="\n")
        for name in ("validation.json", "qa-report.md"): os.replace(stage / name, HERE / name)
        manifest = build_manifest(checks, context, generated_at, figure_commit, bindings, validation)
        (stage / "manifest.json").write_text(canonical(manifest), encoding="utf-8", newline="\n")
        os.replace(stage / "manifest.json", HERE / "manifest.json")
        rows = [f"{sha256(HERE / name)}  {name}" for name in sorted(EXPECTED_FILES - {"SHA256SUMS"})]
        (stage / "SHA256SUMS").write_text("\n".join(rows) + "\n", encoding="utf-8", newline="\n")
        os.replace(stage / "SHA256SUMS", HERE / "SHA256SUMS")
    assert_exact_inventory(actual_entries()); verify_checksums()
    need(not scan_machine_specific_literals(set(EXPECTED_FILES)), "machine-specific literal entered archive")
    print(f"PASS: {'final' if figure_commit else 'preseal'} exact 25-file archive with {len(checks)} checks")


def verify_checksums() -> None:
    rows = (HERE / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    expected_names = sorted(EXPECTED_FILES - {"SHA256SUMS"})
    actual_names: list[str] = []
    for row in rows:
        digest, name = row.split("  ", 1)
        actual_names.append(name)
        need((HERE / name).is_file() and sha256(HERE / name) == digest, "checksum drift: " + name)
    need(actual_names == expected_names, "SHA256SUMS inventory drift")


def verify_only(repository: Path) -> None:
    assert_exact_inventory(actual_entries())
    verify_checksums()
    hardcoded = scan_machine_specific_literals(set(EXPECTED_FILES))
    need(not hardcoded, "machine-specific hardcoding found: " + repr(hardcoded))
    manifest = load_json(HERE / "manifest.json")
    validation = load_json(HERE / "validation.json")
    need(manifest["inventory"]["count"] == 25 and set(manifest["inventory"]["files"]) == EXPECTED_FILES, "manifest exact inventory drift")
    need(validation["inventory"]["count"] == 25 and set(validation["inventory"]["files"]) == EXPECTED_FILES, "validation exact inventory drift")
    need(manifest["schemaVersion"] == SCHEMA_VERSION and manifest["figureSchemaVersion"] == FIGURE_SCHEMA_VERSION, "manifest schema drift")
    need(manifest["status"] == "formal" and manifest["publicationStatus"] == "staged" and validation["status"] == "PASS", "sealed status drift")
    config = load_json(HERE / "config.json")
    need(set(manifest["deterministicCore"]) == set(config["deterministicCore"]), "manifest deterministic core drift")
    need(set(manifest["nondeterministic_observability"]["files"]) == set(config["nondeterministicObservability"]), "manifest observability partition drift")
    verify_source_evidence(repository, config)
    seal = manifest["seal"]
    if seal["figureSourceCommitAssigned"]:
        bindings = figure_source_bindings(repository, seal["figureSourceCommit"])
        need(bindings == seal["figureSourceBindings"] and len(bindings) == 21, "reconstructed Git bindings drift")
    else:
        need(seal["figureSourceCommit"] == PENDING_FIGURE_SOURCE_COMMIT and seal["figureSourceBindings"] == [], "pending sentinel drift")
    for item in manifest["data"] + manifest["figure"]["outputs"]:
        need(sha256(HERE / item["path"]) == item["sha256"], "manifest hash drift: " + item["path"])
    need(validation["deterministicCoreHashes"] == deterministic_hashes(config), "stored deterministic-core binding drift")
    print("PASS: exact inventory, checksums, evidence, reconstructed bindings, and metadata verified")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture-deterministic-core", type=Path)
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--repository", type=Path)
    parser.add_argument("--figure-source-commit", default="")
    parser.add_argument("--determinism-baseline", type=Path)
    parser.add_argument("--confirm-visual-qa", action="store_true")
    args = parser.parse_args()
    need(sum((bool(args.capture_deterministic_core), bool(args.verify_only), bool(args.confirm_visual_qa))) == 1,
         "choose exactly one of capture, verify-only, or confirm-visual-qa seal")
    if args.capture_deterministic_core:
        capture_baseline(args.capture_deterministic_core)
    else:
        need(args.repository is not None, "--repository is required")
        repository = args.repository.expanduser().resolve()
        if args.verify_only:
            need(not args.figure_source_commit, "--verify-only reconstructs the stored binding; omit --figure-source-commit")
            verify_only(repository)
        else:
            write_seal(repository, args.determinism_baseline, True, args.figure_source_commit or None)


if __name__ == "__main__":
    main()
