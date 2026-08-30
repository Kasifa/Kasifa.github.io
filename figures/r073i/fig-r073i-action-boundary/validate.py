#!/usr/bin/env python3
"""Independently validate the formal R0.73I finite figure package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import sys
from typing import Any, Mapping


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FIGURE_ID = "fig-r073i-action-boundary"
EVIDENCE_CLASS = "finite-binary64-galerkin-diagnostic-only"
SOURCE_FILES = {
    "README.md",
    "caption.md",
    "command.txt",
    "config.json",
    "contract.json",
    "plot.py",
    "qa-protocol.md",
    "qa-report.md",
    "requirements.txt",
    "validate.py",
}
GENERATED_FILES = {
    "source-data.csv",
    "figure.pdf",
    "figure.svg",
    "figure.png",
    "qa-final-size.png",
    "qa-grayscale.png",
    "qa-pdf.png",
    "environment.json",
    "progress.ndjson",
    "results.json",
    "manifest.json",
    "SHA256SUMS",
}
DATA_FIELDS = (
    "panel",
    "recordKind",
    "series",
    "evidenceClass",
    "windowId",
    "endpointExpression",
    "endpoint",
    "endpointRole",
    "N",
    "quadratureOrder",
    "Lambda",
    "x",
    "y",
    "finiteAction",
    "finiteAverageRate",
    "finiteWkbCorrection",
    "residualLogGainMinusLambdaAction",
    "residualMinusWkb",
    "sourcePath",
    "sourceSha256",
    "sourceRowKey",
    "note",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--require-formal", action="store_true")
    return parser.parse_args()


ARGS = parse_args()
if ARGS.deps:
    sys.path.insert(0, ARGS.deps)

from PIL import Image, ImageStat  # noqa: E402
from pypdf import PdfReader  # noqa: E402


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink(), f"required JSON absent: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"JSON root is not an object: {path}")
    return value


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    require(path.is_file() and not path.is_symlink(), f"required CSV absent: {path}")
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        fields = list(reader.fieldnames or ())
        return fields, list(reader)


def close(left: object, right: object, tolerance: float = 2.0e-15) -> bool:
    return math.isclose(float(left), float(right), rel_tol=0.0, abs_tol=tolerance)


def validate_claim_boundary(boundary: Mapping[str, object]) -> None:
    require(
        set(key for key, value in boundary.items() if value is True)
        == {
            "formalFiniteDiagnosticFigure",
            "experimentInputsPassedTheirFiniteValidator",
        },
        "figure claim boundary true-set drift",
    )
    require(
        all(isinstance(value, bool) for value in boundary.values()),
        "claim boundary values must be booleans",
    )


def validate_ledger() -> None:
    ledger = HERE / "SHA256SUMS"
    require(ledger.is_file() and not ledger.is_symlink(), "SHA256SUMS is absent")
    names = []
    for line in ledger.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/\\\r\n]+)", line)
        require(match is not None, f"malformed SHA256SUMS row: {line}")
        expected, name = match.groups()
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), f"ledger target absent: {name}")
        require(sha256(path) == expected, f"ledger hash drift: {name}")
        names.append(name)
    actual = sorted(
        path.name for path in HERE.iterdir()
        if path.is_file() and path.name != "SHA256SUMS"
    )
    require(names == sorted(set(names)), "ledger names are not unique and sorted")
    require(names == actual, "ledger does not cover the exact flat package")
    expected_inventory = sorted((SOURCE_FILES | GENERATED_FILES) - {"SHA256SUMS"})
    require(actual == expected_inventory, "formal figure inventory drift")
    require(not any(path.is_dir() for path in HERE.iterdir()), "package must remain flat")


def validate_bindings(
    rows: list[dict[str, object]],
    base: Path,
    expected_names: set[str] | None = None,
) -> None:
    paths = []
    for row in rows:
        relative = str(row.get("path", ""))
        path = base / relative
        require(path.is_file() and not path.is_symlink(), f"binding target absent: {relative}")
        require(int(row.get("bytes", -1)) == path.stat().st_size, f"binding size drift: {relative}")
        require(str(row.get("sha256", "")) == sha256(path), f"binding hash drift: {relative}")
        paths.append(relative)
    require(paths == sorted(paths) or len(paths) == len(set(paths)), "binding paths repeat")
    require(len(paths) == len(set(paths)), "binding paths repeat")
    if expected_names is not None:
        require(set(paths) == expected_names, "binding inventory drift")


def validate_source_data(
    config: Mapping[str, Any],
) -> dict[str, object]:
    fields, rows = read_csv(HERE / "source-data.csv")
    require(tuple(fields) == DATA_FIELDS, "source-data header drift")
    windows = list(config["windows"])
    cutoffs = [int(value) for value in config["cutoffs"]]
    lambdas = [int(value) for value in config["lambdas"]]
    order = int(config["primaryQuadratureOrder"])
    primary_n = int(config["primaryCutoff"])
    expected_count = len(windows) * len(cutoffs) + 2 + len(windows) * len(lambdas) + 2
    require(len(rows) == expected_count, "source-data row count drift")

    action_path = ROOT / config["inputs"]["actionRows"]
    gain_path = ROOT / config["inputs"]["gainRows"]
    _, action_rows = read_csv(action_path)
    _, gain_rows = read_csv(gain_path)
    action_digest = sha256(action_path)
    gain_digest = sha256(gain_path)
    finite_a = [row for row in rows if row["recordKind"] == "finite-average-action"]
    finite_b = [row for row in rows if row["recordKind"] == "finite-residual-minus-wkb"]
    require(len(finite_a) == 9 and len(finite_b) == 15, "finite panel row inventory drift")

    seen_a = set()
    for row in finite_a:
        key = (row["windowId"], int(row["N"]))
        require(key not in seen_a, f"duplicate Panel A row: {key}")
        seen_a.add(key)
        matches = [
            source for source in action_rows
            if source["windowId"] == key[0]
            and int(source["N"]) == key[1]
            and int(source["quadratureOrder"]) == order
            and source["smokeMode"] == "false"
        ]
        require(len(matches) == 1, f"upstream Panel A row is not unique: {key}")
        source = matches[0]
        require(row["evidenceClass"] == EVIDENCE_CLASS, "Panel A evidence class drift")
        require("finite diagnostic only" in row["note"].lower(), "Panel A finite label absent")
        require(row["sourceSha256"] == action_digest, "Panel A source digest drift")
        require(row["endpointRole"] == source["endpointRole"], "Panel A endpoint role drift")
        for field in (
            "endpoint", "finiteAction", "finiteAverageRate", "finiteWkbCorrection"
        ):
            require(close(row[field], source[field]), f"Panel A numeric drift: {key}, {field}")
        require(close(row["y"], source["finiteAverageRate"]), "Panel A y-value drift")
    require(seen_a == {(window, n_cut) for window in windows for n_cut in cutoffs},
            "Panel A grid is incomplete")

    seen_b = set()
    for row in finite_b:
        key = (row["windowId"], int(row["Lambda"]))
        require(key not in seen_b, f"duplicate Panel B row: {key}")
        seen_b.add(key)
        matches = [
            source for source in gain_rows
            if source["gridKind"] == "primary"
            and source["windowId"] == key[0]
            and int(source["N"]) == primary_n
            and int(source["Lambda"]) == key[1]
            and source["smokeMode"] == "false"
        ]
        require(len(matches) == 1, f"upstream Panel B row is not unique: {key}")
        source = matches[0]
        require(row["evidenceClass"] == EVIDENCE_CLASS, "Panel B evidence class drift")
        require("finite diagnostic only" in row["note"].lower(), "Panel B finite label absent")
        require(row["sourceSha256"] == gain_digest, "Panel B source digest drift")
        require(float(row["y"]) > 0.0, "Panel B log datum is not positive")
        for field in (
            "endpoint", "finiteAction", "finiteAverageRate", "finiteWkbCorrection",
            "residualLogGainMinusLambdaAction", "residualMinusWkb",
        ):
            require(close(row[field], source[field]), f"Panel B numeric drift: {key}, {field}")
        require(close(row["y"], source["residualMinusWkb"]), "Panel B y-value drift")
    require(seen_b == {(window, value) for window in windows for value in lambdas},
            "Panel B grid is incomplete")

    references = {row["recordKind"]: row for row in rows if row["panel"] == "A" and row not in finite_a}
    require(set(references) == {
        "analytic-upper-bound-reference", "inherited-rate-reference"
    }, "Panel A reference inventory drift")
    require(close(references["analytic-upper-bound-reference"]["y"], math.sqrt(19.0 / 180.0)),
            "c_H(0) reference drift")
    require(close(references["inherited-rate-reference"]["y"], 0.17035),
            "r reference drift")
    for row in references.values():
        source_path = ROOT / row["sourcePath"]
        require(row["sourceSha256"] == sha256(source_path), "reference source digest drift")

    guides = [row for row in rows if row["recordKind"] == "visual-slope-guide"]
    require(len(guides) == 2, "slope guide inventory drift")
    guide_constant = float(config["panelB"]["inverseLambdaGuideConstant"])
    for row in guides:
        require(row["evidenceClass"] == "visual-guide-only", "guide evidence class drift")
        require("not a fit" in row["note"].lower(), "guide non-fit label absent")
        require(close(row["y"], guide_constant / float(row["x"])), "guide value drift")
        require(row["sourceSha256"] == sha256(HERE / "config.json"), "guide config digest drift")

    for window in windows:
        roles = {row["endpointRole"].lower() for row in finite_a if row["windowId"] == window}
        require(len(roles) == 1 and "not" in next(iter(roles)), f"endpoint role is not fail closed: {window}")
    return {
        "rowCount": len(rows),
        "panelAFiniteRows": len(finite_a),
        "panelBFiniteRows": len(finite_b),
        "panelAReferenceRows": len(references),
        "guideRows": len(guides),
    }


def validate_images(config: Mapping[str, Any]) -> dict[str, object]:
    width_mm = float(config["widthMillimetres"])
    height_mm = float(config["heightMillimetres"])
    png_dpi = int(config["pngDpi"])
    qa_dpi = int(config["qaDpi"])
    expected_master = (
        int(width_mm / 25.4 * png_dpi),
        int(height_mm / 25.4 * png_dpi),
    )
    expected_qa = (
        round(width_mm / 25.4 * qa_dpi),
        round(height_mm / 25.4 * qa_dpi),
    )
    expected_pdf_qa = (
        math.ceil(width_mm / 25.4 * qa_dpi),
        math.ceil(height_mm / 25.4 * qa_dpi),
    )
    with Image.open(HERE / "figure.png") as image:
        require(image.size == expected_master, "master PNG pixel dimensions drift")
        dpi = image.info.get("dpi", (0.0, 0.0))
        require(all(abs(float(value) - png_dpi) < 1.0 for value in dpi), "master PNG dpi drift")
    with Image.open(HERE / "qa-final-size.png") as image:
        require(image.size == expected_qa and image.mode == "RGB", "final-size QA surface drift")
    with Image.open(HERE / "qa-grayscale.png") as image:
        require(image.size == expected_qa and image.mode == "L", "grayscale QA surface drift")
        grayscale_std = float(ImageStat.Stat(image).stddev[0])
        require(grayscale_std >= 20.0, "grayscale QA surface has inadequate contrast")
    with Image.open(HERE / "qa-pdf.png") as image:
        require(image.size == expected_pdf_qa, "PDF QA raster dimensions drift")
    return {
        "masterPixels": list(expected_master),
        "qaPixels": list(expected_qa),
        "pdfQaPixels": list(expected_pdf_qa),
        "grayscaleStandardDeviation": grayscale_std,
    }


def validate_vectors(config: Mapping[str, Any]) -> dict[str, object]:
    reader = PdfReader(str(HERE / "figure.pdf"))
    require(len(reader.pages) == 1, "formal PDF is not one page")
    page = reader.pages[0]
    width_pt = float(page.mediabox.width)
    height_pt = float(page.mediabox.height)
    width_mm = width_pt / 72.0 * 25.4
    height_mm = height_pt / 72.0 * 25.4
    require(abs(width_mm - float(config["widthMillimetres"])) < 0.02, "PDF width drift")
    require(abs(height_mm - float(config["heightMillimetres"])) < 0.02, "PDF height drift")
    metadata = reader.metadata or {}
    require(EVIDENCE_CLASS in str(metadata.get("/Subject", "")), "PDF evidence metadata absent")

    svg = (HERE / "figure.svg").read_text(encoding="utf-8")
    require("<svg" in svg and "finite-binary64-galerkin-diagnostic-only" in svg,
            "SVG structure or evidence metadata absent")
    require("finite diagnostic only" in svg.lower(), "SVG finite diagnostic label absent")
    require("not $d_0$" in svg.lower() and "not endpoint" in svg.lower(),
            "SVG endpoint qualifiers absent")
    declared = {value.lower() for value in config["palette"].values()}
    allowed = declared | {"#000000"}
    used = {value.lower() for value in re.findall(r"#[0-9a-fA-F]{6}", svg)}
    require(used <= allowed, f"SVG contains undeclared colors: {sorted(used - allowed)}")
    require(config["palette"]["blue"].lower() in used, "blue palette root unused")
    require(config["palette"]["orange"].lower() in used, "orange palette root unused")
    return {
        "pdfPages": 1,
        "pdfWidthMillimetres": width_mm,
        "pdfHeightMillimetres": height_mm,
        "svgDeclaredColors": sorted(used),
    }


def validate_progress() -> int:
    rows = []
    for line in (HERE / "progress.ndjson").read_text(encoding="utf-8").splitlines():
        value = json.loads(line)
        require(isinstance(value, dict), "progress row is not an object")
        rows.append(value)
    require(len(rows) >= 5, "progress log is incomplete")
    require([row["sequence"] for row in rows] == list(range(1, len(rows) + 1)),
            "progress sequence drift")
    require(rows[0]["event"] == "start" and rows[-1]["event"] == "complete",
            "progress terminal events drift")
    require(rows[-1].get("finiteDiagnosticOnly") is True,
            "progress terminal evidence boundary absent")
    return len(rows)


def main() -> int:
    if not ARGS.require_formal:
        raise SystemExit("strict validation requires --require-formal")
    checks: dict[str, bool] = {}
    validate_ledger()
    checks["sha256LedgerExact"] = True

    config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    results = load_json(HERE / "results.json")
    manifest = load_json(HERE / "manifest.json")
    environment = load_json(HERE / "environment.json")
    require(config.get("figureId") == FIGURE_ID, "config figure ID drift")
    require(contract.get("figureId") == FIGURE_ID, "contract figure ID drift")
    require(results.get("figureId") == FIGURE_ID, "results figure ID drift")
    require(manifest.get("figureId") == FIGURE_ID, "manifest figure ID drift")
    require(manifest.get("status") == "formal", "manifest is not formal")
    require(results.get("status") == "passed", "results status is not passed")
    require(
        all(value.get("evidenceClass") == EVIDENCE_CLASS for value in (contract, results, manifest)),
        "evidence class drift",
    )
    validate_claim_boundary(contract["claimBoundary"])
    require(results["claimBoundary"] == contract["claimBoundary"], "results boundary drift")
    require(manifest["claimBoundary"] == contract["claimBoundary"], "manifest boundary drift")
    checks["claimBoundaryFailClosed"] = True

    validate_bindings(
        manifest["sourceBindings"], HERE, SOURCE_FILES
    )
    input_names = set(config["inputs"].values())
    validate_bindings(manifest["inputBindings"], ROOT, input_names)
    expected_outputs = GENERATED_FILES - {"manifest.json", "SHA256SUMS"}
    validate_bindings(manifest["outputBindings"], HERE, expected_outputs)
    checks["manifestBindingsExact"] = True

    source_data = validate_source_data(config)
    checks["sourceDataRecomputedFromExperiment"] = True
    image_qa = validate_images(config)
    checks["rasterDimensionsAndGrayscalePass"] = True
    vector_qa = validate_vectors(config)
    checks["vectorDimensionsMetadataAndPalettePass"] = True
    progress_rows = validate_progress()
    checks["progressLogComplete"] = True

    require(
        results["sourceDataRows"] == source_data["rowCount"],
        "results source-data count drift",
    )
    require(results["renderQa"]["textBoundingBoxesWithinCanvas"] is True,
            "renderer recorded text clipping")
    require(results["renderQa"]["manualVisualInspection"] is True,
            "results do not record explicit visual inspection")
    require(manifest["qa"]["visualInspectionExplicit"] is True,
            "manifest does not record explicit visual inspection")
    qa_report = (HERE / "qa-report.md").read_text(encoding="utf-8")
    require("Status: **PASS**" in qa_report and "inspected" in qa_report.lower(),
            "manual QA report is not passed")
    checks["explicitVisualInspectionPass"] = True

    require(environment.get("randomnessUsed") is False, "environment randomness flag drift")
    require(environment.get("sourceCommit") == manifest.get("sourceCommit"),
            "environment/manifest source commit drift")
    require(re.fullmatch(r"[0-9a-f]{40}", str(manifest.get("sourceCommit", ""))) is not None,
            "source commit is malformed")
    checks["environmentAndSourceCommitRecorded"] = True

    prose = "\n".join(
        (HERE / name).read_text(encoding="utf-8")
        for name in ("README.md", "caption.md", "qa-protocol.md")
    ).lower()
    require("finite" in prose and "not `d0`" in prose and "not the inherited" in prose,
            "reader-facing boundary prose drift")
    require("not a regression" in prose and "not a fit" in prose,
            "visual-guide boundary prose drift")
    checks["readerFacingBoundaryLabelsPass"] = True

    output = {
        "schemaVersion": "r073i-action-boundary-validation-v1",
        "figureId": FIGURE_ID,
        "status": "passed",
        "evidenceClass": EVIDENCE_CLASS,
        "allChecksPass": all(checks.values()),
        "checks": checks,
        "sourceData": source_data,
        "imageQa": image_qa,
        "vectorQa": vector_qa,
        "progressRows": progress_rows,
        "continuumConclusion": "none; the figure and validation cover only the archived finite diagnostic plus explicitly sourced analytic reference lines",
    }
    print(json.dumps(output, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
