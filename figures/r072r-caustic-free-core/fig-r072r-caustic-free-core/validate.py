#!/usr/bin/env python3
"""Validate the R0.72R caustic-free-core formal figure package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
from typing import Any

from PIL import Image, ImageStat
from pypdf import PdfReader

from certificate_ledger import verify_flat_certificate_ledger


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
PACKAGE_SOURCES = (
    "README.md", "caption.md", "figure-contract.md", "contract.json",
    "config.json", "command.txt", "requirements.txt", "certificate_ledger.py",
    "plot.py", "qa_images.py", "publish_assets.py", "validate.py",
    "build_manifest.py",
)
FIELDS = [
    "panel", "route", "series", "kind", "x", "y", "phi", "theta",
    "radius", "distance", "source", "pointer", "status", "note",
]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def rows_from(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def gate(name: str, passed: bool, value: Any, requirement: str) -> dict[str, Any]:
    return {"name": name, "passed": bool(passed), "value": value, "requirement": requirement}


def pixels(config: dict[str, Any], dpi: int) -> tuple[int, int]:
    figure = config["figure"]
    return (
        round(float(figure["widthMillimetres"]) * dpi / 25.4),
        round(float(figure["heightMillimetres"]) * dpi / 25.4),
    )


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True).strip()


def tracked_clean() -> bool:
    return all(
        subprocess.run(command, cwd=REPOSITORY, check=False).returncode == 0
        for command in (("git", "diff", "--quiet", "--"), ("git", "diff", "--cached", "--quiet", "--"))
    )


def blob_matches(commit: str, relative: str) -> bool:
    path = (REPOSITORY / relative).resolve()
    if FULL_SHA.fullmatch(commit) is None or not path.is_file():
        return False
    try:
        committed = subprocess.check_output(
            ["git", "rev-parse", f"{commit}:{relative}"], cwd=REPOSITORY,
            text=True, stderr=subprocess.DEVNULL,
        ).strip()
        working = subprocess.check_output(
            ["git", "hash-object", f"--path={relative}", str(path)], cwd=REPOSITORY,
            text=True, stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.CalledProcessError:
        return False
    return committed == working


def asset_checks(config: dict[str, Any]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    required = [
        *PACKAGE_SOURCES, "figure.pdf", "figure.svg", "figure.png", "data.csv",
        "results.json", "environment.txt", "qa-final-size.png",
        "qa-grayscale.png", "qa-pdf.png", "progress.ndjson", "resource-log.ndjson",
    ]
    missing = [name for name in required if not (ROOT / name).is_file()]
    checks.append(gate("required_assets", not missing, missing, "all formal assets exist"))
    if missing:
        return checks

    png_dpi = int(config["figure"]["pngDpi"])
    with Image.open(ROOT / "figure.png") as image:
        png_size = image.size
        png_meta = image.info.get("dpi", (0.0, 0.0))
    expected_png = pixels(config, png_dpi)
    checks.append(gate(
        "png_final_size_600_dpi",
        all(abs(float(item) - png_dpi) < 0.02 for item in png_meta)
        and all(abs(a - b) <= 2 for a, b in zip(png_size, expected_png)),
        {"size": png_size, "expected": expected_png, "dpi": png_meta},
        "PNG is final size at 600 dpi",
    ))

    reader = PdfReader(str(ROOT / "figure.pdf"))
    page = reader.pages[0]
    pdf_mm = (
        float(page.mediabox.width) * 25.4 / 72.0,
        float(page.mediabox.height) * 25.4 / 72.0,
    )
    checks.append(gate(
        "pdf_one_page_final_size",
        len(reader.pages) == 1
        and abs(pdf_mm[0] - float(config["figure"]["widthMillimetres"])) < 0.08
        and abs(pdf_mm[1] - float(config["figure"]["heightMillimetres"])) < 0.08,
        {"pages": len(reader.pages), "millimetres": pdf_mm},
        "PDF is one page at declared final size",
    ))

    svg = (ROOT / "figure.svg").read_text(encoding="utf-8")
    checks.append(gate(
        "svg_editable_vector",
        "<svg" in svg and "<text" in svg
        and svg.count("<image") <= int(config["validation"]["maximumSvgRasterImages"]),
        {"text": "<text" in svg, "rasterImages": svg.count("<image")},
        "SVG retains editable text and no raster image",
    ))

    qa_expected = pixels(config, int(config["figure"]["qaDpi"]))
    qa_sizes: dict[str, tuple[int, int]] = {}
    for name in ("qa-final-size.png", "qa-grayscale.png", "qa-pdf.png"):
        with Image.open(ROOT / name) as image:
            qa_sizes[name] = image.size
    with Image.open(ROOT / "qa-grayscale.png") as image:
        gray_std = float(ImageStat.Stat(image.convert("L")).stddev[0])
    checks.append(gate(
        "final_size_and_grayscale_qa",
        all(size == qa_expected for size in qa_sizes.values())
        and gray_std > float(config["validation"]["minimumGrayscaleStandardDeviation"]),
        {"sizes": qa_sizes, "expected": qa_expected, "grayStd": gray_std},
        "QA surfaces match final size and grayscale contrast gate",
    ))
    return checks


def lineage_checks(config: dict[str, Any], results: dict[str, Any]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    bindings = config["formalGitBindings"]
    canonical = {
        "analyticSource": bindings["sourceCommitPaths"][0],
        **bindings["certificateCommitRoles"],
        "certificateLedger": bindings["certificateLedgerPath"],
    }
    records = results.get("runtimeLineage", {})
    expected_status = {
        "analyticSource": "source",
        "producerConfig": "formal-ready-config",
        "producerResult": "passed",
        "independentConfig": "formal-ready-config",
        "independentResult": "passed",
        "crosscheck": "passed-formal-source-only",
        "certificateLedger": "passed-flat-ledger",
    }
    record_audit: dict[str, Any] = {}
    for role, relative in canonical.items():
        record = records.get(role, {})
        path = Path(record.get("path", "/")).expanduser().resolve()
        expected = (REPOSITORY / relative).resolve()
        record_audit[role] = {
            "canonical": path == expected,
            "exists": path.is_file(),
            "hashMatches": path.is_file() and digest(path) == record.get("sha256"),
            "statusMatches": record.get("status") == expected_status[role],
        }
        record_audit[role]["passed"] = all(record_audit[role].values())
    checks.append(gate(
        "runtime_lineage",
        set(records) == set(canonical) and all(value["passed"] for value in record_audit.values()),
        record_audit,
        "all runtime inputs are canonical, hash-stable repository files",
    ))

    crosscheck = json.loads((REPOSITORY / bindings["certificateCommitRoles"]["crosscheck"]).read_text(encoding="utf-8"))
    cross = crosscheck.get("checks", {})
    source_commit = crosscheck.get("sourceCommit", "")
    build_commit = results.get("repositoryCommitAtBuild", "")
    source_blobs = FULL_SHA.fullmatch(source_commit) is not None and all(
        blob_matches(source_commit, relative) for relative in bindings["sourceCommitPaths"]
    )
    certificate_paths = [
        *bindings["certificateCommitRoles"].values(), bindings["certificateLedgerPath"],
    ]
    certificate_blobs = (
        FULL_SHA.fullmatch(build_commit) is not None
        and build_commit == git_head()
        and all(blob_matches(build_commit, relative) for relative in certificate_paths)
    )
    package_paths = {
        str((ROOT / name).resolve().relative_to(REPOSITORY.resolve()))
        for name in PACKAGE_SOURCES
    }
    package_blobs = results.get("packageSourceGitBlobs", {})
    commit_gate = (
        isinstance(cross, dict) and bool(cross) and all(value is True for value in cross.values())
        and crosscheck.get("status") == "passed"
        and crosscheck.get("temporaryUnsealedSourceAllowed") is False
        and results.get("formalSourceCommit") == source_commit
        and results.get("verifiedTrackedTreeClean") is True
        and results.get("verifiedPackageSourcesAtBuildCommit") is True
        and tracked_clean() and source_blobs and certificate_blobs
        and set(package_blobs) == package_paths
        and all(blob_matches(build_commit, relative) for relative in package_paths)
    )
    checks.append(gate(
        "source_certificate_and_build_commits", commit_gate,
        {"sourceCommit": source_commit, "buildCommit": build_commit,
         "sourceBlobs": source_blobs, "certificateBlobs": certificate_blobs,
         "trackedClean": tracked_clean()},
        "source and certificate/package blobs bind clean declared commits",
    ))

    ledger = verify_flat_certificate_ledger(
        REPOSITORY / Path(bindings["certificateLedgerPath"]).parent,
        required_files={Path(value).name for value in bindings["certificateCommitRoles"].values()},
    )
    recorded = results.get("certificateLedgerAudit", {})
    checks.append(gate(
        "flat_certificate_ledger",
        ledger.get("status") == "passed"
        and ledger.get("ledgerSha256") == recorded.get("ledgerSha256")
        and ledger.get("entryCount") == recorded.get("entryCount")
        and recorded.get("exactDirectoryCoverage") is True,
        {"current": ledger, "recorded": recorded},
        "flat SHA256SUMS exactly seals the certificate bundle",
    ))

    source_hashes = results.get("packageSourceHashes", {})
    changed = [name for name in PACKAGE_SOURCES if source_hashes.get(name) != digest(ROOT / name)]
    checks.append(gate(
        "package_source_hashes", set(source_hashes) == set(PACKAGE_SOURCES) and not changed,
        {"changed": changed}, "all package sources retain build hashes",
    ))
    return checks


def formula_checks(config: dict[str, Any], rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    tolerance = float(config["validation"]["maximumFormulaResidual"])
    parameters = config["parameters"]
    checks.append(gate(
        "data_schema_and_size",
        bool(rows) and list(rows[0]) == FIELDS
        and len(rows) >= int(config["validation"]["minimumDataRows"])
        and set(row["panel"] for row in rows) == {"A", "B", "C"},
        {"rows": len(rows), "panels": sorted(set(row["panel"] for row in rows))},
        "data table has the exact schema, minimum size, and three panels",
    ))

    residuals_a: list[float] = []
    for row in (item for item in rows if item["panel"] == "A"):
        a_value = float(row["x"])
        b_value = float(row["y"])
        series = row["series"]
        if series == "endpoint phi=0":
            residuals_a.append(abs(1.0 + 4.0 * a_value + 9.0 * b_value))
        elif series == "endpoint phi=pi":
            residuals_a.append(abs(1.0 - 4.0 * a_value + 9.0 * b_value))
        elif series == "internal arc":
            x_value = float(row["phi"])
            residuals_a.extend([
                abs(12.0 * b_value * x_value**2 + 4.0 * a_value * x_value + 1.0 - 3.0 * b_value),
                abs(24.0 * b_value * x_value + 4.0 * a_value),
            ])
        elif series.startswith("cone edge"):
            residuals_a.append(abs(4.0 * abs(a_value) + 9.0 * abs(b_value) - 0.5))
        elif series.startswith("K edge"):
            center_z2 = float(parameters["centerZ2"])
            radius_z2 = float(parameters["radiusZ2"])
            radius_z3 = float(parameters["radiusZ3"])
            z2_lower = center_z2 - radius_z2
            z2_upper = center_z2 + radius_z2
            inside = (
                z2_lower - tolerance <= a_value <= z2_upper + tolerance
                and -radius_z3 - tolerance <= b_value <= radius_z3 + tolerance
            )
            boundary = min(
                abs(a_value - z2_lower), abs(a_value - z2_upper),
                abs(b_value + radius_z3), abs(b_value - radius_z3),
            )
            residuals_a.append(0.0 if inside and boundary <= tolerance else math.inf)
        else:
            residuals_a.append(math.inf)
    checks.append(gate(
        "panel_a_exact_real_slice", max(residuals_a, default=math.inf) <= tolerance,
        {"maxResidual": max(residuals_a, default=None)},
        "endpoint walls, internal arc, cone diamond, and K trace match exact formulas",
    ))

    center_z2 = float(parameters["centerZ2"])
    radius_z2 = float(parameters["radiusZ2"])
    radius_z3 = float(parameters["radiusZ3"])
    z2_lower = center_z2 - radius_z2
    z2_upper = center_z2 + radius_z2
    old_q2_boundary = float(parameters["oldQ2Boundary"])
    residuals_b: list[float] = []
    for row in (item for item in rows if item["panel"] == "B"):
        y_value = float(row["x"])
        series = row["series"]
        expected = {
            "lower heat envelope": 4.0 * z2_lower * math.exp(-3.0 * y_value),
            "center heat path": 4.0 * center_z2 * math.exp(-3.0 * y_value),
            "upper heat envelope": (
                4.0 * z2_upper * math.exp(-3.0 * y_value)
                + 9.0 * radius_z3 * math.exp(-8.0 * y_value)
            ),
            "old Q2 boundary": old_q2_boundary,
        }.get(series, math.inf)
        residuals_b.append(abs(float(row["y"]) - expected))
    checks.append(gate(
        "panel_b_exact_heat_paths", max(residuals_b, default=math.inf) <= tolerance,
        {"maxResidual": max(residuals_b, default=None)},
        "heat paths match the three exact envelopes and old boundary",
    ))

    residuals_c: list[float] = []
    radius = float(parameters["criticalLocalization"])
    normalized_local_lower = float(parameters["normalizedLocalSlopeLower"])
    normalized_local_upper = float(parameters["normalizedLocalSlopeUpper"])
    normalized_away_gap = float(parameters["normalizedAwayGap"])
    physical_local_lower = 1.0 / math.sqrt(float(parameters["shapeC0"]))
    physical_away_gap = 1.0 / float(parameters["shapeC1"])
    for row in (item for item in rows if item["panel"] == "C"):
        distance = float(row["x"])
        series = row["series"]
        expected = {
            "normalized certified lower": (
                normalized_local_lower * distance
                if distance <= radius else normalized_away_gap
            ),
            "physical W (0<=y<=1): certified lower": (
                physical_local_lower * distance
                if distance <= radius else physical_away_gap
            ),
            "local upper envelope": normalized_local_upper * min(distance, radius),
        }.get(series, math.inf)
        residuals_c.append(abs(float(row["y"]) - expected))
    checks.append(gate(
        "panel_c_exact_shape_envelopes", max(residuals_c, default=math.inf) <= tolerance,
        {"maxResidual": max(residuals_c, default=None)},
        "normalized and physical two-regime envelopes match the declared 0<=y<=1 contract",
    ))
    return checks


def parameter_contract_checks(
    config: dict[str, Any], contract: dict[str, Any]
) -> list[dict[str, Any]]:
    p = config["parameters"]
    expected = {
        "centerZ2": 3.0 / 20.0,
        "radiusZ2": 1.0 / 100.0,
        "radiusZ3": 1.0 / 1000.0,
        "q2InitialLower": 14.0 / 25.0,
        "q2Y1Upper": 20489.0 / 256000.0,
        "oldQ2Boundary": 1.0 / 2.0,
        "criticalLocalization": math.pi / 48.0,
        "normalizedCurvatureLower": 1517.0 / 4500.0,
        "normalizedLocalSlopeLower": 1.0 / 4.0,
        "normalizedLocalSlopeUpper": 5.0 / 3.0,
        "normalizedAwayGap": 1.0 / 80.0,
        "shapeC0": 144.0,
        "shapeC1": 240.0,
        "slowEta": 81.0 / 2401.0,
        "derivativeSum": 161.0 / 25.0,
    }
    parameter_audit = {
        name: math.isclose(
            float(p.get(name, math.nan)), value, rel_tol=0.0, abs_tol=2.0e-15
        )
        for name, value in expected.items()
    }
    contract_text = " ".join(
        [contract.get("supportedTakeaway", ""), *contract.get("analyticClaims", [])]
    )
    contract_audit = {
        "r072rSchema": contract.get("schemaVersion") == "r072r-figure-contract-v1",
        "closedInternalArc": "-1<=x<=1" in contract_text,
        "r072rShapeContract": "(r,C0,C1)=(pi/48,144,240)" in contract_text,
        "oldConeBoundary": "Q2=1/2" in contract_text,
    }
    return [gate(
        "r072r_parameter_and_contract_consistency",
        all(parameter_audit.values()) and all(contract_audit.values()),
        {"parameters": parameter_audit, "contract": contract_audit},
        "config and contract encode the certified R0.72R core, heat path, and shape constants",
    )]


def publication_checks(config: dict[str, Any]) -> list[dict[str, Any]]:
    publication = config["publication"]
    audit: dict[str, Any] = {}
    for suffix in ("pdf", "svg", "png"):
        master = ROOT / f"figure.{suffix}"
        public = REPOSITORY / publication["directory"] / f"{publication['stem']}.{suffix}"
        audit[suffix] = {
            "exists": public.is_file(),
            "byteIdentical": public.is_file() and digest(public) == digest(master),
        }
    return [gate(
        "public_assets_byte_identical", all(all(value.values()) for value in audit.values()),
        audit, "public PDF, SVG, and PNG are byte-identical to masters",
    )]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--automatic-only", action="store_true")
    args = parser.parse_args()
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    contract = json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))
    results = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
    rows = rows_from(ROOT / "data.csv")

    checks = [
        *asset_checks(config),
        *lineage_checks(config, results),
        *parameter_contract_checks(config, contract),
        *formula_checks(config, rows),
        *publication_checks(config),
    ]
    text = " ".join((
        (ROOT / "README.md").read_text(encoding="utf-8"),
        (ROOT / "caption.md").read_text(encoding="utf-8"),
        (ROOT / "figure-contract.md").read_text(encoding="utf-8"),
        contract["claimBoundary"],
    )).lower()
    boundary_terms = [
        "cannot replace the continuous proof", "four-dimensional caustic",
        "time-dependent phases", "third-carrier", "three-dimensional navier",
        "arnol'd", "not claimed as new",
    ]
    checks.append(gate(
        "claim_boundary_text", all(term in text for term in boundary_terms),
        boundary_terms, "figure text preserves proof, literature, and scope boundaries",
    ))
    result_gate = (
        results.get("status") == "passed"
        and results.get("noPdeEvolution") is True
        and results.get("noFiniteFit") is True
        and results.get("numericSamplingDoesNotReplaceContinuousProof") is True
        and results.get("rowCount") == len(rows)
    )
    checks.append(gate(
        "results_contract", result_gate,
        {key: results.get(key) for key in ("status", "noPdeEvolution", "noFiniteFit", "rowCount")},
        "results record no PDE, no fit, and exact data count",
    ))

    automatic_passed = all(item["passed"] for item in checks)
    visual = os.environ.get("R072R_VISUAL_QA_INSPECTED", "").strip().lower() == "true"
    if not args.automatic_only:
        checks.append(gate(
            "explicit_visual_inspection", visual, visual,
            "R072R_VISUAL_QA_INSPECTED=true after final-size, grayscale, and PDF inspection",
        ))
    all_passed = all(item["passed"] for item in checks)
    validation = {
        "schemaVersion": "r072r-figure-validation-v1",
        "status": "passed" if all_passed else "failed",
        "allPassed": all_passed,
        "automaticOnly": args.automatic_only,
        "automaticChecksPassed": automatic_passed,
        "checkCount": len(checks),
        "checks": checks,
    }
    (ROOT / "validation.json").write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# R0.72R figure QA report", "",
        f"Status: **{validation['status'].upper()}**", "",
        f"Automatic-only run: `{args.automatic_only}`", "",
    ]
    for item in checks:
        lines.append(f"- [{'x' if item['passed'] else ' '}] `{item['name']}` — {item['requirement']}")
    lines.extend(["", "Visual inspection must use the final-size, grayscale, and PDF-raster QA surfaces.", ""])
    (ROOT / "qa-report.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"status": validation["status"], "checks": len(checks),
                      "automaticOnly": args.automatic_only}, indent=2))
    if not all_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
