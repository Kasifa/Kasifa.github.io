#!/usr/bin/env python3
"""Validate the R0.72Q formal phase-robust-shape figure package."""

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


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def rows_from(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def relerr(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def gate(name: str, passed: bool, value: Any, requirement: str) -> dict[str, Any]:
    return {"name": name, "passed": bool(passed), "value": value, "requirement": requirement}


def pixels(config: dict[str, Any], dpi: int) -> tuple[int, int]:
    figure = config["figure"]
    return (
        round(float(figure["widthMillimetres"]) * dpi / 25.4),
        round(float(figure["heightMillimetres"]) * dpi / 25.4),
    )


def caustic(phi: float) -> complex:
    return (
        0.125 * complex(math.cos(3.0 * phi), -math.sin(3.0 * phi))
        - 0.375 * complex(math.cos(phi), -math.sin(phi))
    )


def caustic_residual(value: complex) -> float:
    return (
        (abs(value) ** 2 - 1.0 / 16.0) ** 3
        - (27.0 / 1024.0) * value.imag**2
    )


def unwrap_phase(raw: list[float]) -> list[float]:
    if not raw:
        return []
    first = raw[0] + 2.0 * math.pi if raw[0] < 0.0 else raw[0]
    values = [first]
    for angle in raw[1:]:
        value = angle
        while value - values[-1] > math.pi:
            value -= 2.0 * math.pi
        while value - values[-1] < -math.pi:
            value += 2.0 * math.pi
        values.append(value)
    return values


def git_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True
    ).strip()


def tracked_clean() -> bool:
    return all(
        subprocess.run(command, cwd=REPOSITORY, check=False).returncode == 0
        for command in (
            ("git", "diff", "--quiet", "--"),
            ("git", "diff", "--cached", "--quiet", "--"),
        )
    )


def blob_matches(commit: str, relative: str) -> bool:
    path = (REPOSITORY / relative).resolve()
    if FULL_SHA.fullmatch(commit) is None or not path.is_file():
        return False
    try:
        committed = subprocess.check_output(
            ["git", "rev-parse", f"{commit}:{relative}"],
            cwd=REPOSITORY, text=True, stderr=subprocess.DEVNULL,
        ).strip()
        working = subprocess.check_output(
            ["git", "hash-object", f"--path={relative}", str(path)],
            cwd=REPOSITORY, text=True, stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.CalledProcessError:
        return False
    return committed == working


def asset_checks(config: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    required = [
        *PACKAGE_SOURCES, "figure.pdf", "figure.svg", "figure.png", "data.csv",
        "results.json", "environment.txt", "qa-final-size.png",
        "qa-grayscale.png", "qa-pdf.png", "progress.ndjson",
        "resource-log.ndjson",
    ]
    missing = [name for name in required if not (ROOT / name).is_file()]
    checks.append(gate("required_assets", not missing, missing, "all formal assets exist"))

    png_dpi = int(config["figure"]["pngDpi"])
    with Image.open(ROOT / "figure.png") as image:
        png_size = image.size
        png_meta = image.info.get("dpi", (0.0, 0.0))
    expected_png = pixels(config, png_dpi)
    checks.append(gate(
        "png_600_dpi",
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
        "PDF is one page at 177.8 mm final width",
    ))

    svg = (ROOT / "figure.svg").read_text(encoding="utf-8")
    raster_count = svg.count("<image")
    checks.append(gate(
        "svg_editable_vector",
        "<svg" in svg and "<text" in svg
        and raster_count <= int(config["validation"]["maximumSvgRasterImages"]),
        {"text": "<text" in svg, "rasterImages": raster_count},
        "SVG keeps editable text and contains no raster image",
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
        "all QA surfaces match final size and grayscale contrast gate",
    ))
    return checks, {
        "pngSize": png_size, "pdfMm": pdf_mm,
        "qaExpected": qa_expected, "grayStd": gray_std,
    }


def lineage_checks(
    config: dict[str, Any], results: dict[str, Any]
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    bindings = config["formalGitBindings"]
    records = results.get("runtimeLineage", {})
    required = {
        "analyticSource", "producerConfig", "producerResult",
        "independentConfig", "independentResult", "crosscheck",
        "certificateLedger",
    }
    expected_status = {
        "analyticSource": "source",
        "producerConfig": "formal-ready-config",
        "producerResult": "passed",
        "independentConfig": "formal-ready-config",
        "independentResult": "passed",
        "crosscheck": "passed-formal-source-only",
        "certificateLedger": "passed-flat-ledger",
    }
    canonical = {
        "analyticSource": bindings["sourceCommitPaths"][0],
        **bindings["certificateCommitRoles"],
        "certificateLedger": bindings["certificateLedgerPath"],
    }
    payloads: dict[str, dict[str, Any]] = {}
    audit: dict[str, Any] = {}
    for name in sorted(required):
        record = records.get(name, {})
        path_text = record.get("path") if isinstance(record, dict) else None
        path = Path(path_text).expanduser().resolve() if isinstance(path_text, str) else Path("/")
        exists = isinstance(path_text, str) and path.is_file()
        status: Any = None
        if exists and name not in {"analyticSource", "certificateLedger"}:
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                payload = None
            if isinstance(payload, dict):
                payloads[name] = payload
                status = payload.get("status", "configuration")
        input_ok = (
            name in {"analyticSource", "certificateLedger"}
            or name in {"producerConfig", "independentConfig"} and status == "configuration"
            or name in {"producerResult", "independentResult", "crosscheck"} and status == "passed"
        )
        audit[name] = {
            "exists": exists,
            "canonical": exists and path == (REPOSITORY / canonical[name]).resolve(),
            "hashMatches": exists and digest(path) == record.get("sha256"),
            "statusMatches": record.get("status") == expected_status[name],
            "inputStatus": status,
            "inputOk": input_ok,
        }
        audit[name]["passed"] = all(
            audit[name][key]
            for key in ("exists", "canonical", "hashMatches", "statusMatches", "inputOk")
        )
    checks.append(gate(
        "runtime_lineage",
        set(records) == required and all(item["passed"] for item in audit.values()),
        audit,
        "report, five certificate JSON inputs, and flat ledger are canonical and hash-stable",
    ))

    producer_config = payloads.get("producerConfig", {})
    independent_config = payloads.get("independentConfig", {})
    producer_result = payloads.get("producerResult", {})
    independent_result = payloads.get("independentResult", {})
    crosscheck = payloads.get("crosscheck", {})
    cross = crosscheck.get("checks", {})
    source_commit = crosscheck.get("sourceCommit")
    build_commit = results.get("repositoryCommitAtBuild")
    source_blobs = (
        isinstance(source_commit, str)
        and FULL_SHA.fullmatch(source_commit) is not None
        and all(blob_matches(source_commit, item) for item in bindings["sourceCommitPaths"])
    )
    certificate_relatives = [
        *bindings["certificateCommitRoles"].values(),
        bindings["certificateLedgerPath"],
    ]
    certificate_blobs = (
        isinstance(build_commit, str)
        and FULL_SHA.fullmatch(build_commit) is not None
        and build_commit == git_head()
        and all(blob_matches(build_commit, item) for item in certificate_relatives)
    )
    package_blobs = results.get("packageSourceGitBlobs", {})
    expected_package_paths = {
        str((ROOT / name).resolve().relative_to(REPOSITORY.resolve()))
        for name in PACKAGE_SOURCES
    }
    commit_gate = (
        isinstance(cross, dict)
        and cross.get("formalSourceReady") is True
        and cross.get("sourceCommitMatches") is True
        and cross.get("sourceReadyOrExplicitlyAllowed") is True
        and cross.get("producerPassed") is True
        and cross.get("independentPassed") is True
        and crosscheck.get("temporaryUnsealedSourceAllowed") is False
        and producer_config.get("gitCommit") == source_commit
        and independent_config.get("gitCommit") == source_commit
        and producer_config.get("sourceTracked") is True
        and independent_config.get("sourceTracked") is True
        and producer_config.get("trackedChangesDirty") is False
        and independent_config.get("trackedChangesDirty") is False
        and producer_result.get("status") == "passed"
        and independent_result.get("status") == "passed"
        and results.get("formalSourceCommit") == source_commit
        and results.get("lineageStatuses") == {
            "producer": "passed",
            "independent": "passed",
            "crosscheck": "passed",
            "formalSourceReady": True,
            "temporaryUnsealedSourceAllowed": False,
        }
        and results.get("verifiedTrackedTreeClean") is True
        and results.get("verifiedPackageSourcesAtBuildCommit") is True
        and tracked_clean() and source_blobs and certificate_blobs
        and isinstance(package_blobs, dict)
        and set(package_blobs) == expected_package_paths
        and all(isinstance(value, str) and FULL_SHA.fullmatch(value)
                for value in package_blobs.values())
    )
    checks.append(gate(
        "source_certificate_and_build_commits",
        commit_gate,
        {
            "sourceCommit": source_commit, "certificateCommit": build_commit,
            "sourceBlobs": source_blobs, "certificateBlobs": certificate_blobs,
            "trackedClean": tracked_clean(),
        },
        "source blobs bind sourceCommit and certificate/package blobs bind clean build commit",
    ))

    ledger = verify_flat_certificate_ledger(
        REPOSITORY / Path(bindings["certificateLedgerPath"]).parent,
        required_files={
            Path(item).name for item in bindings["certificateCommitRoles"].values()
        },
    )
    recorded = results.get("certificateLedgerAudit", {})
    checks.append(gate(
        "flat_certificate_ledger",
        ledger.get("status") == "passed"
        and ledger.get("ledgerSha256")
        == records.get("certificateLedger", {}).get("sha256")
        == recorded.get("ledgerSha256")
        and ledger.get("entryCount") == recorded.get("entryCount")
        and recorded.get("exactDirectoryCoverage") is True
        and recorded.get("uniqueByteSortedRows") is True
        and recorded.get("symlinksRejected") is True,
        {"current": ledger, "recorded": recorded},
        "flat SHA256SUMS exactly, uniquely, and symlink-safely seals certificate bundle",
    ))

    recorded_hashes = results.get("packageSourceHashes", {})
    changed = [
        name for name in PACKAGE_SOURCES
        if recorded_hashes.get(name) != digest(ROOT / name)
    ]
    checks.append(gate(
        "package_source_hashes",
        set(recorded_hashes) == set(PACKAGE_SOURCES) and not changed,
        {"changed": changed, "recorded": sorted(recorded_hashes)},
        "all thirteen package sources retain build hashes",
    ))
    return checks


def mathematical_checks(
    config: dict[str, Any], contract: dict[str, Any],
    results: dict[str, Any], rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    p = config["parameters"]
    mu = (math.sqrt(3.0) - 1.0) / 2.0
    parameter_gate = (
        p["fixedMRequired"] is True
        and float(p["q2Maximum"]) == 0.5
        and float(p["q1Maximum"]) == 0.25
        and float(p["oneTwoCausticFreeRadius"]) == 0.25
        and float(p["oneTwoContractRadius"]) == 0.125
        and float(p["oneTwoWallMaximumRadius"]) == 0.5
        and relerr(float(p["criticalLocalization"]), math.pi / 12.0) < 2.0e-15
        and relerr(float(p["curvatureZone"]), math.pi / 6.0) < 2.0e-15
        and relerr(float(p["curvatureMu"]), mu) < 2.0e-15
        and float(p["shapeC0"]) == 81.0
        and float(p["shapeC1"]) == 36.0
        and float(p["normalizedFShapeC1"]) == 12.0
        and float(p["normalizedFAwayGapLower"]) == 1.0 / 12.0
    )
    checks.append(gate(
        "formal_parameters", parameter_gate, p,
        "formal W contract is (pi/12,81,36), with normalized F away gap greater than 1/12",
    ))

    text = "\n".join([
        (ROOT / "README.md").read_text(encoding="utf-8"),
        (ROOT / "caption.md").read_text(encoding="utf-8"),
        (ROOT / "figure-contract.md").read_text(encoding="utf-8"),
        "\n".join(contract["analyticClaims"]), contract["claimBoundary"],
    ]).lower().replace(chr(96), "")
    terms = [
        "cannot replace the continuous proof", "normalized f away gap",
        "w=e^{-y}f", "c1=36", "fixed", "growing", "fast phase",
        "three-dimensional navier",
    ]
    checks.append(gate(
        "sampling_and_claim_boundary", all(term in text for term in terms), terms,
        "text separates exact samples from proof and retains all scope limits",
    ))

    fields = [
        "panel", "route", "series", "kind", "x", "y", "phi", "theta",
        "radius", "distance", "source", "pointer", "status", "note",
    ]
    expected = {
        "A": int(config["panels"]["A"]["samples"])
        + 2 * int(config["panels"]["A"]["circleSamples"]),
        "B": int(config["panels"]["B"]["samples"]),
        "C": 2 * int(config["panels"]["C"]["samples"]),
    }
    counts = {name: sum(row["panel"] == name for row in rows) for name in "ABC"}
    checks.append(gate(
        "data_schema_and_counts",
        bool(rows) and list(rows[0]) == fields
        and len(rows) >= int(config["validation"]["minimumDataRows"])
        and counts == expected and set(row["panel"] for row in rows) == set("ABC"),
        {"rows": len(rows), "counts": counts, "expected": expected},
        "data table has exact three-panel schema and row counts",
    ))

    tolerance = float(config["validation"]["maximumFormulaResidual"])
    panel_a = [row for row in rows if row["panel"] == "A"]
    a_error: list[float] = []
    a_implicit: list[float] = []
    for row in panel_a:
        x, y, radius = float(row["x"]), float(row["y"]), float(row["radius"])
        if row["series"] == "caustic":
            exact = caustic(float(row["phi"]))
            a_error.extend([abs(x - exact.real), abs(y - exact.imag), abs(radius - abs(exact))])
            a_implicit.append(abs(caustic_residual(complex(x, y))))
        elif row["series"] == "arbitrary-phase safe circle":
            a_error.extend([abs(math.hypot(x, y) - 0.25), abs(radius - 0.25)])
        elif row["series"] == "Q2 contract circle":
            a_error.extend([abs(math.hypot(x, y) - 0.125), abs(radius - 0.125)])
        else:
            a_error.append(math.inf)
    checks.append(gate(
        "panel_a_caustic_and_disks",
        len(panel_a) == expected["A"]
        and max(a_error, default=math.inf) <= tolerance
        and max(a_implicit, default=math.inf) <= tolerance,
        {"maxFormulaError": max(a_error, default=None),
         "maxImplicitResidual": max(a_implicit, default=None)},
        "Panel A is exact caustic plus radii 1/4 and 1/8",
    ))

    panel_b = [row for row in rows if row["panel"] == "B"]
    points = [caustic(float(row["phi"])) for row in panel_b]
    theta = unwrap_phase([math.atan2(value.imag, value.real) for value in points])
    b_error: list[float] = []
    for row, point, angle in zip(panel_b, points, theta, strict=True):
        b_error.extend([
            abs(float(row["x"]) - angle), abs(float(row["theta"]) - angle),
            abs(float(row["y"]) - abs(point)), abs(float(row["radius"]) - abs(point)),
        ])
    radii = [float(row["radius"]) for row in panel_b]
    monotone = all(right < left for left, right in zip(theta, theta[1:]))
    checks.append(gate(
        "panel_b_unique_phase_ray_wall",
        len(panel_b) == expected["B"]
        and max(b_error, default=math.inf) <= tolerance and monotone
        and abs(min(radii, default=math.inf) - 0.25) <= tolerance
        and abs(max(radii, default=-math.inf) - 0.5) <= tolerance
        and abs(theta[0] - math.pi) <= tolerance
        and abs(theta[-1] + math.pi) <= tolerance,
        {"maxFormulaError": max(b_error, default=None), "monotone": monotone,
         "radiusRange": [min(radii, default=None), max(radii, default=None)]},
        "Panel B is exact one-wall radial graph with radius in [1/4,1/2]",
    ))

    panel_c = [row for row in rows if row["panel"] == "C"]
    c_error: list[float] = []
    for row in panel_c:
        distance = float(row["distance"])
        exact = (
            math.cos(distance) - 0.5
            if row["series"] == "normalized curvature lower bound"
            else math.sin(distance) - 0.25
            if row["series"] == "normalized away-gradient lower bound"
            else math.nan
        )
        c_error.extend([abs(float(row["x"]) - distance), abs(float(row["y"]) - exact)])
    checks.append(gate(
        "panel_c_fixed_m_margins",
        len(panel_c) == expected["C"]
        and max(c_error, default=math.inf) <= tolerance
        and relerr(math.cos(math.pi / 6.0) - 0.5, mu) < 2.0e-15
        and math.sin(math.pi / 6.0) - 0.25 > 1.0 / 12.0
        and math.exp(-1.0) / 12.0 > 1.0 / 36.0,
        {"maxFormulaError": max(c_error, default=None), "mu": mu,
         "normalizedAwayAtPiOverSix": math.sin(math.pi / 6.0) - 0.25,
         "formalWAwayLower": math.exp(-1.0) / 12.0},
        "Panel C verifies normalized margins and conservative W C1=36",
    ))

    formula = results.get("formulaChecks", {})
    formula_gate = (
        float(formula.get("maxCausticImplicitResidual", math.inf)) <= tolerance
        and relerr(float(formula.get("minimumWallRadius", math.nan)), 0.25) < 2.0e-15
        and relerr(float(formula.get("maximumWallRadius", math.nan)), 0.5) < 2.0e-15
        and formula.get("phaseParameterStrictlyMonotone") is True
        and relerr(float(formula.get("q2AtContractRadius", math.nan)), 0.5) < 2.0e-15
        and relerr(float(formula.get("curvatureAtZoneBoundary", math.nan)), mu) < 2.0e-15
        and relerr(float(formula.get("expectedCurvatureMu", math.nan)), mu) < 2.0e-15
        and relerr(float(formula.get("normalizedAwayAtZoneBoundary", math.nan)), 0.25) < 2.0e-15
        and formula.get("numericCurvesAreExactFormulaSamples") is True
        and formula.get("continuousProofRequired") is True
        and results.get("numericSamplingDoesNotReplaceContinuousProof") is True
        and results.get("noPdeEvolution") is True
        and results.get("noFiniteFit") is True
        and contract["renderPolicy"]["finiteFit"] == "forbidden"
    )
    checks.append(gate(
        "results_formula_and_no_fit_gate", formula_gate, formula,
        "results ledger records exact formulas and forbids proof by sampling",
    ))
    return checks


def main(*, automatic_only: bool = False) -> int:
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    contract = json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))
    results = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
    rows = rows_from(ROOT / "data.csv")

    checks, dimensions = asset_checks(config)
    checks.extend(lineage_checks(config, results))
    checks.extend(mathematical_checks(config, contract, results, rows))

    publication = config["publication"]
    public_root = REPOSITORY / publication["directory"]
    identity = {
        suffix: (public_root / f"{publication['stem']}.{suffix}").is_file()
        and digest(public_root / f"{publication['stem']}.{suffix}")
        == digest(ROOT / f"figure.{suffix}")
        for suffix in ("pdf", "svg", "png")
    }
    checks.append(gate(
        "public_byte_identity", all(identity.values()), identity,
        "public masters are byte-identical to archival masters",
    ))

    visual = os.environ.get("R072Q_VISUAL_QA_INSPECTED", "").strip().lower() == "true"
    checks.append(gate(
        "visual_inspection_declared", visual, visual,
        "final-size, grayscale, and PDF-raster surfaces were explicitly inspected",
    ))

    automatic = [item for item in checks if item["name"] != "visual_inspection_declared"]
    automatic_passed = all(item["passed"] for item in automatic)
    all_passed = automatic_passed and visual
    run_passed = automatic_passed if automatic_only else all_passed
    payload = {
        "schemaVersion": 1,
        "figureId": "R0.72Q-1",
        "status": (
            "automatic-passed" if automatic_only and automatic_passed
            else "passed" if all_passed else "failed"
        ),
        "allPassed": all_passed,
        "automaticOnly": automatic_only,
        "automaticChecksPassed": automatic_passed,
        "checkCount": len(checks),
        "checks": checks,
    }
    (ROOT / "validation.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    failed = [
        item["name"] for item in checks
        if not item["passed"]
        and not (automatic_only and item["name"] == "visual_inspection_declared")
    ]
    (ROOT / "qa-report.md").write_text(
        "\n".join([
            "# R0.72Q figure QA report", "",
            f"- Automatic validation: {'PASS' if automatic_passed else 'FAIL'} ({len(automatic)} checks).",
            f"- Final print size: {dimensions['pdfMm'][0]:.3f} x {dimensions['pdfMm'][1]:.3f} mm.",
            f"- PNG: {dimensions['pngSize'][0]} x {dimensions['pngSize'][1]} px at 600 dpi.",
            f"- QA: {dimensions['qaExpected'][0]} x {dimensions['qaExpected'][1]} px; grayscale standard deviation {dimensions['grayStd']:.3f}.",
            "- Formula gate: all panels sample exact formulas; samples do not replace continuum proof.",
            "- Shape gate: normalized F away gap >1/12; formal W contract is (pi/12,81,36).",
            "- Boundary: fixed M and Q2<=1/2; no growing-M, fast-phase, or general 3D conclusion.",
            "- Human inspection declared." if visual else "- Human inspection not declared.",
            f"- Failed checks: {', '.join(failed) if failed else 'none'}.", "",
        ]),
        encoding="utf-8",
    )
    print(json.dumps(
        {"status": payload["status"], "checks": len(checks), "failed": failed},
        sort_keys=True,
    ))
    return 0 if run_passed else 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--automatic-only", action="store_true")
    arguments = parser.parse_args()
    raise SystemExit(main(automatic_only=arguments.automatic_only))
