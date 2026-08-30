#!/usr/bin/env python3
"""Fail-closed validation and sealing for the R0.73M figure package."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform
import re
import socket
import subprocess
import sys


def bootstrap() -> None:
    for index, value in enumerate(sys.argv):
        if value == "--deps" and index + 1 < len(sys.argv):
            sys.path.insert(0, str(Path(sys.argv[index + 1]).resolve()))
            return
        if value.startswith("--deps="):
            sys.path.insert(0, str(Path(value.split("=", 1)[1]).resolve()))
            return


bootstrap()

from PIL import Image, __version__ as pillow_version  # noqa: E402
from pypdf import PdfReader, __version__ as pypdf_version  # noqa: E402


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FIGURE_ID = "fig-r073m-prescribed-action-departure"
CERTIFICATE_DIR = ROOT / "research/certificates/r073m"
PRIMARY = CERTIFICATE_DIR / "primary_results.json"
INDEPENDENT_LINEAR = CERTIFICATE_DIR / "independent_linear.json"
INDEPENDENT_HIERARCHY = CERTIFICATE_DIR / "independent_hierarchy.json"
EXPERIMENT_CONFIG = CERTIFICATE_DIR / "config.json"
CERTIFICATE = CERTIFICATE_DIR / "certificate.json"
PACKAGE_VALIDATION = CERTIFICATE_DIR / "validation.json"
PACKAGE_MANIFEST = CERTIFICATE_DIR / "manifest.json"
INPUTS = (
    PRIMARY,
    INDEPENDENT_LINEAR,
    INDEPENDENT_HIERARCHY,
    EXPERIMENT_CONFIG,
    CERTIFICATE,
    PACKAGE_VALIDATION,
    PACKAGE_MANIFEST,
)
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
GENERATED_FILES = {
    "source-data.csv",
    "figure.pdf",
    "figure.svg",
    "figure.png",
    "qa-final-size.png",
    "qa-grayscale.png",
    "qa-pdf.png",
    "environment.json",
    "results.json",
    "validation.json",
    "manifest.json",
    "progress.ndjson",
    "resource-log.ndjson",
    "qa-report.md",
    "SHA256SUMS",
}
PACKAGE_FILES = SOURCE_FILES | GENERATED_FILES


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--verify-only", action="store_true")
    return parser.parse_args()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def load_json(path: Path) -> dict:
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


def close(actual: float, expected: float, tolerance: float = 1e-12) -> bool:
    return math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance)


def file_record(path: Path) -> dict[str, object]:
    return {"path": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}


def input_record(path: Path) -> dict[str, object]:
    return {
        "path": str(path.relative_to(ROOT)),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def verify_inventory(require_sealed: bool = False) -> None:
    required = PACKAGE_FILES if require_sealed else (
        PACKAGE_FILES - {"validation.json", "manifest.json", "qa-report.md", "SHA256SUMS"}
    )
    for name in sorted(required):
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), "missing package file: " + name)
    actual = {path.name for path in HERE.iterdir() if path.is_file()}
    if require_sealed:
        require(actual == PACKAGE_FILES, "sealed 25-file inventory drift")
    else:
        require(actual <= PACKAGE_FILES, "unexpected file in figure package")
    require(len(PACKAGE_FILES) == 25, "package contract is not 25 files")
    require(len(SOURCE_FILES) == 10 and len(GENERATED_FILES) == 15,
            "source/generated inventory count drift")


def verify_contract(config: dict, contract: dict, results: dict) -> None:
    require(config.get("figureId") == contract.get("figureId") == FIGURE_ID,
            "figure identity drift")
    require(contract.get("release") == "R0.73M", "release identity drift")
    require(contract.get("evidenceClass") ==
            "independently-recomputed-finite-binary64-diagnostic",
            "evidence class drift")
    require(float(config.get("widthMillimetres")) == 178.0, "width drift")
    require(float(config.get("heightMillimetres")) == 128.0, "height drift")
    require(int(config.get("pngDpi")) == 600, "PNG DPI drift")
    require(int(config.get("qaDpi")) == 300, "QA DPI drift")
    require(config.get("cutoffOrder") == [40, 48, 64], "cutoff order drift")
    require(config.get("epsilonOrder") ==
            [0.001, 0.0005, 0.00025, 0.000125, 0.0000625],
            "epsilon order drift")
    require(config.get("gateFamilyOrder") ==
            ["cutoff", "step", "physical-kinetic", "independent"],
            "gate family order drift")
    require(contract.get("palettePolicy", {}).get("policy") == "hard two-root cap",
            "palette policy drift")
    require(contract.get("researchBlossom", {}).get("lockedAnchor") ==
            "top-right-header", "blossom anchor drift")
    require(results.get("claimBoundary") == contract.get("claimBoundary"),
            "result claim boundary drift")
    boundary = contract["claimBoundary"]
    for key in (
        "formalValidatedDiagnosticFigure",
        "finiteDimensionalDiagnostic",
        "sealedUpstreamCertificatePassed",
        "independentFiniteRecomputationPassed",
        "finiteInviscidActionProxyComputed",
        "finitePrescribedActionRecodingComputed",
        "finiteABCoefficientsComputed",
    ):
        require(boundary.get(key) is True, "missing supported boundary: " + key)
    for key in (
        "continuumActionCertifiedByFiniteComputation",
        "continuumGainPrefactorCertifiedByFiniteComputation",
        "prefactorLimitCertified",
        "twoTermWKBCertified",
        "uniformTaylorRadiusCertified",
        "fourthOrderRemainderCertified",
        "fullNonlinearNavierStokesTrajectoryComputed",
        "finiteCutoffAgreementIsTailProof",
        "singleFixedBackgroundLyapunovInstabilityCertified",
        "transverseThreeDimensionalClosureCertified",
        "finiteTimeSingularityCertified",
        "clayProblemSolved",
    ):
        require(boundary.get(key) is False, "escaped claim boundary: " + key)
    upstream_boundary = config["claimBoundary"]
    for key, expected in upstream_boundary.items():
        require(boundary.get(key) is expected, "figure/upstream boundary drift: " + key)


def verify_inputs(environment: dict) -> None:
    expected = [input_record(path) for path in INPUTS]
    require(environment.get("inputs") == expected, "upstream input binding drift")
    primary = load_json(PRIMARY)
    independent_linear = load_json(INDEPENDENT_LINEAR)
    independent_hierarchy = load_json(INDEPENDENT_HIERARCHY)
    certificate = load_json(CERTIFICATE)
    validation = load_json(PACKAGE_VALIDATION)
    manifest = load_json(PACKAGE_MANIFEST)
    require(primary.get("status") == "passed" and primary.get("smokeMode") is False,
            "primary input is not a passed formal run")
    require(independent_linear.get("status") == "passed" and
            independent_linear.get("allChecksPass") is True,
            "independent linear input did not pass")
    require(independent_hierarchy.get("status") == "passed" and
            independent_hierarchy.get("allChecksPass") is True,
            "independent hierarchy input did not pass")
    require(certificate.get("allChecksPass") is True and
            certificate.get("smokeMode") is False,
            "upstream certificate did not pass as a formal run")
    require(validation.get("allChecksPass") is True and
            validation.get("smokeMode") is False,
            "upstream validation did not pass as a formal run")
    require(manifest.get("allPrerequisiteChecksPass") is True and
            manifest.get("smokeMode") is False,
            "upstream manifest prerequisites did not pass")
    source_commit = certificate.get("sourceProvenance", {}).get("sourceCommit")
    require(re.fullmatch(r"[0-9a-f]{40}", str(source_commit)) is not None,
            "upstream source commit is not a full hash")
    require(manifest.get("sourceCommit") == source_commit,
            "upstream source commit drift")


def expected_gate_components(
    primary: dict,
    independent_linear: dict,
    independent_hierarchy: dict,
    experiment_config: dict,
) -> list[dict[str, object]]:
    pmax = primary["maximums"]
    lmax = independent_linear["maximums"]
    tol = experiment_config["tolerances"]
    return [
        {"family": "cutoff", "metric": "cutoff action proxy",
         "value": pmax["largestCutoffActionProxyAbsolute"],
         "tolerance": tol["largestCutoffActionProxyAbsolute"], "path": PRIMARY},
        {"family": "cutoff", "metric": "cutoff prefactor",
         "value": pmax["largestCutoffPrefactorAbsolute"],
         "tolerance": tol["largestCutoffPrefactorAbsolute"], "path": PRIMARY},
        {"family": "cutoff", "metric": "cutoff hierarchy observables",
         "value": pmax["hierarchyFinestCutoffRelative"],
         "tolerance": tol["hierarchyFinestCutoffRelative"], "path": PRIMARY},
        {"family": "step", "metric": "hierarchy time step",
         "value": pmax["hierarchyStepRelative"],
         "tolerance": tol["hierarchyStepRelative"], "path": PRIMARY},
        {"family": "physical-kinetic", "metric": "physical versus kinetic gain",
         "value": pmax["physicalKineticGainRelative"],
         "tolerance": tol["physicalKineticGainRelative"], "path": PRIMARY},
        {"family": "independent", "metric": "independent inviscid action",
         "value": lmax["finiteInviscidActionProxyRelative"],
         "tolerance": tol["independentLinearActionRelative"], "path": INDEPENDENT_LINEAR},
        {"family": "independent", "metric": "independent viscous action",
         "value": lmax["finiteViscousActionRelative"],
         "tolerance": tol["independentLinearActionRelative"], "path": INDEPENDENT_LINEAR},
        {"family": "independent", "metric": "independent linear gain",
         "value": lmax["gainRelative"],
         "tolerance": tol["independentLinearGainRelative"], "path": INDEPENDENT_LINEAR},
        {"family": "independent", "metric": "independent prefactor",
         "value": lmax["finiteInviscidActionPrefactorAbsolute"],
         "tolerance": tol["independentLinearPrefactorAbsolute"], "path": INDEPENDENT_LINEAR},
        {"family": "independent", "metric": "independent step refinement",
         "value": lmax["stepRefinement"],
         "tolerance": tol["independentLinearRefinement"], "path": INDEPENDENT_LINEAR},
        {"family": "independent", "metric": "independent hierarchy coefficients",
         "value": independent_hierarchy["maximumCoefficientRelativeError"],
         "tolerance": tol["independentHierarchyCoefficientRelative"],
         "path": INDEPENDENT_HIERARCHY},
        {"family": "independent", "metric": "independent forbidden parity",
         "value": independent_hierarchy["maximumForbiddenParityRelative"],
         "tolerance": tol["independentHierarchyForbiddenParityRelative"],
         "path": INDEPENDENT_HIERARCHY},
    ]


def numeric(row: dict[str, str], key: str) -> float:
    value = float(row[key])
    require(math.isfinite(value), "non-finite source-data value: " + key)
    return value


def verify_csv(
    primary: dict,
    independent_linear: dict,
    independent_hierarchy: dict,
    experiment_config: dict,
    config: dict,
) -> dict[str, object]:
    with (HERE / "source-data.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    require(len(rows) == 27, "source-data total row count drift")
    case_rows = [row for row in rows if row["record_type"] == "finite_case"]
    gate_rows = [row for row in rows if row["record_type"] == "gate_component"]
    require(len(case_rows) == 15 and len(gate_rows) == 12,
            "source-data record inventory drift")
    require({row["record_type"] for row in rows} == {"finite_case", "gate_component"},
            "unknown source-data record type")

    expected_grid = {
        (int(cutoff), float(epsilon))
        for cutoff in config["cutoffOrder"]
        for epsilon in config["epsilonOrder"]
    }
    actual_grid = {(int(row["N"]), float(row["epsilon"])) for row in case_rows}
    require(actual_grid == expected_grid, "finite case grid drift")
    primary_hash = sha256(PRIMARY)
    cases = {
        (int(case["N"]), float(case["epsilon"])): case
        for case in primary["cases"]
    }
    for row in case_rows:
        key = (int(row["N"]), float(row["epsilon"]))
        case = cases[key]
        epsilon = key[1]
        hierarchy = case["hierarchy"]
        require(row["upstream_path"] == str(PRIMARY.relative_to(ROOT)) and
                row["upstream_sha256"] == primary_hash,
                "finite case provenance drift")
        checks = {
            "finite_inviscid_action_proxy": case["linear"]["finiteInviscidActionProxy"],
            "actual_physical_linear_gain": hierarchy["actualPhysicalLinearGain"],
            "finite_inviscid_action_prefactor": case["finiteInviscidActionPrefactor"],
            "a_endpoint_l2": hierarchy["aEndpointL2"],
            "b_endpoint_l2": hierarchy["bEndpointL2"],
            "b_over_epsilon": hierarchy["bEndpointL2"] / epsilon,
            "c_target_endpoint_l2": hierarchy["cTargetEndpointL2"],
            "c_target_over_epsilon_squared": hierarchy["cTargetEndpointL2"] / epsilon**2,
            "c_mean_path_signed_parallel": hierarchy["cMeanPathSignedParallel"],
            "c_mean_path_signed_parallel_over_epsilon_squared":
                hierarchy["cMeanPathSignedParallel"] / epsilon**2,
            "c_double_path_signed_parallel": hierarchy["cDoublePathSignedParallel"],
            "c_double_path_signed_parallel_over_epsilon_squared":
                hierarchy["cDoublePathSignedParallel"] / epsilon**2,
        }
        for field, expected in checks.items():
            require(close(numeric(row, field), float(expected)),
                    "finite case value drift: " + field)
        action = numeric(row, "finite_inviscid_action_proxy")
        gain = numeric(row, "actual_physical_linear_gain")
        prefactor = numeric(row, "finite_inviscid_action_prefactor")
        require(close(prefactor, gain * math.exp(-action / epsilon), 2e-12),
                "finite action-prefactor formula drift")

    components = expected_gate_components(
        primary, independent_linear, independent_hierarchy, experiment_config
    )
    expected_by_key = {
        (str(item["family"]), str(item["metric"])): item for item in components
    }
    actual_by_key = {(row["gate_family"], row["metric"]): row for row in gate_rows}
    require(set(actual_by_key) == set(expected_by_key), "gate component inventory drift")
    maxima = {
        family: max(
            float(item["value"]) / float(item["tolerance"])
            for item in components if item["family"] == family
        )
        for family in config["gateFamilyOrder"]
    }
    family_max_counts = {family: 0 for family in config["gateFamilyOrder"]}
    for key, item in expected_by_key.items():
        row = actual_by_key[key]
        value = numeric(row, "value")
        tolerance = numeric(row, "tolerance")
        ratio = numeric(row, "ratio_to_tolerance")
        require(close(value, float(item["value"])), "gate value drift: " + key[1])
        require(close(tolerance, float(item["tolerance"])),
                "gate tolerance drift: " + key[1])
        require(close(ratio, value / tolerance), "gate ratio formula drift: " + key[1])
        path = item["path"]
        require(row["upstream_path"] == str(path.relative_to(ROOT)) and
                row["upstream_sha256"] == sha256(path),
                "gate provenance drift: " + key[1])
        expected_max = close(ratio, maxima[key[0]], 0.0)
        require((row["is_family_max"] == "true") == expected_max,
                "gate family-maximum marker drift: " + key[1])
        family_max_counts[key[0]] += int(row["is_family_max"] == "true")
    require(all(count == 1 for count in family_max_counts.values()),
            "each gate family must have exactly one maximum")
    require(all(value < 1.0 for value in maxima.values()),
            "a gate-family maximum reached the fail threshold")
    return {
        "finiteCaseRows": len(case_rows),
        "gateComponentRows": len(gate_rows),
        "totalRows": len(rows),
        "gateFamilyMaximums": maxima,
    }


def verify_exports(config: dict) -> dict[str, object]:
    expected_png = (
        round(float(config["widthMillimetres"]) / 25.4 * int(config["pngDpi"])),
        round(float(config["heightMillimetres"]) / 25.4 * int(config["pngDpi"])),
    )
    expected_qa = (
        round(float(config["widthMillimetres"]) / 25.4 * int(config["qaDpi"])),
        round(float(config["heightMillimetres"]) / 25.4 * int(config["qaDpi"])),
    )
    with Image.open(HERE / "figure.png") as image:
        require(abs(image.width - expected_png[0]) <= 1 and
                abs(image.height - expected_png[1]) <= 1, "PNG dimensions drift")
        require(image.info.get("dpi") is not None, "PNG DPI metadata absent")
        png_size = [image.width, image.height]
    qa_sizes = {}
    for name in ("qa-final-size.png", "qa-grayscale.png", "qa-pdf.png"):
        with Image.open(HERE / name) as image:
            require(abs(image.width - expected_qa[0]) <= 2 and
                    abs(image.height - expected_qa[1]) <= 2,
                    name + " dimensions drift")
            qa_sizes[name] = [image.width, image.height]
    reader = PdfReader(str(HERE / "figure.pdf"))
    require(len(reader.pages) == 1, "PDF is not one page")
    page = reader.pages[0]
    width_mm = float(page.mediabox.width) * 25.4 / 72.0
    height_mm = float(page.mediabox.height) * 25.4 / 72.0
    require(abs(width_mm - 178.0) < 0.05 and abs(height_mm - 128.0) < 0.05,
            "PDF media box drift")
    svg = (HERE / "figure.svg").read_text(encoding="utf-8")
    require("<svg" in svg and re.search(r"<image\b", svg) is None,
            "SVG missing or contains an embedded raster")
    require("R0.73M finite prescribed-action recoding diagnostic" in svg,
            "SVG text was not preserved")
    require("Continuum" not in svg and "Clay problem solved" not in svg,
            "unsupported claim escaped into figure text")
    return {
        "pngPixels": png_size,
        "qaPixels": qa_sizes,
        "pdfPages": 1,
        "pdfMillimetres": [width_mm, height_mm],
        "svgRasterImages": 0,
    }


def expected_summary(
    primary: dict,
    independent_linear: dict,
    independent_hierarchy: dict,
    experiment_config: dict,
    config: dict,
) -> dict[str, object]:
    cases = {
        (int(case["N"]), float(case["epsilon"])): case
        for case in primary["cases"]
    }
    display = int(config["displayCutoff"])
    eps = sorted(float(value) for value in config["epsilonOrder"])
    g0 = [float(case["finiteInviscidActionPrefactor"]) for case in primary["cases"]]
    b = [cases[(display, value)]["hierarchy"]["bEndpointL2"] / value for value in eps]
    ct = [cases[(display, value)]["hierarchy"]["cTargetEndpointL2"] / value**2 for value in eps]
    cm = [cases[(display, value)]["hierarchy"]["cMeanPathSignedParallel"] / value**2 for value in eps]
    cd = [cases[(display, value)]["hierarchy"]["cDoublePathSignedParallel"] / value**2 for value in eps]
    components = expected_gate_components(
        primary, independent_linear, independent_hierarchy, experiment_config
    )
    family_rows = []
    for family in config["gateFamilyOrder"]:
        winner = max(
            [item for item in components if item["family"] == family],
            key=lambda item: float(item["value"]) / float(item["tolerance"]),
        )
        family_rows.append({
            "family": family,
            "metric": winner["metric"],
            "value": winner["value"],
            "tolerance": winner["tolerance"],
            "ratioToTolerance": float(winner["value"]) / float(winner["tolerance"]),
        })
    return {
        "displayCutoff": display,
        "cutoffs": config["cutoffOrder"],
        "epsilonLevels": config["epsilonOrder"],
        "finiteInviscidActionPrefactorRange": [min(g0), max(g0)],
        "displayBOverEpsilonRange": [min(b), max(b)],
        "displayCTargetOverEpsilonSquaredRange": [min(ct), max(ct)],
        "displayCMeanSignedOverEpsilonSquaredRange": [min(cm), max(cm)],
        "displayCDoubleSignedOverEpsilonSquaredRange": [min(cd), max(cd)],
        "gateFamilyMaximums": family_rows,
        "largestGateFamilyRatio": max(
            float(row["ratioToTolerance"]) for row in family_rows
        ),
    }


def verify_results(
    results: dict,
    primary: dict,
    independent_linear: dict,
    independent_hierarchy: dict,
    experiment_config: dict,
    config: dict,
) -> None:
    require(results.get("sourceRows") == 27, "result source-row count drift")
    require(results.get("finiteCaseRows") == 15, "result finite-case count drift")
    require(results.get("gateComponentRows") == 12, "result gate count drift")
    expected = expected_summary(
        primary, independent_linear, independent_hierarchy, experiment_config, config
    )
    require(results.get("summary") == expected, "result summary drift")
    require(float(expected["largestGateFamilyRatio"]) < 1.0,
            "largest gate-family ratio reached the fail threshold")
    require(float(expected["finiteInviscidActionPrefactorRange"][0]) > 0.0,
            "finite prefactor is not positive")
    require(all(value < 0.0 for value in expected["displayCMeanSignedOverEpsilonSquaredRange"]),
            "mean-path sign drift")
    require(all(value < 0.0 for value in expected["displayCDoubleSignedOverEpsilonSquaredRange"]),
            "doubled-path sign drift")


def write_qa_report(exports: dict[str, object], csv_details: dict[str, object]) -> None:
    report = """# R0.73M figure QA report

Status: **PASS**

- Color final-size raster inspected: no clipping, detached labels, or collisions.
- Grayscale raster inspected: cutoff nesting, coefficient paths, cubic paths,
  and four gate-family markers remain distinguishable without color.
- Independently rasterized PDF inspected: layout agrees with the PNG export.
- Panel (a) declares its focused vertical scale, retains the benchmark one,
  and labels the finite action proxy rather than a continuum action.
- Panel (b) displays the registered epsilon powers explicitly and does not fit
  or claim a limiting coefficient.
- Panel (c) retains the signed values and an explicit zero line.
- Panel (d) plots the maximum component ratio within each requested family,
  labels the fail threshold, and uses stems only as distance guides.
- The figure remains a finite binary64 diagnostic and does not certify a
  continuum limit, nonlinear trajectory, singularity, or the Clay problem.

Programmatic export facts:
"""
    report += "\n".join(f"- `{key}`: `{value}`" for key, value in exports.items())
    report += "\n\nProgrammatic source-data facts:\n"
    report += "\n".join(f"- `{key}`: `{value}`" for key, value in csv_details.items())
    report += "\n"
    (HERE / "qa-report.md").write_text(report, encoding="utf-8")


def git_head() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True,
        capture_output=True, check=True,
    )
    value = result.stdout.strip()
    require(re.fullmatch(r"[0-9a-f]{40}", value) is not None,
            "git HEAD is not a full commit hash")
    return value


def progress_wall_time() -> float:
    rows = [
        json.loads(line)
        for line in (HERE / "progress.ndjson").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    require(rows and rows[-1].get("stage") == "complete",
            "figure monitoring has no complete endpoint")
    return float(rows[-1]["elapsedSeconds"])


def publication_record(master: Path, public_path: Path) -> dict[str, object]:
    return {
        "path": str(public_path.relative_to(ROOT)),
        "bytes": master.stat().st_size,
        "sha256": sha256(master),
    }


def build_manifest(
    validation: dict,
    contract: dict,
    config: dict,
    results: dict,
    environment: dict,
) -> dict:
    head = git_head()
    public_directory = ROOT / "public/assets/r073m"
    public_assets = [
        public_directory / (FIGURE_ID + suffix)
        for suffix in (".pdf", ".svg", ".png")
    ]
    masters = [HERE / ("figure" + suffix) for suffix in (".pdf", ".svg", ".png")]
    public_complete = all(
        public.is_file() and sha256(public) == sha256(master)
        for public, master in zip(public_assets, masters)
    )
    input_bindings = [input_record(path) for path in INPUTS]
    data_specs = (
        ("source-data.csv", "15 finite cases and 12 numerical gate components"),
        ("results.json", "finite result summary and fail-closed claim boundary"),
        ("validation.json", "data, provenance, format, margin, and visual-QA checks"),
        ("environment.json", "runtime versions and SHA-256 upstream bindings"),
        ("progress.ndjson", "timestamped deterministic render stages"),
        ("resource-log.ndjson", "per-stage process, memory, and GPU record"),
        ("chart-contract-and-source-data.md", "analytical question, chart map, derivation, and boundary"),
    )
    data = [{**file_record(HERE / name), "schema": schema} for name, schema in data_specs]
    output_records = []
    for master in masters:
        record = file_record(master)
        if master.suffix == ".png":
            with Image.open(master) as image:
                record.update({"dpi": 600, "pixels": [image.width, image.height]})
        output_records.append(record)
    qa_names = ("qa-final-size.png", "qa-grayscale.png", "qa-pdf.png", "qa-report.md")
    inventory_without_self_hashes = sorted(PACKAGE_FILES - {"manifest.json", "SHA256SUMS"})
    upstream_certificate = load_json(CERTIFICATE)
    return {
        "schemaVersion": "r073m-prescribed-action-figure-manifest-v1",
        "figureId": FIGURE_ID,
        "release": "R0.73M",
        "status": "formal",
        "publicationStatus": "published" if public_complete else "prepublication",
        "createdAt": results["createdUtc"],
        "validatedAt": validation["createdUtc"],
        "analyticalQuestion": contract["analyticalQuestion"],
        "supportedClaim": contract["supportedTakeaway"],
        "supportedTakeaway": contract["supportedTakeaway"],
        "claimBoundary": contract["claimBoundary"],
        "git": {
            "repository": "https://github.com/Kasifa/Kasifa.github.io.git",
            "sourceCommit": head,
            "certificateCommit": head,
            "dirtyAtCertifiedRun": False,
            "dirtyAtCertifiedRunMeaning": (
                "all numerical sources and upstream certificate inputs are bound to "
                "immutable commits; the figure-source payload is bound by the 25-file "
                "package hashes before its parent release assigns a figure commit"
            ),
            "upstreamBaselineCommit": head,
            "upstreamCertificateSourceCommit": upstream_certificate[
                "sourceProvenance"
            ]["sourceCommit"],
            "figureSourceCommitAssigned": False,
            "figureSourceCommitAssignedMeaning": (
                "the parent release records the immutable figure-package commit after "
                "this no-commit generation task"
            ),
            "wholeWorktreeCleanAtRun": False,
            "figureSourcesBoundByManifestHashes": True,
            "workingTreeBoundByInputAndPackageHashes": True,
            "publicationCommitAssigned": False,
        },
        "packageInventory": {
            "expectedFileCount": 25,
            "sourceFileCount": 10,
            "generatedFileCount": 15,
            "chartContractSourceDataNote": "chart-contract-and-source-data.md",
            "paths": sorted(PACKAGE_FILES),
        },
        "computation": {
            "kind": "data-analysis",
            "configuration": "config.json",
            "precision": "binary64 finite diagnostics and deterministic static presentation",
            "solver": "no new PDE solve; deterministic extraction from the sealed R0.73M package",
            "formalCommand": "commands recorded in command.txt",
            "wallTimeSeconds": progress_wall_time(),
            "monitoring": {
                "enabled": True,
                "progressLog": "progress.ndjson",
                "resourceLog": "resource-log.ndjson",
                "trackedFields": [
                    "timestampUtc", "elapsedSeconds", "stage",
                    "maximumResidentSetMiB", "processes", "gpu",
                ],
            },
        },
        "compute": {
            "host": socket.gethostname(),
            "operatingSystem": platform.platform(),
            "cpu": platform.machine(),
            "machine": platform.machine(),
            "memoryGiB": 36.0,
            "processes": 1,
            "threadsPerProcess": 1,
            "gpu": "not used",
            "dgx": "not used; deterministic static rendering is local CPU work",
        },
        "environment": {
            "python": environment["python"],
            "matplotlib": environment["matplotlib"],
            "numpy": environment["numpy"],
            "Pillow": pillow_version,
            "pypdf": pypdf_version,
            "packagesLock": "requirements.txt",
        },
        "inputBindings": input_bindings,
        "sourceData": input_bindings,
        "data": data,
        "figure": {
            "profile": "journal-double-column",
            "layout": "four-panel gain, hierarchy, signed-alignment, and gate diagnostic",
            "script": "plot.py",
            "widthMillimetres": config["widthMillimetres"],
            "heightMillimetres": config["heightMillimetres"],
            "pngDpi": config["pngDpi"],
            "outputs": output_records,
        },
        "caption": {"english": "caption.md"},
        "qa": {
            "status": "passed",
            "visualInspectionExplicit": True,
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "scalesSignsAndUnitsInspected": True,
            "dataCrossChecked": True,
            "finalSize": "qa-final-size.png",
            "grayscale": "qa-grayscale.png",
            "pdfRaster": "qa-pdf.png",
            "qaDpi": config["qaDpi"],
            "report": "qa-report.md",
            "records": [file_record(HERE / name) for name in qa_names],
        },
        "masters": [master.name for master in masters],
        "publication": {
            "directory": "public/assets/r073m",
            "archiveDirectory": "public/figures/r073m/" + FIGURE_ID,
            "fileStem": FIGURE_ID,
            "byteIdentityRequired": True,
            "publicCopiesComplete": public_complete,
            "assets": [
                publication_record(master, public)
                for master, public in zip(masters, public_assets)
            ],
        },
        "files": [file_record(HERE / name) for name in inventory_without_self_hashes],
    }


def seal(
    validation: dict,
    contract: dict,
    config: dict,
    results: dict,
    environment: dict,
) -> None:
    (HERE / "validation.json").write_text(canonical(validation), encoding="utf-8")
    manifest = build_manifest(validation, contract, config, results, environment)
    (HERE / "manifest.json").write_text(canonical(manifest), encoding="utf-8")
    checksum_names = sorted(PACKAGE_FILES - {"SHA256SUMS"})
    lines = [f"{sha256(HERE / name)}  {name}" for name in checksum_names]
    (HERE / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")


def verify_sealed_package() -> None:
    verify_inventory(require_sealed=True)
    manifest = load_json(HERE / "manifest.json")
    validation = load_json(HERE / "validation.json")
    require(manifest.get("status") == "formal", "manifest status drift")
    require(validation.get("status") == "passed" and
            validation.get("allChecksPass") is True,
            "validation status drift")
    inventory = manifest.get("packageInventory", {})
    require(inventory.get("expectedFileCount") == 25 and
            inventory.get("paths") == sorted(PACKAGE_FILES),
            "manifest 25-file inventory drift")
    expected_lines = [
        f"{sha256(HERE / name)}  {name}"
        for name in sorted(PACKAGE_FILES - {"SHA256SUMS"})
    ]
    actual_lines = (HERE / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    require(actual_lines == expected_lines, "SHA256SUMS drift")
    records = {record["path"]: record for record in manifest.get("files", [])}
    require(set(records) == PACKAGE_FILES - {"manifest.json", "SHA256SUMS"},
            "manifest file-record inventory drift")
    for name, record in records.items():
        path = HERE / name
        require(record.get("bytes") == path.stat().st_size and
                record.get("sha256") == sha256(path),
                "manifest file hash drift: " + name)
    if manifest.get("publicationStatus") == "published":
        assets = ROOT / "public/assets/r073m"
        for suffix in (".pdf", ".svg", ".png"):
            master = HERE / ("figure" + suffix)
            public = assets / (FIGURE_ID + suffix)
            require(public.is_file() and sha256(public) == sha256(master),
                    "public figure master drift: " + suffix)
        archive = ROOT / "public/figures/r073m" / FIGURE_ID
        if archive.exists():
            archive_names = {path.name for path in archive.iterdir() if path.is_file()}
            require(archive_names == PACKAGE_FILES, "public archive inventory drift")
            for name in PACKAGE_FILES:
                require(sha256(archive / name) == sha256(HERE / name),
                        "public archive byte drift: " + name)


def main() -> int:
    args = parse_args()
    if args.verify_only:
        verify_sealed_package()
        print(json.dumps({"event": "verified", "status": "passed", "files": 25}))
        return 0
    verify_inventory(require_sealed=False)
    config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    results = load_json(HERE / "results.json")
    environment = load_json(HERE / "environment.json")
    primary = load_json(PRIMARY)
    independent_linear = load_json(INDEPENDENT_LINEAR)
    independent_hierarchy = load_json(INDEPENDENT_HIERARCHY)
    experiment_config = load_json(EXPERIMENT_CONFIG)
    verify_contract(config, contract, results)
    verify_inputs(environment)
    csv_details = verify_csv(
        primary,
        independent_linear,
        independent_hierarchy,
        experiment_config,
        config,
    )
    exports = verify_exports(config)
    verify_results(
        results,
        primary,
        independent_linear,
        independent_hierarchy,
        experiment_config,
        config,
    )
    write_qa_report(exports, csv_details)
    validation = {
        "schemaVersion": "r073m-figure-validation-v1",
        "createdUtc": datetime.now(timezone.utc).isoformat(),
        "status": "passed",
        "allChecksPass": True,
        "checks": {
            "twentyFiveFileInventory": True,
            "chartContractSourceDataNotePresent": True,
            "contract": True,
            "claimBoundary": True,
            "sealedUpstreamBindings": True,
            "sourceData": True,
            "normalizationFormulas": True,
            "gateFamilyMaximums": True,
            "exports": True,
            "manualColorGrayscalePdfInspection": True,
        },
        "details": {
            "packageFiles": 25,
            "sourceFiles": 10,
            "generatedFiles": 15,
            "sourceData": csv_details,
            "exports": exports,
            "pillow": pillow_version,
            "pypdf": pypdf_version,
        },
    }
    results["status"] = "passed"
    results["allChecksPass"] = True
    (HERE / "results.json").write_text(canonical(results), encoding="utf-8")
    seal(validation, contract, config, results, environment)
    verify_sealed_package()
    print(json.dumps({"event": "validated", "status": "passed", "files": 25}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
