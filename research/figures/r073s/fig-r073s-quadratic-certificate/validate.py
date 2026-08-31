#!/usr/bin/env python3
"""Independent fail-closed validation and sealing for the R0.73S figure."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from fractions import Fraction
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
FIGURE_ID = "fig-r073s-quadratic-certificate"
CERTIFICATE_CSV = ROOT / "research/certificates/r073s/source-data.csv"
CERTIFICATE_VALIDATOR = ROOT / "research/certificates/r073s/validate_certificate.py"
CERTIFICATE_SEALER = ROOT / "research/certificates/r073s/seal_package.py"
SOURCE_FILES = {
    "README.md", "caption.md", "chart-contract-and-source-data.md", "command.txt",
    "config.json", "contract.json", "plot.py", "qa-protocol.md", "requirements.txt",
    "validate.py",
}
RAW_FILES = {
    "source-data.csv", "figure.pdf", "figure.svg", "figure.png", "qa-final-size.png",
    "qa-grayscale.png", "qa-pdf.png", "environment.json", "results.json",
    "progress.ndjson", "resource-log.ndjson",
}
METADATA_FILES = {"validation.json", "manifest.json", "qa-report.md", "SHA256SUMS"}
PACKAGE_FILES = SOURCE_FILES | RAW_FILES | METADATA_FILES
MANIFEST_BOUND_FILES = SOURCE_FILES | RAW_FILES | {"validation.json", "qa-report.md"}
EXPECTED_DEPENDENCIES = {
    "matplotlib": "3.10.6",
    "numpy": "2.5.2",
    "pillow": "12.3.0",
    "pypdf": "6.10.0",
    "pypdfium2": "5.13.0",
}
CSV_FIELDS = (
    "panel", "series", "parameter", "x", "y", "quantity_class",
    "source_origin", "source_record_type", "source_family", "formula",
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


def close(actual: float, expected: float, tolerance: float = 3e-12) -> bool:
    return math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance)


def add(checks: list[dict[str, object]], check_id: str, passed: bool) -> None:
    checks.append({"id": check_id, "pass": bool(passed)})
    require(bool(passed), "check failed: " + check_id)


def verify_inventory(*, metadata_required: bool) -> None:
    required = SOURCE_FILES | RAW_FILES | (METADATA_FILES if metadata_required else set())
    actual = {path.name for path in HERE.iterdir() if path.is_file()}
    require(actual <= PACKAGE_FILES, "unexpected figure-package files: " + repr(sorted(actual - PACKAGE_FILES)))
    require(required <= actual, "missing figure-package files: " + repr(sorted(required - actual)))
    require(len(SOURCE_FILES) == 10 and len(RAW_FILES) == 11 and len(PACKAGE_FILES) == 25,
            "frozen inventory count drift")


def git_blob(commit: str, relative_path: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"{commit}:{relative_path}"], cwd=ROOT,
        capture_output=True, check=False,
    )
    require(completed.returncode == 0, "source file absent from source commit: " + relative_path)
    return completed.stdout


def verify_source_commit(commit: str) -> None:
    require(bool(re.fullmatch(r"[0-9a-f]{40}", commit)), "source commit must be a full lowercase SHA-1")
    completed = subprocess.run(
        ["git", "cat-file", "-e", commit + "^{commit}"], cwd=ROOT,
        capture_output=True, check=False,
    )
    require(completed.returncode == 0, "source commit does not resolve")
    for name in sorted(SOURCE_FILES):
        path = HERE / name
        relative = path.relative_to(ROOT).as_posix()
        require(git_blob(commit, relative) == path.read_bytes(), "source drift from commit: " + name)


def verify_certificate(*, require_final: bool) -> None:
    require(CERTIFICATE_CSV.is_file(), "missing R0.73S certificate source-data")
    completed = subprocess.run(
        [sys.executable, str(CERTIFICATE_VALIDATOR), "--verify-only"], cwd=ROOT,
        text=True, capture_output=True, check=False,
    )
    require(completed.returncode == 0, "R0.73S certificate structural verification failed")
    if require_final:
        completed = subprocess.run(
            [sys.executable, str(CERTIFICATE_SEALER), "--verify-only"], cwd=ROOT,
            text=True, capture_output=True, check=False,
        )
        require(completed.returncode == 0, "R0.73S certificate final seal verification failed")


def read_figure_rows() -> list[dict[str, str]]:
    with (HERE / "source-data.csv").open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        require(tuple(reader.fieldnames or ()) == CSV_FIELDS, "figure source-data schema drift")
        rows = list(reader)
    require(all(set(row) == set(CSV_FIELDS) for row in rows), "figure source-data row schema drift")
    return rows


def read_certificate_rows() -> list[dict[str, str]]:
    with CERTIFICATE_CSV.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def expected_row(
    panel: str, series: str, parameter: int, x: float, y: float,
    quantity_class: str, source_origin: str, source_record_type: str,
    source_family: str, formula: str,
) -> dict[str, object]:
    return {
        "panel": panel,
        "series": series,
        "parameter": str(parameter),
        "x": x,
        "y": y,
        "quantity_class": quantity_class,
        "source_origin": source_origin,
        "source_record_type": source_record_type,
        "source_family": source_family,
        "formula": formula,
    }


def reconstruct_rows(config: dict[str, Any], certificate: list[dict[str, str]]) -> list[dict[str, object]]:
    expected: list[dict[str, object]] = []
    spikes = {int(item["parameter"]): item for item in certificate
              if item["record_type"] in {
                  "fixed_quartic_spike", "bounded_quartic_spike",
                  "asymptotically_fixed_quartic_spike",
              }}
    for m_value in config["panelA"]["mValues"]:
        source = spikes[int(m_value)]
        gamma = float(Fraction(source["l4_fourth"]))
        theta = float(Fraction(source["l6_sixth"]))
        support_field = "autocorrelation_support" if "autocorrelation_support" in source else "difference_support"
        support = int(source[support_field])
        expected.extend((
            expected_row("A", "exact_theta", m_value, support, theta, "exact",
                         "sealed-r073s-certificate", source["record_type"], source["family"], "Theta_m"),
            expected_row("A", "autocorrelation_certificate", m_value, support,
                         gamma * math.sqrt(support * gamma), "rigorous-upper-bound",
                         "sealed-r073s-certificate", source["record_type"], source["family"],
                         "Gamma_m^(3/2)*sqrt(D_C)"),
            expected_row("A", "sharp_asymptotic_guide", m_value, support,
                         11.0 / 40.0 * math.sqrt(support), "analytic-asymptotic-guide",
                         "exact-formula", source["record_type"], source["family"],
                         "(11/40)*sqrt(D_C)"),
        ))

    matched = {(item["family"], int(item["parameter"])): item for item in certificate
               if item["record_type"] == "matched_r073r"}
    for exponent in range(int(config["panelB"]["minimumExponent"]),
                          int(config["panelB"]["maximumExponent"]) + 1):
        m_value = 2**exponent
        for family in ("D", "RS"):
            source = matched[(family, exponent)]
            theta = float(Fraction(source["l6_sixth"]))
            exact = m_value ** (-2.0 / 3.0) * theta ** (1.0 / 6.0)
            bound = float(source["scaled_heat_proxy"])
            expected.extend((
                expected_row("B", f"{family}_certificate", exponent, m_value, bound,
                             "rigorous-upper-bound", "sealed-r073s-certificate",
                             source["record_type"], family, "m^(-2/3)*(A*Q)^(1/6)"),
                expected_row("B", f"{family}_exact", exponent, m_value, exact, "exact",
                             "sealed-r073s-certificate", source["record_type"], family,
                             "m^(-2/3)*Theta^(1/6)"),
            ))

    panel_c = config["panelC"]
    no_go_counts: dict[int, set[str]] = {}
    for item in certificate:
        if item["record_type"] == "riesz_product_no_go":
            no_go_counts.setdefault(int(item["parameter"]), set()).add(item["family"])
    sealed_depths = {depth for depth, families in no_go_counts.items() if families == {"A", "B"}}
    for depth in range(int(panel_c["minimumDepth"]), int(panel_c["maximumDepth"]) + 1,
                       int(panel_c["depthStep"])):
        expected.append(expected_row(
            "C", "l6_norm_ratio", depth, depth, (323.0 / 311.0) ** (depth / 6.0),
            "exact", "sealed-r073s-certificate" if depth in sealed_depths else "exact-formula",
            "riesz_product_no_go", "B/A", "(323/311)^(r/6)",
        ))
    return expected


def check_formula_data(config: dict[str, Any], checks: list[dict[str, object]]) -> dict[str, object]:
    rows = read_figure_rows()
    certificate = read_certificate_rows()
    expected = reconstruct_rows(config, certificate)
    expected_panel_counts = {
        "A": 3 * len(config["panelA"]["mValues"]),
        "B": 4 * (
            int(config["panelB"]["maximumExponent"])
            - int(config["panelB"]["minimumExponent"]) + 1
        ),
        "C": len(range(
            int(config["panelC"]["minimumDepth"]),
            int(config["panelC"]["maximumDepth"]) + 1,
            int(config["panelC"]["depthStep"]),
        )),
    }
    expected_row_count = sum(expected_panel_counts.values())
    add(checks, "source-row-count", len(rows) == len(expected) == expected_row_count)
    panel_counts = {panel: sum(item["panel"] == panel for item in rows) for panel in "ABC"}
    add(checks, "source-panel-counts", panel_counts == expected_panel_counts)
    maximum_error = 0.0
    for index, (actual, wanted) in enumerate(zip(rows, expected, strict=True)):
        exact_fields = set(CSV_FIELDS) - {"x", "y"}
        exact_ok = all(actual[field] == str(wanted[field]) for field in exact_fields)
        x_value = float(actual["x"])
        y_value = float(actual["y"])
        numeric_ok = close(x_value, float(wanted["x"])) and close(y_value, float(wanted["y"]))
        denominator = max(1.0, abs(float(wanted["y"])))
        maximum_error = max(maximum_error, abs(y_value - float(wanted["y"])) / denominator)
        add(checks, f"source-row-{index:02d}", exact_ok and numeric_ok)

    by_series = {(item["series"], int(item["parameter"])): float(item["y"]) for item in rows}
    for exponent in range(
        int(config["panelB"]["minimumExponent"]),
        int(config["panelB"]["maximumExponent"]) + 1,
    ):
        for family in ("D", "RS"):
            add(checks, f"panel-b-upper-{family}-{exponent}",
                by_series[(f"{family}_exact", exponent)] <=
                by_series[(f"{family}_certificate", exponent)] * (1.0 + 2e-13))
    c_values = [float(item["y"]) for item in rows if item["panel"] == "C"]
    c_parameters = [int(item["parameter"]) for item in rows if item["panel"] == "C"]
    add(checks, "panel-c-strict-growth", all(right > left for left, right in zip(c_values, c_values[1:])))
    add(checks, "panel-c-starts-at-one", close(c_values[0], 1.0))
    add(checks, "panel-c-every-integer-depth",
        int(config["panelC"]["depthStep"]) == 1
        and c_parameters == list(range(
            int(config["panelC"]["minimumDepth"]),
            int(config["panelC"]["maximumDepth"]) + 1,
        )))
    add(checks, "panel-c-no-carry-radix", int(config["panelC"]["minimumRadix"]) >= 14)

    generic = {item["family"]: item for item in certificate
               if item["record_type"] == "generic_sequence" and item["family"] in {"A", "B"}}
    add(checks, "panel-c-base-pair-present", set(generic) == {"A", "B"})
    add(checks, "panel-c-base-low-summary-match",
        generic["A"]["modes"] == generic["B"]["modes"] == "5"
        and generic["A"]["l2_squared"] == generic["B"]["l2_squared"] == "5"
        and generic["A"]["l4_fourth"] == generic["B"]["l4_fourth"] == "37")
    add(checks, "panel-c-base-sixth-split",
        generic["A"]["l6_sixth"] == "311" and generic["B"]["l6_sixth"] == "323"
        and Fraction(generic["B"]["l6_sixth"]) > Fraction(generic["A"]["l6_sixth"]))

    no_go = {(item["family"], int(item["parameter"])): item for item in certificate
             if item["record_type"] == "riesz_product_no_go"}
    sealed_maximum = int(config["panelC"]["sealedMaximumDepth"])
    for depth in range(1, sealed_maximum + 1):
        left = no_go[("A", depth)]
        right = no_go[("B", depth)]
        add(checks, f"panel-c-sealed-factorization-{depth}",
            left["modes"] == right["modes"] == str(5**depth)
            and left["l2_squared"] == right["l2_squared"] == str(5**depth)
            and left["l4_fourth"] == right["l4_fourth"] == str(37**depth)
            and left["l6_sixth"] == str(311**depth)
            and right["l6_sixth"] == str(323**depth)
            and left.get("autocorrelation_support", "") == right.get("autocorrelation_support", "") == ""
            and left.get("difference_set_size", "") == right.get("difference_set_size", "") == str(9**depth))
    c_origins = {int(item["parameter"]): item["source_origin"] for item in rows if item["panel"] == "C"}
    add(checks, "panel-c-origin-membership",
        c_origins.get(0) == "exact-formula"
        and all(c_origins.get(depth) == "sealed-r073s-certificate" for depth in range(1, sealed_maximum + 1))
        and all(c_origins.get(depth) == "exact-formula"
                for depth in range(sealed_maximum + 1, int(config["panelC"]["maximumDepth"]) + 1)))
    add(checks, "panel-c-unbounded-identity-base", Fraction(323, 311) > 1)
    return {"rowCount": len(rows), "panelRowCounts": panel_counts, "maximumRelativeError": maximum_error}


def check_assets(config: dict[str, Any], checks: list[dict[str, object]]) -> dict[str, object]:
    from pypdf import PdfReader  # type: ignore

    width_mm = float(config["widthMillimetres"])
    height_mm = float(config["heightMillimetres"])
    with Image.open(HERE / "figure.png") as image:
        png_size = image.size
        add(checks, "png-mode", image.mode in {"RGB", "RGBA"})
    expected_png = (round(width_mm / 25.4 * int(config["pngDpi"])),
                    round(height_mm / 25.4 * int(config["pngDpi"])))
    add(checks, "png-pixels", all(abs(a - b) <= 1 for a, b in zip(png_size, expected_png, strict=True)))

    expected_qa = (round(width_mm / 25.4 * int(config["qaDpi"])),
                   round(height_mm / 25.4 * int(config["qaDpi"])))
    for name in ("qa-final-size.png", "qa-grayscale.png", "qa-pdf.png"):
        with Image.open(HERE / name) as image:
            add(checks, "qa-size-" + name, all(abs(a - b) <= 1 for a, b in zip(image.size, expected_qa, strict=True)))

    reader = PdfReader(str(HERE / "figure.pdf"))
    add(checks, "pdf-one-page", len(reader.pages) == 1)
    page = reader.pages[0]
    actual_width_mm = float(page.mediabox.width) * 25.4 / 72.0
    actual_height_mm = float(page.mediabox.height) * 25.4 / 72.0
    add(checks, "pdf-physical-size", abs(actual_width_mm - width_mm) < 0.05 and abs(actual_height_mm - height_mm) < 0.05)
    add(checks, "pdf-vector-only", len(page.images) == 0)

    svg = (HERE / "figure.svg").read_text(encoding="utf-8")
    add(checks, "svg-vector-only", "<image" not in svg.lower())
    add(checks, "svg-has-three-panel-labels", all(f">{letter}<" in svg for letter in "ABC"))
    add(checks, "svg-required-panel-titles", all(text in svg for text in (
        "The $D_C^{1/2}$ loss is sharp",
        "Matched support, separated phase",
        "Low summaries miss $L^6$",
    )))
    add(checks, "svg-no-clay-overclaim", "Clay problem solved" not in svg)
    return {
        "pngPixels": list(png_size),
        "pdfMillimetres": [actual_width_mm, actual_height_mm],
        "embeddedPdfImages": len(page.images),
    }


def check_metadata(config: dict[str, Any], contract: dict[str, Any], checks: list[dict[str, object]]) -> dict[str, object]:
    add(checks, "figure-id", config.get("figureId") == contract.get("figureId") == FIGURE_ID)
    claim = contract["claimBoundary"]
    expected_claim = {
        "exactFormulaAndUpperBoundOnly": True,
        "fittedScalingLaw": False,
        "navierStokesSimulation": False,
        "complexityLowerBound": False,
        "necessaryRegularityCriterion": False,
        "unsafeDynamics": False,
        "finiteTimeSingularity": False,
        "arbitraryL2SmallDataSafe": False,
        "clayProblemSolved": False,
        "sharpnessLiftHasZeroConvection": True,
    }
    add(checks, "claim-boundary", claim == expected_claim)
    chart_text = (HERE / "chart-contract-and-source-data.md").read_text(encoding="utf-8")
    caption_text = (HERE / "caption.md").read_text(encoding="utf-8")
    add(checks, "text-quantifier-boundary",
        "every integer radix \\(q\\ge14\\)" in chart_text
        and "integer depth \\(r\\in\\mathbb N_0\\)" in chart_text
        and "not from the finite" in chart_text
        and "empty-product identity" in caption_text)
    add(checks, "text-dynamics-boundary",
        "zero-convection shear flows" in caption_text
        and "do not indicate singular dynamics" in caption_text)
    environment = load_json(HERE / "environment.json")
    add(checks, "environment-no-dgx", environment.get("dgxUsed") is False and environment.get("gpu") == "not used")
    add(checks, "dependency-versions", environment.get("packages") == EXPECTED_DEPENDENCIES)
    results = load_json(HERE / "results.json")
    expected_rows = (
        3 * len(config["panelA"]["mValues"])
        + 4 * (int(config["panelB"]["maximumExponent"]) - int(config["panelB"]["minimumExponent"]) + 1)
        + len(range(int(config["panelC"]["minimumDepth"]),
                    int(config["panelC"]["maximumDepth"]) + 1,
                    int(config["panelC"]["depthStep"])))
    )
    add(checks, "results-row-count", results.get("rowCount") == expected_rows)
    add(checks, "results-claim-boundary", results.get("isFittedScalingLaw") is False
        and results.get("isNavierStokesSimulation") is False
        and results.get("isComplexityLowerBound") is False
        and results.get("dgxUsed") is False)
    add(checks, "results-certificate-binding",
        results.get("certificateSource", {}).get("sha256") == sha256(CERTIFICATE_CSV))
    return {"certificateSha256": sha256(CERTIFICATE_CSV), "dependencies": environment.get("packages")}


def build_validation(*, final: bool, visual_confirmed: bool, source_commit: str) -> dict[str, object]:
    verify_inventory(metadata_required=False)
    verify_certificate(require_final=final)
    if final:
        verify_source_commit(source_commit)
    config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    checks: list[dict[str, object]] = []
    formula = check_formula_data(config, checks)
    assets = check_assets(config, checks)
    metadata = check_metadata(config, contract, checks)
    add(checks, "visual-qa-confirmed", visual_confirmed if final else True)
    return {
        "schemaVersion": "r073s-quadratic-certificate-figure-validation-v1",
        "figureId": FIGURE_ID,
        "createdAt": utc_now(),
        "mode": "final" if final else "preseal",
        "formalStatus": "pass" if final else "preseal-pass",
        "sourceCommit": source_commit if final else None,
        "visualQaConfirmed": visual_confirmed if final else False,
        "allChecksPass": all(item["pass"] for item in checks),
        "checkCount": len(checks),
        "checks": checks,
        "formulaAudit": formula,
        "assetAudit": assets,
        "metadataAudit": metadata,
    }


def write_qa_report(validation: dict[str, object]) -> None:
    lines = [
        "# R0.73S independent figure QA report",
        "",
        f"- Independent reconstruction of all {validation['formulaAudit']['rowCount']} plotted source-data rows: **PASS**.",
        f"- Structural and formula checks: **{validation['checkCount']}/{validation['checkCount']} PASS**.",
        "- Panel B exact values lie below their AQ certificates: **PASS**.",
        "- Vector PDF/SVG, 600-dpi PNG, and PDF-raster checks: **PASS**.",
        "- PDF physical size 178 by 96 mm; embedded raster objects: **zero**.",
        "- Final-size, grayscale, and PDF-raster visual inspection: **CONFIRMED**.",
        "- Labels, legends, colour/marker redundancy, and claim boundaries: **PASS**.",
        "- R0.73S source certificate final seal: **VERIFIED**.",
        "- DGX or GPU use: **no**.",
        "- Package sealing state: **FORMAL PASS**.",
        "",
        "The validator independently rebuilds every plotted value without importing",
        "plotting code. It checks the sealed 311/323 seed and the exact factorization",
        "rows through depth eight. Panel C values beyond depth eight are independently",
        "re-evaluated closed-form values, not additional finite-enumeration claims.",
        "The final seal binds all source files to the immutable Git source",
        f"commit `{validation['sourceCommit']}`.",
        "",
    ]
    (HERE / "qa-report.md").write_text("\n".join(lines), encoding="utf-8")


def write_seal(validation: dict[str, object]) -> None:
    write_qa_report(validation)
    bound = [record(HERE / name) for name in sorted(MANIFEST_BOUND_FILES)]
    manifest = {
        "schemaVersion": "r073s-quadratic-certificate-figure-manifest-v1",
        "figureId": FIGURE_ID,
        "release": "R0.73S",
        "status": "sealed",
        "finalSeal": True,
        "sourceCommit": validation["sourceCommit"],
        "sourceCommitAssigned": True,
        "visualQaConfirmed": True,
        "boundFileCount": len(bound),
        "files": bound,
    }
    (HERE / "manifest.json").write_text(canonical(manifest), encoding="utf-8")
    checksum_names = sorted(MANIFEST_BOUND_FILES | {"manifest.json"})
    lines = [f"{sha256(HERE / name)}  {name}" for name in checksum_names]
    (HERE / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")


def verify_seal() -> dict[str, object]:
    verify_inventory(metadata_required=True)
    manifest = load_json(HERE / "manifest.json")
    require(manifest.get("figureId") == FIGURE_ID, "manifest figure id drift")
    require(manifest.get("status") == "sealed" and manifest.get("finalSeal") is True,
            "manifest is not a final seal")
    commit = str(manifest.get("sourceCommit", ""))
    verify_source_commit(commit)
    verify_certificate(require_final=True)
    records = manifest.get("files")
    require(isinstance(records, list) and len(records) == len(MANIFEST_BOUND_FILES),
            "manifest file count drift")
    by_name = {item["path"]: item for item in records if isinstance(item, dict)}
    require(set(by_name) == MANIFEST_BOUND_FILES, "manifest path inventory drift")
    for name in MANIFEST_BOUND_FILES:
        item = by_name[name]
        require(item.get("sha256") == sha256(HERE / name), "manifest hash drift: " + name)
        require(item.get("bytes") == (HERE / name).stat().st_size, "manifest size drift: " + name)
    lines = (HERE / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    expected_names = sorted(MANIFEST_BOUND_FILES | {"manifest.json"})
    require(len(lines) == len(expected_names), "checksum line count drift")
    parsed: dict[str, str] = {}
    for line in lines:
        match = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9_.-]+)", line)
        require(match is not None, "malformed checksum line")
        parsed[match.group(2)] = match.group(1)
    require(sorted(parsed) == expected_names, "checksum path inventory drift")
    for name in expected_names:
        require(parsed[name] == sha256(HERE / name), "checksum hash drift: " + name)
    saved = load_json(HERE / "validation.json")
    require(saved.get("allChecksPass") is True and saved.get("formalStatus") == "pass",
            "saved validation is not final pass")
    require(saved.get("sourceCommit") == commit and saved.get("visualQaConfirmed") is True,
            "saved validation source/visual state drift")
    require("FORMAL PASS" in (HERE / "qa-report.md").read_text(encoding="utf-8"),
            "QA report lacks formal status")
    return {"sealed": True, "sourceCommit": commit, "boundFiles": len(records),
            "checksumLines": len(lines)}


def main() -> int:
    args = parse_args()
    if args.verify_only:
        require(args.final, "--verify-only requires --final")
        seal = verify_seal()
        validation = build_validation(
            final=True, visual_confirmed=True, source_commit=str(seal["sourceCommit"])
        )
        require(validation["allChecksPass"] is True, "post-seal structural validation failed")
        print(canonical({
            "allChecksPass": True,
            "checkCount": validation["checkCount"],
            "sealVerified": True,
            **seal,
        }), end="")
        return 0

    final = bool(args.final)
    if final:
        require(args.confirm_visual_qa, "final seal requires --confirm-visual-qa")
        require(bool(args.source_commit), "final seal requires --source-commit")
    validation = build_validation(
        final=final,
        visual_confirmed=bool(args.confirm_visual_qa),
        source_commit=args.source_commit,
    )
    require(validation["allChecksPass"] is True, "one or more figure checks failed")
    (HERE / "validation.json").write_text(canonical(validation), encoding="utf-8")
    if final:
        write_seal(validation)
        seal = verify_seal()
        print(canonical({
            "allChecksPass": True,
            "checkCount": validation["checkCount"],
            "sealVerified": True,
            **seal,
        }), end="")
    else:
        print(canonical({
            "allChecksPass": True,
            "checkCount": validation["checkCount"],
            "sealVerified": False,
        }), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
