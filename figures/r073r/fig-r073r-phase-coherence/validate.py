#!/usr/bin/env python3
"""Fail-closed independent validation for the R0.73R figure package."""

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
FIGURE_ID = "fig-r073r-phase-coherence"
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
METADATA_FILES = {"validation.json", "manifest.json", "qa-report.md", "SHA256SUMS"}
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
    "family",
    "m",
    "N",
    "q",
    "s",
    "k1",
    "k2",
    "k3",
    "coefficient_sign",
    "coefficient_modulus",
    "r",
    "unscaled_dirichlet_guide",
    "unscaled_rudin_shapiro_guide",
    "unscaled_ratio_guide",
    "scaled_l2_guide",
    "scaled_dirichlet_heat_guide",
    "scaled_rudin_shapiro_heat_guide",
    "scaled_hhalf_guide",
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


def rs_sign(index: int) -> int:
    """Independent closed form: parity of overlapping 11 pairs in index bits."""
    require(index >= 0, "negative Rudin--Shapiro index")
    return -1 if (index & (index >> 1)).bit_count() % 2 else 1


def triple_convolution(coefficients: list[int]) -> list[int]:
    result = [0] * (3 * len(coefficients) - 2)
    for first, a in enumerate(coefficients):
        for second, b in enumerate(coefficients):
            for third, c in enumerate(coefficients):
                result[first + second + third] += a * b * c
    return result


def read_csv() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    with (HERE / "source-data.csv").open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        require(tuple(reader.fieldnames or ()) == CSV_FIELDS, "source-data.csv schema drift")
        rows = list(reader)
    require(all(set(row) == set(CSV_FIELDS) for row in rows), "source-data row schema drift")
    packet = [row for row in rows if row["record_type"] == "positive_fourier_packet"]
    scaling = [row for row in rows if row["record_type"] == "analytic_scaling_guide"]
    require(len(rows) == len(packet) + len(scaling), "unexpected source-data record type")
    require(len(rows) == 141, "source-data must contain exactly 141 rows")
    return packet, scaling


def verify_inventory(*, metadata_required: bool) -> None:
    required = SOURCE_FILES | RAW_FILES
    if metadata_required:
        required |= METADATA_FILES
    actual = {path.name for path in HERE.iterdir() if path.is_file()}
    require(actual <= PACKAGE_FILES, "unexpected figure-package file: " + repr(sorted(actual - PACKAGE_FILES)))
    require(required <= actual, "missing figure-package files: " + repr(sorted(required - actual)))
    require(len(SOURCE_FILES) == 10, "source inventory count drift")
    require(len(RAW_FILES) == 11, "raw inventory count drift")
    require(len(PACKAGE_FILES) == 25, "formal package inventory count drift")


def check_formula_data(config: dict[str, Any]) -> tuple[dict[str, bool], dict[str, Any]]:
    packet, scaling = read_csv()
    panel = config["panelA"]
    m = int(panel["m"])
    carrier = int(panel["carrierFactor"]) * m
    require(m == 8 and carrier == 64, "Panel A frozen grid drift")
    expected_modulus = 1.0 / (math.sqrt(2.0) * m)
    unused_packet = {
        "r", "unscaled_dirichlet_guide", "unscaled_rudin_shapiro_guide",
        "unscaled_ratio_guide", "scaled_l2_guide", "scaled_dirichlet_heat_guide",
        "scaled_rudin_shapiro_heat_guide", "scaled_hhalf_guide",
    }
    require(len(packet) == 2 * m * m, "positive-packet row count drift")
    maximum_packet_error = 0.0
    sites_by_family: dict[str, set[tuple[int, int, int]]] = {}
    signs_by_family: dict[str, list[int]] = {}
    cursor = 0
    for family in ("Dirichlet", "Rudin-Shapiro"):
        sites: set[tuple[int, int, int]] = set()
        signs: list[int] = []
        for q_index in range(m):
            for s_index in range(m):
                row = packet[cursor]
                cursor += 1
                require(row["family"] == family, "packet family/order drift")
                require(int(row["m"]) == m and int(row["N"]) == carrier, "packet m/N drift")
                require(int(row["q"]) == q_index and int(row["s"]) == s_index, "packet index drift")
                site = (carrier + q_index, s_index, 0)
                require((int(row["k1"]), int(row["k2"]), int(row["k3"])) == site,
                        "packet Fourier site drift")
                coefficient = 1 if family == "Dirichlet" else rs_sign(q_index) * rs_sign(s_index)
                require(int(row["coefficient_sign"]) == coefficient, "packet sign drift")
                actual_modulus = float(row["coefficient_modulus"])
                require(close(actual_modulus, expected_modulus), "packet coefficient modulus drift")
                maximum_packet_error = max(maximum_packet_error, abs(actual_modulus / expected_modulus - 1.0))
                require(all(row[field] == "" for field in unused_packet), "packet row contains scaling fields")
                sites.add(site)
                signs.append(coefficient)
        sites_by_family[family] = sites
        signs_by_family[family] = signs

    expected_exponents = exponent_grid(config["scaling"])
    require(len(scaling) == len(expected_exponents) == 13, "scaling row count drift")
    scaling_fields = (
        "unscaled_dirichlet_guide", "unscaled_rudin_shapiro_guide",
        "unscaled_ratio_guide", "scaled_l2_guide",
        "scaled_dirichlet_heat_guide", "scaled_rudin_shapiro_heat_guide",
        "scaled_hhalf_guide",
    )
    powers = (1.0 / 6.0, -1.0 / 2.0, 2.0 / 3.0, -1.0 / 6.0, 0.0, -2.0 / 3.0, 1.0 / 3.0)
    maximum_scaling_error = 0.0
    series = {field: [] for field in scaling_fields}
    for row, exponent in zip(scaling, expected_exponents, strict=True):
        shell_size = 2**exponent
        require(row["family"] == "" and int(row["m"]) == shell_size, "scaling m/family drift")
        require(int(row["N"]) == 8 * shell_size and int(row["r"]) == exponent, "scaling N/r drift")
        require(all(row[field] == "" for field in (
            "q", "s", "k1", "k2", "k3", "coefficient_sign", "coefficient_modulus"
        )), "scaling row contains packet fields")
        for field, power in zip(scaling_fields, powers, strict=True):
            expected = shell_size**power
            actual = float(row[field])
            require(close(actual, expected), "scaling formula drift: " + field)
            maximum_scaling_error = max(maximum_scaling_error, abs(actual / expected - 1.0))
            series[field].append(actual)

    ratio_checks = [
        all(close(values[index + 1] / values[index], 2.0**power)
            for index in range(len(values) - 1))
        for values, power in ((series[field], power) for field, power in zip(scaling_fields, powers, strict=True))
    ]
    dirichlet = [1] * m
    rudin = [rs_sign(index) for index in range(m)]
    direct_dirichlet_sixth = sum(value * value for value in triple_convolution(dirichlet))
    closed_dirichlet_sixth = (11 * m**5 + 5 * m**3 + 4 * m) // 20
    rudin_sixth = sum(value * value for value in triple_convolution(rudin))
    checks = {
        "all141RowsIndependentlyRecomputed": max(maximum_packet_error, maximum_scaling_error) <= 3e-15,
        "packetRowCount": len(packet) == 128,
        "scalingRowCount": len(scaling) == 13,
        "matchedPositivePacketSites": sites_by_family["Dirichlet"] == sites_by_family["Rudin-Shapiro"],
        "matchedCoefficientModuli": maximum_packet_error <= 3e-15,
        "dirichletSignsAllPositive": set(signs_by_family["Dirichlet"]) == {1},
        "rudinShapiroSignsArePlusMinus": set(signs_by_family["Rudin-Shapiro"]) == {-1, 1},
        "fullSupportSizeByConjugateReflection": 2 * len(sites_by_family["Dirichlet"]) == 2 * m * m,
        "allAnalyticStepRatios": all(ratio_checks),
        "phaseSeparationPower": close(series["unscaled_ratio_guide"][-1], (2**expected_exponents[-1]) ** (2.0 / 3.0)),
        "dirichletSixthMomentIdentity": direct_dirichlet_sixth == closed_dirichlet_sixth,
        "rudinShapiroSixthMomentFinite": 0 < rudin_sixth <= 4 * m**3,
    }
    details = {
        "rows": {
            "total": len(packet) + len(scaling),
            "positivePacket": len(packet),
            "analyticScaling": len(scaling),
            "maximumRelativeRecomputationError": max(maximum_packet_error, maximum_scaling_error),
        },
        "panelA": {
            "m": m,
            "carrier": carrier,
            "positiveSupportSizePerFamily": len(sites_by_family["Dirichlet"]),
            "fullSupportSizePerFamily": 2 * len(sites_by_family["Dirichlet"]),
            "coefficientModulus": expected_modulus,
            "dirichletSixthMoment": direct_dirichlet_sixth,
            "rudinShapiroSixthMoment": rudin_sixth,
        },
        "scaling": {
            "exponentRange": [expected_exponents[0], expected_exponents[-1]],
            "mRange": [2**expected_exponents[0], 2**expected_exponents[-1]],
            "powers": dict(zip(scaling_fields, powers, strict=True)),
            "maximumRelativeRecomputationError": maximum_scaling_error,
        },
    }
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
        "pdfPageDimensions178x94mm": all(
            abs(actual - expected) < 0.02
            for actual, expected in zip(pdf_size_mm, (width_mm, height_mm), strict=True)
        ),
        "pdfQaRasterDimensions": all(
            abs(actual - expected) <= 2
            for actual, expected in zip(pdf_qa_pixels, expected_qa, strict=True)
        ),
        "pdfHasNoRasterImageObjects": pdf_image_count == 0,
        "svgIsNonemptyVectorSurface": "<svg" in svg and "<path" in svg and len(svg) > 10000,
        "svgContainsNoImageElement": re.search(r"<(?:svg:)?image\b", svg, flags=re.IGNORECASE) is None,
        "svgLabelsAnalyticNotSimulation": "analytic scaling" in svg and "not simulation" in svg,
        "svgUsesHomogeneousHhalfLabel": r"shared $\dot H^{1/2}\propto m^{1/3}$" in svg,
        "allPanelLettersPresentInSvg": all(f">{letter}<" in svg for letter in ("A", "B", "C")),
        "svgClaimBoundaryVisible": "no fit, PDE solve, safety inference, or Clay conclusion" in svg,
    }
    details = {
        "figurePng": {"pixels": png_pixels, "expectedPixels": expected_png, "dpi": png_dpi_actual, "mode": png_mode},
        "qaRasters": qa,
        "expectedQaPixels": expected_qa,
        "pdf": {
            "pageSizeMillimetres": pdf_size_mm,
            "qaPixels": pdf_qa_pixels,
            "qaMode": pdf_qa_mode,
            "embeddedImageObjectCount": pdf_image_count,
        },
        "svgBytes": (HERE / "figure.svg").stat().st_size,
        "svgEmbeddedImageElementCount": len(re.findall(r"<(?:svg:)?image\b", svg, flags=re.IGNORECASE)),
    }
    return checks, details


def verify_dependencies(environment: dict[str, Any]) -> dict[str, bool]:
    runtime = {name: package_version(name) for name in EXPECTED_DEPENDENCIES}
    recorded = environment.get("packages", {})
    requirements = {}
    for line in (HERE / "requirements.txt").read_text(encoding="utf-8").splitlines():
        name, value = line.split("==", 1)
        requirements[name] = value
    return {
        "runtimeDependenciesPinned": runtime == EXPECTED_DEPENDENCIES,
        "recordedDependenciesPinned": recorded == EXPECTED_DEPENDENCIES,
        "requirementsDependenciesPinned": requirements == EXPECTED_DEPENDENCIES,
        "dgxNotUsed": environment.get("dgxUsed") is False and environment.get("gpu") == "not used",
    }


def verify_results(results: dict[str, Any], details: dict[str, Any]) -> dict[str, bool]:
    facts = results.get("facts", {})
    return {
        "resultsFigureId": results.get("figureId") == FIGURE_ID,
        "resultsMode": results.get("mode") == "render-preseal",
        "resultsAnalyticGuideFlag": results.get("isAnalyticScalingGuide") is True,
        "resultsNotFitFlag": results.get("isFittedScalingLaw") is False,
        "resultsNotSimulationFlag": results.get("isNavierStokesSimulation") is False,
        "resultsNotNonlinearCertificateFlag": results.get("isNonlinearPdeCertificate") is False,
        "resultsDgxFlag": results.get("dgxUsed") is False,
        "resultsPdfFlag": results.get("pdfGenerated") is True,
        "resultsRowCount": results.get("rowCount") == details["rows"]["total"] == 141,
        "resultsPacketInventory": facts.get("panelA", {}).get("positivePacketRowCount") == 128,
        "resultsScalingInventory": facts.get("scaling", {}).get("rowCount") == 13,
    }


def verify_contract(contract: dict[str, Any]) -> dict[str, bool]:
    boundary = contract.get("claimBoundary", {})
    required_true = {"analyticPowersOnly", "fieldsHaveZeroConvection"}
    required_false = {
        "fittedScalingLaw", "navierStokesSimulation", "nonlinearPdeCertificate",
        "necessaryRegularityCriterion", "unsafeDynamics", "finiteTimeSingularity",
        "arbitraryL2SmallDataSafe", "clayProblemSolved",
    }
    caption = (HERE / "caption.md").read_text(encoding="utf-8")
    source_note = (HERE / "chart-contract-and-source-data.md").read_text(encoding="utf-8")
    readme = (HERE / "README.md").read_text(encoding="utf-8")
    return {
        "contractFigureId": contract.get("figureId") == FIGURE_ID,
        "contractPositiveBoundaries": all(boundary.get(key) is True for key in required_true),
        "contractNegativeBoundaries": all(boundary.get(key) is False for key in required_false),
        "captionStatesAnalyticNotFit": "analytic powers" in caption and "not fitted data or simulations" in caption,
        "captionStatesZeroConvection": "zero convection" in caption,
        "captionDeniesUnsafeInference": "not evidence of\nsingular dynamics" in caption,
        "sourceNoteStatesNoEmpiricalSample": "No empirical sample" in source_note,
        "sourceNoteDeniesClayConclusion": "solution of the Clay problem" in source_note,
        "readmeStatesTwoStageSeal": "two-stage package" in readme and "immutable source commit" in readme,
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
                "committed source differs byte-for-byte from working source: " + relative)
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
    require(len(bindings) == 10, "committed source binding count drift")
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
    expected = {path.name for path in HERE.iterdir() if path.is_file() and path.name != "SHA256SUMS"}
    require(set(parsed) == expected, "SHA256SUMS inventory drift")
    for name, expected_hash in parsed.items():
        require(sha256(HERE / name) == expected_hash, "SHA256SUMS mismatch: " + name)


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
    formal = final and len(bindings) == 10 and all(checks.values())
    git = ({
        "repository": "https://github.com/kasifa/kasifa.github.io",
        "sourceCommit": source_commit,
        "sourceFilesMatchCommitByteForByte": True,
        "artifactCommit": "pending-second-stage-commit",
    } if final else current_git_state())
    return {
        "schemaVersion": "research-figure-manifest-v1",
        "figureId": FIGURE_ID,
        "status": "formal" if formal else "source-unsealed-preseal",
        "createdAt": utc_now(),
        "analyticalQuestion": "How can matched Fourier support and coefficient moduli coexist with a growing phase-sensitive heat-flow separation?",
        "supportedClaim": "The matched Dirichlet and Rudin-Shapiro tensors have identical Fourier support and coefficient moduli, while their normalized analytic heat-flow guides separate by m^(2/3).",
        "allPrerequisiteChecksPass": formal,
        "allFormulaAndVisualChecksPass": all(checks.values()),
        "sourceCommitAssigned": formal,
        "git": git,
        "computation": {
            "kind": "analytic-formula-and-scaling-guide audit",
            "configuration": "config.json",
            "precision": "IEEE-754 binary64 evaluation of exact signs and closed-form powers",
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
            {**record(HERE / "source-data.csv"), "schema": "128 exact packet-sign rows plus 13 analytic-scaling rows"},
            {**record(HERE / "results.json"), "schema": "formula facts and output inventory"},
            {**record(HERE / "environment.json"), "schema": "runtime and hardware record"},
            {**record(HERE / "progress.ndjson"), "schema": "timestamped generation stages"},
            {**record(HERE / "resource-log.ndjson"), "schema": "timestamped process resource observations"},
        ],
        "figure": {
            "widthMillimetres": 178.0,
            "heightMillimetres": 94.0,
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
            "all141RowsRecomputed": True,
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
    return f"""# R0.73R independent figure QA report

- Independent reconstruction of all 141 source-data rows: **PASS**.
- Matched packet support/moduli, sign sequence, and analytic powers: **PASS**.
- Vector PDF, SVG, 600-dpi PNG, and PDF-raster checks: **PASS**.
- PDF physical size 178 by 94 mm; embedded raster objects: **zero**.
- SVG embedded image elements: **zero**.
- Final-size and grayscale visual inspection: **CONFIRMED**.
- Labels, legends, colours, marker redundancy, and print-size readability: **PASS**.
- Claim-boundary labels: **PASS**.
- DGX or GPU use: **no**.
- Package sealing state: **{sealing}**.

The validator independently reconstructs Rudin--Shapiro signs from binary
adjacent-pair parity and all seven analytic powers; it never imports plotting
code. A preseal is not formal. Formal sealing additionally binds all ten
source files byte for byte to an immutable Git source commit, after which the
generated assets and metadata require a separate artifact commit.
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
        require(validation.get("allAutomatedChecksPass") is True, "recorded validation did not pass")
        require(all(validation.get("checks", {}).values()), "recorded validation contains failed checks")
        require(manifest.get("figureId") == FIGURE_ID, "manifest figureId drift")
        expected_status = "formal" if final else "source-unsealed-preseal"
        require(manifest.get("status") == expected_status, "manifest status drift")
        if final:
            source_commit = str(manifest.get("git", {}).get("sourceCommit", ""))
            bindings = source_commit_bindings(source_commit)
            require(manifest.get("sourceBindings") == bindings, "recorded source bindings drift")
        else:
            require(manifest.get("sourceBindings") == [], "preseal must not contain source bindings")
            require(manifest.get("sourceCommitAssigned") is False, "preseal must not claim a source commit")
        verify_manifest_records(manifest)
        verify_checksum_file()
        print(canonical({
            "figureId": FIGURE_ID,
            "mode": "final" if final else "preseal",
            "status": "verified",
            "allAutomatedChecksPass": True,
            "recordedQaStatus": manifest.get("qa", {}).get("status"),
            "rowCountIndependentlyRecomputed": 141,
        }), end="")
        return 0

    bindings: list[dict[str, object]] = []
    if final:
        bindings = source_commit_bindings(args.source_commit)
    validation = {
        "schemaVersion": "r073r-phase-coherence-validation-v1",
        "figureId": FIGURE_ID,
        "createdAt": utc_now(),
        "mode": "final" if final else "preseal",
        "status": "formal-passed" if final else "source-unsealed-preseal-passed",
        "allAutomatedChecksPass": True,
        "independentFormulaRecomputationPass": True,
        "rowCountIndependentlyRecomputed": 141,
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
        "rowCountIndependentlyRecomputed": 141,
    }), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
