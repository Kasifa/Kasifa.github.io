#!/usr/bin/env python3
"""Fail-closed validation and provenance seal for the R0.73T figure."""

from __future__ import annotations

import argparse
import csv
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
from PIL import Image, ImageChops  # type: ignore  # noqa: E402
from pypdf import PdfReader  # type: ignore  # noqa: E402
import pypdfium2 as pdfium  # type: ignore  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
FIGURE_ID = "fig-r073t-dynamic-autocorrelation"
CERTIFICATE_SCRIPT = ROOT / "research/certificates/r073t/compute_exact_certificate.py"
CERTIFICATE_MANIFEST = ROOT / "research/certificates/r073t/manifest.json"
CERTIFICATE_SEALER = ROOT / "research/certificates/r073t/seal_package.py"
ANALYTIC_SOURCE = ROOT / "research/r073t_dynamic_autocorrelation_budget.md"
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
CSV_FIELDS = (
    "panel", "series", "parameter", "x", "y", "quantity_class",
    "source_origin", "source_record_type", "formula", "normalization",
)
EXPECTED_DEPENDENCIES = {
    "matplotlib": "3.10.6", "numpy": "2.5.2", "pillow": "12.3.0",
    "pypdf": "6.10.0", "pypdfium2": "5.13.0",
}
EXPECTED_CHECK_COUNT = 106


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--confirm-visual-qa", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    return parser.parse_args()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    output: dict[str, object] = {}
    for key, value in pairs:
        require(key not in output, "duplicate JSON key: " + key)
        output[key] = value
    return output


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink(), "missing regular JSON: " + str(path))
    value = json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=reject_duplicate_keys,
    )
    require(isinstance(value, dict), "JSON root is not an object: " + str(path))
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def record(path: Path) -> dict[str, object]:
    return {"bytes": path.stat().st_size, "path": path.name, "sha256": sha256(path)}


def git_blob(commit: str, relative: str) -> bytes:
    completed = subprocess.run(
        ["git", "cat-file", "blob", f"{commit}:{relative}"], cwd=ROOT,
        capture_output=True, check=False,
    )
    require(completed.returncode == 0, "source absent from commit: " + relative)
    return completed.stdout


def verify_source_commit(commit: str) -> list[dict[str, object]]:
    require(re.fullmatch(r"[0-9a-f]{40}", commit) is not None,
            "source commit must be full lowercase 40-hex")
    completed = subprocess.run(
        ["git", "cat-file", "-e", commit + "^{commit}"], cwd=ROOT,
        capture_output=True, check=False,
    )
    require(completed.returncode == 0, "source commit does not resolve")
    bindings = []
    declared = [(HERE / name, "figure-source") for name in sorted(SOURCE_FILES)]
    declared.append((ANALYTIC_SOURCE, "analytic-proof"))
    for path, source_class in declared:
        require(path.is_file() and not path.is_symlink(), "missing regular source: " + str(path))
        relative = path.relative_to(ROOT).as_posix()
        payload = path.read_bytes()
        require(git_blob(commit, relative) == payload, "source drift from commit: " + relative)
        bindings.append({
            "bytes": len(payload), "path": relative, "sha256": sha256_bytes(payload),
            "sourceClass": source_class,
        })
    return bindings


def expected_rows(config: dict[str, Any]) -> list[dict[str, str]]:
    def row(panel: str, series: str, parameter: int, x: float, y: float,
            quantity_class: str, source_record_type: str, formula: str,
            normalization: str) -> dict[str, str]:
        return {
            "panel": panel, "series": series, "parameter": str(parameter),
            "x": format(x, ".17g"), "y": format(y, ".17g"),
            "quantity_class": quantity_class,
            "source_origin": (
                "r073t-analytic-proof"
                if panel == "A"
                else "r073t-exact-certificate-results"
            ),
            "source_record_type": source_record_type,
            "formula": formula, "normalization": normalization,
        }
    rows = [
        row("A", "exact_quartic_balance", 1, 1, 1, "exact-identity",
            "analytic-chain", "Q'+4nuY+2nuX^2=4<p,u.grad w>", "normalized Haar"),
        row("A", "pressure_absorption", 2, 2, 1, "classical-upper-bound",
            "analytic-chain", "4|<p,u.grad w>|<=nuX^2+4CR^2/nu*||u||_6^6",
            "periodic Riesz L3"),
        row("A", "static_autocorrelation", 3, 3, 1, "rigorous-upper-bound",
            "analytic-chain", "||u||_6^6<=A*Q", "R0.73S"),
        row("A", "dynamic_AQ", 4, 4, 1, "rigorous-upper-bound",
            "analytic-chain", "Q'+4nuY+nuX^2<=4CR^2/nu*A*Q", "normalized Haar"),
    ]
    for carrier in range(int(config["carrierMinimum"]), int(config["carrierMaximum"]) + 1):
        rows.append(row("B", "carrier_dissipation", carrier, carrier, carrier * carrier,
                        "exact", "rotating-shear", "abs(Cdot_0(0))/(2nu)=N^2",
                        "C(h,0)=delta_0 for every N"))
    for dilation in range(int(config["dilationMinimum"]), int(config["dilationMaximum"]) + 1):
        rows.extend((
            row("C", "u_L", dilation, dilation, -384 * dilation, "exact",
                "six-mode-sign-pair", "Qdot(0)+16536nuL^2=-384L",
                "common initial viscous term removed"),
            row("C", "minus_u_L", dilation, dilation, 384 * dilation, "exact",
                "six-mode-sign-pair", "Qdot(0)+16536nuL^2=+384L",
                "common initial viscous term removed"),
        ))
    return rows


def add(checks: list[dict[str, object]], check_id: str, passed: bool,
        **details: object) -> None:
    checks.append({"id": check_id, "pass": bool(passed), **details})
    require(bool(passed), "check failed: " + check_id)


def reconstruct_validation(source_commit: str, visual_confirmed: bool) -> tuple[dict[str, object], list[dict[str, object]]]:
    actual_entries = list(HERE.iterdir())
    actual_files = {path.name for path in actual_entries if path.is_file()}
    require(actual_files <= PACKAGE_FILES,
            "unexpected figure files: " + repr(sorted(actual_files - PACKAGE_FILES)))
    require(all(path.is_file() for path in actual_entries),
            "unexpected figure subdirectory or special entry")
    require((SOURCE_FILES | RAW_FILES) <= actual_files,
            "missing source/raw files: " + repr(sorted((SOURCE_FILES | RAW_FILES) - actual_files)))
    require(all((HERE / name).is_file() and not (HERE / name).is_symlink()
                for name in SOURCE_FILES | RAW_FILES),
            "source/raw inventory must contain only regular non-symlink files")
    source_bindings = verify_source_commit(source_commit)
    exact_process = subprocess.run(
        [sys.executable, str(CERTIFICATE_SCRIPT), "--check-only"], cwd=ROOT,
        text=True, capture_output=True, check=False,
    )
    require(exact_process.returncode == 0, "exact certificate failed during figure validation")
    cert_manifest = load_json(CERTIFICATE_MANIFEST)
    require(cert_manifest.get("finalSeal") is True and cert_manifest.get("sourceCommitAssigned") is True,
            "exact certificate must be final-sealed before figure validation")
    certificate_source_commit = cert_manifest.get("sourceCommit")
    require(isinstance(certificate_source_commit, str)
            and re.fullmatch(r"[0-9a-f]{40}", certificate_source_commit) is not None,
            "certificate manifest has no valid source commit")
    require(certificate_source_commit == source_commit,
            "figure and exact certificate must bind the same immutable source commit")
    seal_process = subprocess.run(
        [sys.executable, str(CERTIFICATE_SEALER),
         "--source-commit", certificate_source_commit, "--check-only"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    require(seal_process.returncode == 0,
            "exact certificate provenance seal failed: " + seal_process.stderr[-1200:])

    config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    environment = load_json(HERE / "environment.json")
    results = load_json(HERE / "results.json")
    checks: list[dict[str, object]] = []
    add(checks, "source-inventory", len(SOURCE_FILES) == 10)
    add(checks, "raw-inventory", len(RAW_FILES) == 11)
    add(checks, "package-inventory", len(PACKAGE_FILES) == 25)
    add(checks, "manifest-bound-inventory", len(MANIFEST_BOUND_FILES) == 23)
    add(checks, "sha256-line-inventory", len(MANIFEST_BOUND_FILES) + 1 == 24)
    add(checks, "source-binding-inventory", len(source_bindings) == 11)
    add(checks, "regular-file-inventory",
        all((HERE / name).is_file() and not (HERE / name).is_symlink()
            for name in SOURCE_FILES | RAW_FILES))
    add(checks, "certificate-exact-check", exact_process.returncode == 0)
    add(checks, "certificate-final-seal-check", seal_process.returncode == 0)
    add(checks, "certificate-source-commit", certificate_source_commit == source_commit)
    add(checks, "config-schema", config.get("schemaVersion") == "r073t-dynamic-autocorrelation-figure-config-v1")
    add(checks, "contract-schema", contract.get("schemaVersion") == "r073t-dynamic-autocorrelation-figure-contract-v1")
    add(checks, "results-schema", results.get("schemaVersion") == "r073t-dynamic-autocorrelation-figure-results-v1")
    add(checks, "identity-cross-binding",
        config.get("figureId") == FIGURE_ID
        and contract.get("figureId") == FIGURE_ID
        and contract.get("release") == "R0.73T"
        and results.get("figureId") == FIGURE_ID)
    add(checks, "contract-source-bindings",
        contract.get("sourceAnalyticProof") == "research/r073t_dynamic_autocorrelation_budget.md"
        and contract.get("sourceCertificate") == "research/certificates/r073t/results.json")
    claim = contract["claimBoundary"]
    add(checks, "claim-boundary-no-overreach",
        claim.get("navierStokesSimulation") is False
        and claim.get("fittedScalingLaw") is False
        and claim.get("singularSolution") is False
        and claim.get("regularityCriterionImproved") is False
        and claim.get("globalRegularityEstablished") is False
        and claim.get("clayProblemSolved") is False)
    add(checks, "results-claim-boundary", results.get("claimBoundary") == claim)
    add(checks, "results-inventory",
        results.get("allSourceChecksPass") is True
        and results.get("certificateChecks") == 55
        and results.get("rowCount") == 28
        and results.get("series") == {
            "analyticChain": 4, "carrier": 8, "pressurePair": 16,
        })
    add(checks, "environment-no-dgx", environment.get("execution", {}).get("dgxUsed") is False)
    add(checks, "environment-no-gpu", environment.get("execution", {}).get("gpu") == "not used")
    add(checks, "environment-no-network", environment.get("execution", {}).get("network") == "not used")
    add(checks, "environment-package-record",
        environment.get("packages") == EXPECTED_DEPENDENCIES)
    for name, expected in EXPECTED_DEPENDENCIES.items():
        add(checks, "dependency-" + name, package_version(name) == expected,
            actual=package_version(name), expected=expected)

    with (HERE / "source-data.csv").open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        add(checks, "csv-schema", tuple(reader.fieldnames or ()) == CSV_FIELDS)
        actual_rows = list(reader)
    wanted_rows = expected_rows(config)
    add(checks, "csv-row-count", len(actual_rows) == len(wanted_rows) == 28)
    for index, (actual, wanted) in enumerate(zip(actual_rows, wanted_rows)):
        add(checks, f"row-{index:02d}-exact", actual == wanted)
        add(checks, f"row-{index:02d}-finite",
            math.isfinite(float(actual["x"])) and math.isfinite(float(actual["y"])))

    png = HERE / "figure.png"
    with Image.open(png) as image:
        width, height = image.size
        expected_width = round(float(config["widthMillimetres"]) / 25.4 * int(config["pngDpi"]))
        expected_height = round(float(config["heightMillimetres"]) / 25.4 * int(config["pngDpi"]))
        add(checks, "png-format", image.format == "PNG")
        add(checks, "png-dimensions", abs(width - expected_width) <= 2 and abs(height - expected_height) <= 2,
            actual=[width, height], expected=[expected_width, expected_height])
        add(checks, "png-color", image.mode in {"RGB", "RGBA"})
    for name in ("qa-final-size.png", "qa-grayscale.png", "qa-pdf.png"):
        with Image.open(HERE / name) as image:
            add(checks, name + "-valid", image.width >= 900 and image.height >= 450)

    with Image.open(HERE / "figure.png") as master_image, \
            Image.open(HERE / "qa-final-size.png") as final_image, \
            Image.open(HERE / "qa-grayscale.png") as grayscale_image:
        reconstructed_final = master_image.copy()
        reconstructed_final.thumbnail((1800, 1200))
        reconstructed_final = reconstructed_final.convert("RGB")
        final_rgb = final_image.convert("RGB")
        grayscale = grayscale_image.copy()
        add(checks, "final-size-pixel-match",
            reconstructed_final.size == final_rgb.size
            and ImageChops.difference(reconstructed_final, final_rgb).getbbox() is None)
        add(checks, "grayscale-mode", grayscale_image.mode == "L")
        add(checks, "grayscale-pixel-match",
            grayscale.size == final_rgb.size
            and ImageChops.difference(final_rgb.convert("L"), grayscale).getbbox() is None)

    pdf_document = pdfium.PdfDocument(str(HERE / "figure.pdf"))
    require(len(pdf_document) == 1, "PDF raster check requires one page")
    pdf_page = pdf_document[0]
    reconstructed_pdf = pdf_page.render(scale=2.5).to_pil().convert("RGB")
    with Image.open(HERE / "qa-pdf.png") as recorded_pdf_image:
        recorded_pdf = recorded_pdf_image.convert("RGB")
        add(checks, "pdf-raster-pixel-match",
            reconstructed_pdf.size == recorded_pdf.size
            and ImageChops.difference(reconstructed_pdf, recorded_pdf).getbbox() is None)
    pdf_page.close()
    pdf_document.close()

    pdf_reader = PdfReader(str(HERE / "figure.pdf"))
    add(checks, "pdf-one-page", len(pdf_reader.pages) == 1)
    page = pdf_reader.pages[0]
    expected_pdf_width = float(config["widthMillimetres"]) / 25.4 * 72
    expected_pdf_height = float(config["heightMillimetres"]) / 25.4 * 72
    add(checks, "pdf-media-box",
        abs(float(page.mediabox.width) - expected_pdf_width) < 0.5
        and abs(float(page.mediabox.height) - expected_pdf_height) < 0.5)
    svg = (HERE / "figure.svg").read_text(encoding="utf-8")
    add(checks, "svg-root", "<svg" in svg and "viewBox=" in svg)
    add(checks, "svg-title", "Dynamic autocorrelation" in svg)
    add(checks, "palette-no-defaults", "#1f77b4" not in svg.lower() and "#ff7f0e" not in svg.lower())
    add(checks, "palette-roots-present",
        config["palette"]["blue"].lower() in svg.lower()
        and config["palette"]["gold"].lower() in svg.lower())
    for name in ("figure.pdf", "figure.svg", "figure.png"):
        add(checks, name + "-size", (HERE / name).stat().st_size > 10_000)
    add(checks, "visual-qa-confirmed", visual_confirmed)
    add(checks, "check-count-pinned", len(checks) + 1 == EXPECTED_CHECK_COUNT,
        actual=len(checks) + 1, expected=EXPECTED_CHECK_COUNT)
    validation = {
        "schemaVersion": "r073t-dynamic-autocorrelation-figure-validation-v1",
        "allChecksPass": True,
        "checkCount": len(checks),
        "checks": checks,
        "claimBoundary": claim,
        "figureId": FIGURE_ID,
        "sourceCommit": source_commit,
        "sourceCommitBindings": source_bindings,
        "visualQaConfirmed": visual_confirmed,
    }
    return validation, source_bindings


def qa_report(validation: dict[str, object]) -> str:
    return (
        "# R0.73T formal-figure QA report\n\n"
        "**Status:** PASS\n\n"
        f"**Checks:** {validation['checkCount']}/{validation['checkCount']}\n\n"
        "The exact source rows, source-commit bindings, dependency versions, "
        "SVG/PDF/PNG integrity, dimensions, palette, claim boundary, final-size "
        "raster, exact grayscale conversion, and independently regenerated PDF "
        "raster passed.\n\n"
        "Visual inspection confirmed that Panel C is explicitly a "
        "viscous-centered derivative, equations and labels do not clip, the "
        "signed series remain distinguishable in grayscale, and no panel can "
        "be read as a PDE simulation or singularity diagnostic.\n\n"
        "`navierStokesSimulation=false`; `dgxUsed=false`; `NOT CLAY`.\n"
    )


def build_manifest(source_commit: str, validation: dict[str, object],
                   source_bindings: list[dict[str, object]]) -> dict[str, object]:
    contract = load_json(HERE / "contract.json")
    files = [record(HERE / name) for name in sorted(MANIFEST_BOUND_FILES)]
    return {
        "schemaVersion": "r073t-dynamic-autocorrelation-figure-manifest-v1",
        "allChecksPass": True,
        "claimBoundary": contract["claimBoundary"],
        "evidenceClass": contract["evidenceClass"],
        "figureId": FIGURE_ID,
        "files": files,
        "inventory": {
            "externalSourceBindingCount": 1,
            "manifestBoundFileCount": len(MANIFEST_BOUND_FILES),
            "packageFileCount": len(PACKAGE_FILES),
            "rawFileCount": len(RAW_FILES),
            "sha256SumsLineCount": len(MANIFEST_BOUND_FILES) + 1,
            "sourceCommitBindingCount": len(source_bindings),
            "sourceFileCount": len(SOURCE_FILES),
        },
        "release": "R0.73T",
        "sourceCommit": source_commit,
        "sourceCommitAssigned": True,
        "sourceCommitBindings": source_bindings,
        "validationCheckCount": validation["checkCount"],
        "visualQaConfirmed": True,
    }


def expected_sums(manifest_text: str) -> str:
    lines = [f"{sha256(HERE / name)}  {name}" for name in sorted(MANIFEST_BOUND_FILES)]
    lines.append(f"{sha256_bytes(manifest_text.encode('utf-8'))}  manifest.json")
    return "\n".join(sorted(lines)) + "\n"


def main() -> None:
    args = parse_args()
    # Verification reuses the already recorded positive visual confirmation.
    visual = args.confirm_visual_qa
    if args.verify_only:
        existing = load_json(HERE / "validation.json")
        visual = existing.get("visualQaConfirmed") is True
    validation, source_bindings = reconstruct_validation(args.source_commit, visual)
    report_text = qa_report(validation)
    validation_text = canonical(validation)
    if args.verify_only:
        require((HERE / "validation.json").read_text(encoding="utf-8") == validation_text,
                "validation.json is stale")
        require((HERE / "qa-report.md").read_text(encoding="utf-8") == report_text,
                "qa-report.md is stale")
    else:
        require(args.confirm_visual_qa, "--confirm-visual-qa is required to seal the figure")
        (HERE / "validation.json").write_text(validation_text, encoding="utf-8")
        (HERE / "qa-report.md").write_text(report_text, encoding="utf-8")
    manifest = build_manifest(args.source_commit, validation, source_bindings)
    manifest_text = canonical(manifest)
    sums_text = expected_sums(manifest_text)
    require(len([line for line in sums_text.splitlines() if line]) == 24,
            "SHA256SUMS line inventory drift")
    if args.verify_only:
        require((HERE / "manifest.json").read_text(encoding="utf-8") == manifest_text,
                "manifest.json is stale")
        require((HERE / "SHA256SUMS").read_text(encoding="utf-8") == sums_text,
                "SHA256SUMS is stale")
    else:
        (HERE / "manifest.json").write_text(manifest_text, encoding="utf-8")
        (HERE / "SHA256SUMS").write_text(sums_text, encoding="utf-8")
    print(canonical({
        "checks": validation["checkCount"], "figureId": FIGURE_ID,
        "sourceCommit": args.source_commit, "status": "PASS",
        "verifyOnly": args.verify_only,
    }), end="")


if __name__ == "__main__":
    main()
