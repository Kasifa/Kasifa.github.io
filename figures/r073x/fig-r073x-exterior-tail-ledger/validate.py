#!/usr/bin/env python3
"""Validate and seal the R0.73X exterior-tail ledger figure package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import importlib.util
import json
import math
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
from typing import Any

from PIL import Image, ImageChops, ImageOps
from pypdf import PdfReader
import pypdfium2 as pdfium


HERE = Path(__file__).resolve().parent
DEFAULT_REPOSITORY = HERE.parents[2]
FIGURE_ID = "fig-r073x-exterior-tail-ledger"
REPOSITORY_URL = "https://github.com/Kasifa/Kasifa.github.io.git"
SOURCE_FILES = (
    "README.md", "caption.md", "chart-contract-and-source-data.md",
    "command.txt", "config.json", "contract.json", "plot.py",
    "qa-protocol.md", "requirements.txt", "validate.py",
)
RAW_FILES = (
    "environment.json", "figure.pdf", "figure.png", "figure.svg",
    "progress.ndjson", "qa-final-size.png", "qa-grayscale.png",
    "qa-pdf.png", "resource-log.ndjson", "results.json", "source-data.csv",
)
METADATA_FILES = ("manifest.json", "qa-report.md", "validation.json", "SHA256SUMS")
EXPECTED_FILES = set(SOURCE_FILES + RAW_FILES + METADATA_FILES)
BOUND_FILES = frozenset(SOURCE_FILES + RAW_FILES)
BOUND_FOR_SUMS = tuple(sorted(set(SOURCE_FILES + RAW_FILES + ("manifest.json", "qa-report.md", "validation.json"))))
EXPECTED_PACKAGES = {
    "matplotlib": "3.10.6",
    "numpy": "2.5.2",
    "pillow": "12.3.0",
    "pypdf": "6.10.0",
    "pypdfium2": "5.13.0",
}


def need(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    need(isinstance(value, dict), "JSON root must be an object: " + str(path))
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def add(checks: list[dict[str, object]], identifier: str, passed: bool, **details: object) -> None:
    checks.append({"id": identifier, "pass": bool(passed), **details})
    need(passed, "validation failed: " + identifier)


def load_plot_module() -> Any:
    spec = importlib.util.spec_from_file_location("r073x_exterior_tail_plot_validation", HERE / "plot.py")
    need(spec is not None and spec.loader is not None, "cannot load plot.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_csv() -> list[dict[str, str]]:
    with (HERE / "source-data.csv").open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def check_pdf_fonts(page: Any) -> dict[str, object]:
    resources = page.get("/Resources")
    if resources is None:
        return {"fontReferenceCount": 0, "embeddedFontCount": 0, "allReferencedFontsEmbedded": False, "fonts": []}
    resources = resources.get_object()
    fonts_object = resources.get("/Font", {})
    fonts_object = fonts_object.get_object() if hasattr(fonts_object, "get_object") else fonts_object
    rows: list[dict[str, object]] = []
    for resource_name, reference in fonts_object.items():
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
        rows.append({
            "baseFont": str(font.get("/BaseFont", "")),
            "embedded": embedded,
            "resource": str(resource_name),
            "subtype": str(font.get("/Subtype", "")),
        })
    return {
        "fontReferenceCount": len(rows),
        "embeddedFontCount": sum(bool(item["embedded"]) for item in rows),
        "allReferencedFontsEmbedded": bool(rows) and all(bool(item["embedded"]) for item in rows),
        "fonts": rows,
    }


def render_pdf(path: Path, maximum_width: int) -> Image.Image:
    document = pdfium.PdfDocument(str(path))
    need(len(document) == 1, "PDF raster source is not one page")
    page = document[0]
    width_points, _ = page.get_size()
    image = page.render(scale=maximum_width / float(width_points)).to_pil().convert("RGB")
    page.close()
    document.close()
    return image


def file_record(name: str, schema: str) -> dict[str, object]:
    path = HERE / name
    return {"bytes": path.stat().st_size, "path": name, "schema": schema, "sha256": sha256(path)}


def validate_content(repository: Path) -> tuple[list[dict[str, object]], dict[str, Any]]:
    checks: list[dict[str, object]] = []
    config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    results = load_json(HERE / "results.json")
    environment = load_json(HERE / "environment.json")
    add(checks, "source-files-present", all((HERE / name).is_file() for name in SOURCE_FILES), files=list(SOURCE_FILES))
    add(checks, "raw-files-present", all((HERE / name).is_file() for name in RAW_FILES), files=list(RAW_FILES))
    add(checks, "figure-id", config["figureId"] == FIGURE_ID == contract["figureId"])
    versions = {name: importlib.metadata.version(name) for name in EXPECTED_PACKAGES}
    add(checks, "dependency-versions", versions == EXPECTED_PACKAGES, actual=versions, expected=EXPECTED_PACKAGES)
    runtime = environment["runtime"]
    recorded_python = runtime.get("pythonExecutable")
    recorded_python_path = runtime.get("pythonPathEnvironment")
    recorded_imports = runtime.get("imports")
    python_path_roots = (
        [Path(value).resolve() for value in recorded_python_path.split(":") if value]
        if isinstance(recorded_python_path, str) else []
    )
    import_paths = (
        {name: Path(value).resolve() for name, value in recorded_imports.items()}
        if isinstance(recorded_imports, dict)
        and all(isinstance(name, str) and isinstance(value, str)
                for name, value in recorded_imports.items())
        else {}
    )
    imports_under_recorded_path = bool(python_path_roots) and all(
        any(root == path or root in path.parents for root in python_path_roots)
        for path in import_paths.values()
    )
    recorded_runtime = {
        "pythonExecutable": recorded_python,
        "pythonPathEnvironment": recorded_python_path,
        "imports": recorded_imports,
    }
    add(
        checks,
        "runtime-provenance",
        isinstance(recorded_python, str)
        and Path(recorded_python).is_absolute()
        and set(import_paths) == {"matplotlib", "numpy"}
        and all(path.is_absolute() for path in import_paths.values())
        and imports_under_recorded_path,
        recorded=recorded_runtime,
        interpretation="certified-run provenance is internally consistent; live verifier portability is checked by pinned package versions",
    )

    plot = load_plot_module()
    expected_rows, verified = plot.generate_rows(repository, config, contract)
    actual_rows = read_csv()
    add(checks, "source-data-schema", tuple(actual_rows[0].keys()) == plot.CSV_FIELDS, actual=list(actual_rows[0].keys()))
    add(checks, "source-data-exact-reconstruction", actual_rows == expected_rows, rows=len(actual_rows))
    panel_counts = {panel: sum(item["panel"] == panel for item in actual_rows) for panel in ("A", "B", "C")}
    add(checks, "panel-row-counts", panel_counts == {"A": 21, "B": 14, "C": 11}, actual=panel_counts)
    add(checks, "panel-a-analytic-formula-label", all(item["evidence_class"] == "analytic formula" for item in actual_rows if item["panel"] == "A"))
    add(checks, "panel-b-analytic-formula-label", all(item["evidence_class"] == "analytic formula" for item in actual_rows if item["panel"] == "B"))
    add(checks, "panel-c-static-functional-label", all(item["evidence_class"] == "static functional diagnostic" for item in actual_rows if item["panel"] == "C"))
    for series in ("gaussian-normalized", "pressure-algebraic-normalized"):
        first = next(item for item in actual_rows if item["panel"] == "B" and item["series"] == series and item["record"] == "m-01")
        add(checks, "panel-b-normalization-" + series, float(first["y"]) == 1.0)
    for series in ("weighted-L3", "weighted-L2-to-3/2"):
        base = next(item for item in actual_rows if item["panel"] == "C" and item["series"] == series and abs(float(item["x"]) - 0.25) < 1e-15)
        add(checks, "panel-c-normalization-" + series, float(base["y"]) == 1.0)
    landmark = next(item for item in actual_rows if item["series"] == "ratio-landmark")
    add(checks, "panel-c-smallest-ratio", abs(float(landmark["y"]) - 299.3965269759089) < 1e-12, actual=float(landmark["y"]))
    final_slopes = results["certificate"]["finalNumericSlopes"]
    add(checks, "panel-c-final-l3-slope", abs(float(final_slopes["weighted_L3"]) - 3.0) < 2e-4, actual=final_slopes["weighted_L3"])
    add(checks, "panel-c-final-l2-proxy-slope", abs(float(final_slopes["weighted_L2_to_three_halves"]) - 4.5) < 3e-4, actual=final_slopes["weighted_L2_to_three_halves"])
    add(checks, "panel-c-final-ratio-slope", abs(float(final_slopes["ratio_L3_over_L2_to_three_halves"]) + 1.5) < 1e-4, actual=final_slopes["ratio_L3_over_L2_to_three_halves"])
    panel_a_raw_maximum = max(float(item["raw_value"]) for item in actual_rows if item["panel"] == "A")
    add(
        checks,
        "panel-a-log-ticks-include-unity",
        config["panelA"]["majorTickExponents"] == [0, -40, -80, -120, -160, -200]
        and float(config["panelA"]["yMaximum"]) > panel_a_raw_maximum,
        majorTickExponents=config["panelA"]["majorTickExponents"],
        yMaximum=config["panelA"]["yMaximum"],
        rawMaximum=panel_a_raw_maximum,
    )
    add(
        checks,
        "panel-b-log-ticks-include-unity",
        config["panelB"]["majorTickExponents"] == [0, -10, -20, -30, -40, -50]
        and float(config["panelB"]["yMaximum"]) > 1.0,
        majorTickExponents=config["panelB"]["majorTickExponents"],
        yMaximum=config["panelB"]["yMaximum"],
    )
    add(
        checks,
        "owner-final-size-visual-review",
        contract["ownerVisualReview"]["status"] == "PASS"
        and len(contract["ownerVisualReview"]["confirmed"]) == 7,
        reviewedAsset=contract["ownerVisualReview"]["reviewedAsset"],
        confirmed=contract["ownerVisualReview"]["confirmed"],
    )
    add(checks, "renderer-artist-bounds", results["render"]["artistBoundsPass"] is True, failures=results["render"]["artistBoundsFailures"])
    add(checks, "claim-boundary", contract["claimBoundary"]["navierStokesSimulation"] is False
        and contract["claimBoundary"]["dns"] is False
        and contract["claimBoundary"]["associatedPressureCounterexample"] is False
        and contract["claimBoundary"]["clayProblemSolved"] is False
        and contract["claimBoundary"]["notClay"] is True)

    width_mm = float(config["widthMillimetres"])
    height_mm = float(config["heightMillimetres"])
    dpi = int(config["pngDpi"])
    expected_pixels = [int(width_mm / 25.4 * dpi), int(height_mm / 25.4 * dpi)]
    with Image.open(HERE / "figure.png") as opened:
        info = dict(opened.info)
        master = opened.convert("RGB")
        actual_pixels = [master.width, master.height]
        reported_dpi = info.get("dpi", (0.0, 0.0))
        qa_width = min(int(config["qaMaximumWidthPixels"]), master.width)
        qa_height = round(master.height * qa_width / master.width)
        expected_final = master.resize((qa_width, qa_height), Image.Resampling.LANCZOS)
    add(checks, "png-pixel-dimensions", actual_pixels == expected_pixels, actual=actual_pixels, expected=expected_pixels)
    add(checks, "png-600-dpi-metadata", len(reported_dpi) == 2 and all(abs(float(value) - dpi) < 0.1 for value in reported_dpi), actual=list(reported_dpi), expected=dpi)
    with Image.open(HERE / "qa-final-size.png") as opened:
        stored_final = opened.convert("RGB")
    add(checks, "qa-final-size-exact", stored_final.size == expected_final.size and ImageChops.difference(stored_final, expected_final).getbbox() is None, pixels=list(stored_final.size))
    expected_gray = ImageOps.grayscale(expected_final).convert("RGB")
    with Image.open(HERE / "qa-grayscale.png") as opened:
        stored_gray = opened.convert("RGB")
    add(checks, "qa-grayscale-exact", stored_gray.size == expected_gray.size and ImageChops.difference(stored_gray, expected_gray).getbbox() is None, pixels=list(stored_gray.size))

    reader = PdfReader(str(HERE / "figure.pdf"))
    add(checks, "pdf-one-page", len(reader.pages) == 1, pages=len(reader.pages))
    page = reader.pages[0]
    media = [float(page.mediabox.width), float(page.mediabox.height)]
    expected_points = [width_mm / 25.4 * 72.0, height_mm / 25.4 * 72.0]
    add(checks, "pdf-mediabox", all(abs(left - right) < 0.02 for left, right in zip(media, expected_points)), actualPoints=media, expectedPoints=expected_points)
    font_report = check_pdf_fonts(page)
    add(checks, "pdf-font-references", font_report["fontReferenceCount"] >= 1, fontReferenceCount=font_report["fontReferenceCount"])
    add(checks, "pdf-fonts-embedded", bool(font_report["allReferencedFontsEmbedded"]), embeddedFontCount=font_report["embeddedFontCount"], fontReferenceCount=font_report["fontReferenceCount"])
    fresh_pdf = render_pdf(HERE / "figure.pdf", int(config["qaMaximumWidthPixels"]))
    with Image.open(HERE / "qa-pdf.png") as opened:
        stored_pdf = opened.convert("RGB")
    add(checks, "qa-pdf-independent-raster-exact", stored_pdf.size == fresh_pdf.size and ImageChops.difference(stored_pdf, fresh_pdf).getbbox() is None, pixels=list(stored_pdf.size))

    svg_text = (HERE / "figure.svg").read_text(encoding="utf-8")
    svg_root = ET.fromstring(svg_text)
    view_box = [float(value) for value in svg_root.attrib["viewBox"].split()]
    add(checks, "svg-viewbox", len(view_box) == 4 and abs(view_box[2] - expected_points[0]) < 0.02 and abs(view_box[3] - expected_points[1]) < 0.02, actual=view_box)
    add(checks, "svg-no-remote-links", re.search(r"(?:xlink:)?href=[\"']https?://", svg_text) is None)
    for token in ("analytic formula", "static functional diagnostic", "NOT DNS", "NOT CLAY", "not interchangeable"):
        add(checks, "svg-visible-token-" + re.sub(r"[^a-z]+", "-", token.lower()).strip("-"), token in svg_text)
    for index in range(1, 6):
        add(checks, f"research-blossom-petal-{index}", f'id="research-blossom-petal-{index}"' in svg_text)
    add(checks, "research-blossom-center", 'id="research-blossom-center"' in svg_text)
    palette_colors = {value.lower() for value in config["palette"].values()} | {"#000000", "#ffffff"}
    used_colors = {value.lower() for value in re.findall(r"#[0-9A-Fa-f]{6}", svg_text)}
    add(checks, "svg-declared-palette-only", used_colors.issubset(palette_colors), used=sorted(used_colors), allowed=sorted(palette_colors))

    return checks, {
        "config": config,
        "contract": contract,
        "results": results,
        "environment": environment,
        "fontReport": font_report,
        "mediaPoints": media,
        "qaFinalPixels": list(stored_final.size),
        "qaPdfPixels": list(stored_pdf.size),
        "panelCounts": panel_counts,
        "versions": versions,
        "verified": verified,
    }


def git_text(repository: Path, args: list[str]) -> str:
    completed = subprocess.run(
        ["git", *args], cwd=repository, capture_output=True, text=True, check=False,
    )
    need(completed.returncode == 0, "git command failed: " + " ".join(args))
    return completed.stdout.strip()


def figure_source_bindings(repository: Path, commit: str) -> list[dict[str, object]]:
    need(re.fullmatch(r"[0-9a-f]{40}", commit) is not None,
         "figure source commit must be full lowercase 40-hex")
    exists = subprocess.run(
        ["git", "cat-file", "-e", commit + "^{commit}"], cwd=repository,
        capture_output=True, check=False,
    )
    need(exists.returncode == 0, "figure source commit does not resolve")
    bindings: list[dict[str, object]] = []
    scoped_paths: list[str] = []
    for name in sorted(BOUND_FILES):
        path = HERE / name
        try:
            repository_path = path.relative_to(repository).as_posix()
        except ValueError as error:
            raise RuntimeError(
                "formal sealing requires the figure package to be inside --repository"
            ) from error
        payload = path.read_bytes()
        committed = subprocess.run(
            ["git", "cat-file", "blob", commit + ":" + repository_path],
            cwd=repository, capture_output=True, check=False,
        )
        need(committed.returncode == 0,
             "figure source blob absent from commit: " + repository_path)
        need(committed.stdout == payload,
             "figure source blob differs from current bytes: " + repository_path)
        blob_object_id = git_text(
            repository, ["rev-parse", commit + ":" + repository_path],
        )
        need(re.fullmatch(r"[0-9a-f]{40,64}", blob_object_id) is not None,
             "invalid figure source blob object id: " + repository_path)
        bindings.append({
            "bytes": len(payload),
            "gitBlobObjectId": blob_object_id,
            "path": repository_path,
            "sha256": hashlib.sha256(payload).hexdigest(),
            "sourceClass": "immutable-figure-source-or-raw-artifact",
        })
        scoped_paths.append(repository_path)
    need(len(bindings) == 21, "figure source binding inventory drift")
    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all", "--",
         *scoped_paths], cwd=repository, capture_output=True, check=False,
    )
    need(status.returncode == 0, "figure source scoped git status failed")
    need(not status.stdout, "figure source/raw bound scope is dirty")
    return bindings


def build_validation(
    checks: list[dict[str, object]], visual_confirmed: bool,
    figure_source_commit: str | None,
) -> dict[str, object]:
    final_source_seal = figure_source_commit is not None
    seal_state = ("formal-figure-source-seal" if final_source_seal
                  else "HASH_BOUND_PREPUBLICATION_ARTIFACT")
    passed = sum(bool(item["pass"]) for item in checks)
    return {
        "schemaVersion": "r073x-exterior-tail-ledger-validation-v1",
        "figureId": FIGURE_ID,
        "status": "PASS",
        "sealState": seal_state,
        "figureSourceCommit": figure_source_commit,
        "figureSourceCommitAssigned": final_source_seal,
        "checkCount": len(checks),
        "passCount": passed,
        "passed": passed,
        "required": len(checks),
        "checksPassed": passed,
        "checksRequired": len(checks),
        "allChecksPass": passed == len(checks),
        "visualQaConfirmed": visual_confirmed,
        "ownerVisualQaStatus": "PASS",
        "tickRepairRecorded": True,
        "checks": checks,
    }


def build_qa_report(
    validation: dict[str, object], context: dict[str, Any],
    figure_source_commit: str | None,
) -> str:
    config = context["config"]
    fonts = context["fontReport"]
    media = context["mediaPoints"]
    final_source_seal = figure_source_commit is not None
    report_status = ("FORMAL FIGURE-SOURCE SEAL" if final_source_seal
                     else "HASH-BOUND PREPUBLICATION ARTIFACT")
    lifecycle = (
        "The 21 figure source/raw artifacts are byte-identical to immutable "
        f"commit `{figure_source_commit}` and their exact scoped Git status is "
        "clean.  This is the formal figure-source seal; only the four metadata "
        "files are left for the separate reseal commit."
        if final_source_seal else
        "The 21 source/raw figure files are hash-bound but not yet package-commit-bound; "
        "the Site owner must commit exactly those files before upgrading this seal to "
        "a formal figure-source seal."
    )
    return rf"""# R0.73X figure QA report

**Status:** PASS — {report_status}

**Checks:** {validation['passed']}/{validation['required']}

All four frozen sources matched their SHA-256 values and immutable blobs at
source commit `{context['contract']['sourceCommit']}`.  The renderer parsed the
Gaussian denominator `32` and harmonic-pressure exponent `4` from the proof,
then reconstructed all {context['results']['sourceDataRows']} source-data rows.

SVG, PDF, and 600 dpi PNG integrity passed at
{config['widthMillimetres']:.0f} mm by {config['heightMillimetres']:.0f} mm.
The PDF has one page, MediaBox {media[0]:.6f} by {media[1]:.6f} pt,
{fonts['fontReferenceCount']} referenced font resource(s), and
{fonts['embeddedFontCount']} embedded font resource(s).  The independently
regenerated PDF raster is {context['qaPdfPixels'][0]} by
{context['qaPdfPixels'][1]} pixels and exactly matches `qa-pdf.png`.

Final-size, grayscale, and PDF rasters were inspected for clipped or colliding
titles, formulas, labels, ticks, legends, annotations, and footer text.  No
clipping was observed.  Solid/dashed lines, filled/open markers, and distinct
circle/square/triangle shapes preserve every comparison in grayscale.  The
locked five-petal research blossom is present at the top-right data-free token.

After the log-axis repair, the Site owner independently reviewed the final-size
asset and returned `PASS`: Panels A and B both display the $10^0$ major tick;
Panel A keeps `yMaximum=40`, above the $\theta^{{-2}}$ prefactor's largest
plotted value; Panel B remains normalized at $m=1$.  The owner also confirmed
no clipping or collisions, grayscale-distinguishable line/marker encodings,
PDF/PNG visual consistency, and clear `NOT DNS` / `NOT CLAY` boundaries.

Panels A--B are visibly labelled `analytic formula`.  Panel C is visibly
labelled `static functional diagnostic · NOT DNS`.  The pressure and Gaussian
rows are marked as non-interchangeable.  The static packet is not an NSE
trajectory or associated-pressure counterexample.  No DNS, fit, compact-cutoff
closure, epsilon regularity, global regularity, or Clay claim is made.

{lifecycle}  `dgxUsed=false`; `NOT CLAY`.
"""


def build_manifest(
    context: dict[str, Any], validation: dict[str, object],
    figure_source_commit: str | None,
    figure_bindings: list[dict[str, object]],
) -> dict[str, object]:
    config = context["config"]
    contract = context["contract"]
    environment = context["environment"]
    execution = environment["execution"]
    resource_row = json.loads((HERE / "resource-log.ndjson").read_text(encoding="utf-8").strip())
    final_source_seal = figure_source_commit is not None
    seal_state = ("formal-figure-source-seal" if final_source_seal
                  else "HASH_BOUND_PREPUBLICATION_ARTIFACT")
    data_names = (
        "source-data.csv", "results.json", "environment.json", "progress.ndjson",
        "resource-log.ndjson", "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png",
        "validation.json", "qa-report.md",
    )
    source_data = []
    for source in contract["sources"]:
        source_data.append({
            "location": "Git source commit " + contract["sourceCommit"],
            "fileName": source["path"],
            "bytes": (context["repository"] / source["path"]).stat().st_size,
            "sha256": source["sha256"],
            "extractionCommand": "git show " + contract["sourceCommit"] + ":" + source["path"],
        })
    return {
        "schemaVersion": "research-figure-manifest-v1",
        "figureSchemaVersion": "r073x-exterior-tail-ledger-manifest-v1",
        "figureId": FIGURE_ID,
        "release": "R0.73X",
        "status": "formal" if final_source_seal else "draft",
        "publicationStatus": "staged" if final_source_seal else "prepublication",
        "createdAt": environment["createdUtc"],
        "analyticalQuestion": contract["analyticalQuestion"],
        "supportedClaim": contract["supportedClaim"],
        "git": {
            "repository": REPOSITORY_URL,
            "sourceCommit": figure_source_commit if final_source_seal else contract["sourceCommit"],
            "sourceEvidenceCommit": contract["sourceCommit"],
            "certificateCommit": contract["sourceCommit"],
            "dirtyAtCertifiedRun": False,
            "figureSourceCommit": figure_source_commit,
            "figureSourceCommitBound": final_source_seal,
            "sourceCommitMeaning": (
                "immutable commit containing byte-identical figure source and raw artifacts"
                if final_source_seal else
                "immutable source-evidence commit; figure source/raw commit not yet assigned"
            ),
        },
        "computation": {
            "kind": "exact-formula-audit",
            "configuration": "config.json",
            "precision": "parsed closed formulas and audited binary64 packet rows",
            "solver": "none",
            "formalCommand": "python plot.py --render-preseal; python validate.py --confirm-visual-qa; python validate.py --figure-source-commit <full-40-hex> --confirm-visual-qa; python validate.py --verify-only",
            "wallTimeSeconds": resource_row["elapsedSeconds"],
            "monitoring": {
                "enabled": True,
                "progressLog": "progress.ndjson",
                "resourceLog": "resource-log.ndjson",
                "trackedFields": ["elapsedSeconds", "event", "maximumResidentSetSizeRaw"],
            },
        },
        "compute": {
            "host": execution["host"],
            "operatingSystem": execution["operatingSystem"],
            "cpu": execution["cpu"],
            "memoryGiB": execution["memoryGiB"],
            "processes": execution["processes"],
            "threadsPerProcess": execution["threadsPerProcess"],
            "gpu": execution["gpu"],
            "network": execution["network"],
            "dgxUsed": execution["dgxUsed"],
            "ordinaryTranslationPath": execution["ordinaryTranslationPath"],
        },
        "environment": {
            "python": execution["python"],
            "packagesLock": "requirements.txt",
            "packages": environment["packages"],
            "runtime": environment["runtime"],
        },
        "sourceData": source_data,
        "data": [file_record(name, "r073x-exterior-tail-ledger-package-file-v1") for name in data_names],
        "figure": {
            "widthMillimetres": config["widthMillimetres"],
            "heightMillimetres": config["heightMillimetres"],
            "outputs": [
                file_record("figure.svg", "svg-journal-master"),
                file_record("figure.pdf", "one-page-pdf-journal-master"),
                {**file_record("figure.png", "png-journal-master"), "dpi": config["pngDpi"]},
            ],
        },
        "caption": {"english": "caption.md"},
        "qa": {
            "status": "passed",
            "validationChecks": validation["required"],
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "dataCrossChecked": True,
            "pdfInspected": True,
            "visualQaConfirmed": validation["visualQaConfirmed"],
            "ownerVisualQaStatus": validation["ownerVisualQaStatus"],
            "tickRepairRecorded": validation["tickRepairRecorded"],
            "report": "qa-report.md",
        },
        "claimBoundary": contract["claimBoundary"],
        "seal": {
            "state": seal_state,
            "sourceEvidenceCommitBound": True,
            "figureSourceCommitBound": final_source_seal,
            "figureSourceBindings": figure_bindings,
            "figureSourceCommit": figure_source_commit,
            "figureSourceCommitAssigned": final_source_seal,
            "requiresFigureSourceCommitFinalReseal": not final_source_seal,
            "requiresParentFigureSourceCommitFinalReseal": not final_source_seal,
            "upgradeRequired": (
                None if final_source_seal else
                "commit all 21 source/raw files, then reseal the four metadata files"
            ),
        },
        "ordinaryTranslationPath": "LOCAL_DIRECT_NO_DGX",
        "dgxUsed": False,
        "notClay": True,
    }


def sums_text() -> str:
    return "\n".join(f"{sha256(HERE / name)}  {name}" for name in BOUND_FOR_SUMS) + "\n"


def verify_seal(
    expected_checks: list[dict[str, object]], context: dict[str, Any],
    expected_figure_bindings: list[dict[str, object]],
) -> dict[str, object]:
    validation = load_json(HERE / "validation.json")
    manifest = load_json(HERE / "manifest.json")
    need(validation.get("status") == "PASS"
         and validation.get("visualQaConfirmed") is True,
         "stored validation is not a visually confirmed pass")
    need(manifest.get("schemaVersion") == "research-figure-manifest-v1"
         and manifest.get("figureSchemaVersion")
         == "r073x-exterior-tail-ledger-manifest-v1"
         and manifest.get("figureId") == FIGURE_ID
         and manifest.get("release") == "R0.73X",
         "manifest schema or identity drift")
    need(validation.get("checksPassed") == len(expected_checks)
         and validation.get("checksRequired") == len(expected_checks)
         and validation.get("passed") == len(expected_checks)
         and validation.get("required") == len(expected_checks)
         and validation.get("checkCount") == len(expected_checks)
         and validation.get("passCount") == len(expected_checks)
         and validation.get("checks") == expected_checks,
         "validation check reconstruction drift")
    need(manifest.get("qa", {}).get("validationChecks")
         == validation.get("required"),
         "manifest QA validation-count drift")
    seal = manifest.get("seal", {})
    assigned = seal.get("figureSourceCommitAssigned") is True
    expected_state = ("formal-figure-source-seal" if assigned
                      else "HASH_BOUND_PREPUBLICATION_ARTIFACT")
    need(seal.get("state") == expected_state, "manifest seal state drift")
    need(validation.get("sealState") == expected_state,
         "validation seal state drift")
    if assigned:
        figure_source_commit = seal.get("figureSourceCommit")
        need(isinstance(figure_source_commit, str),
             "assigned figure source commit is not a string")
        need(manifest.get("status") == "formal"
             and manifest.get("publicationStatus") == "staged",
             "formal manifest publication state drift")
        need(seal.get("figureSourceCommitBound") is True
             and seal.get("requiresParentFigureSourceCommitFinalReseal") is False
             and seal.get("requiresFigureSourceCommitFinalReseal") is False,
             "formal reseal boundary drift")
        need(seal.get("figureSourceBindings") == expected_figure_bindings,
             "figure source bindings drift")
        need(len(expected_figure_bindings) == 21,
             "formal figure source binding inventory drift")
        need(manifest.get("git", {}).get("sourceCommit") == figure_source_commit
             and manifest.get("git", {}).get("figureSourceCommit") == figure_source_commit
             and manifest.get("git", {}).get("figureSourceCommitBound") is True
             and manifest.get("git", {}).get("dirtyAtCertifiedRun") is False,
             "formal git source boundary drift")
    else:
        need(manifest.get("status") == "draft"
             and manifest.get("publicationStatus") == "prepublication",
             "prepublication manifest state drift")
        need(seal.get("figureSourceCommitBound") is False
             and seal.get("figureSourceBindings") == []
             and seal.get("requiresParentFigureSourceCommitFinalReseal") is True
             and seal.get("requiresFigureSourceCommitFinalReseal") is True,
             "prepublication reseal boundary drift")

    hash_records = list(manifest.get("data", []))
    hash_records.extend(manifest.get("figure", {}).get("outputs", []))
    for item in hash_records:
        path = HERE / item["path"]
        need(path.is_file() and sha256(path) == item["sha256"],
             "manifest-bound file drift: " + item["path"])
    repository = context["repository"]
    for item in manifest.get("sourceData", []):
        path = repository / item["fileName"]
        need(path.is_file() and sha256(path) == item["sha256"],
             "manifest source-data drift: " + item["fileName"])

    expected_names = sorted(path.name for path in HERE.iterdir()
                            if path.is_file() and path.name != "SHA256SUMS")
    parsed: dict[str, str] = {}
    for line in (HERE / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        need(name not in parsed, "duplicate SHA256SUMS entry: " + name)
        parsed[name] = digest
    need(sorted(parsed) == expected_names, "SHA256SUMS inventory drift")
    for name, expected in parsed.items():
        need(sha256(HERE / name) == expected, "SHA256SUMS mismatch: " + name)
    return {
        "figureSourceBindings": len(expected_figure_bindings),
        "figureSourceCommitAssigned": assigned,
        "manifestHashRecords": len(hash_records),
        "sha256SumsEntries": len(parsed),
        "sourceDataBindings": len(manifest.get("sourceData", [])),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", type=Path, default=DEFAULT_REPOSITORY)
    parser.add_argument("--confirm-visual-qa", action="store_true")
    parser.add_argument("--figure-source-commit", default="")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    need(not (args.verify_only and args.figure_source_commit),
         "--verify-only reads the stored seal; do not pass --figure-source-commit")
    need(args.confirm_visual_qa != args.verify_only,
         "choose exactly one validation mode")
    repository = args.repository.resolve()
    checks, context = validate_content(repository)
    context["repository"] = repository
    actual_files = {path.name for path in HERE.iterdir() if path.is_file()}
    need(actual_files == EXPECTED_FILES,
         "package inventory mismatch: " + repr(sorted(actual_files ^ EXPECTED_FILES)))
    need(all(path.is_file() for path in HERE.iterdir()),
         "package contains a subdirectory or special entry")
    need(len(SOURCE_FILES) == 10 and len(RAW_FILES) == 11
         and len(METADATA_FILES) == 4 and len(BOUND_FILES) == 21,
         "two-commit figure inventory drift")

    if args.verify_only:
        stored_manifest = load_json(HERE / "manifest.json")
        stored_seal = stored_manifest.get("seal", {})
        stored_bindings: list[dict[str, object]] = []
        if stored_seal.get("figureSourceCommitAssigned") is True:
            stored_commit = stored_seal.get("figureSourceCommit")
            need(isinstance(stored_commit, str),
                 "stored figure source commit is not a string")
            stored_bindings = figure_source_bindings(repository, stored_commit)
            add(checks, "figure-source-commit-bound", len(stored_bindings) == 21,
                commit=stored_commit, boundFiles=len(stored_bindings))
            add(checks, "figure-source-blob-byte-identity", True,
                blobObjectIds=[item["gitBlobObjectId"] for item in stored_bindings])
            add(checks, "figure-source-bound-scope-clean", True,
                paths=[item["path"] for item in stored_bindings])
        seal_report = verify_seal(checks, context, stored_bindings)
        print(json.dumps({
            "checks": len(checks),
            "figureId": FIGURE_ID,
            "mode": "verify-only",
            "seal": seal_report,
            "status": "PASS",
        }, indent=2, sort_keys=True))
        return 0

    figure_source_commit = args.figure_source_commit or None
    bindings: list[dict[str, object]] = []
    if figure_source_commit is not None:
        bindings = figure_source_bindings(repository, figure_source_commit)
        add(checks, "figure-source-commit-bound", len(bindings) == 21,
            commit=figure_source_commit, boundFiles=len(bindings))
        add(checks, "figure-source-blob-byte-identity", True,
            blobObjectIds=[item["gitBlobObjectId"] for item in bindings])
        add(checks, "figure-source-bound-scope-clean", True,
            paths=[item["path"] for item in bindings])
    validation = build_validation(checks, visual_confirmed=True,
                                  figure_source_commit=figure_source_commit)
    qa_report = build_qa_report(validation, context, figure_source_commit)
    (HERE / "validation.json").write_text(canonical(validation), encoding="utf-8")
    (HERE / "qa-report.md").write_text(qa_report, encoding="utf-8")
    manifest = build_manifest(context, validation, figure_source_commit, bindings)
    (HERE / "manifest.json").write_text(canonical(manifest), encoding="utf-8")
    (HERE / "SHA256SUMS").write_text(sums_text(), encoding="utf-8")
    seal_report = verify_seal(checks, context, bindings)
    print(json.dumps({
        "checks": len(checks),
        "figureSourceCommit": figure_source_commit,
        "figureId": FIGURE_ID,
        "mode": "write-seal",
        "seal": seal_report,
        "status": "PASS",
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
