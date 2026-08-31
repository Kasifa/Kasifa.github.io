#!/usr/bin/env python3
"""Fail-closed independent validation for the R0.73Q figure package."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version as package_version
import json
import math
from pathlib import Path
import re
import subprocess
import sys
from typing import Any


def bootstrap() -> None:
    for index, value in enumerate(sys.argv):
        if value == "--deps" and index + 1 < len(sys.argv):
            sys.path.insert(0, str(Path(sys.argv[index + 1]).resolve()))
            return
        if value.startswith("--deps="):
            sys.path.insert(0, str(Path(value.split("=", 1)[1]).resolve()))
            return


bootstrap()
from PIL import Image  # type: ignore  # noqa: E402


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
FIGURE_ID = "fig-r073q-heat-flow-separation"
SOURCE_FILES = {
    "README.md",
    "caption.md",
    "chart-contract-and-source-data.md",
    "command.txt",
    "config.json",
    "contract.json",
    "plot.py",
    "qa-protocol.md",
    "requirements.txt",
    "validate.py",
}
RAW_FILES = {
    "source-data.csv",
    "figure.pdf",
    "figure.svg",
    "figure.png",
    "qa-final-size.png",
    "qa-grayscale.png",
    "qa-pdf.png",
    "environment.json",
    "results.json",
    "progress.ndjson",
    "resource-log.ndjson",
}
METADATA_FILES = {
    "validation.json",
    "manifest.json",
    "qa-report.md",
    "SHA256SUMS",
}
PACKAGE_FILES = SOURCE_FILES | RAW_FILES | METADATA_FILES
EXPECTED_DEPENDENCIES = {
    "matplotlib": "3.10.6",
    "numpy": "2.5.2",
    "pillow": "12.3.0",
    "pypdf": "6.10.0",
    "pypdfium2": "5.13.0",
}
CSV_FIELDS = (
    "record_type",
    "sample_index",
    "j",
    "N",
    "l2_norm",
    "heat_trace_norm",
    "hhalf_seminorm",
    "heat_to_l2_ratio",
    "hhalf_to_l2_ratio",
    "hhalf_to_heat_ratio",
    "n",
    "g_l4_fourth",
    "g_l4_norm",
    "fractional_output",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--preseal", action="store_true")
    modes.add_argument("--final", action="store_true")
    parser.add_argument("--confirm-visual-qa", action="store_true")
    parser.add_argument("--source-commit", default="")
    parser.add_argument("--verify-only", action="store_true")
    return parser.parse_args()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink(), "missing regular file: " + str(path))
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), "JSON root is not an object: " + str(path))
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def record(path: Path) -> dict[str, object]:
    return {"path": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}


def close(actual: float, expected: float, tolerance: float = 2e-13) -> bool:
    return math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance)


def exponent_grid(settings: dict[str, Any]) -> list[int]:
    minimum = int(settings["minimumExponent"])
    maximum = int(settings["maximumExponent"])
    step = int(settings["exponentStep"])
    require(0 <= minimum <= maximum and step >= 1, "invalid exponent grid")
    return list(range(minimum, maximum + 1, step))


def read_csv() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    with (HERE / "source-data.csv").open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        require(tuple(reader.fieldnames or ()) == CSV_FIELDS, "source-data.csv schema drift")
        rows = list(reader)
    require(all(set(row) == set(CSV_FIELDS) for row in rows), "source-data row schema drift")
    shear = [row for row in rows if row["record_type"] == "shear_norm"]
    endpoint = [row for row in rows if row["record_type"] == "endpoint_counterexample"]
    require(len(rows) == len(shear) + len(endpoint), "unexpected source-data record type")
    return shear, endpoint


def verify_inventory(*, metadata_required: bool) -> None:
    required = SOURCE_FILES | RAW_FILES
    if metadata_required:
        required |= METADATA_FILES
    actual = {path.name for path in HERE.iterdir() if path.is_file()}
    require(actual <= PACKAGE_FILES, "unexpected file in figure package: " + repr(sorted(actual - PACKAGE_FILES)))
    require(required <= actual, "missing package files: " + repr(sorted(required - actual)))
    require(len(SOURCE_FILES) == 10, "source inventory count drift")
    require(len(RAW_FILES) == 11, "raw asset inventory count drift")
    require(len(PACKAGE_FILES) == 25, "formal package inventory count drift")


def check_formula_data(config: dict[str, Any]) -> tuple[dict[str, bool], dict[str, Any]]:
    shear, endpoint = read_csv()
    checks: dict[str, bool] = {}
    details: dict[str, Any] = {}

    expected_j = exponent_grid(config["panelA"])
    require(len(shear) == len(expected_j), "shear row count drift")
    c6 = (5.0 / 16.0) ** (1.0 / 6.0)
    heat_constant = c6 / (4.0 ** 0.25)
    l2_constant = 2.0 ** -0.5
    errors: list[float] = []
    l2_values: list[float] = []
    heat_values: list[float] = []
    hhalf_values: list[float] = []
    for index, (row, exponent) in enumerate(zip(shear, expected_j, strict=True)):
        require(int(row["sample_index"]) == index, "shear sample index drift")
        require(int(row["j"]) == exponent, "shear exponent grid drift")
        frequency = 2**exponent
        require(int(row["N"]) == frequency, "shear frequency grid drift")
        expected_l2 = l2_constant * frequency ** -0.25
        expected_heat = heat_constant * frequency ** -0.75
        expected_hhalf = l2_constant * frequency ** 0.25
        expected = {
            "l2_norm": expected_l2,
            "heat_trace_norm": expected_heat,
            "hhalf_seminorm": expected_hhalf,
            "heat_to_l2_ratio": expected_heat / expected_l2,
            "hhalf_to_l2_ratio": expected_hhalf / expected_l2,
            "hhalf_to_heat_ratio": expected_hhalf / expected_heat,
        }
        for field, value in expected.items():
            actual = float(row[field])
            require(close(actual, value), "shear formula drift: " + field)
            errors.append(abs(actual / value - 1.0))
        require(all(row[field] == "" for field in (
            "n", "g_l4_fourth", "g_l4_norm", "fractional_output"
        )), "shear row contains endpoint fields")
        l2_values.append(float(row["l2_norm"]))
        heat_values.append(float(row["heat_trace_norm"]))
        hhalf_values.append(float(row["hhalf_seminorm"]))

    checks["shearClosedFormValues"] = max(errors, default=0.0) <= 3e-15
    checks["shearL2StrictlyDecreases"] = all(a > b for a, b in zip(l2_values, l2_values[1:]))
    checks["shearHeatTraceStrictlyDecreases"] = all(a > b for a, b in zip(heat_values, heat_values[1:]))
    checks["shearHhalfStrictlyIncreases"] = all(a < b for a, b in zip(hhalf_values, hhalf_values[1:]))
    checks["shearExactStepRatios"] = all(
        close(l2_values[i + 1] / l2_values[i], 2.0 ** -0.25)
        and close(heat_values[i + 1] / heat_values[i], 2.0 ** -0.75)
        and close(hhalf_values[i + 1] / hhalf_values[i], 2.0 ** 0.25)
        for i in range(len(shear) - 1)
    )
    details["shear"] = {
        "rowCount": len(shear),
        "exponentRange": [expected_j[0], expected_j[-1]],
        "frequencyRange": [2 ** expected_j[0], 2 ** expected_j[-1]],
        "constants": {
            "c6": c6,
            "l2": l2_constant,
            "heatTrace": heat_constant,
        },
        "maximumRelativeFormulaError": max(errors, default=0.0),
        "firstValues": {
            "l2": l2_values[0],
            "heatTrace": heat_values[0],
            "hhalf": hhalf_values[0],
        },
        "lastValues": {
            "l2": l2_values[-1],
            "heatTrace": heat_values[-1],
            "hhalf": hhalf_values[-1],
        },
    }

    expected_n_j = exponent_grid(config["panelC"])
    require(len(endpoint) == len(expected_n_j), "endpoint row count drift")
    log_two = math.log(2.0)
    endpoint_errors: list[float] = []
    g_norms: list[float] = []
    outputs: list[float] = []
    for index, (row, exponent) in enumerate(zip(endpoint, expected_n_j, strict=True)):
        require(int(row["sample_index"]) == index, "endpoint sample index drift")
        require(int(row["j"]) == exponent, "endpoint exponent grid drift")
        n = 2**exponent
        require(int(row["n"]) == n, "endpoint n grid drift")
        g_fourth = 1.0 - log_two / n
        g_norm = g_fourth ** 0.25
        output = n ** 0.75 - n ** -0.25 * log_two
        expected = {
            "g_l4_fourth": g_fourth,
            "g_l4_norm": g_norm,
            "fractional_output": output,
        }
        for field, value in expected.items():
            actual = float(row[field])
            require(close(actual, value), "endpoint formula drift: " + field)
            endpoint_errors.append(abs(actual / value - 1.0))
        require(all(row[field] == "" for field in (
            "N", "l2_norm", "heat_trace_norm", "hhalf_seminorm",
            "heat_to_l2_ratio", "hhalf_to_l2_ratio", "hhalf_to_heat_ratio"
        )), "endpoint row contains shear fields")
        g_norms.append(float(row["g_l4_norm"]))
        outputs.append(float(row["fractional_output"]))

    checks["endpointClosedFormValues"] = max(endpoint_errors, default=0.0) <= 3e-15
    checks["endpointInputBoundedBelowOne"] = all(0.0 < value < 1.0 for value in g_norms)
    checks["endpointInputTendsUpTowardOneOnGrid"] = all(a < b for a, b in zip(g_norms, g_norms[1:]))
    checks["endpointOutputStrictlyIncreases"] = all(a < b for a, b in zip(outputs, outputs[1:]))
    checks["endpointOutputGrowthVisible"] = outputs[-1] > 1000.0 * outputs[0]
    details["endpoint"] = {
        "rowCount": len(endpoint),
        "exponentRange": [expected_n_j[0], expected_n_j[-1]],
        "nRange": [2 ** expected_n_j[0], 2 ** expected_n_j[-1]],
        "maximumRelativeFormulaError": max(endpoint_errors, default=0.0),
        "gNormRange": [min(g_norms), max(g_norms)],
        "fractionalOutputRange": [min(outputs), max(outputs)],
    }
    checks["strictSeparationQuantifierEncoded"] = (
        checks["shearHeatTraceStrictlyDecreases"]
        and checks["shearHhalfStrictlyIncreases"]
        and close(heat_values[-1] / heat_values[0], (2 ** expected_j[-1]) ** -0.75)
        and close(hhalf_values[-1] / hhalf_values[0], (2 ** expected_j[-1]) ** 0.25)
    )
    return checks, details


def surface_facts(config: dict[str, Any]) -> tuple[dict[str, bool], dict[str, Any]]:
    from pypdf import PdfReader  # type: ignore

    width_mm = float(config["widthMillimetres"])
    height_mm = float(config["heightMillimetres"])
    png_dpi = int(config["pngDpi"])
    qa_dpi = int(config["qaDpi"])
    expected_png = [int(width_mm / 25.4 * png_dpi), int(height_mm / 25.4 * png_dpi)]
    expected_qa = [round(width_mm / 25.4 * qa_dpi), round(height_mm / 25.4 * qa_dpi)]
    with Image.open(HERE / "figure.png") as image:
        png_pixels = list(image.size)
        png_mode = image.mode
        png_dpi_actual = list(image.info.get("dpi", (0.0, 0.0)))
    qa: dict[str, Any] = {}
    for name in ("qa-final-size.png", "qa-grayscale.png"):
        with Image.open(HERE / name) as image:
            qa[name] = {"pixels": list(image.size), "mode": image.mode}
    with Image.open(HERE / "qa-pdf.png") as image:
        pdf_qa_pixels = list(image.size)
        pdf_qa_mode = image.mode

    svg = (HERE / "figure.svg").read_text(encoding="utf-8")
    reader = PdfReader(str(HERE / "figure.pdf"))
    require(len(reader.pages) == 1, "figure.pdf must have exactly one page")
    page = reader.pages[0]
    pdf_size_mm = [
        float(page.mediabox.width) * 25.4 / 72.0,
        float(page.mediabox.height) * 25.4 / 72.0,
    ]
    try:
        pdf_image_count = len(list(page.images))
    except Exception:
        pdf_image_count = -1
    checks = {
        "pngPixelDimensions": png_pixels == expected_png,
        "pngDpi": all(abs(float(value) - png_dpi) < 0.1 for value in png_dpi_actual),
        "qaRasterDimensions": all(item["pixels"] == expected_qa for item in qa.values()),
        "pdfOnePage": True,
        "pdfPageDimensions": all(
            abs(actual - expected) < 0.02
            for actual, expected in zip(pdf_size_mm, (width_mm, height_mm), strict=True)
        ),
        "pdfQaRasterDimensions": all(
            abs(actual - expected) <= 2
            for actual, expected in zip(pdf_qa_pixels, expected_qa, strict=True)
        ),
        "pdfHasNoRasterImageObjects": pdf_image_count == 0,
        "svgIsNonemptyVectorSurface": "<svg" in svg and "<path" in svg and len(svg) > 10000,
        "svgRadiusBoundaryVisible": (
            "NO RADIUS ORDERING" in svg and "THE STABLE SET IS A UNION" in svg
        ),
        "svgEndpointBoundaryVisible": (
            "BARE ENDPOINT MAP ONLY" in svg and "NOT KOCH--TATARU THEORY" in svg
        ),
        "svgNotSimulationVisible": "not a Navier--Stokes simulation" in svg,
        "allPanelLettersPresentInSvg": all(f">{letter}<" in svg for letter in ("A", "B", "C")),
    }
    details = {
        "figurePng": {
            "pixels": png_pixels,
            "expectedPixels": expected_png,
            "dpi": png_dpi_actual,
            "mode": png_mode,
        },
        "qaRasters": qa,
        "expectedQaPixels": expected_qa,
        "pdf": {
            "pageSizeMillimetres": pdf_size_mm,
            "qaPixels": pdf_qa_pixels,
            "qaMode": pdf_qa_mode,
            "embeddedImageObjectCount": pdf_image_count,
        },
        "svgBytes": (HERE / "figure.svg").stat().st_size,
    }
    return checks, details


def verify_dependencies(environment: dict[str, Any]) -> dict[str, bool]:
    runtime = {name: package_version(name) for name in EXPECTED_DEPENDENCIES}
    recorded = environment.get("packages", {})
    return {
        "runtimeDependenciesPinned": runtime == EXPECTED_DEPENDENCIES,
        "recordedDependenciesPinned": recorded == EXPECTED_DEPENDENCIES,
        "dgxNotUsed": environment.get("dgxUsed") is False and environment.get("gpu") == "not used",
    }


def verify_results(results: dict[str, Any], details: dict[str, Any]) -> dict[str, bool]:
    facts = results.get("facts", {})
    return {
        "resultsFigureId": results.get("figureId") == FIGURE_ID,
        "resultsMode": results.get("mode") == "render-preseal",
        "resultsFormulaDiagnosticFlag": results.get("isFormulaDiagnostic") is True,
        "resultsNotSimulationFlag": results.get("isNavierStokesSimulation") is False,
        "resultsNotNonlinearCertificateFlag": results.get("isNonlinearPdeCertificate") is False,
        "resultsDgxFlag": results.get("dgxUsed") is False,
        "resultsPdfFlag": results.get("pdfGenerated") is True,
        "resultsRowCount": results.get("rowCount") == (
            details["shear"]["rowCount"] + details["endpoint"]["rowCount"]
        ),
        "resultsShearDirections": all(
            facts.get("shear", {}).get(key) is True
            for key in ("l2StrictlyDecreasing", "heatTraceStrictlyDecreasing", "hhalfStrictlyIncreasing")
        ),
        "resultsEndpointDirections": all(
            facts.get("endpoint", {}).get(key) is True
            for key in ("gNormBelowOne", "gNormStrictlyIncreasing", "fractionalOutputStrictlyIncreasing")
        ),
    }


def verify_contract(contract: dict[str, Any]) -> dict[str, bool]:
    boundary = contract.get("claimBoundary", {})
    required_true = {
        "exactShearNormConstants",
        "strictStructuredDomainSeparation",
        "exactEndpointCounterexample",
    }
    required_false = {
        "oldAndNewRadiiOrdered",
        "navierStokesSimulation",
        "arbitraryL2SmallDataSafe",
        "fullKochTataruTheoryRefuted",
        "nonlinearPdeCertificate",
        "globalRegularityTheorem",
        "finiteTimeSingularity",
        "clayProblemSolved",
    }
    caption = (HERE / "caption.md").read_text(encoding="utf-8")
    source_note = (HERE / "chart-contract-and-source-data.md").read_text(encoding="utf-8")
    return {
        "contractFigureId": contract.get("figureId") == FIGURE_ID,
        "contractPositiveBoundaries": all(boundary.get(key) is True for key in required_true),
        "contractNegativeBoundaries": all(boundary.get(key) is False for key in required_false),
        "captionNoRadiusOrdering": "does not order" in caption and "stable set is their union" in caption,
        "captionEndpointScope": "does not refute the full" in caption,
        "captionDeniesSimulation": "not Navier--Stokes simulations" in caption,
        "captionDeniesMillenniumSolution": "millennium problem has been solved" in caption,
        "sourceNoteStatesNoEmpiricalData": "There is no empirical sample" in source_note,
    }


def source_commit_bindings(source_commit: str) -> list[dict[str, object]]:
    require(re.fullmatch(r"[0-9a-f]{40}", source_commit) is not None,
            "source commit must be a full lowercase 40-hex hash")
    subprocess.run(["git", "cat-file", "-e", source_commit + "^{commit}"],
                   cwd=ROOT, check=True, capture_output=True)
    bindings: list[dict[str, object]] = []
    for name in sorted(SOURCE_FILES):
        path = HERE / name
        relative = path.relative_to(ROOT).as_posix()
        blob = subprocess.check_output(["git", "show", source_commit + ":" + relative], cwd=ROOT)
        require(hashlib.sha256(blob).hexdigest() == sha256(path),
                "committed source differs from working source: " + relative)
        tree = subprocess.check_output(
            ["git", "ls-tree", source_commit, "--", relative], cwd=ROOT, text=True
        ).strip()
        match = re.fullmatch(r"100(?:644|755) blob ([0-9a-f]+)\t" + re.escape(relative), tree)
        require(match is not None, "source commit lacks figure source: " + relative)
        bindings.append({
            "path": relative,
            "bytes": len(blob),
            "sha256": hashlib.sha256(blob).hexdigest(),
            "gitBlobObjectId": match.group(1),
        })
    return bindings


def current_git_state() -> dict[str, Any]:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    relative = HERE.relative_to(ROOT).as_posix()
    dirty = subprocess.check_output(
        ["git", "status", "--porcelain", "--", relative], cwd=ROOT, text=True
    ).strip()
    return {
        "repository": "https://github.com/kasifa/kasifa.github.io",
        "headAtPreseal": commit,
        "packageDirtyAtPreseal": bool(dirty),
        "sourceCommitAssigned": False,
    }


def checksum_lines() -> str:
    files = sorted(path for path in HERE.iterdir() if path.is_file() and path.name != "SHA256SUMS")
    return "".join(f"{sha256(path)}  {path.name}\n" for path in files)


def verify_checksum_file() -> None:
    checksum = HERE / "SHA256SUMS"
    require(checksum.is_file(), "SHA256SUMS is missing")
    parsed: dict[str, str] = {}
    for line in checksum.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        require(match is not None, "invalid SHA256SUMS line")
        parsed[match.group(2)] = match.group(1)
    expected_names = {path.name for path in HERE.iterdir() if path.is_file() and path.name != "SHA256SUMS"}
    require(set(parsed) == expected_names, "SHA256SUMS inventory drift")
    for name, expected in parsed.items():
        require(sha256(HERE / name) == expected, "SHA256SUMS mismatch: " + name)


def build_manifest(
    *,
    final: bool,
    checks: dict[str, bool],
    details: dict[str, Any],
    environment: dict[str, Any],
    results: dict[str, Any],
    source_commit: str,
    bindings: list[dict[str, object]],
) -> dict[str, Any]:
    formal = final and bool(bindings) and all(checks.values())
    git: dict[str, Any]
    if final:
        git = {
            "repository": "https://github.com/kasifa/kasifa.github.io",
            "sourceCommit": source_commit,
            "certificateCommit": source_commit,
            "dirtyAtCertifiedRun": False,
        }
    else:
        git = current_git_state()
    return {
        "schemaVersion": "research-figure-manifest-v1",
        "figureId": FIGURE_ID,
        "status": "formal" if formal else "source-unsealed-preseal",
        "createdAt": utc_now(),
        "analyticalQuestion": "Does the exact smooth shear family vanish in L2 and heat-flow trace while diverging in H1/2, and what scalar endpoint sequence blocks the bare Kato-sup proof route?",
        "supportedClaim": "The exact structured shear sequence tends to zero in L2 and heat-flow trace while diverging in H1/2; the exact endpoint sequence has bounded L4 input and divergent fractional output.",
        "allPrerequisiteChecksPass": formal,
        "allFormulaAndVisualChecksPass": all(checks.values()),
        "sourceCommitAssigned": formal,
        "git": git,
        "computation": {
            "kind": "exact-formula-audit",
            "configuration": "config.json",
            "precision": "IEEE-754 binary64 evaluations of closed-form constants and powers",
            "solver": "none; direct formula evaluation only",
            "command": "plot.py --render-preseal",
            "wallTimeSeconds": results.get("scientificWallTimeSeconds"),
            "monitoring": {
                "enabled": True,
                "reportIntervalSeconds": 0.0,
                "trackedFields": ["stage", "elapsedSeconds", "maximumResidentSetMiB"],
                "progressLog": "progress.ndjson",
                "resourceLog": "resource-log.ndjson",
            },
        },
        "compute": {
            "host": environment.get("host") or "not reported",
            "operatingSystem": environment.get("operatingSystem") or "not reported",
            "cpu": environment.get("cpu") or "not reported",
            "memoryGiB": environment.get("memoryGiB") or "not reported",
            "processes": 1,
            "threadsPerProcess": 1,
            "gpu": "not used",
            "dgxUsed": False,
        },
        "environment": {
            "python": environment.get("python"),
            "packagesLock": "requirements.txt",
            **EXPECTED_DEPENDENCIES,
        },
        "data": [
            {**record(HERE / "source-data.csv"), "schema": "exact shear-norm and endpoint-counterexample rows"},
            {**record(HERE / "results.json"), "schema": "closed-form facts and output inventory"},
            {**record(HERE / "environment.json"), "schema": "runtime and hardware record"},
            {**record(HERE / "progress.ndjson"), "schema": "timestamped generation stages"},
            {**record(HERE / "resource-log.ndjson"), "schema": "timestamped process resource observations"},
        ],
        "figure": {
            "widthMillimetres": 178.0,
            "heightMillimetres": 90.0,
            "outputs": [
                {**record(HERE / "figure.pdf"), "format": "PDF vector"},
                {**record(HERE / "figure.svg"), "format": "SVG vector"},
                {**record(HERE / "figure.png"), "format": "PNG", "dpi": 600},
            ],
        },
        "caption": {"english": "caption.md"},
        "qa": {
            "status": "passed" if formal else "passed-source-unsealed",
            "independentFormulaRecomputation": True,
            "dataCrossChecked": True,
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "pdfRasterInspected": True,
            "qaArtifacts": [
                record(HERE / "qa-final-size.png"),
                record(HERE / "qa-grayscale.png"),
                record(HERE / "qa-pdf.png"),
            ],
        },
        "claimBoundary": load_json(HERE / "contract.json")["claimBoundary"],
        "formulaAudit": details,
        "sourceBindings": bindings,
    }


def qa_report(*, final: bool) -> str:
    sealing = "FORMAL PASS" if final else "SOURCE-UNSEALED PRESEAL"
    return f"""# R0.73Q independent figure QA report

- Independent formula reconstruction: **PASS**.
- CSV schema, row inventory, and exact sampled identities: **PASS**.
- Vector PDF, SVG, 600-dpi PNG, and PDF-raster checks: **PASS**.
- Final-size and grayscale visual inspection: **CONFIRMED**.
- Claim-boundary labels and no-radius-ordering warning: **PASS**.
- DGX or GPU use: **no**.
- Package sealing state: **{sealing}**.

The validator separately recomputed all shear norms and endpoint formulas;
it did not import the plotting code. The present preseal is not formal until
the ten source files are bound to an immutable Git commit and the resulting
metadata and assets are committed in a second stage. The figure is a formula
diagnostic, not a Navier--Stokes simulation or nonlinear PDE certificate.
"""


def verify_manifest_records(manifest: dict[str, Any]) -> None:
    records = (
        list(manifest.get("data", []))
        + list(manifest.get("figure", {}).get("outputs", []))
        + list(manifest.get("qa", {}).get("qaArtifacts", []))
    )
    for item in records:
        path = HERE / str(item.get("path", ""))
        require(path.is_file(), "manifest record is missing: " + str(path))
        require(item.get("sha256") == sha256(path), "manifest hash mismatch: " + path.name)


def main() -> int:
    args = parse_args()
    final = bool(args.final)
    if not args.verify_only:
        require(args.confirm_visual_qa, "metadata generation requires --confirm-visual-qa")
        if final:
            require(bool(args.source_commit), "formal sealing requires --source-commit")
        else:
            require(not args.source_commit, "preseal must not assign a source commit")

    verify_inventory(metadata_required=args.verify_only)
    config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    environment = load_json(HERE / "environment.json")
    results = load_json(HERE / "results.json")
    require(config.get("figureId") == FIGURE_ID, "config figureId drift")

    checks, formula_details = check_formula_data(config)
    surface_checks, surface_details = surface_facts(config)
    checks.update(surface_checks)
    checks.update(verify_dependencies(environment))
    checks.update(verify_results(results, formula_details))
    checks.update(verify_contract(contract))
    details: dict[str, Any] = {**formula_details, "surfaces": surface_details}
    failed = sorted(name for name, passed in checks.items() if passed is not True)
    require(not failed, "validation checks failed: " + repr(failed))

    if args.verify_only:
        validation = load_json(HERE / "validation.json")
        manifest = load_json(HERE / "manifest.json")
        require(validation.get("allAutomatedChecksPass") is True,
                "recorded validation did not pass")
        require(all(validation.get("checks", {}).values()),
                "recorded validation contains a failed check")
        require(manifest.get("figureId") == FIGURE_ID, "manifest figureId drift")
        expected_status = "formal" if final else "source-unsealed-preseal"
        require(manifest.get("status") == expected_status, "manifest status drift")
        if final:
            source_commit = str(manifest.get("git", {}).get("sourceCommit", ""))
            bindings = source_commit_bindings(source_commit)
            require(manifest.get("sourceBindings") == bindings, "recorded source bindings drift")
        else:
            require(manifest.get("sourceBindings") == [], "preseal must not contain source bindings")
            require(manifest.get("sourceCommitAssigned") is False,
                    "preseal must not claim a source commit")
        verify_manifest_records(manifest)
        verify_checksum_file()
        print(canonical({
            "figureId": FIGURE_ID,
            "mode": "final" if final else "preseal",
            "status": "verified",
            "allAutomatedChecksPass": True,
            "recordedQaStatus": manifest.get("qa", {}).get("status"),
        }), end="")
        return 0

    bindings: list[dict[str, object]] = []
    if final:
        bindings = source_commit_bindings(args.source_commit)
    validation = {
        "schemaVersion": "r073q-heat-flow-separation-validation-v1",
        "figureId": FIGURE_ID,
        "createdAt": utc_now(),
        "mode": "final" if final else "preseal",
        "status": "formal-passed" if final else "source-unsealed-preseal-passed",
        "allAutomatedChecksPass": True,
        "independentFormulaRecomputationPass": True,
        "visualQaConfirmed": True,
        "pdfGenerated": True,
        "pdfQaConfirmed": True,
        "sourceCommitAssigned": final and bool(bindings),
        "checks": checks,
        "details": details,
        "claimBoundary": contract["claimBoundary"],
    }
    (HERE / "validation.json").write_text(canonical(validation), encoding="utf-8")
    manifest = build_manifest(
        final=final,
        checks=checks,
        details=details,
        environment=environment,
        results=results,
        source_commit=args.source_commit,
        bindings=bindings,
    )
    (HERE / "manifest.json").write_text(canonical(manifest), encoding="utf-8")
    (HERE / "qa-report.md").write_text(qa_report(final=final), encoding="utf-8")
    (HERE / "SHA256SUMS").write_text(checksum_lines(), encoding="utf-8")
    verify_inventory(metadata_required=True)
    verify_checksum_file()
    print(canonical({
        "figureId": FIGURE_ID,
        "mode": "final" if final else "preseal",
        "status": validation["status"],
        "allAutomatedChecksPass": True,
        "visualQaConfirmed": True,
        "pdfGenerated": True,
    }), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
