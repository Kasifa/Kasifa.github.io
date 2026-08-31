#!/usr/bin/env python3
"""Fail-closed validation and provenance seal for the R0.73U figure."""

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
from PIL import Image, ImageChops  # type: ignore  # noqa: E402
from pypdf import PdfReader  # type: ignore  # noqa: E402
import pypdfium2 as pdfium  # type: ignore  # noqa: E402

from plot import CSV_FIELDS, generate_rows  # type: ignore  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
FIGURE_ID = "fig-r073u-tensor-heat-hierarchy"
AUTHORITATIVE_SOURCE_COMMIT = "84e808dae473f6381cbf9df55a71f5fe81a1cfce"
SUPERSEDED_SOURCE_COMMIT = "72493751370aa948947000df169e21199fc5c95d"
ANALYTIC_SOURCE_FILES = {
    "research/r073u_problem_freeze.md",
    "research/r073u_tensor_heat_hierarchy.md",
    "research/r073u_independent_analytic_audit.md",
}
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
    "matplotlib": "3.10.6", "numpy": "2.5.2", "pillow": "12.3.0",
    "pypdf": "6.10.0", "pypdfium2": "5.13.0",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--source-commit", default="")
    parser.add_argument("--confirm-visual-qa", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


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
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys)
    require(isinstance(value, dict), "JSON root is not an object: " + str(path))
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(path: Path) -> dict[str, object]:
    return {"bytes": path.stat().st_size, "path": path.name, "sha256": sha256(path)}


def add(checks: list[dict[str, object]], check_id: str, passed: bool,
        **details: object) -> None:
    checks.append({"id": check_id, "pass": bool(passed), **details})
    require(bool(passed), "check failed: " + check_id)


def git_blob(commit: str, relative: str) -> bytes:
    completed = subprocess.run(
        ["git", "cat-file", "blob", f"{commit}:{relative}"], cwd=ROOT,
        capture_output=True, check=False,
    )
    require(completed.returncode == 0, "source absent from commit: " + relative)
    return completed.stdout


def source_bindings(commit: str) -> list[dict[str, object]]:
    if not commit:
        return []
    require(re.fullmatch(r"[0-9a-f]{40}", commit) is not None,
            "source commit must be full lowercase 40-hex")
    require(commit != SUPERSEDED_SOURCE_COMMIT, "superseded analytic source commit rejected")
    require(commit == AUTHORITATIVE_SOURCE_COMMIT,
            "source commit is not the authoritative R0.73U analytic commit")
    completed = subprocess.run(["git", "cat-file", "-e", commit + "^{commit}"],
                               cwd=ROOT, capture_output=True, check=False)
    require(completed.returncode == 0, "source commit does not resolve")
    bindings = []
    for relative in sorted(ANALYTIC_SOURCE_FILES):
        path = ROOT / relative
        payload = path.read_bytes()
        require(git_blob(commit, relative) == payload, "source drift from commit: " + relative)
        bindings.append({
            "bytes": len(payload), "path": relative, "sha256": sha256(path),
            "sourceClass": "frozen-analytic-source",
        })
    return bindings


def reconstruct_checks(source_commit: str, visual_confirmed: bool) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    actual_entries = list(HERE.iterdir())
    actual_files = {path.name for path in actual_entries if path.is_file()}
    require(actual_files <= PACKAGE_FILES,
            "unexpected figure files: " + repr(sorted(actual_files - PACKAGE_FILES)))
    require(all(path.is_file() for path in actual_entries),
            "unexpected figure subdirectory or special entry")
    require((SOURCE_FILES | RAW_FILES) <= actual_files,
            "missing source/raw files: " + repr(sorted((SOURCE_FILES | RAW_FILES) - actual_files)))
    bindings = source_bindings(source_commit)
    config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    environment = load_json(HERE / "environment.json")
    results = load_json(HERE / "results.json")
    checks: list[dict[str, object]] = []

    add(checks, "source-inventory", len(SOURCE_FILES) == 10)
    add(checks, "raw-inventory", len(RAW_FILES) == 11)
    add(checks, "package-inventory", len(PACKAGE_FILES) == 25)
    add(checks, "manifest-bound-inventory", len(MANIFEST_BOUND_FILES) == 23)
    add(checks, "regular-file-inventory", all(
        (HERE / name).is_file() and not (HERE / name).is_symlink()
        for name in SOURCE_FILES | RAW_FILES
    ))
    add(checks, "config-schema",
        config.get("schemaVersion") == "r073u-tensor-heat-hierarchy-figure-config-v1")
    add(checks, "contract-schema",
        contract.get("schemaVersion") == "r073u-tensor-heat-hierarchy-figure-contract-v1")
    add(checks, "results-schema",
        results.get("schemaVersion") == "r073u-tensor-heat-hierarchy-figure-results-v1")
    add(checks, "identity-cross-binding",
        config.get("figureId") == FIGURE_ID
        and contract.get("figureId") == FIGURE_ID
        and contract.get("release") == "R0.73U"
        and results.get("figureId") == FIGURE_ID)
    add(checks, "authoritative-source-commit-contract",
        contract.get("authoritativeAnalyticSourceCommit") == AUTHORITATIVE_SOURCE_COMMIT
        and contract.get("supersededAnalyticSourceCommitRejected") == SUPERSEDED_SOURCE_COMMIT)
    claim = contract["claimBoundary"]
    add(checks, "claim-boundary-no-overreach",
        claim.get("exactFormulaAndFiniteDiagnosticOnly") is True
        and claim.get("navierStokesSimulation") is False
        and claim.get("fittedScalingLaw") is False
        and claim.get("closureModel") is False
        and claim.get("singularSolution") is False
        and claim.get("regularityCriterionImproved") is False
        and claim.get("globalRegularityEstablished") is False
        and claim.get("clayProblemSolved") is False)
    add(checks, "results-claim-boundary", results.get("claimBoundary") == claim)
    compute = contract["compute"]
    execution = environment["execution"]
    add(checks, "contract-no-dgx", compute.get("dgxUsed") is False)
    add(checks, "environment-no-dgx", execution.get("dgxUsed") is False)
    add(checks, "environment-no-gpu", execution.get("gpu") == "not used")
    add(checks, "environment-no-network", execution.get("network") == "not used")
    add(checks, "translation-path-contract",
        compute.get("ordinaryTranslationPath") == "LOCAL_DIRECT_NO_DGX")
    add(checks, "translation-path-environment",
        execution.get("ordinaryTranslationPath") == "LOCAL_DIRECT_NO_DGX")
    add(checks, "result-inventory",
        results.get("rowCount") == 138
        and results.get("series") == {
            "analyticCurveSamples": 111,
            "analyticSchematic": 4,
            "exactFiniteDiagnostic": 22,
            "exactPeak": 1,
        })
    constants = results["exactConstants"]
    a = constants["cubicMatrixA"]
    b = constants["pressureVelocityMatrixB"]
    k = constants["totalMatrix"]
    add(checks, "matrix-A", a == [[-2, 3], [3, -4]])
    add(checks, "matrix-B", b == [[0, -2], [-2, 4]])
    add(checks, "matrix-addition",
        [[a[i][j] + b[i][j] for j in range(2)] for i in range(2)] == k == [[-2, 1], [1, 0]])
    add(checks, "matrix-frobenius", sum(value * value for row in k for value in row) == 6)
    add(checks, "heat-exponent", constants.get("heatExponentAtWitness") == 5)

    add(checks, "environment-package-record", environment.get("packages") == EXPECTED_DEPENDENCIES)
    for name, expected in EXPECTED_DEPENDENCIES.items():
        add(checks, "dependency-" + name, package_version(name) == expected,
            actual=package_version(name), expected=expected)

    with (HERE / "source-data.csv").open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        add(checks, "csv-schema", tuple(reader.fieldnames or ()) == CSV_FIELDS)
        actual_rows = list(reader)
    wanted_rows = generate_rows(config)
    add(checks, "csv-row-count", len(actual_rows) == len(wanted_rows) == 138)
    for index, (actual, wanted) in enumerate(zip(actual_rows, wanted_rows)):
        add(checks, f"row-{index:03d}-exact", actual == wanted)
        if actual["x"] or actual["y"]:
            add(checks, f"row-{index:03d}-finite",
                (not actual["x"] or math.isfinite(float(actual["x"])))
                and (not actual["y"] or math.isfinite(float(actual["y"]))))
    peak = next(row for row in actual_rows if row["series"] == "exact_peak")
    peak_x = float(peak["x"])
    peak_y = float(peak["y"])
    add(checks, "peak-x", math.isclose(peak_x, 1 / math.sqrt(10), rel_tol=0, abs_tol=1e-15))
    add(checks, "peak-y", math.isclose(peak_y, math.exp(-0.5) / math.sqrt(10), rel_tol=0, abs_tol=1e-15))
    add(checks, "peak-stationary", math.isclose(1 - 10 * peak_x * peak_x, 0, abs_tol=1e-14))
    peak_second = math.exp(-5 * peak_x * peak_x) * (100 * peak_x**3 - 30 * peak_x)
    add(checks, "peak-second-derivative-negative", peak_second < 0,
        secondDerivative=peak_second)

    with Image.open(HERE / "figure.png") as image:
        width, height = image.size
        expected_width = round(float(config["widthMillimetres"]) / 25.4 * int(config["pngDpi"]))
        expected_height = round(float(config["heightMillimetres"]) / 25.4 * int(config["pngDpi"]))
        add(checks, "png-format", image.format == "PNG")
        add(checks, "png-dimensions", abs(width - expected_width) <= 2 and abs(height - expected_height) <= 2,
            actual=[width, height], expected=[expected_width, expected_height])
        expected_final = image.copy()
        expected_final.thumbnail((int(config["qaMaximumWidthPixels"]), 1200))
        expected_final = expected_final.convert("RGB")
        with Image.open(HERE / "qa-final-size.png") as stored_final:
            add(checks, "qa-final-size-exact",
                ImageChops.difference(expected_final, stored_final.convert("RGB")).getbbox() is None)
        expected_grey = expected_final.convert("L")
        with Image.open(HERE / "qa-grayscale.png") as stored_grey:
            add(checks, "qa-grayscale-exact",
                ImageChops.difference(expected_grey, stored_grey.convert("L")).getbbox() is None)

    reader = PdfReader(str(HERE / "figure.pdf"))
    add(checks, "pdf-one-page", len(reader.pages) == 1)
    box = reader.pages[0].mediabox
    expected_w_pt = float(config["widthMillimetres"]) / 25.4 * 72.0
    expected_h_pt = float(config["heightMillimetres"]) / 25.4 * 72.0
    add(checks, "pdf-media-box",
        abs(float(box.width) - expected_w_pt) < 0.05 and abs(float(box.height) - expected_h_pt) < 0.05,
        actual=[float(box.width), float(box.height)], expected=[expected_w_pt, expected_h_pt])
    document = pdfium.PdfDocument(str(HERE / "figure.pdf"))
    page = document[0]
    regenerated_pdf = page.render(scale=2.5).to_pil().convert("RGB")
    with Image.open(HERE / "qa-pdf.png") as stored_pdf:
        add(checks, "qa-pdf-raster-exact",
            ImageChops.difference(regenerated_pdf, stored_pdf.convert("RGB")).getbbox() is None)
    page.close()
    document.close()

    svg_text = (HERE / "figure.svg").read_text(encoding="utf-8")
    view_box = re.search(r'viewBox="([^"]+)"', svg_text)
    add(checks, "svg-viewbox-present", view_box is not None)
    if view_box is not None:
        values = [float(value) for value in view_box.group(1).split()]
        add(checks, "svg-viewbox-dimensions", len(values) == 4
            and abs(values[2] - expected_w_pt) < 0.05
            and abs(values[3] - expected_h_pt) < 0.05)
    remote_drawable = re.search(
        r'<(?:image|use)[^>]+(?:href|xlink:href)="https?://', svg_text,
        flags=re.IGNORECASE,
    )
    add(checks, "svg-no-remote-drawable", remote_drawable is None)
    declared_colors = {value.lower() for value in config["palette"].values()}
    svg_colors = {value.lower() for value in re.findall(r"#[0-9a-fA-F]{6}", svg_text)}
    permitted = declared_colors | {"#ffffff", "#000000"}
    add(checks, "svg-palette", svg_colors <= permitted,
        undeclared=sorted(svg_colors - permitted))
    add(checks, "visual-qa-confirmed", visual_confirmed)
    add(checks, "source-commit-format-or-preseal",
        not source_commit or source_commit == AUTHORITATIVE_SOURCE_COMMIT)
    add(checks, "source-binding-count", len(bindings) in {0, 3})
    return checks, bindings


def write_outputs(source_commit: str, checks: list[dict[str, object]],
                  bindings: list[dict[str, object]]) -> None:
    passed = sum(1 for item in checks if item["pass"])
    require(passed == len(checks), "not all checks passed")
    final_seal = bool(source_commit)
    validation = {
        "schemaVersion": "r073u-tensor-heat-hierarchy-validation-v1",
        "figureId": FIGURE_ID,
        "generatedUtc": utc_now(),
        "status": "PASS",
        "checksPassed": passed,
        "checksRequired": len(checks),
        "checks": checks,
        "sourceCommit": source_commit or None,
        "sourceCommitAssigned": final_seal,
        "finalSeal": final_seal,
        "visualQaConfirmed": True,
    }
    (HERE / "validation.json").write_text(canonical(validation), encoding="utf-8")
    seal_label = "PUBLICATION SEAL" if final_seal else "LOCAL ARTIFACT PRESEAL"
    qa_report = f"""# R0.73U formal-figure QA report

**Status:** PASS - {seal_label}

**Checks:** {passed}/{len(checks)}

Exact source-row reconstruction, matrix arithmetic, analytic peak, dependency
versions, SVG/PDF/PNG integrity, dimensions, palette, claim boundary,
final-size raster, grayscale conversion, and independently regenerated PDF
raster passed.

Visual inspection confirmed that the schematic arrows and blocked map are
unambiguous, every matrix entry is legible, the analytic curve peak is
labelled without collision, and the parabolic $s^{{-1/2}}$ statement is
explicitly coefficient-level.  The figure cannot reasonably be read as a PDE
simulation or fitted scaling law.

`navierStokesSimulation=false`; `fittedScalingLaw=false`; `dgxUsed=false`;
`ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX`; `NOT CLAY`.
"""
    if not final_seal:
        qa_report += "\nThe immutable source-commit publication seal remains pending.\n"
    (HERE / "qa-report.md").write_text(qa_report, encoding="utf-8")
    bound = [record(HERE / name) for name in sorted(MANIFEST_BOUND_FILES)]
    manifest = {
        "schemaVersion": "r073u-tensor-heat-hierarchy-manifest-v1",
        "figureId": FIGURE_ID,
        "createdUtc": utc_now(),
        "claimBoundary": load_json(HERE / "contract.json")["claimBoundary"],
        "dgxUsed": False,
        "ordinaryTranslationPath": "LOCAL_DIRECT_NO_DGX",
        "sourceCommit": source_commit or None,
        "sourceCommitAssigned": final_seal,
        "finalSeal": final_seal,
        "sourceBindings": bindings,
        "files": bound,
        "validation": {
            "status": "PASS",
            "checksPassed": passed,
            "checksRequired": len(checks),
        },
    }
    (HERE / "manifest.json").write_text(canonical(manifest), encoding="utf-8")
    checksum_names = sorted(MANIFEST_BOUND_FILES | {"manifest.json"})
    lines = [f"{sha256(HERE / name)}  {name}" for name in checksum_names]
    (HERE / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")


def verify_seal(functional_checks: list[dict[str, object]]) -> None:
    validation = load_json(HERE / "validation.json")
    manifest = load_json(HERE / "manifest.json")
    require(validation.get("status") == "PASS", "stored validation is not PASS")
    require(validation.get("visualQaConfirmed") is True, "visual QA not stored as confirmed")
    require(validation.get("checksPassed") == validation.get("checksRequired"),
            "stored validation count mismatch")
    stored_ids = [item["id"] for item in validation.get("checks", [])]
    actual_ids = [item["id"] for item in functional_checks]
    require(stored_ids == actual_ids, "stored validation check inventory drift")
    require(all(item.get("pass") is True for item in validation.get("checks", [])),
            "stored validation contains a failure")
    expected_records = {item["path"]: item for item in manifest.get("files", [])}
    require(set(expected_records) == MANIFEST_BOUND_FILES, "manifest file inventory drift")
    for name, item in expected_records.items():
        path = HERE / name
        require(path.stat().st_size == item["bytes"], "manifest byte-count drift: " + name)
        require(sha256(path) == item["sha256"], "manifest hash drift: " + name)
    checksum_lines = (HERE / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    parsed = {}
    for line in checksum_lines:
        digest, name = line.split("  ", 1)
        require(name not in parsed, "duplicate checksum line: " + name)
        parsed[name] = digest
    expected_names = MANIFEST_BOUND_FILES | {"manifest.json"}
    require(set(parsed) == expected_names, "checksum inventory drift")
    for name in expected_names:
        require(parsed[name] == sha256(HERE / name), "checksum drift: " + name)
    stored_commit = validation.get("sourceCommit") or ""
    require(stored_commit == (manifest.get("sourceCommit") or ""), "seal commit mismatch")
    require(validation.get("finalSeal") == manifest.get("finalSeal"), "final-seal flag mismatch")


def main() -> None:
    args = parse_args()
    if args.verify_only:
        validation = load_json(HERE / "validation.json")
        stored_commit = validation.get("sourceCommit") or ""
        checks, _ = reconstruct_checks(stored_commit, True)
        verify_seal(checks)
        print(canonical({
            "figureId": FIGURE_ID,
            "finalSeal": bool(validation.get("finalSeal")),
            "status": "PASS",
            "verifyOnly": True,
        }), end="")
        return
    require(args.confirm_visual_qa, "--confirm-visual-qa is required to write the seal")
    checks, bindings = reconstruct_checks(args.source_commit, True)
    write_outputs(args.source_commit, checks, bindings)
    verify_seal(checks)
    print(canonical({
        "checks": len(checks),
        "figureId": FIGURE_ID,
        "finalSeal": bool(args.source_commit),
        "status": "PASS",
    }), end="")


if __name__ == "__main__":
    main()
