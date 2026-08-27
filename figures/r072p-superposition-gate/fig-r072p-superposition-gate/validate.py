#!/usr/bin/env python3
"""Validate the R0.72P formal figure package and public masters."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import re
from typing import Any

from PIL import Image, ImageStat
from pypdf import PdfReader

from certificate_ledger import verify_flat_certificate_ledger


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
PACKAGE_SOURCES = (
    "README.md",
    "caption.md",
    "figure-contract.md",
    "contract.json",
    "config.json",
    "command.txt",
    "requirements.txt",
    "certificate_ledger.py",
    "plot.py",
    "qa_images.py",
    "publish_assets.py",
    "validate.py",
    "build_manifest.py",
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def relerr(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def check(name: str, passed: bool, value: Any, requirement: str) -> dict[str, Any]:
    return {
        "name": name,
        "passed": bool(passed),
        "value": value,
        "requirement": requirement,
    }


def expected_pixels(config: dict[str, Any], dpi: int) -> tuple[int, int]:
    figure = config["figure"]
    return (
        round(float(figure["widthMillimetres"]) / 25.4 * dpi),
        round(float(figure["heightMillimetres"]) / 25.4 * dpi),
    )


def profile(y_value: float, phi: float, lam: float) -> float:
    return math.exp(-y_value) * math.cos(phi) + lam * math.exp(-4.0 * y_value) * math.cos(2.0 * phi)


def window_representative(r_value: float, p_value: float) -> float:
    return p_value ** (4.0 / 3.0) * r_value ** (4.0 / 3.0) * (1.0 + math.log(r_value)) ** 2


def main(*, automatic_only: bool = False) -> int:
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    contract = json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))
    results = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
    rows = read_csv(ROOT / "data.csv")
    items: list[dict[str, Any]] = []

    required = [
        *PACKAGE_SOURCES,
        "figure.pdf",
        "figure.svg",
        "figure.png",
        "data.csv",
        "results.json",
        "environment.txt",
        "qa-final-size.png",
        "qa-grayscale.png",
        "qa-pdf.png",
        "progress.ndjson",
        "resource-log.ndjson",
    ]
    missing = [name for name in required if not (ROOT / name).is_file()]
    items.append(
        check(
            "required_assets",
            not missing,
            missing,
            "all source, master, data, QA, and archive inputs exist",
        )
    )

    width_mm = float(config["figure"]["widthMillimetres"])
    height_mm = float(config["figure"]["heightMillimetres"])
    png_dpi = int(config["figure"]["pngDpi"])
    with Image.open(ROOT / "figure.png") as image:
        png_size = image.size
        png_dpi_meta = image.info.get("dpi", (0.0, 0.0))
    expected_png = expected_pixels(config, png_dpi)
    items.append(
        check(
            "png_600_dpi",
            all(abs(float(value) - png_dpi) < 0.02 for value in png_dpi_meta),
            png_dpi_meta,
            "PNG metadata is 600 dpi",
        )
    )
    items.append(
        check(
            "png_dimensions",
            all(abs(left - right) <= 2 for left, right in zip(png_size, expected_png)),
            {"actual": png_size, "expected": expected_png},
            "PNG pixels match final size at 600 dpi",
        )
    )

    reader = PdfReader(str(ROOT / "figure.pdf"))
    page = reader.pages[0]
    pdf_mm = (
        float(page.mediabox.width) * 25.4 / 72.0,
        float(page.mediabox.height) * 25.4 / 72.0,
    )
    items.append(check("pdf_one_page", len(reader.pages) == 1, len(reader.pages), "PDF has one page"))
    items.append(
        check(
            "pdf_dimensions",
            abs(pdf_mm[0] - width_mm) < 0.08 and abs(pdf_mm[1] - height_mm) < 0.08,
            pdf_mm,
            f"PDF matches {width_mm:g} x {height_mm:g} mm",
        )
    )
    svg = (ROOT / "figure.svg").read_text(encoding="utf-8")
    raster_count = svg.count("<image")
    items.append(
        check(
            "svg_vector_text",
            "<svg" in svg
            and "<text" in svg
            and raster_count <= int(config["validation"]["maximumSvgRasterImages"]),
            {"svg": "<svg" in svg, "text": "<text" in svg, "rasterImages": raster_count},
            "SVG is vector-only and keeps editable text",
        )
    )

    qa_dpi = int(config["figure"]["qaDpi"])
    qa_expected = expected_pixels(config, qa_dpi)
    qa_sizes: dict[str, tuple[int, int]] = {}
    for name in ("qa-final-size.png", "qa-grayscale.png", "qa-pdf.png"):
        with Image.open(ROOT / name) as image:
            qa_sizes[name] = image.size
    items.append(
        check(
            "qa_dimensions",
            all(size == qa_expected for size in qa_sizes.values()),
            qa_sizes,
            "QA surfaces match final print size at 180 dpi",
        )
    )
    with Image.open(ROOT / "qa-grayscale.png") as image:
        gray_std = float(ImageStat.Stat(image.convert("L")).stddev[0])
    minimum_gray = float(config["validation"]["minimumGrayscaleStandardDeviation"])
    items.append(
        check(
            "grayscale_contrast",
            gray_std > minimum_gray,
            gray_std,
            f"grayscale standard deviation exceeds {minimum_gray:g}",
        )
    )

    parameters = config["parameters"]
    declared_parameters = {
        "carrierMultipliers": parameters["carrierMultipliers"],
        "N": parameters["carrierCount"],
        "B": parameters["coherenceB"],
        "p": parameters["p"],
        "lambdaSafe": parameters["lambdaSafe"],
        "positiveLowerCone": parameters["lambdaLowerMustBePositive"],
        "shapeRadius": parameters["shapeRadius"],
        "shapeC0": parameters["shapeC0"],
        "shapeC1": parameters["shapeC1"],
    }
    parameter_gate = (
        parameters["carrierMultipliers"] == [1, 2]
        and int(parameters["carrierCount"]) == 2
        and float(parameters["coherenceB"]) == 2.0
        and relerr(float(parameters["p"]), 1.0 / math.sqrt(2.0)) < 2.0e-15
        and float(parameters["lambdaSafe"]) == 1.0 / 8.0
        and parameters["lambdaLowerMustBePositive"] is True
        and relerr(float(parameters["shapeRadius"]), math.pi / 4.0) < 2.0e-15
        and float(parameters["shapeC0"]) == 144.0
        and float(parameters["shapeC1"]) == 12.0
    )
    items.append(
        check(
            "declared_two_carrier_parameters",
            parameter_gate,
            declared_parameters,
            "the package is locked to the declared (R,2R), B=2, p=1/sqrt(2), nonzero safe-cone class",
        )
    )

    cell_factor_text = "\n".join(
        [
            (ROOT / "README.md").read_text(encoding="utf-8"),
            (ROOT / "caption.md").read_text(encoding="utf-8"),
            (ROOT / "figure-contract.md").read_text(encoding="utf-8"),
            (ROOT / "plot.py").read_text(encoding="utf-8"),
            "\n".join(contract["analyticClaims"]),
        ]
    ).lower()
    cell_factor_terms = [
        "signed shifts",
        "factor `2",
        "epsilon` absorbs",
        "b=2` does not cancel",
    ]
    items.append(
        check(
            "panel_a_signed_shift_factor_claim",
            all(term in cell_factor_text for term in cell_factor_terms)
            and "b=2$ cancels" not in cell_factor_text,
            cell_factor_terms,
            "Panel A says paired signed shifts give factor 2 and epsilon absorbs it; B=2 is not a cancellation",
        )
    )

    lineage = results.get("runtimeLineage", {})
    required_lineage = {
        "analyticSource",
        "producerConfig",
        "producerResult",
        "independentConfig",
        "independentResult",
        "crosscheck",
        "certificateLedger",
    }
    expected_record_status = {
        "analyticSource": "source",
        "producerConfig": "formal-ready-config",
        "producerResult": "passed",
        "independentConfig": "formal-ready-config",
        "independentResult": "passed",
        "crosscheck": "passed-formal-source-only",
        "certificateLedger": "passed-flat-ledger",
    }
    lineage_checks: dict[str, Any] = {}
    lineage_payloads: dict[str, dict[str, Any]] = {}
    for name in sorted(required_lineage):
        record = lineage.get(name, {})
        path_text = record.get("path") if isinstance(record, dict) else None
        path = Path(path_text).expanduser().resolve() if isinstance(path_text, str) else Path("/")
        exists = isinstance(path_text, str) and path.is_file()
        current_hash = digest(path) if exists else None
        status_ok = record.get("status") == expected_record_status[name]
        json_status = None
        if exists and name not in {"analyticSource", "certificateLedger"}:
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
                if isinstance(payload, dict):
                    lineage_payloads[name] = payload
                    json_status = payload.get("status", "configuration")
                else:
                    json_status = "not-an-object"
            except (json.JSONDecodeError, UnicodeDecodeError):
                json_status = "unreadable"
        input_ok = (
            name == "analyticSource"
            or name == "certificateLedger"
            or name in {"producerConfig", "independentConfig"}
            and json_status == "configuration"
            or name in {"producerResult", "independentResult", "crosscheck"}
            and json_status == "passed"
        )
        lineage_checks[name] = {
            "exists": exists,
            "hashMatches": exists and current_hash == record.get("sha256"),
            "recordStatus": record.get("status"),
            "inputStatus": json_status,
            "path": path_text,
            "passed": exists
            and current_hash == record.get("sha256")
            and status_ok
            and input_ok,
        }
    lineage_paths = [lineage_checks[name]["path"] for name in sorted(required_lineage)]
    certificate_names = required_lineage - {"analyticSource"}
    certificate_parents = {
        str(Path(lineage_checks[name]["path"]).expanduser().resolve().parent)
        for name in certificate_names
        if isinstance(lineage_checks[name]["path"], str)
    }
    producer_config = lineage_payloads.get("producerConfig", {})
    independent_config = lineage_payloads.get("independentConfig", {})
    producer_result = lineage_payloads.get("producerResult", {})
    independent_result = lineage_payloads.get("independentResult", {})
    crosscheck = lineage_payloads.get("crosscheck", {})
    crosscheck_checks = crosscheck.get("checks", {})
    source_commit = crosscheck.get("sourceCommit")
    expected_lineage_statuses = {
        "producer": "passed",
        "independent": "passed",
        "crosscheck": "passed",
        "formalSourceReady": True,
        "temporaryUnsealedSourceAllowed": False,
    }
    expected_package_git_paths = {
        str((ROOT / name).resolve().relative_to(REPOSITORY.resolve()))
        for name in PACKAGE_SOURCES
    }
    package_git_blobs = results.get("packageSourceGitBlobs", {})
    formal_source_gate = (
        isinstance(crosscheck_checks, dict)
        and crosscheck_checks.get("formalSourceReady") is True
        and crosscheck_checks.get("sourceCommitMatches") is True
        and crosscheck_checks.get("sourceReadyOrExplicitlyAllowed") is True
        and crosscheck_checks.get("producerPassed") is True
        and crosscheck_checks.get("independentPassed") is True
        and crosscheck.get("temporaryUnsealedSourceAllowed") is False
        and isinstance(source_commit, str)
        and FULL_SHA.fullmatch(source_commit) is not None
        and producer_config.get("gitCommit") == source_commit
        and independent_config.get("gitCommit") == source_commit
        and producer_config.get("sourceTracked") is True
        and independent_config.get("sourceTracked") is True
        and producer_config.get("trackedChangesDirty") is False
        and independent_config.get("trackedChangesDirty") is False
        and producer_result.get("status") == "passed"
        and independent_result.get("status") == "passed"
        and results.get("formalSourceCommit") == source_commit
        and results.get("lineageStatuses") == expected_lineage_statuses
        and results.get("verifiedTrackedTreeClean") is True
        and results.get("verifiedPackageSourcesAtBuildCommit") is True
        and isinstance(package_git_blobs, dict)
        and set(package_git_blobs) == expected_package_git_paths
        and all(
            isinstance(value, str) and FULL_SHA.fullmatch(value) is not None
            for value in package_git_blobs.values()
        )
        and isinstance(results.get("repositoryCommitAtBuild"), str)
        and FULL_SHA.fullmatch(results["repositoryCommitAtBuild"]) is not None
    )
    bindings = config["formalGitBindings"]
    canonical_paths = {
        "analyticSource": bindings["sourceCommitPaths"][0],
        **bindings["certificateCommitRoles"],
        "certificateLedger": bindings["certificateLedgerPath"],
    }
    canonical_runtime_paths = {
        name: isinstance(lineage_checks[name]["path"], str)
        and Path(lineage_checks[name]["path"]).expanduser().resolve()
        == (REPOSITORY / relative).resolve()
        for name, relative in canonical_paths.items()
    }
    items.append(
        check(
            "runtime_lineage",
            set(lineage) == required_lineage
            and all(value["passed"] for value in lineage_checks.values())
            and len(set(lineage_paths)) == len(lineage_paths)
            and certificate_parents == {
                str((REPOSITORY / "research/certificates/r072p").resolve())
            }
            and all(canonical_runtime_paths.values()),
            {
                "records": lineage_checks,
                "certificateParents": sorted(certificate_parents),
                "canonicalPaths": canonical_runtime_paths,
            },
            "the frozen report, five runtime certificate JSON files, and the flat certificate ledger retain hashes at canonical paths",
        )
    )

    ledger_audit = verify_flat_certificate_ledger(
        REPOSITORY / Path(bindings["certificateLedgerPath"]).parent,
        required_files={
            Path(relative).name
            for relative in bindings["certificateCommitRoles"].values()
        },
    )
    recorded_ledger_audit = results.get("certificateLedgerAudit", {})
    items.append(
        check(
            "flat_certificate_ledger",
            ledger_audit.get("status") == "passed"
            and ledger_audit.get("ledgerSha256")
            == lineage["certificateLedger"].get("sha256")
            == recorded_ledger_audit.get("ledgerSha256")
            and ledger_audit.get("entryCount")
            == recorded_ledger_audit.get("entryCount")
            and ledger_audit.get("requiredRuntimeJson")
            == recorded_ledger_audit.get("requiredRuntimeJson")
            and recorded_ledger_audit.get("exactDirectoryCoverage") is True
            and recorded_ledger_audit.get("uniqueByteSortedRows") is True
            and recorded_ledger_audit.get("symlinksRejected") is True,
            {
                "current": ledger_audit,
                "recordedLedgerSha256": recorded_ledger_audit.get("ledgerSha256"),
                "recordedEntryCount": recorded_ledger_audit.get("entryCount"),
            },
            "SHA256SUMS is unique, byte-sorted, digest-correct, symlink-free, and exactly covers the canonical certificate directory including all five runtime JSON files",
        )
    )
    items.append(
        check(
            "formal_source_certificate_gate",
            formal_source_gate,
            {
                "sourceCommit": source_commit,
                "crosscheckStatus": crosscheck.get("status"),
                "formalSourceReady": crosscheck_checks.get("formalSourceReady")
                if isinstance(crosscheck_checks, dict)
                else None,
                "temporaryUnsealedSourceAllowed": crosscheck.get(
                    "temporaryUnsealedSourceAllowed"
                ),
                "producerConfigCommit": producer_config.get("gitCommit"),
                "independentConfigCommit": independent_config.get("gitCommit"),
                "producerSourceTracked": producer_config.get("sourceTracked"),
                "independentSourceTracked": independent_config.get("sourceTracked"),
                "producerTrackedDirty": producer_config.get("trackedChangesDirty"),
                "independentTrackedDirty": independent_config.get("trackedChangesDirty"),
                "resultsFormalSourceCommit": results.get("formalSourceCommit"),
                "verifiedTrackedTreeClean": results.get("verifiedTrackedTreeClean"),
                "verifiedPackageSourcesAtBuildCommit": results.get(
                    "verifiedPackageSourcesAtBuildCommit"
                ),
                "packageSourceGitBlobCount": len(package_git_blobs)
                if isinstance(package_git_blobs, dict)
                else None,
            },
            "temporary certificates are rejected and both clean tracked route configs bind one 40-hex source commit",
        )
    )

    changed_package_sources = [
        name
        for name, expected in results.get("packageSourceHashes", {}).items()
        if not (ROOT / name).is_file() or digest(ROOT / name) != expected
    ]
    source_hash_keys = set(results.get("packageSourceHashes", {}))
    items.append(
        check(
            "package_source_lineage",
            source_hash_keys == set(PACKAGE_SOURCES) and not changed_package_sources,
            {"recorded": sorted(source_hash_keys), "changed": changed_package_sources},
            "all package sources retain their build hashes",
        )
    )

    minimum_rows = int(config["validation"]["minimumDataRows"])
    panel_counts = {panel: sum(row["panel"] == panel for row in rows) for panel in "ABCD"}
    expected_counts = {
        "A": len(config["panels"]["A"]["ySlices"]) * int(config["panels"]["A"]["samples"]),
        "B": 3 * int(config["panels"]["B"]["samples"]),
        "C": 2 * int(config["panels"]["C"]["samples"]),
        "D": int(config["panels"]["D"]["samples"]) + 2 * len(config["panels"]["D"]["statusAnchors"]),
    }
    items.append(
        check(
            "data_completeness",
            len(rows) >= minimum_rows and panel_counts == expected_counts,
            {"rows": len(rows), "panels": panel_counts, "expectedPanels": expected_counts},
            f"data.csv has the exact four-panel row counts and at least {minimum_rows} traceable rows",
        )
    )

    panel_a = [row for row in rows if row["panel"] == "A"]
    a_errors = [
        relerr(
            float(row["y"]),
            profile(float(row["yParameter"]), float(row["x"]), float(row["lambda"])),
        )
        for row in panel_a
    ]
    items.append(
        check(
            "panel_a_exact_profile",
            len(panel_a) == expected_counts["A"]
            and max(a_errors, default=math.inf) < 3.0e-15
            and all(row["status"] == "proved declared two-carrier class" for row in panel_a),
            {"rows": len(panel_a), "maxRelativeError": max(a_errors, default=None)},
            "Panel A directly evaluates the exact full two-carrier profile",
        )
    )

    panel_b = [row for row in rows if row["panel"] == "B"]
    b_errors: list[float] = []
    for row in panel_b:
        phi = float(row["x"])
        if row["series"] == "bracket lower envelope":
            expected = 1.0 - 0.5 * abs(math.cos(phi))
        elif row["series"] == "bracket upper envelope":
            expected = 1.0 + 0.5 * abs(math.cos(phi))
        elif row["series"] == "positive-boundary bracket":
            expected = 1.0 + 4.0 * float(parameters["lambdaExample"]) * math.cos(phi)
        else:
            expected = math.nan
        b_errors.append(relerr(float(row["y"]), expected))
    b_lower = [float(row["y"]) for row in panel_b if row["series"] == "bracket lower envelope"]
    b_upper = [float(row["y"]) for row in panel_b if row["series"] == "bracket upper envelope"]
    analytic_bracket_gate = 4.0 * float(parameters["lambdaSafe"]) == 0.5
    items.append(
        check(
            "panel_b_uniform_bracket",
            len(panel_b) == expected_counts["B"]
            and max(b_errors, default=math.inf) < 3.0e-15
            and min(b_lower, default=-math.inf) >= 0.5 - 2.0e-15
            and max(b_upper, default=math.inf) <= 1.5 + 2.0e-15
            and analytic_bracket_gate,
            {
                "rows": len(panel_b),
                "maxRelativeError": max(b_errors, default=None),
                "denseMinimum": min(b_lower, default=None),
                "denseMaximum": max(b_upper, default=None),
                "analyticFourLambdaSafe": 4.0 * float(parameters["lambdaSafe"]),
            },
            "Panel B evaluates the exact envelope; the continuum proof is the analytic bound 4|lambda|<=1/2, not sampling",
        )
    )

    panel_c = [row for row in rows if row["panel"] == "C"]
    c_errors: list[float] = []
    for row in panel_c:
        y_value = float(row["x"])
        expected = (
            0.25 * math.exp(3.0 * y_value)
            if row["series"] == "time-slice Morse wall"
            else float(parameters["lambdaSafe"])
            if row["series"] == "safe-cone ceiling"
            else math.nan
        )
        c_errors.append(relerr(float(row["y"]), expected))
    wall_rows = [row for row in panel_c if row["series"] == "time-slice Morse wall"]
    items.append(
        check(
            "panel_c_exact_morse_wall",
            len(panel_c) == expected_counts["C"]
            and max(c_errors, default=math.inf) < 3.0e-15
            and bool(wall_rows)
            and min(float(row["y"]) for row in wall_rows) == 0.25
            and all(row["status"] == "exact wall; not ED failure" for row in wall_rows),
            {"rows": len(panel_c), "maxRelativeError": max(c_errors, default=None)},
            "Panel C evaluates |lambda|=exp(3y)/4 and labels it only as this Morse certificate's boundary",
        )
    )

    panel_d = [row for row in rows if row["panel"] == "D"]
    d_errors = [
        relerr(
            float(row["y"]),
            window_representative(float(row["x"]), float(row["p"])),
        )
        for row in panel_d
    ]
    d_counts = {
        series: sum(row["series"] == series for row in panel_d)
        for series in (
            "proved-class physical-window representative",
            "R0.72O conditional status marker",
            "R0.72P proved status marker",
        )
    }
    anchors = len(config["panels"]["D"]["statusAnchors"])
    panel_d_contract = config["panels"]["D"]
    items.append(
        check(
            "panel_d_claim_promotion",
            len(panel_d) == expected_counts["D"]
            and max(d_errors, default=math.inf) < 3.0e-15
            and d_counts["proved-class physical-window representative"] == int(config["panels"]["D"]["samples"])
            and d_counts["R0.72O conditional status marker"] == anchors
            and d_counts["R0.72P proved status marker"] == anchors
            and all(
                row["status"] == "proved declared two-carrier class"
                for row in panel_d
                if row["series"] in {"proved-class physical-window representative", "R0.72P proved status marker"}
            )
            and all(
                row["status"] == "conditional before R0.72P shape proof"
                for row in panel_d
                if row["series"] == "R0.72O conditional status marker"
            )
            and panel_d_contract.get("exactLedgerFactor") == "L_(R,epsilon)^2"
            and panel_d_contract.get("displayedRepresentativeAssumption") == "fixed-polynomial coupling"
            and panel_d_contract.get("displayedLRepresentative") == "1+log R",
            {
                "rows": len(panel_d),
                "series": d_counts,
                "maxRelativeError": max(d_errors, default=None),
                "ledgerContract": {
                    "exact": panel_d_contract.get("exactLedgerFactor"),
                    "assumption": panel_d_contract.get("displayedRepresentativeAssumption"),
                    "representative": panel_d_contract.get("displayedLRepresentative"),
                },
            },
            "Panel D uses the same fixed-polynomial representative values for prior conditional and current proved statuses in only the declared class",
        )
    )

    formula_checks = results.get("formulaChecks", {})
    result_formula_gate = (
        relerr(float(formula_checks.get("bracketLower", math.nan)), 0.5) < 2.0e-15
        and relerr(float(formula_checks.get("bracketUpper", math.nan)), 1.5) < 2.0e-15
        and relerr(float(formula_checks.get("morseWallAtYZero", math.nan)), 0.25) < 2.0e-15
        and relerr(
            float(formula_checks.get("windowRepresentativePFactor", math.nan)),
            2.0 ** (-2.0 / 3.0),
        )
        < 2.0e-15
        and relerr(
            float(formula_checks.get("windowRepresentativePFactor", math.nan)),
            float(formula_checks.get("expectedWindowRepresentativePFactor", math.nan)),
        )
        < 2.0e-15
        and formula_checks.get("exactLedgerRetainsLREpsilon") is True
        and formula_checks.get("displayedWindowIsFixedPolynomialAsymptoticRepresentative") is True
    )
    items.append(
        check(
            "result_formula_ledger",
            result_formula_gate,
            formula_checks,
            "results.json records the exact safe-bracket and first-wall factors and labels the p=1/sqrt(2) curve as only a fixed-polynomial representative",
        )
    )

    finite_rows = [
        row
        for row in rows
        if "finite" in row["kind"].lower() or "finite" in row["status"].lower()
    ]
    finite_rows_well_labeled = all(
        "finite-only" in row["kind"].lower() or "finite-only" in row["status"].lower()
        for row in finite_rows
    )
    no_fit = (
        results.get("noPdeEvolution") is True
        and results.get("noFiniteFit") is True
        and results.get("formulaCurvesNotCertificateInterpolation") is True
        and contract["renderPolicy"]["finiteFit"] == "forbidden"
        and finite_rows_well_labeled
        and not any(" fitted " in f" {row['series'].lower()} " for row in rows)
    )
    items.append(
        check(
            "no_simulation_fit_or_unlabeled_finite_diagnostic",
            no_fit,
            {
                "noPdeEvolution": results.get("noPdeEvolution"),
                "noFiniteFit": results.get("noFiniteFit"),
                "formulaCurvesNotCertificateInterpolation": results.get("formulaCurvesNotCertificateInterpolation"),
                "finiteRows": len(finite_rows),
                "finiteRowsWellLabeled": finite_rows_well_labeled,
            },
            "the package contains no PDE evolution, fit, certificate interpolation, or unlabeled finite-only diagnostic",
        )
    )

    publication = config["publication"]
    public_root = REPOSITORY / publication["directory"]
    identities = {
        suffix: (public_root / f"{publication['stem']}.{suffix}").is_file()
        and digest(public_root / f"{publication['stem']}.{suffix}") == digest(ROOT / f"figure.{suffix}")
        for suffix in ("pdf", "svg", "png")
    }
    items.append(
        check(
            "public_byte_identity",
            all(identities.values()),
            identities,
            "public masters are byte-identical to archival masters",
        )
    )

    combined = "\n".join(
        [
            (ROOT / "README.md").read_text(encoding="utf-8"),
            (ROOT / "caption.md").read_text(encoding="utf-8"),
            (ROOT / "figure-contract.md").read_text(encoding="utf-8"),
            contract["claimBoundary"],
        ]
    ).lower()
    boundary_terms = [
        "fixed nonzero coefficient cone",
        "arbitrary `n`",
        "finite-only",
        "not a counterexample",
        "enhanced dissipation itself",
        "fixed-polynomial-coupling asymptotic representative",
        "exact ledger retains",
        "global navier",
    ]
    items.append(
        check(
            "claim_boundary",
            all(term in combined for term in boundary_terms),
            boundary_terms,
            "the package preserves the nonzero-cone, arbitrary-N, finite-only, Morse-wall, and Clay-problem boundaries",
        )
    )

    visual = os.environ.get("R072P_VISUAL_QA_INSPECTED", "").strip().lower() == "true"
    items.append(
        check(
            "visual_inspection_declared",
            visual,
            visual,
            "final-size, grayscale, and PDF-raster surfaces were explicitly inspected",
        )
    )

    automatic_items = [item for item in items if item["name"] != "visual_inspection_declared"]
    automatic_passed = all(item["passed"] for item in automatic_items)
    all_passed = automatic_passed and visual
    run_passed = automatic_passed if automatic_only else all_passed
    payload = {
        "schemaVersion": 1,
        "figureId": "R0.72P-1",
        "status": (
            "automatic-passed"
            if automatic_only and automatic_passed
            else "passed"
            if all_passed
            else "failed"
        ),
        "allPassed": all_passed,
        "automaticOnly": automatic_only,
        "automaticChecksPassed": automatic_passed,
        "checkCount": len(items),
        "checks": items,
    }
    (ROOT / "validation.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    failed = [
        item["name"]
        for item in items
        if not item["passed"]
        and not (automatic_only and item["name"] == "visual_inspection_declared")
    ]
    (ROOT / "qa-report.md").write_text(
        "\n".join(
            [
                "# R0.72P figure QA report",
                "",
                f"- Automatic validation: **{'PASS' if automatic_passed else 'FAIL'}** ({len(automatic_items)} automatic checks).",
                f"- Final print size: {pdf_mm[0]:.3f} x {pdf_mm[1]:.3f} mm; PNG {png_size[0]} x {png_size[1]} px at 600 dpi.",
                f"- QA surfaces: {qa_expected[0]} x {qa_expected[1]} px at 180 dpi; grayscale standard deviation {gray_std:.3f}.",
                (
                    "- Human inspection: final-size, grayscale, and PDF-raster surfaces checked for legibility, collisions, wall/cone separation, and open/filled status distinction."
                    if visual
                    else "- Human inspection: not declared."
                ),
                "- Formula gate: Panels A--C are direct analytic evaluations; Panel D uses a fixed-polynomial-coupling asymptotic representative with distinct claim-status markers and retains L_(R,epsilon) in the exact ledger.",
                "- Claim boundary: proved only for the declared two-carrier nonzero cone and affine row; no arbitrary-N or general Navier--Stokes conclusion.",
                (
                    "- Human-inspection gate: deferred by --automatic-only; do not set R072P_VISUAL_QA_INSPECTED before viewing all three QA surfaces."
                    if automatic_only
                    else "- Human-inspection gate: included in the final validation status."
                ),
                f"- Failed automatic/final checks: {', '.join(failed) if failed else 'none'}.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(json.dumps({"status": payload["status"], "checks": len(items), "failed": failed}, sort_keys=True))
    return 0 if run_passed else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--automatic-only",
        action="store_true",
        help="run all machine checks while deferring the mandatory human visual gate",
    )
    arguments = parser.parse_args()
    raise SystemExit(main(automatic_only=arguments.automatic_only))
