#!/usr/bin/env python3
"""Validate the R0.72S singular-strata formal figure package."""

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

    expected_series = {
        "A": {"A4 closure", "A5 point"},
        "B": {"A2 exact +", "A2 exact -", "A2 leading +", "A2 leading -"},
        "C": {"A3 exact +", "A3 exact -", "A3 leading +", "A3 leading -",
              "A3 persistent axis"},
    }
    actual_series = {
        panel: {row["series"] for row in rows if row["panel"] == panel}
        for panel in "ABC"
    }
    grouped = {
        series: [row for row in rows if row["series"] == series]
        for values in expected_series.values() for series in values
    }
    panel_a = config["panels"]["A"]
    panel_b = config["panels"]["B"]
    panel_c = config["panels"]["C"]
    step_b = (
        float(panel_b["deltaMaximum"]) - float(panel_b["deltaMinimum"])
    ) / (int(panel_b["samples"]) - 1)
    step_c = (
        float(panel_c["deltaMaximum"]) - float(panel_c["deltaMinimum"])
    ) / (int(panel_c["samples"]) - 1)

    def x_bounds(series: str) -> tuple[float, float]:
        values = [float(row["x"]) for row in grouped[series]]
        return min(values, default=math.inf), max(values, default=-math.inf)

    active_b = [len(grouped[name]) for name in sorted(expected_series["B"])]
    active_c = [
        len(grouped[name]) for name in sorted(expected_series["C"])
        if name != "A3 persistent axis"
    ]
    ranges_b = [x_bounds(name) for name in sorted(expected_series["B"])]
    ranges_c = [
        x_bounds(name) for name in sorted(expected_series["C"])
        if name != "A3 persistent axis"
    ]
    persistent_c_range = x_bounds("A3 persistent axis")
    a4_phi = [float(row["phi"]) for row in grouped["A4 closure"]]
    coverage = {
        "seriesExact": actual_series == expected_series,
        "a4Samples": len(grouped["A4 closure"]) == int(panel_a["phiSamples"]),
        "a4PhiRange": (
            abs(min(a4_phi, default=math.inf) + math.pi) <= tolerance
            and abs(max(a4_phi, default=-math.inf) - math.pi) <= tolerance
        ),
        "a5Samples": len(grouped["A5 point"]) == 2,
        "a2Balanced": min(active_b, default=0) >= 2 and len(set(active_b)) == 1,
        "a2Range": all(
            abs(low - float(panel_b["deltaMinimum"])) <= tolerance
            and -step_b - tolerance <= high <= tolerance
            for low, high in ranges_b
        ),
        "a3Balanced": min(active_c, default=0) >= 2 and len(set(active_c)) == 1,
        "a3Range": all(
            abs(low - float(panel_c["deltaMinimum"])) <= tolerance
            and -step_c - tolerance <= high <= tolerance
            for low, high in ranges_c
        ),
        "persistentSamples": len(grouped["A3 persistent axis"]) == int(panel_c["samples"]),
        "persistentRange": (
            abs(persistent_c_range[0] - float(panel_c["deltaMinimum"])) <= tolerance
            and abs(persistent_c_range[1] - float(panel_c["deltaMaximum"])) <= tolerance
        ),
    }
    checks.append(gate(
        "required_series_and_sampling_intervals",
        all(coverage.values()),
        {"checks": coverage, "series": {key: sorted(value) for key, value in actual_series.items()},
         "counts": {key: len(value) for key, value in grouped.items()},
         "rangesB": ranges_b, "rangesC": ranges_c,
         "persistentCRange": persistent_c_range},
        "every declared exact, leading, and persistent series covers its configured interval",
    ))

    residuals_a: list[float] = []
    for row in (item for item in rows if item["panel"] == "A"):
        a_value = float(row["x"])
        b_value = float(row["y"])
        phi_value = float(row["phi"])
        if row["series"] == "A4 closure":
            residuals_a.extend([
                abs(a_value - math.cos(phi_value) / 15.0),
                abs(b_value - math.sin(phi_value) / 5.0),
                abs((15.0 * a_value) ** 2 + (5.0 * b_value) ** 2 - 1.0),
            ])
        elif row["series"] == "A5 point":
            residuals_a.extend([
                abs(b_value), abs(abs(15.0 * a_value) - 1.0),
                abs(math.sin(phi_value)),
            ])
        else:
            residuals_a.append(math.inf)
    checks.append(gate(
        "panel_a_exact_higher_stratum_spine", max(residuals_a, default=math.inf) <= tolerance,
        {"maxResidual": max(residuals_a, default=None)},
        "A4 closure and the two A5 points match the exact incidence formulas",
    ))

    residuals_b: list[float] = []
    for row in (item for item in rows if item["panel"] == "B"):
        delta = float(row["x"])
        xi = float(row["y"])
        if row["series"].startswith("A2 exact"):
            k_value = math.exp(-3.0 * delta)
            residuals_b.append(abs(-math.cos(xi) + k_value * math.cos(2.0 * xi)))
        elif row["series"].startswith("A2 leading"):
            residuals_b.append(abs(xi * xi + 2.0 * delta))
        else:
            residuals_b.append(math.inf)
    checks.append(gate(
        "panel_b_exact_a2_branches", max(residuals_b, default=math.inf) <= tolerance,
        {"maxResidual": max(residuals_b, default=None)},
        "the A2 exact branches and leading squared law match their formulas",
    ))

    residuals_c: list[float] = []
    a0 = -2563.0 / 1280.0
    b0 = 1.0 / 30.0
    for row in (item for item in rows if item["panel"] == "C"):
        delta = float(row["x"])
        phi_value = float(row["y"])
        series = row["series"]
        if series.startswith("A3 exact"):
            tau = 0.5 * math.exp(-delta)
            x_value = math.cos(phi_value)
            residuals_c.append(abs(
                12.0 * b0 * tau**8 * x_value * x_value
                + 4.0 * a0 * tau**3 * x_value
                + 1.0 - 3.0 * b0 * tau**8
            ))
        elif series.startswith("A3 leading"):
            residuals_c.append(abs(phi_value * phi_value + 6.0 * delta))
        elif series == "A3 persistent axis":
            residuals_c.append(abs(phi_value))
        else:
            residuals_c.append(math.inf)
    checks.append(gate(
        "panel_c_exact_a3_branches", max(residuals_c, default=math.inf) <= tolerance,
        {"maxResidual": max(residuals_c, default=None)},
        "the A3 exact, leading, and persistent branches match their formulas",
    ))
    return checks


def parameter_contract_checks(
    config: dict[str, Any], contract: dict[str, Any]
) -> list[dict[str, Any]]:
    p = config["parameters"]
    expected = {
        "a2CrossingY": math.log(2.0),
        "a2SplitSquared": -2.0,
        "a2ThirdJet": -3.0,
        "a3A0": -2563.0 / 1280.0,
        "a3B0": 1.0 / 30.0,
        "a3CrossingY": math.log(2.0),
        "a3SplitSquared": -6.0,
        "a3FourthJet": -1533.0 / 512.0,
        "coefficientDerivativeJetDeterminant": 5400.0,
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
        "r072sSchema": contract.get("schemaVersion") == "r072s-figure-contract-v1",
        "restrictedMiniversality": "restricted miniversality" in contract_text,
        "a2Counts": "4/3/2" in contract_text,
        "a3Counts": "4/2/2" in contract_text,
        "coefficientJet": "determinant 5400" in contract_text,
    }
    return [gate(
        "r072s_parameter_and_contract_consistency",
        all(parameter_audit.values()) and all(contract_audit.values()),
        {"parameters": parameter_audit, "contract": contract_audit},
        "config and contract encode the certified R0.72S strata and heat collisions",
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
        "real-even", "arnol'd", "not claimed as new",
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
    visual = os.environ.get("R072S_VISUAL_QA_INSPECTED", "").strip().lower() == "true"
    if not args.automatic_only:
        checks.append(gate(
            "explicit_visual_inspection", visual, visual,
            "R072S_VISUAL_QA_INSPECTED=true after final-size, grayscale, and PDF inspection",
        ))
    all_passed = all(item["passed"] for item in checks)
    validation = {
        "schemaVersion": "r072s-figure-validation-v1",
        "status": "passed" if all_passed else "failed",
        "allPassed": all_passed,
        "automaticOnly": args.automatic_only,
        "automaticChecksPassed": automatic_passed,
        "checkCount": len(checks),
        "checks": checks,
    }
    (ROOT / "validation.json").write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# R0.72S figure QA report", "",
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
