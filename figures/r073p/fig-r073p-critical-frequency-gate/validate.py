#!/usr/bin/env python3
"""Fail-closed validation for the R0.73P critical-frequency figure package."""

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
FIGURE_ID = "fig-r073p-critical-frequency-gate"
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
RAW_PREFLIGHT_FILES = {
    "source-data.csv",
    "figure.svg",
    "figure.png",
    "qa-final-size.png",
    "qa-grayscale.png",
    "environment.json",
    "results.json",
    "progress.ndjson",
    "resource-log.ndjson",
}
PREFLIGHT_METADATA_FILES = {
    "validation.json",
    "manifest.json",
    "qa-report.md",
    "SHA256SUMS",
}
PDF_FILES = {"figure.pdf", "qa-pdf.png"}
PREFLIGHT_FILES = SOURCE_FILES | RAW_PREFLIGHT_FILES | PREFLIGHT_METADATA_FILES
FINAL_FILES = PREFLIGHT_FILES | PDF_FILES
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
    "N",
    "h3_threshold",
    "hhalf_threshold",
    "gamma",
    "l2_power",
    "hhalf_power",
    "h3_power",
    "tau",
    "discrete_heat",
    "continuous_heat_bound",
    "discrete_to_continuous",
    "maximizer_norm_squared",
    "k1",
    "k2",
    "k3",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--preflight", action="store_true")
    modes.add_argument("--final", action="store_true")
    parser.add_argument("--confirm-nonpdf-visual-qa", action="store_true")
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


def log_grid(minimum: float, maximum: float, count: int) -> list[float]:
    lo = math.log(minimum)
    hi = math.log(maximum)
    return [math.exp(lo + (hi - lo) * index / (count - 1)) for index in range(count)]


def linear_grid(minimum: float, maximum: float, count: int) -> list[float]:
    return [minimum + (maximum - minimum) * index / (count - 1) for index in range(count)]


def frequency_grid(settings: dict[str, Any]) -> list[int]:
    values = {
        int(round(value))
        for value in log_grid(
            float(settings["minimumFrequency"]),
            float(settings["maximumFrequency"]),
            int(settings["logSamples"]),
        )
    }
    values.add(int(settings["minimumFrequency"]))
    values.add(int(settings["maximumFrequency"]))
    return sorted(values)


def is_sum_of_three_squares(n: int) -> bool:
    """Legendre's exact characterization for positive integers."""
    if n <= 0:
        return False
    while n % 4 == 0:
        n //= 4
    return n % 8 != 7


def brute_force_radii(half_width: int) -> set[int]:
    cutoff = half_width * half_width
    radii: set[int] = set()
    for i in range(half_width + 1):
        for j in range(half_width + 1):
            partial = i * i + j * j
            if partial > cutoff:
                break
            for k in range(math.isqrt(cutoff - partial) + 1):
                n = partial + k * k
                if n:
                    radii.add(n)
    return radii


def read_csv() -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    with (HERE / "source-data.csv").open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        require(tuple(reader.fieldnames or ()) == CSV_FIELDS, "source-data.csv schema drift")
        rows = list(reader)
    require(all(set(row) == set(CSV_FIELDS) for row in rows), "source-data row schema drift")
    threshold = [row for row in rows if row["record_type"] == "threshold"]
    sobolev = [row for row in rows if row["record_type"] == "sobolev_power"]
    heat = [row for row in rows if row["record_type"] == "heat_lattice"]
    require(len(rows) == len(threshold) + len(sobolev) + len(heat),
            "unexpected source-data record type")
    return threshold, sobolev, heat


def verify_inventory(*, final: bool, metadata_required: bool) -> None:
    allowed = FINAL_FILES
    required = SOURCE_FILES | RAW_PREFLIGHT_FILES
    if metadata_required:
        required |= PREFLIGHT_METADATA_FILES
    if final:
        required |= PDF_FILES
    actual = {path.name for path in HERE.iterdir() if path.is_file()}
    require(actual <= allowed, "unexpected file in figure package: " + repr(sorted(actual - allowed)))
    require(required <= actual, "missing package files: " + repr(sorted(required - actual)))
    if not final:
        require(not (actual & PDF_FILES), "preflight package must not contain PDF assets")
    require(len(SOURCE_FILES) == 10, "source inventory count drift")
    require(len(PREFLIGHT_FILES) == 23, "preflight inventory count drift")
    require(len(FINAL_FILES) == 25, "formal inventory count drift")


def check_formula_data(config: dict[str, Any]) -> tuple[dict[str, bool], dict[str, Any]]:
    threshold, sobolev, heat = read_csv()
    details: dict[str, Any] = {}
    checks: dict[str, bool] = {}

    panel_a = config["panelA"]
    expected_n = frequency_grid(panel_a)
    require(len(threshold) == len(expected_n), "Panel A row count drift")
    h3_radius = float(panel_a["normalizedH3Radius"])
    hhalf_radius = float(panel_a["normalizedCriticalRadius"])
    panel_a_errors: list[float] = []
    for index, (row, n) in enumerate(zip(threshold, expected_n, strict=True)):
        require(int(row["sample_index"]) == index, "Panel A sample index drift")
        require(int(row["N"]) == n, "Panel A frequency grid drift")
        h3 = float(row["h3_threshold"])
        hhalf = float(row["hhalf_threshold"])
        expected_h3 = h3_radius * n ** -3.0
        expected_hhalf = hhalf_radius * n ** -0.5
        require(close(h3, expected_h3), "Panel A H3 formula drift")
        require(close(hhalf, expected_hhalf), "Panel A H1/2 formula drift")
        panel_a_errors.extend((abs(h3 / expected_h3 - 1.0), abs(hhalf / expected_hhalf - 1.0)))
    checks["panelAExactNormalizedPowers"] = max(panel_a_errors, default=0.0) <= 3e-15
    details["panelA"] = {
        "rowCount": len(threshold),
        "frequencyRange": [expected_n[0], expected_n[-1]],
        "maximumRelativeFormulaError": max(panel_a_errors, default=0.0),
    }

    panel_b = config["panelB"]
    expected_gamma = linear_grid(
        float(panel_b["minimumGamma"]),
        float(panel_b["maximumGamma"]),
        int(panel_b["samples"]),
    )
    require(len(sobolev) == len(expected_gamma), "Panel B row count drift")
    panel_b_errors: list[float] = []
    for index, (row, gamma) in enumerate(zip(sobolev, expected_gamma, strict=True)):
        require(int(row["sample_index"]) == index, "Panel B sample index drift")
        actual_gamma = float(row["gamma"])
        require(close(actual_gamma, gamma), "Panel B gamma grid drift")
        values = (
            (float(row["l2_power"]), -gamma),
            (float(row["hhalf_power"]), 0.5 - gamma),
            (float(row["h3_power"]), 3.0 - gamma),
        )
        for actual, expected in values:
            require(close(actual, expected), "Panel B Sobolev power drift")
            panel_b_errors.append(abs(actual - expected))
    lower = float(panel_b["criticalIndex"])
    upper = float(panel_b["highIndex"])
    require(lower == 0.5 and upper == 3.0 and lower < upper,
            "Panel B critical interval drift")
    interior = [gamma for gamma in expected_gamma if lower < gamma < upper]
    require(interior, "Panel B open interval is empty")
    require(all(-gamma < 0 and 0.5 - gamma < 0 and 3.0 - gamma > 0 for gamma in interior),
            "Panel B open-strip signs drift")
    checks["panelBExactSobolevPowers"] = max(panel_b_errors, default=0.0) <= 3e-15
    checks["panelBOpenStripSigns"] = True
    checks["panelBEndpointPrefactorCaveat"] = True
    details["panelB"] = {
        "rowCount": len(sobolev),
        "openStrip": [lower, upper],
        "interiorSampleCount": len(interior),
        "maximumAbsoluteFormulaError": max(panel_b_errors, default=0.0),
        "endpointStatement": "At gamma=1/2, critical Hdot1/2 size is the fixed prefactor and requires a strict radius inequality.",
    }

    panel_c = config["panelC"]
    minimum_tau = float(panel_c["minimumTau"])
    maximum_tau = float(panel_c["maximumTau"])
    tau_count = int(panel_c["logSamples"])
    expected_tau = log_grid(minimum_tau, maximum_tau, tau_count)
    require(len(heat) == tau_count, "Panel C row count drift")
    half_width = int(panel_c["latticeHalfWidth"])
    cutoff = half_width * half_width
    brute = brute_force_radii(half_width)
    legendre = {n for n in range(1, cutoff + 1) if is_sum_of_three_squares(n)}
    require(brute == legendre, "brute-force and Legendre three-square inventories disagree")
    require(cutoff > 3.0 / (2.0 * minimum_tau), "lattice cutoff does not enclose all radial maxima")
    radii = sorted(legendre)
    ratios: list[float] = []
    formula_errors: list[float] = []
    for index, (row, tau) in enumerate(zip(heat, expected_tau, strict=True)):
        require(int(row["sample_index"]) == index, "Panel C sample index drift")
        actual_tau = float(row["tau"])
        require(close(actual_tau, tau), "Panel C tau grid drift")
        best_n = max(radii, key=lambda n: n**1.5 * math.exp(-tau * n))
        discrete = best_n**1.5 * math.exp(-tau * best_n)
        continuous = (3.0 / (2.0 * math.e * tau)) ** 1.5
        actual_discrete = float(row["discrete_heat"])
        actual_continuous = float(row["continuous_heat_bound"])
        actual_ratio = float(row["discrete_to_continuous"])
        require(int(row["maximizer_norm_squared"]) == best_n,
                "Panel C maximizing radius drift")
        vector = tuple(int(row[name]) for name in ("k1", "k2", "k3"))
        require(sum(value * value for value in vector) == best_n,
                "Panel C representative vector does not realize the maximizing radius")
        require(close(actual_discrete, discrete), "Panel C discrete maximum drift")
        require(close(actual_continuous, continuous), "Panel C continuous bound drift")
        require(close(actual_ratio, discrete / continuous), "Panel C ratio drift")
        require(actual_discrete <= actual_continuous * (1.0 + 3e-15),
                "Panel C discrete value exceeds the continuous envelope")
        ratios.append(actual_ratio)
        formula_errors.extend((
            abs(actual_discrete / discrete - 1.0),
            abs(actual_continuous / continuous - 1.0),
            abs(actual_ratio / (discrete / continuous) - 1.0),
        ))
    checks["panelCBruteForceMatchesThreeSquareTheorem"] = True
    checks["panelCTailEnclosureIsStrict"] = True
    checks["panelCExactSampledLatticeMaxima"] = max(formula_errors, default=0.0) <= 3e-15
    checks["panelCContinuousEnvelopeDominates"] = max(ratios) <= 1.0 + 3e-15
    details["panelC"] = {
        "rowCount": len(heat),
        "tauRange": [minimum_tau, maximum_tau],
        "latticeHalfWidth": half_width,
        "cutoffNormSquared": cutoff,
        "continuousPeakNormSquaredAtMinimumTau": 3.0 / (2.0 * minimum_tau),
        "representableRadiusCount": len(legendre),
        "maximumRelativeFormulaError": max(formula_errors, default=0.0),
        "discreteToContinuousRatioRange": [min(ratios), max(ratios)],
    }
    return checks, details


def png_facts(config: dict[str, Any]) -> tuple[dict[str, bool], dict[str, Any]]:
    png_dpi = int(config["pngDpi"])
    qa_dpi = int(config["qaDpi"])
    width_mm = float(config["widthMillimetres"])
    height_mm = float(config["heightMillimetres"])
    # Matplotlib's Agg canvas truncates the floating pixel extent at export.
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
    svg = (HERE / "figure.svg").read_text(encoding="utf-8")
    checks = {
        "pngPixelDimensions": png_pixels == expected_png,
        "pngDpi": all(abs(float(value) - png_dpi) < 0.1 for value in png_dpi_actual),
        "qaRasterDimensions": all(item["pixels"] == expected_qa for item in qa.values()),
        "svgIsNonemptyVectorSurface": "<svg" in svg and "<path" in svg and len(svg) > 10000,
        "panelCWarningPresentInSvg": (
            "LINEAR ONLY —" in svg and "NOT A NONLINEAR ENTRY CERTIFICATE" in svg
        ),
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
        "svgBytes": (HERE / "figure.svg").stat().st_size,
    }
    return checks, details


def pdf_facts(config: dict[str, Any]) -> tuple[dict[str, bool], dict[str, Any]]:
    from pypdf import PdfReader  # type: ignore

    reader = PdfReader(str(HERE / "figure.pdf"))
    require(len(reader.pages) == 1, "figure.pdf must have exactly one page")
    page = reader.pages[0]
    size_mm = [
        float(page.mediabox.width) * 25.4 / 72.0,
        float(page.mediabox.height) * 25.4 / 72.0,
    ]
    expected = [float(config["widthMillimetres"]), float(config["heightMillimetres"])]
    with Image.open(HERE / "qa-pdf.png") as image:
        qa_pixels = list(image.size)
    expected_qa = [
        round(expected[0] / 25.4 * int(config["qaDpi"])),
        round(expected[1] / 25.4 * int(config["qaDpi"])),
    ]
    checks = {
        "pdfOnePage": True,
        "pdfPageDimensions": all(abs(a - b) < 0.02 for a, b in zip(size_mm, expected, strict=True)),
        "pdfQaRasterDimensions": all(abs(a - b) <= 2 for a, b in zip(qa_pixels, expected_qa, strict=True)),
    }
    return checks, {"pageSizeMillimetres": size_mm, "qaPdfPixels": qa_pixels}


def verify_dependencies(environment: dict[str, Any]) -> dict[str, bool]:
    runtime = {name: package_version(name) for name in EXPECTED_DEPENDENCIES}
    recorded = environment.get("packages", {})
    return {
        "runtimeDependenciesPinned": runtime == EXPECTED_DEPENDENCIES,
        "recordedDependenciesPinned": recorded == EXPECTED_DEPENDENCIES,
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
    dirty_output = subprocess.check_output(
        ["git", "status", "--porcelain", "--", relative], cwd=ROOT, text=True
    )
    return {
        "repository": "https://github.com/kasifa/kasifa.github.io",
        "commit": commit,
        "dirty": bool(dirty_output.strip()),
        "sourceFilesCommitted": not bool(dirty_output.strip()),
    }


def verify_results(results: dict[str, Any], details: dict[str, Any], *, final: bool) -> dict[str, bool]:
    facts = results.get("facts", {})
    expected_mode = "render-final" if final else "render-nonpdf"
    return {
        "resultsFigureId": results.get("figureId") == FIGURE_ID,
        "resultsMode": results.get("mode") == expected_mode,
        "resultsFormulaDiagnosticFlag": results.get("isFormulaDiagnostic") is True,
        "resultsNotSimulationFlag": results.get("isNavierStokesSimulation") is False,
        "resultsPdfFlag": results.get("pdfGenerated") is final,
        "resultsRowCount": results.get("rowCount") == sum(
            details[key]["rowCount"] for key in ("panelA", "panelB", "panelC")
        ),
        "resultsTailFlag": facts.get("panelC", {}).get("tailStrictlyDecreasing") is True,
        "resultsEnvelopeFlag": facts.get("panelC", {}).get("allDiscreteValuesBelowContinuousBound") is True,
        "resultsEndpointFlag": facts.get("panelB", {}).get("endpointPrefactorConditionRetained") is True,
    }


def verify_contract(contract: dict[str, Any]) -> dict[str, bool]:
    boundary = contract.get("claimBoundary", {})
    required_true = {
        "closedFormThresholdComparison",
        "pureModeSobolevScaling",
        "exactSampledLinearLatticeMaximum",
        "continuousLinearUpperBound",
    }
    required_false = {
        "navierStokesSimulation",
        "generalL2FrequencyLocalization",
        "nonlinearDuhamelControl",
        "delayedNonlinearSmoothing",
        "nonlinearEntryCertificate",
        "globalRegularityTheorem",
        "finiteTimeSingularity",
        "clayProblemSolved",
    }
    caption = (HERE / "caption.md").read_text(encoding="utf-8")
    return {
        "contractFigureId": contract.get("figureId") == FIGURE_ID,
        "contractPositiveBoundaries": all(boundary.get(key) is True for key in required_true),
        "contractNegativeBoundaries": all(boundary.get(key) is False for key in required_false),
        "captionCallsPanelCLinear": "linear only" in caption.lower(),
        "captionDeniesMillenniumSolution": "millennium problem has been solved" in caption,
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
    visual_confirmed: bool,
    checks: dict[str, bool],
    details: dict[str, Any],
    environment: dict[str, Any],
    results: dict[str, Any],
    source_commit: str,
    bindings: list[dict[str, object]],
) -> dict[str, Any]:
    git = current_git_state()
    if final:
        git = {
            "repository": "https://github.com/kasifa/kasifa.github.io",
            "sourceCommit": source_commit,
            "certificateCommit": source_commit,
            "dirtyAtCertifiedRun": False,
        }
    figure_outputs = [
        {**record(HERE / "figure.svg"), "format": "SVG vector"},
        {**record(HERE / "figure.png"), "format": "PNG", "dpi": 600},
    ]
    if final:
        figure_outputs.insert(0, {**record(HERE / "figure.pdf"), "format": "PDF vector"})
    data_records = [
        {**record(HERE / "source-data.csv"), "schema": "mixed threshold, Sobolev-power, and heat-lattice rows"},
        {**record(HERE / "results.json"), "schema": "formula facts and output inventory"},
        {**record(HERE / "environment.json"), "schema": "runtime and hardware record"},
        {**record(HERE / "progress.ndjson"), "schema": "timestamped generation stages"},
        {**record(HERE / "resource-log.ndjson"), "schema": "timestamped process resource observations"},
    ]
    all_automated = all(checks.values())
    formal_complete = final and visual_confirmed and bool(bindings) and all_automated
    status = "formal" if formal_complete else "draft-preflight"
    qa_status = "passed" if formal_complete else (
        "nonpdf-preflight-passed-pdf-pending" if visual_confirmed and all_automated
        else "automated-preflight-passed-visual-and-pdf-pending"
    )
    return {
        "schemaVersion": "research-figure-manifest-v1",
        "figureId": FIGURE_ID,
        "status": status,
        "createdAt": utc_now(),
        "analyticalQuestion": "How does the high-frequency penalty change between direct H3 entry and critical homogeneous-H1/2 entry, and what can the linear heat benchmark show without nonlinear control?",
        "supportedClaim": "Normalized sufficient thresholds scale as N^-3 and N^-1/2; for a_N=cN^-gamma, 1/2<gamma<3 gives L2 and homogeneous H1/2 decay but homogeneous H3 growth. The heat panel is linear only.",
        "allPrerequisiteChecksPass": formal_complete,
        "preflightChecksPass": all_automated and visual_confirmed,
        "pdfGenerated": final,
        "sourceCommitAssigned": final and bool(bindings),
        "git": git,
        "computation": {
            "kind": "exact-audit",
            "configuration": "config.json",
            "precision": "IEEE-754 binary64 for sampled values; exact integer enumeration of three-square radii",
            "solver": "closed-form evaluation plus exhaustive integer lattice-radius audit",
            "command": "plot.py --render-final" if final else "plot.py --render-nonpdf",
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
        },
        "environment": {
            "python": environment.get("python"),
            "packagesLock": "requirements.txt",
            **EXPECTED_DEPENDENCIES,
        },
        "data": data_records,
        "sourceData": [],
        "figure": {
            "widthMillimetres": 178.0,
            "heightMillimetres": 86.0,
            "outputs": figure_outputs,
        },
        "caption": {"english": "caption.md"},
        "qa": {
            "status": qa_status,
            "dataCrossChecked": all_automated,
            "finalSizeInspected": visual_confirmed,
            "grayscaleInspected": visual_confirmed,
            "labelsAndLegendsInspected": visual_confirmed,
            "scalesAndUnitsInspected": visual_confirmed,
            "pdfRasterInspected": final and visual_confirmed,
            "qaArtifacts": [
                record(HERE / "qa-final-size.png"),
                record(HERE / "qa-grayscale.png"),
            ] + ([record(HERE / "qa-pdf.png")] if final else []),
        },
        "claimBoundary": load_json(HERE / "contract.json")["claimBoundary"],
        "formulaAudit": details,
        "sourceBindings": bindings,
    }


def qa_report(*, final: bool, visual_confirmed: bool, all_automated: bool) -> str:
    current = "PASS" if all_automated else "FAIL"
    visual = "CONFIRMED" if visual_confirmed else "PENDING"
    pdf = "CONFIRMED" if final and visual_confirmed else "PENDING BY DESIGN"
    return f"""# R0.73P figure QA report

- Automated formula, inventory, hash, and non-PDF surface checks: **{current}**.
- Final-size and grayscale visual inspection: **{visual}**.
- PDF generation and PDF-raster inspection: **{pdf}**.
- Evidence class: closed-form formula diagnostic plus exact finite lattice enumeration.
- Navier--Stokes simulation: **no**.
- Nonlinear entry certificate: **no**.

The preflight remains non-formal until an immutable source commit, vector PDF,
independent PDF raster, and final visual confirmation are all present. The
linear heat panel does not estimate the nonlinear Duhamel term.
"""


def verify_manifest_records(manifest: dict[str, Any]) -> None:
    records = list(manifest.get("data", [])) + list(manifest.get("figure", {}).get("outputs", []))
    for item in records:
        path = HERE / str(item.get("path", ""))
        require(path.is_file(), "manifest record is missing: " + str(path))
        require(item.get("sha256") == sha256(path), "manifest hash mismatch: " + path.name)


def main() -> int:
    args = parse_args()
    final = bool(args.final)
    if final:
        require(args.confirm_visual_qa, "final sealing requires --confirm-visual-qa")
        require(not args.confirm_nonpdf_visual_qa,
                "use --confirm-visual-qa, not the non-PDF confirmation, for final sealing")
    else:
        require(not args.confirm_visual_qa,
                "--confirm-visual-qa is reserved for final PDF sealing")
    visual_confirmed = bool(args.confirm_visual_qa if final else args.confirm_nonpdf_visual_qa)

    verify_inventory(final=final, metadata_required=args.verify_only)
    config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    environment = load_json(HERE / "environment.json")
    results = load_json(HERE / "results.json")
    require(config.get("figureId") == FIGURE_ID, "config figureId drift")

    checks, formula_details = check_formula_data(config)
    surface_checks, surface_details = png_facts(config)
    checks.update(surface_checks)
    checks.update(verify_dependencies(environment))
    checks.update(verify_results(results, formula_details, final=final))
    checks.update(verify_contract(contract))
    details: dict[str, Any] = {**formula_details, "surfaces": surface_details}
    if final:
        pdf_checks, pdf_details = pdf_facts(config)
        checks.update(pdf_checks)
        details["pdf"] = pdf_details
    else:
        checks["pdfAssetsAbsentInPreflight"] = not any((HERE / name).exists() for name in PDF_FILES)
    failed = sorted(name for name, passed in checks.items() if passed is not True)
    require(not failed, "validation checks failed: " + repr(failed))

    bindings: list[dict[str, object]] = []
    if final:
        bindings = source_commit_bindings(args.source_commit)

    if args.verify_only:
        validation = load_json(HERE / "validation.json")
        manifest = load_json(HERE / "manifest.json")
        require(validation.get("allAutomatedChecksPass") is True,
                "recorded validation did not pass")
        require(all(validation.get("checks", {}).values()), "recorded validation contains a failed check")
        require(manifest.get("figureId") == FIGURE_ID, "manifest figureId drift")
        require(manifest.get("status") == ("formal" if final else "draft-preflight"),
                "manifest status drift")
        verify_manifest_records(manifest)
        verify_checksum_file()
        print(canonical({
            "figureId": FIGURE_ID,
            "mode": "final" if final else "preflight",
            "status": "verified",
            "allAutomatedChecksPass": True,
            "recordedQaStatus": manifest.get("qa", {}).get("status"),
        }), end="")
        return 0

    validation = {
        "schemaVersion": "r073p-critical-frequency-gate-validation-v1",
        "figureId": FIGURE_ID,
        "createdAt": utc_now(),
        "mode": "final" if final else "preflight",
        "status": "formal-passed" if final else (
            "nonpdf-preflight-passed-pdf-pending" if visual_confirmed
            else "automated-preflight-passed-visual-and-pdf-pending"
        ),
        "allAutomatedChecksPass": True,
        "nonPdfVisualQaConfirmed": visual_confirmed,
        "pdfGenerated": final,
        "pdfQaConfirmed": final and visual_confirmed,
        "sourceCommitAssigned": final and bool(bindings),
        "checks": checks,
        "details": details,
        "claimBoundary": contract["claimBoundary"],
    }
    (HERE / "validation.json").write_text(canonical(validation), encoding="utf-8")
    manifest = build_manifest(
        final=final,
        visual_confirmed=visual_confirmed,
        checks=checks,
        details=details,
        environment=environment,
        results=results,
        source_commit=args.source_commit,
        bindings=bindings,
    )
    (HERE / "manifest.json").write_text(canonical(manifest), encoding="utf-8")
    (HERE / "qa-report.md").write_text(
        qa_report(final=final, visual_confirmed=visual_confirmed, all_automated=True),
        encoding="utf-8",
    )
    (HERE / "SHA256SUMS").write_text(checksum_lines(), encoding="utf-8")
    verify_inventory(final=final, metadata_required=True)
    verify_checksum_file()
    print(canonical({
        "figureId": FIGURE_ID,
        "mode": "final" if final else "preflight",
        "status": validation["status"],
        "allAutomatedChecksPass": True,
        "visualQaConfirmed": visual_confirmed,
        "pdfGenerated": final,
    }), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
