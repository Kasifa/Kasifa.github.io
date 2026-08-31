#!/usr/bin/env python3
"""Fail-closed validation and hash binding for the R0.73N figure package."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from decimal import Decimal, getcontext
import hashlib
from importlib.metadata import version as package_version
import json
import math
from pathlib import Path
import re
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
ROOT = HERE.parents[3]
FIGURE_ID = "fig-r073n-finite-strain-bracket"
CERTIFICATE_DIR = ROOT / "research/certificates/r073n"
DIAGNOSTIC = CERTIFICATE_DIR / "diagnostic.json"
SOURCE_DATA = CERTIFICATE_DIR / "source-data.csv"
INDEPENDENT = CERTIFICATE_DIR / "independent_validation.json"
CERTIFICATE = CERTIFICATE_DIR / "certificate.json"
PACKAGE_VALIDATION = CERTIFICATE_DIR / "validation.json"
PACKAGE_MANIFEST = CERTIFICATE_DIR / "manifest.json"
INPUTS = (
    DIAGNOSTIC,
    SOURCE_DATA,
    INDEPENDENT,
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
EXPECTED_DEPENDENCIES = {
    "matplotlib": "3.10.6",
    "numpy": "2.5.2",
    "pillow": "12.3.0",
    "pypdf": "6.10.0",
    "pypdfium2": "5.13.0",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--confirm-visual-qa", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument(
        "--source-commit",
        default="",
        help="immutable 40-hex R0.73N theorem-source commit for final sealing",
    )
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


def file_record(path: Path) -> dict[str, object]:
    return {"path": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}


def input_record(path: Path) -> dict[str, object]:
    return {
        "path": str(path.relative_to(ROOT)),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def source_commit_bindings(source_commit: str) -> list[dict[str, object]]:
    if re.fullmatch(r"[0-9a-f]{40}", source_commit) is None:
        raise RuntimeError("source commit must be a full lowercase 40-hex hash")
    commit_check = subprocess.run(
        ["git", "cat-file", "-e", source_commit + "^{commit}"],
        cwd=ROOT,
        capture_output=True,
        check=False,
    )
    if commit_check.returncode != 0:
        raise RuntimeError("source commit is not an available commit object")
    bindings = []
    for name in sorted(SOURCE_FILES):
        path = HERE / name
        relative = path.relative_to(ROOT).as_posix()
        tree = subprocess.run(
            ["git", "ls-tree", source_commit, "--", relative],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        match = re.fullmatch(r"100(?:644|755) blob ([0-9a-f]+)\t" + re.escape(relative), tree)
        if match is None:
            raise RuntimeError("source commit lacks a regular figure-source blob: " + relative)
        blob = subprocess.run(
            ["git", "show", source_commit + ":" + relative],
            cwd=ROOT,
            capture_output=True,
            check=True,
        ).stdout
        committed_sha = hashlib.sha256(blob).hexdigest()
        if committed_sha != sha256(path) or len(blob) != path.stat().st_size:
            raise RuntimeError("source commit blob differs from current figure source: " + relative)
        bindings.append({
            "path": relative,
            "bytes": len(blob),
            "sha256": committed_sha,
            "gitBlobObjectId": match.group(1),
        })
    return bindings


def close(actual: float, expected: float, tolerance: float = 2e-12) -> bool:
    return math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance)


def verify_inventory(*, complete: bool) -> None:
    required = PACKAGE_FILES if complete else (
        PACKAGE_FILES - {"validation.json", "manifest.json", "qa-report.md", "SHA256SUMS"}
    )
    for name in sorted(required):
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), "missing package file: " + name)
    actual = {path.name for path in HERE.iterdir() if path.is_file()}
    if complete:
        require(actual == PACKAGE_FILES, "hash-bound 25-file inventory drift")
    else:
        require(actual <= PACKAGE_FILES, "unexpected file in figure package")
    require(len(SOURCE_FILES) == 10, "source-file count drift")
    require(len(GENERATED_FILES) == 15, "generated-file count drift")
    require(len(PACKAGE_FILES) == 25, "package contract is not exactly 25 files")


def verify_contract(config: dict, contract: dict, results: dict) -> None:
    require(config.get("schemaVersion") == "r073n-finite-strain-figure-config-v1",
            "config schema drift")
    require(contract.get("schemaVersion") == "r073n-finite-strain-figure-contract-v1",
            "contract schema drift")
    require(config.get("figureId") == contract.get("figureId") == FIGURE_ID,
            "figure identity drift")
    require(contract.get("release") == "R0.73N", "release identity drift")
    require(contract.get("evidenceClass") ==
            "exact-rational-and-high-precision-illustrative-diagnostic",
            "evidence class drift")
    require(float(config.get("widthMillimetres")) == 178.0, "width drift")
    require(float(config.get("heightMillimetres")) == 96.0, "height drift")
    require(int(config.get("pngDpi")) == 600, "PNG DPI drift")
    require(int(config.get("qaDpi")) == 300, "QA DPI drift")
    require(config.get("panelOrder") ==
            ["strain-envelope", "cumulative-j", "marked-basepoint-bracket"],
            "panel order drift")
    require(contract.get("palettePolicy", {}).get("policy") == "hard two-root cap",
            "palette policy drift")
    require(config.get("claimBoundary") == contract.get("claimBoundary"),
            "config/contract claim-boundary drift")
    require(results.get("claimBoundary") == contract.get("claimBoundary"),
            "results/contract claim-boundary drift")
    boundary = contract["claimBoundary"]
    for key in (
        "formalValidatedDiagnosticFigure",
        "upstreamCertificateValidationPassed",
        "independentFiniteRecomputationPassed",
        "finiteExactStrainEnvelopeIdentityChecked",
        "finiteCumulativeJFormulaChecked",
        "jInfinityExactRationalChecked",
        "jStarStrictRationalLowerChecked",
        "inheritedActionIntervalRecorded",
        "markedBasepointExponentFactorsIllustrated",
    ):
        require(boundary.get(key) is True, "missing supported boundary: " + key)
    for key in (
        "finiteComputationProvesInheritedActionInterval",
        "finiteComputationProvesContinuumEnergyEstimate",
        "finiteComputationProvesFixedMemberStabilityTube",
        "sharpFamilyLipschitzExponentCertified",
        "singleFixedBackgroundLyapunovInstabilityCertified",
        "fullThreeDimensionalFPSH3L2StabilityCertified",
        "transverseCriticalNormGrowthCertified",
        "finiteTimeSingularityCertified",
        "clayProblemSolved",
    ):
        require(boundary.get(key) is False, "escaped claim boundary: " + key)


def verify_inputs(environment: dict, expected_source_commit: str = "") -> None:
    require(environment.get("inputs") == [input_record(path) for path in INPUTS],
            "upstream input binding drift")
    diagnostic = load_json(DIAGNOSTIC)
    independent = load_json(INDEPENDENT)
    certificate = load_json(CERTIFICATE)
    validation = load_json(PACKAGE_VALIDATION)
    manifest = load_json(PACKAGE_MANIFEST)
    for name, payload in (
        ("diagnostic", diagnostic),
        ("independent validation", independent),
        ("certificate", certificate),
        ("package validation", validation),
    ):
        require(payload.get("status") == "passed" and payload.get("allChecksPass") is True,
                name + " did not pass")
    require(manifest.get("allPrerequisiteChecksPass") is True,
            "upstream certificate prerequisites did not pass")
    assigned = manifest.get("sourceCommitAssigned")
    if assigned is True:
        source_commit = manifest.get("sourceCommit")
        require(re.fullmatch(r"[0-9a-f]{40}", str(source_commit)) is not None,
                "upstream certificate source commit is not a full hash")
        require(manifest.get("status") == "sealed" and manifest.get("finalSeal") is True,
                "upstream certificate final-seal status drift")
        require(environment.get("sourceCommitAssigned") is True and
                environment.get("sourceCommit") == source_commit,
                "figure environment/upstream source commit drift")
        if expected_source_commit:
            require(source_commit == expected_source_commit,
                    "figure and certificate source commits differ")
            certificate_verify = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(CERTIFICATE_DIR / "seal_package.py"),
                    "--source-commit",
                    expected_source_commit,
                    "--verify-only",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            require(certificate_verify.returncode == 0,
                    "upstream certificate commit/blob verification failed")
    elif assigned is False:
        require(manifest.get("status") == "hash-bound-uncommitted" and
                manifest.get("finalSeal") is False,
                "upstream certificate pre-seal status drift")
        require(environment.get("sourceCommitAssigned") is False and
                "sourceCommit" not in environment,
                "figure environment assigns an unsupported source commit")
        require(not expected_source_commit,
                "final figure seal requires the certificate sealed to the same commit")
    else:
        raise RuntimeError("upstream certificate source-commit state drift")


def verify_runtime_versions(environment: dict) -> dict[str, str]:
    lock_lines = (HERE / "requirements.txt").read_text(encoding="utf-8").splitlines()
    expected_lines = [
        f"{name}=={version}" for name, version in EXPECTED_DEPENDENCIES.items()
    ]
    require(lock_lines == expected_lines, "requirements lock drift")
    actual = {name: package_version(name) for name in EXPECTED_DEPENDENCIES}
    require(actual == EXPECTED_DEPENDENCIES, "runtime dependency version drift")
    environment_versions = {
        "matplotlib": str(environment.get("matplotlib")),
        "numpy": str(environment.get("numpy")),
        "pillow": str(environment.get("Pillow")),
        "pypdf": str(environment.get("pypdf")),
        "pypdfium2": str(environment.get("pypdfium2")),
    }
    require(environment_versions == EXPECTED_DEPENDENCIES,
            "render environment dependency version drift")
    require(pillow_version == EXPECTED_DEPENDENCIES["pillow"] and
            pypdf_version == EXPECTED_DEPENDENCIES["pypdf"],
            "validator dependency version drift")
    return actual


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        fields = list(reader.fieldnames or [])
        rows = list(reader)
    return fields, rows


def finite_number(row: dict[str, str], key: str) -> float:
    value = float(row[key])
    require(math.isfinite(value), "non-finite source-data value: " + key)
    return value


def verify_csv(diagnostic: dict) -> dict[str, object]:
    upstream_fields, upstream_rows = read_csv(SOURCE_DATA)
    figure_fields, figure_rows = read_csv(HERE / "source-data.csv")
    require(figure_fields == upstream_fields + ["upstream_path", "upstream_sha256"],
            "source-data fields drift")
    require(len(upstream_rows) == len(figure_rows) == 605, "source-data row count drift")
    upstream_path = str(SOURCE_DATA.relative_to(ROOT))
    upstream_hash = sha256(SOURCE_DATA)
    for index, (upstream, figure) in enumerate(zip(upstream_rows, figure_rows)):
        require({key: figure[key] for key in upstream_fields} == upstream,
                "source-data row drift at index " + str(index))
        require(figure["upstream_path"] == upstream_path and
                figure["upstream_sha256"] == upstream_hash,
                "source-data provenance drift at index " + str(index))
    strain = [row for row in figure_rows if row["record_type"] == "strain_sample"]
    cumulative = [row for row in figure_rows if row["record_type"] == "cumulative_sample"]
    basepoints = [row for row in figure_rows if row["record_type"] == "marked_basepoint_sample"]
    require((len(strain), len(cumulative), len(basepoints)) == (241, 243, 121),
            "source-data record inventory drift")
    require({row["record_type"] for row in figure_rows} ==
            {"strain_sample", "cumulative_sample", "marked_basepoint_sample"},
            "unknown source-data record type")
    require(len({row["record_id"] for row in figure_rows}) == 605,
            "duplicate source-data record id")
    for row in strain:
        t = finite_number(row, "t")
        slow = finite_number(row, "slow_strain_component")
        fast = finite_number(row, "fast_strain_component")
        envelope = finite_number(row, "normalized_half_strain_envelope")
        require(close(slow, math.exp(-4 * t), 5e-14), "slow strain formula drift")
        require(close(fast, math.exp(-16 * t), 5e-14), "fast strain formula drift")
        require(close(envelope, slow + fast, 5e-14), "strain envelope formula drift")
    for row in cumulative:
        t = finite_number(row, "t")
        value = finite_number(row, "cumulative_j")
        expected = -math.expm1(-4 * t) / 4 - math.expm1(-16 * t) / 16
        require(close(value, expected, 5e-14), "cumulative j formula drift")
    action_low = float(diagnostic["highPrecision"]["inheritedActionLower"])
    action_high = float(diagnostic["highPrecision"]["inheritedActionUpper"])
    j_star = float(diagnostic["highPrecision"]["jStar"])
    for row in basepoints:
        lam = finite_number(row, "lambda")
        checks = {
            "log10_action_factor_lower": lam * action_low / math.log(10),
            "log10_action_factor_upper": lam * action_high / math.log(10),
            "log10_strain_factor_upper": lam * j_star / math.log(10),
            "marked_basepoint_l2": lam * math.sqrt(5 / 8),
        }
        for key, expected in checks.items():
            require(close(finite_number(row, key), expected, 5e-13),
                    "marked-basepoint formula drift: " + key)
    getcontext().prec = 100
    high = diagnostic["highPrecision"]
    j_star_decimal = Decimal(high["jStar"])
    rational = Decimal(359) / Decimal(324000)
    action_upper = Decimal(173) / Decimal(450000)
    require(Decimal(high["jInfinity"]) == Decimal(5) / Decimal(16),
            "j(infinity) exact value drift")
    require(j_star_decimal > rational > action_upper,
            "strict endpoint exponent chain drift")
    require(abs(Decimal(high["jStarRationalLower"]) - rational) < Decimal("1e-80"),
            "stored high-precision rational witness drift")
    return {
        "strainSamples": len(strain),
        "cumulativeSamples": len(cumulative),
        "markedBasepointSamples": len(basepoints),
        "totalRows": len(figure_rows),
        "upstreamPath": upstream_path,
        "upstreamSha256": upstream_hash,
    }


def image_xobjects(resources: object) -> int:
    """Count raster Image XObjects, recursively following Form XObjects."""
    if resources is None:
        return 0
    if hasattr(resources, "get_object"):
        resources = resources.get_object()
    if not hasattr(resources, "get"):
        return 0
    xobjects = resources.get("/XObject")
    if xobjects is None:
        return 0
    if hasattr(xobjects, "get_object"):
        xobjects = xobjects.get_object()
    total = 0
    for value in xobjects.values():
        obj = value.get_object() if hasattr(value, "get_object") else value
        subtype = obj.get("/Subtype") if hasattr(obj, "get") else None
        if subtype == "/Image":
            total += 1
        elif subtype == "/Form":
            total += image_xobjects(obj.get("/Resources"))
    return total


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
                abs(image.height - expected_png[1]) <= 1,
                "600-dpi PNG dimensions drift")
        dpi = image.info.get("dpi")
        require(dpi is not None and abs(float(dpi[0]) - 600) < 1 and
                abs(float(dpi[1]) - 600) < 1, "PNG DPI metadata drift")
        png_size = [image.width, image.height]
        png_dpi = [float(dpi[0]), float(dpi[1])]
    qa_sizes: dict[str, list[int]] = {}
    for name in ("qa-final-size.png", "qa-grayscale.png", "qa-pdf.png"):
        with Image.open(HERE / name) as image:
            require(abs(image.width - expected_qa[0]) <= 2 and
                    abs(image.height - expected_qa[1]) <= 2,
                    name + " dimensions drift")
            qa_sizes[name] = [image.width, image.height]
    reader = PdfReader(str(HERE / "figure.pdf"))
    require(len(reader.pages) == 1, "PDF is not one page")
    page = reader.pages[0]
    width_mm = float(page.mediabox.width) * 25.4 / 72
    height_mm = float(page.mediabox.height) * 25.4 / 72
    require(abs(width_mm - 178.0) <= 0.02 and abs(height_mm - 96.0) <= 0.02,
            "PDF media box drift")
    raster_xobjects = image_xobjects(page.get("/Resources"))
    require(raster_xobjects == 0, "PDF contains raster image XObjects")
    svg = (HERE / "figure.svg").read_text(encoding="utf-8")
    require("<svg" in svg and re.search(r"<text\b", svg) is not None,
            "SVG text was not preserved")
    require(re.search(r"<image\b", svg) is None, "SVG contains an embedded raster")
    require("R0.73N | finite strain and marked-basepoint exponent bracket" in svg,
            "SVG title text drift")
    require("FINITE / ILLUSTRATIVE" in svg,
            "SVG evidence-boundary footer missing")
    return {
        "pngPixels": png_size,
        "pngDpi": png_dpi,
        "qaPixels": qa_sizes,
        "pdfPages": 1,
        "pdfMillimetres": [width_mm, height_mm],
        "pdfRasterImageXObjects": raster_xobjects,
        "svgRasterImages": 0,
        "svgTextPreserved": True,
    }


def expected_summary(diagnostic: dict, rows: list[dict[str, str]]) -> dict[str, object]:
    return {
        "jStar": diagnostic["highPrecision"]["jStar"],
        "jInfinity": diagnostic["highPrecision"]["jInfinity"],
        "jStarRationalLower": diagnostic["highPrecision"]["jStarRationalLower"],
        "inheritedActionLower": diagnostic["highPrecision"]["inheritedActionLower"],
        "inheritedActionUpper": diagnostic["highPrecision"]["inheritedActionUpper"],
        "margins": diagnostic["highPrecision"]["margins"],
        "maximumDisplayedLog10StrainFactor": max(
            float(row["log10_strain_factor_upper"])
            for row in rows if row["record_type"] == "marked_basepoint_sample"
        ),
    }


def verify_results(results: dict, diagnostic: dict, csv_details: dict[str, object]) -> None:
    require(results.get("schemaVersion") == "r073n-finite-strain-figure-results-v1",
            "results schema drift")
    require(results.get("release") == "R0.73N" and results.get("figureId") == FIGURE_ID,
            "results identity drift")
    require(results.get("allComputationalChecksPass") is True,
            "figure computations did not pass")
    expected_counts = {
        "strainSamples": 241,
        "cumulativeSamples": 243,
        "markedBasepointSamples": 121,
        "totalRows": 605,
    }
    require(results.get("sourceRows") == expected_counts, "result row counts drift")
    _, rows = read_csv(HERE / "source-data.csv")
    require(results.get("summary") == expected_summary(diagnostic, rows),
            "result summary drift")
    require(csv_details["totalRows"] == 605, "validated row total drift")


def verify_monitoring() -> dict[str, object]:
    progress = [
        json.loads(line)
        for line in (HERE / "progress.ndjson").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    resources = [
        json.loads(line)
        for line in (HERE / "resource-log.ndjson").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    expected = ["start", "source-data", "exports", "qa-surfaces", "complete"]
    require([row.get("stage") for row in progress] == expected,
            "progress stage sequence drift")
    require([row.get("stage") for row in resources] == expected,
            "resource stage sequence drift")
    require(all(float(row.get("elapsedSeconds", -1)) >= 0 for row in progress),
            "invalid progress elapsed time")
    require(all(row.get("gpu") == "not used" and row.get("processes") == 1
                for row in resources), "resource-log compute declaration drift")
    return {
        "stages": expected,
        "events": len(progress),
        "wallTimeSeconds": float(progress[-1]["elapsedSeconds"]),
    }


def write_qa_report(
    exports: dict[str, object],
    csv_details: dict[str, object],
    *,
    final: bool,
) -> None:
    status = "PASS - sealed" if final else "PASS - hash-bound, uncommitted"
    final_note = (
        "- The immutable theorem-source commit and all ten figure-source blobs passed verification."
        if final else
        "- Final source-commit sealing is pending; this report confirms visual QA and hash binding."
    )
    report = f"""# R0.73N figure QA report

Status: **{status}**

- The 600-dpi color master and final-size raster were inspected: panel labels,
  legends, annotations, axes, and the two-line evidence boundary are legible and
  unclipped.
- The grayscale raster was inspected: envelope/components, action interval,
  strain curve, and rational witness remain distinguishable by line style and
  fill as well as hue.
- The independently rasterized PDF was inspected and agrees with the PNG
  layout; the PDF itself contains no raster image XObjects.
- Panel B visibly marks both `T*=1/1800` and `j(infinity)=5/16`.
- Panel C states that the curves evaluate formula factors at different marked
  basepoints and does not identify them with a sharp flow-map modulus.
- The figure remains finite and illustrative.  The inherited action interval
  is an analytic input; arbitrary fixed-background instability, full 3D stability,
  singularity, and Clay claims remain open.
{final_note}

Programmatic export facts:
"""
    report += "\n".join(f"- `{key}`: `{value}`" for key, value in exports.items())
    report += "\n\nProgrammatic source-data facts:\n"
    report += "\n".join(f"- `{key}`: `{value}`" for key, value in csv_details.items())
    report += "\n"
    (HERE / "qa-report.md").write_text(report, encoding="utf-8")


def build_manifest(
    validation: dict,
    config: dict,
    contract: dict,
    results: dict,
    environment: dict,
    monitoring: dict[str, object],
    source_commit: str = "",
) -> dict:
    output_records = []
    for name in ("figure.pdf", "figure.svg", "figure.png"):
        row = file_record(HERE / name)
        if name == "figure.png":
            with Image.open(HERE / name) as image:
                row.update({"dpi": 600, "pixels": [image.width, image.height]})
        output_records.append(row)
    data_specs = (
        ("source-data.csv", "605 exact/high-precision source rows with upstream hashes"),
        ("results.json", "finite result summary and claim boundary"),
        ("validation.json", "data, provenance, export, vector, and visual-QA checks"),
        ("environment.json", "runtime versions and SHA-256 upstream bindings"),
        ("progress.ndjson", "deterministic render progress"),
        ("resource-log.ndjson", "process, memory, and GPU monitoring"),
        ("chart-contract-and-source-data.md", "analytical question, derivation, and evidence boundary"),
    )
    qa_names = ("qa-final-size.png", "qa-grayscale.png", "qa-pdf.png", "qa-report.md")
    final = bool(source_commit)
    committed_bindings = source_commit_bindings(source_commit) if final else None
    manifest = {
        "schemaVersion": "r073n-finite-strain-figure-manifest-v1",
        "figureId": FIGURE_ID,
        "release": "R0.73N",
        "status": "sealed" if final else "hash-bound-uncommitted",
        "finalSeal": final,
        "sourceCommitAssigned": final,
        "sourceCommitAssignedMeaning": (
            "The immutable commit contains byte-identical copies of all ten figure source files."
            if final else
            "Source and generated bytes are bound by SHA-256; the parent release may "
            "assign an immutable source commit later."
        ),
        "publicationStatus": "not-published",
        "allPrerequisiteChecksPass": True,
        "validatedAt": validation["createdUtc"],
        "analyticalQuestion": contract["analyticalQuestion"],
        "supportedTakeaway": contract["supportedTakeaway"],
        "claimBoundary": contract["claimBoundary"],
        "packageInventory": {
            "expectedFileCount": 25,
            "sourceFileCount": 10,
            "generatedFileCount": 15,
            "manifestBoundFileCount": 23,
            "sha256SumsLineCount": 24,
            "chartContractSourceDataNote": "chart-contract-and-source-data.md",
            "paths": sorted(PACKAGE_FILES),
        },
        "sourceBindings": [file_record(HERE / name) for name in sorted(SOURCE_FILES)],
        "inputBindings": [input_record(path) for path in INPUTS],
        "certificateSourceData": input_record(SOURCE_DATA),
        "data": [
            {**file_record(HERE / name), "schema": schema}
            for name, schema in data_specs
        ],
        "figure": {
            "profile": "journal-double-column",
            "layout": "three-panel strain, cumulative-j, and marked-basepoint exponent bracket",
            "widthMillimetres": config["widthMillimetres"],
            "heightMillimetres": config["heightMillimetres"],
            "pngDpi": config["pngDpi"],
            "outputs": output_records,
        },
        "computation": {
            "kind": "deterministic finite diagnostic presentation",
            "solver": "no PDE solve; exact formulas and certificate source rows only",
            "precision": "upstream 100-digit diagnostic; deterministic binary64 plotting",
            "monitoring": monitoring,
            "gpu": "not used",
        },
        "environment": {
            "python": environment["python"],
            "matplotlib": environment["matplotlib"],
            "numpy": environment["numpy"],
            "Pillow": pillow_version,
            "pypdf": pypdf_version,
            "pypdfium2": environment["pypdfium2"],
            "packagesLock": "requirements.txt",
        },
        "caption": {"english": "caption.md"},
        "qa": {
            "status": "passed",
            "visualInspectionExplicit": True,
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "pdfRasterInspected": True,
            "labelsLegendsScalesAndUnitsInspected": True,
            "dataCrossChecked": True,
            "qaDpi": config["qaDpi"],
            "records": [file_record(HERE / name) for name in qa_names],
        },
        "masters": ["figure.pdf", "figure.svg", "figure.png"],
        "publication": {
            "publicCopiesCreated": False,
            "publicPagesModified": False,
            "byteIdentityRequiredOnFuturePublication": True,
        },
        "files": [
            file_record(HERE / name)
            for name in sorted(PACKAGE_FILES - {"manifest.json", "SHA256SUMS"})
        ],
    }
    certificate_manifest = load_json(PACKAGE_MANIFEST)
    if certificate_manifest.get("sourceCommitAssigned") is True:
        manifest["upstreamCertificateSourceCommit"] = certificate_manifest["sourceCommit"]
    if final:
        manifest["sourceCommit"] = source_commit
        manifest["sourceCommitBindings"] = committed_bindings
    else:
        manifest["finalSealPendingReason"] = (
            "No immutable R0.73N theorem-source commit has been assigned to this figure package."
        )
    return manifest


def write_hash_binding(manifest: dict, validation: dict) -> None:
    (HERE / "validation.json").write_text(canonical(validation), encoding="utf-8")
    (HERE / "manifest.json").write_text(canonical(manifest), encoding="utf-8")
    lines = [
        f"{sha256(HERE / name)}  {name}"
        for name in sorted(PACKAGE_FILES - {"SHA256SUMS"})
    ]
    (HERE / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")


def verify_hash_binding(expected_source_commit: str = "") -> None:
    verify_inventory(complete=True)
    manifest = load_json(HERE / "manifest.json")
    validation = load_json(HERE / "validation.json")
    require(manifest.get("schemaVersion") == "r073n-finite-strain-figure-manifest-v1",
            "manifest schema drift")
    require(manifest.get("publicationStatus") == "not-published",
            "unexpected publication claim")
    require(validation.get("status") == "passed" and
            validation.get("allChecksPass") is True,
            "figure package validation did not pass")
    inventory = manifest.get("packageInventory", {})
    require(inventory.get("expectedFileCount") == 25 and
            inventory.get("sourceFileCount") == 10 and
            inventory.get("generatedFileCount") == 15 and
            inventory.get("manifestBoundFileCount") == 23 and
            inventory.get("sha256SumsLineCount") == 24 and
            inventory.get("paths") == sorted(PACKAGE_FILES),
            "manifest inventory drift")
    require(manifest.get("sourceBindings") == [
        file_record(HERE / name) for name in sorted(SOURCE_FILES)
    ], "manifest source bindings drift")
    require(manifest.get("certificateSourceData") == input_record(SOURCE_DATA),
            "certificate source-data manifest binding drift")
    records = {row["path"]: row for row in manifest.get("files", [])}
    require(set(records) == PACKAGE_FILES - {"manifest.json", "SHA256SUMS"},
            "manifest file-record inventory drift")
    for name, row in records.items():
        path = HERE / name
        require(path.stat().st_size == row.get("bytes") and sha256(path) == row.get("sha256"),
                "manifest file binding drift: " + name)
    expected_lines = [
        f"{sha256(HERE / name)}  {name}"
        for name in sorted(PACKAGE_FILES - {"SHA256SUMS"})
    ]
    actual_lines = (HERE / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    require(actual_lines == expected_lines, "SHA256SUMS binding drift")
    assigned = manifest.get("sourceCommitAssigned")
    if assigned is True:
        source_commit = manifest.get("sourceCommit")
        require(re.fullmatch(r"[0-9a-f]{40}", str(source_commit)) is not None,
                "sealed figure source commit is not a full hash")
        if expected_source_commit:
            require(source_commit == expected_source_commit,
                    "requested source commit differs from sealed figure manifest")
        require(manifest.get("status") == "sealed" and manifest.get("finalSeal") is True,
                "sealed figure provenance status drift")
        require(manifest.get("sourceCommitBindings") ==
                source_commit_bindings(str(source_commit)),
                "sealed figure source-commit bindings drift")
        certificate_manifest = load_json(PACKAGE_MANIFEST)
        require(certificate_manifest.get("status") == "sealed" and
                certificate_manifest.get("finalSeal") is True and
                certificate_manifest.get("sourceCommit") == source_commit and
                manifest.get("upstreamCertificateSourceCommit") == source_commit,
                "sealed figure/certificate source commit drift")
        results = load_json(HERE / "results.json")
        require(results.get("status") == "passed-sealed" and
                results.get("finalSeal") is True and
                results.get("sourceCommit") == source_commit,
                "sealed figure results provenance drift")
        require(validation.get("finalSeal") is True and
                validation.get("sourceCommitAssigned") is True and
                validation.get("sourceCommit") == source_commit,
                "sealed figure validation provenance drift")
    elif assigned is False:
        require(not expected_source_commit,
                "figure manifest is not sealed to the requested source commit")
        require(manifest.get("status") == "hash-bound-uncommitted" and
                manifest.get("finalSeal") is False,
                "uncommitted figure provenance status drift")
        require("sourceCommit" not in manifest and "sourceCommitBindings" not in manifest,
                "uncommitted figure manifest contains source-commit claims")
        results = load_json(HERE / "results.json")
        require(results.get("status") == "passed-hash-bound-uncommitted" and
                results.get("finalSeal") is False and
                results.get("sourceCommitAssigned") is False and
                "sourceCommit" not in results,
                "uncommitted figure results provenance drift")
        require(validation.get("finalSeal") is False and
                validation.get("sourceCommitAssigned") is False and
                "sourceCommit" not in validation,
                "uncommitted figure validation provenance drift")
    else:
        raise RuntimeError("figure manifest source-commit state drift")


def semantic_checks(
    expected_source_commit: str = "",
) -> tuple[dict, dict, dict, dict, dict[str, object], dict[str, object], dict[str, object]]:
    config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    results = load_json(HERE / "results.json")
    environment = load_json(HERE / "environment.json")
    diagnostic = load_json(DIAGNOSTIC)
    verify_runtime_versions(environment)
    verify_contract(config, contract, results)
    verify_inputs(environment, expected_source_commit)
    csv_details = verify_csv(diagnostic)
    exports = verify_exports(config)
    verify_results(results, diagnostic, csv_details)
    monitoring = verify_monitoring()
    return config, contract, results, environment, csv_details, exports, monitoring


def main() -> int:
    args = parse_args()
    if args.verify_only:
        verify_hash_binding(args.source_commit)
        manifest = load_json(HERE / "manifest.json")
        sealed_commit = (
            str(manifest["sourceCommit"])
            if manifest.get("sourceCommitAssigned") is True else ""
        )
        semantic_checks(sealed_commit)
        print(canonical({
            "event": "verified",
            "status": manifest["status"],
            "files": 25,
            "verifyOnly": True,
        }), end="")
        return 0
    require(args.confirm_visual_qa,
            "visual QA is not confirmed; inspect all three QA surfaces first")
    if args.source_commit:
        source_commit_bindings(args.source_commit)
    verify_inventory(complete=False)
    config, contract, results, environment, csv_details, exports, monitoring = semantic_checks(
        args.source_commit
    )
    final = bool(args.source_commit)
    write_qa_report(exports, csv_details, final=final)
    results["status"] = "passed-sealed" if final else "passed-hash-bound-uncommitted"
    results["allChecksPass"] = True
    results["finalSeal"] = final
    results["sourceCommitAssigned"] = final
    if final:
        results["sourceCommit"] = args.source_commit
    else:
        results.pop("sourceCommit", None)
    results["visualQA"] = {
        "confirmed": True,
        "surfaces": ["qa-final-size.png", "qa-grayscale.png", "qa-pdf.png"],
    }
    (HERE / "results.json").write_text(canonical(results), encoding="utf-8")
    validation = {
        "schemaVersion": "r073n-finite-strain-figure-validation-v1",
        "createdUtc": datetime.now(timezone.utc).isoformat(),
        "status": "passed",
        "allChecksPass": True,
        "finalSeal": final,
        "sourceCommitAssigned": final,
        "checks": {
            "twentyFiveFileInventory": True,
            "tenSourceAndFifteenGeneratedFiles": True,
            "chartContractSourceDataNotePresent": True,
            "contractAndClaimBoundaryExact": True,
            "validatedUpstreamBindings": True,
            "sourceDataRowForRowBinding": True,
            "exactAndHighPrecisionSummary": True,
            "strictExponentChain": True,
            "exportDimensionsAndDpi": True,
            "vectorPdfAndSvg": True,
            "monitoringComplete": True,
            "manualColorGrayscalePdfInspection": True,
        },
        "details": {
            "packageFiles": 25,
            "sourceFiles": 10,
            "generatedFiles": 15,
            "sourceData": csv_details,
            "exports": exports,
            "monitoring": monitoring,
            "pillow": pillow_version,
            "pypdf": pypdf_version,
            "dependencyVersions": EXPECTED_DEPENDENCIES,
        },
    }
    if final:
        validation["sourceCommit"] = args.source_commit
    (HERE / "validation.json").write_text(canonical(validation), encoding="utf-8")
    manifest = build_manifest(
        validation, config, contract, results, environment, monitoring, args.source_commit
    )
    write_hash_binding(manifest, validation)
    verify_hash_binding(args.source_commit)
    semantic_checks(args.source_commit)
    print(canonical({
        "event": "validated",
        "status": "sealed" if final else "hash-bound-uncommitted",
        "files": 25,
        "visualQA": "confirmed",
        "sourceCommitAssigned": final,
    }), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
