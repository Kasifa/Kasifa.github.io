#!/usr/bin/env python3
"""Fail-closed validation and source sealing for the R0.73O figure."""

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


def bootstrap() -> None:
    for index, value in enumerate(sys.argv):
        if value == "--deps" and index + 1 < len(sys.argv):
            sys.path.insert(0, str(Path(sys.argv[index + 1]).resolve()))
            return
        if value.startswith("--deps="):
            sys.path.insert(0, str(Path(value.split("=", 1)[1]).resolve()))
            return


bootstrap()
from PIL import Image  # noqa: E402
from pypdf import PdfReader  # noqa: E402


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CERTIFICATE = ROOT / "research/certificates/r073o"
FIGURE_ID = "fig-r073o-kolmogorov-spectrum"
DIAGNOSTIC = CERTIFICATE / "diagnostic.json"
INDEPENDENT = CERTIFICATE / "independent_validation.json"
UPSTREAM_SOURCE = CERTIFICATE / "source-data.csv"
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
    parser.add_argument("--source-commit", default="")
    return parser.parse_args()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


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


def record(path: Path, *, relative_to_root: bool = False) -> dict[str, object]:
    name = str(path.relative_to(ROOT)) if relative_to_root else path.name
    return {"path": name, "bytes": path.stat().st_size, "sha256": sha256(path)}


def close(actual: float, expected: float, tolerance: float) -> bool:
    return math.isclose(actual, expected, rel_tol=tolerance, abs_tol=tolerance)


def verify_inventory(*, complete: bool) -> None:
    optional = {"validation.json", "manifest.json", "SHA256SUMS"}
    required = PACKAGE_FILES if complete else PACKAGE_FILES - optional
    for name in sorted(required):
        path = HERE / name
        require(path.is_file() and not path.is_symlink(), "missing package file: " + name)
    actual = {path.name for path in HERE.iterdir() if path.is_file()}
    require(actual <= PACKAGE_FILES, "unexpected file in figure package")
    if complete:
        require(actual == PACKAGE_FILES, "25-file package inventory drift")
    require(len(SOURCE_FILES) == 10, "source inventory count drift")
    require(len(GENERATED_FILES) == 15, "generated inventory count drift")


def pdf_image_count(reader: PdfReader) -> int:
    count = 0
    for page in reader.pages:
        resources = page.get("/Resources")
        if resources is None:
            continue
        resources = resources.get_object()
        xobjects = resources.get("/XObject")
        if xobjects is None:
            continue
        for value in xobjects.get_object().values():
            obj = value.get_object()
            if obj.get("/Subtype") == "/Image":
                count += 1
    return count


def source_commit_bindings(source_commit: str) -> list[dict[str, object]]:
    require(re.fullmatch(r"[0-9a-f]{40}", source_commit) is not None,
            "source commit must be a full lowercase 40-hex hash")
    check = subprocess.run(
        ["git", "cat-file", "-e", source_commit + "^{commit}"],
        cwd=ROOT, capture_output=True, check=False,
    )
    require(check.returncode == 0, "source commit is not an available commit")
    bindings: list[dict[str, object]] = []
    for name in sorted(SOURCE_FILES):
        path = HERE / name
        relative = path.relative_to(ROOT).as_posix()
        tree = subprocess.run(
            ["git", "ls-tree", source_commit, "--", relative],
            cwd=ROOT, text=True, capture_output=True, check=True,
        ).stdout.strip()
        match = re.fullmatch(r"100(?:644|755) blob ([0-9a-f]+)\t" + re.escape(relative), tree)
        require(match is not None, "source commit lacks figure source: " + relative)
        blob = subprocess.run(
            ["git", "show", source_commit + ":" + relative],
            cwd=ROOT, capture_output=True, check=True,
        ).stdout
        require(hashlib.sha256(blob).hexdigest() == sha256(path),
                "committed source differs from working source: " + relative)
        bindings.append({
            "path": relative,
            "bytes": len(blob),
            "sha256": hashlib.sha256(blob).hexdigest(),
            "gitBlobObjectId": match.group(1),
        })
    return bindings


def collect_facts(source_commit: str) -> tuple[dict[str, bool], dict[str, object]]:
    config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    diagnostic = load_json(DIAGNOSTIC)
    independent = load_json(INDEPENDENT)
    environment = load_json(HERE / "environment.json")
    results = load_json(HERE / "results.json")

    runtime = {name: package_version(name) for name in EXPECTED_DEPENDENCIES}
    boundary = contract.get("claimBoundary", {})
    required_true = {
        "finiteFourierDiagnostic",
        "independentScalingReproduction",
        "criticalIntervalImportedFromComputerAssistedProof",
    }
    required_false = {
        "finiteComputationProvesPositiveInfiniteDimensionalSpectrum",
        "finiteComputationReplacesNagatouCertificate",
        "nonlinearEscapeComputed",
        "essentiallyThreeDimensionalInstability",
        "finiteTimeSingularity",
        "clayProblemSolved",
    }

    with (HERE / "source-data.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    convergence = [row for row in rows if row.get("record_type") == "convergence"]
    sweep = [row for row in rows if row.get("record_type") == "sweep"]

    with Image.open(HERE / "figure.png") as image:
        png_pixels = list(image.size)
        png_dpi = list(image.info.get("dpi", (0.0, 0.0)))
    qa_pixels: dict[str, list[int]] = {}
    for name in ("qa-final-size.png", "qa-grayscale.png", "qa-pdf.png"):
        with Image.open(HERE / name) as image:
            qa_pixels[name] = list(image.size)

    reader = PdfReader(str(HERE / "figure.pdf"))
    require(len(reader.pages) == 1, "figure PDF page-count drift")
    page = reader.pages[0]
    pdf_mm = [
        float(page.mediabox.width) * 25.4 / 72.0,
        float(page.mediabox.height) * 25.4 / 72.0,
    ]
    image_xobjects = pdf_image_count(reader)
    svg = (HERE / "figure.svg").read_text(encoding="utf-8")

    result_outputs = results.get("outputs", [])
    output_hashes_current = all(
        isinstance(item, dict)
        and (HERE / str(item.get("path", ""))).is_file()
        and item.get("sha256") == sha256(HERE / str(item["path"]))
        and item.get("bytes") == (HERE / str(item["path"])).stat().st_size
        for item in result_outputs
    )
    independent_pass = (
        independent.get("status") == "passed"
        and independent.get("allChecksPass") is True
    )
    environment_inputs = environment.get("inputs", [])
    input_paths = {
        item.get("path") for item in environment_inputs if isinstance(item, dict)
    }

    checks = {
        "configSchema": config.get("schemaVersion") ==
            "r073o-kolmogorov-spectrum-figure-config-v1",
        "contractSchema": contract.get("schemaVersion") ==
            "r073o-kolmogorov-spectrum-figure-contract-v1",
        "identity": config.get("figureId") == contract.get("figureId") ==
            results.get("figureId") == FIGURE_ID,
        "release": contract.get("release") == results.get("release") == "R0.73O",
        "dimensionsContract": float(config.get("widthMillimetres")) == 178.0
            and float(config.get("heightMillimetres")) == 82.0,
        "claimBoundaryBound": config.get("claimBoundary") == boundary ==
            results.get("claimBoundary") == diagnostic.get("claimBoundary"),
        "supportedBoundary": all(boundary.get(key) is True for key in required_true),
        "excludedBoundary": all(boundary.get(key) is False for key in required_false),
        "diagnosticPassed": diagnostic.get("status") == "passed"
            and diagnostic.get("allChecksPass") is True,
        "independentFiniteValidationPassed": independent_pass,
        "rigorousThresholdNotRecomputed": diagnostic.get("externalRigorousInput", {}).get(
            "recomputedByThisScript") is False,
        "upstreamSourceHash": sha256(UPSTREAM_SOURCE) ==
            diagnostic.get("sourceData", {}).get("sha256"),
        "copiedSourceHash": sha256(HERE / "source-data.csv") == sha256(UPSTREAM_SOURCE),
        "sourceRows": len(rows) == 131 and len(convergence) == 10 and len(sweep) == 121,
        "finiteTargetValue": close(
            float(diagnostic.get("finiteResults", {}).get("leadingEigenvalueReal", 0.0)),
            3.7327236415731776e-05, 2e-14,
        ),
        "physicalGrowthValue": close(
            float(diagnostic.get("finiteResults", {}).get("physicalGrowthRate", 0.0)),
            0.011242963608418411, 2e-13,
        ),
        "runtimeVersions": runtime == EXPECTED_DEPENDENCIES,
        "environmentRuntime": all(environment.get(name) == value for name, value in {
            "matplotlib": "3.10.6",
            "numpy": "2.5.2",
            "pillow": "12.3.0",
            "pypdfium2": "5.13.0",
        }.items()),
        "environmentBindsIndependent": str(INDEPENDENT.relative_to(ROOT)) in input_paths,
        "resultsOutputHashes": output_hashes_current and len(result_outputs) == 7,
        "pngPixels": png_pixels == [4204, 1937],
        "pngDpi": all(close(float(value), 600.0, 0.02) for value in png_dpi),
        "qaPixels": qa_pixels["qa-final-size.png"] == [2102, 969]
            and qa_pixels["qa-grayscale.png"] == [2102, 969]
            and abs(qa_pixels["qa-pdf.png"][0] - 2102) <= 1
            and qa_pixels["qa-pdf.png"][1] == 969,
        "pdfDimensions": close(pdf_mm[0], 178.0, 0.02)
            and close(pdf_mm[1], 82.0, 0.02),
        "pdfVector": image_xobjects == 0,
        "svgVector": "<image" not in svg.lower(),
        "svgTextPreserved": "<text" in svg.lower(),
    }
    bindings = source_commit_bindings(source_commit) if source_commit else []
    facts: dict[str, object] = {
        "figureId": FIGURE_ID,
        "sourceRows": {
            "total": len(rows),
            "convergence": len(convergence),
            "sweep": len(sweep),
        },
        "finiteResults": diagnostic.get("finiteResults"),
        "pngPixels": png_pixels,
        "pngDpi": png_dpi,
        "qaPixels": qa_pixels,
        "pdfPages": len(reader.pages),
        "pdfMillimetres": pdf_mm,
        "pdfRasterImageXObjects": image_xobjects,
        "svgRasterImages": svg.lower().count("<image"),
        "svgTextPreserved": "<text" in svg.lower(),
        "runtimeVersions": runtime,
        "upstreamInputs": [record(path, relative_to_root=True) for path in (
            DIAGNOSTIC, INDEPENDENT, UPSTREAM_SOURCE
        )],
        "sourceCommitAssigned": bool(source_commit),
        "sourceCommit": source_commit or None,
        "sourceBindings": bindings,
    }
    return checks, facts


def expected_sums() -> str:
    names = sorted(PACKAGE_FILES - {"SHA256SUMS"})
    return "".join(f"{sha256(HERE / name)}  {name}\n" for name in names)


def write_outputs(checks: dict[str, bool], facts: dict[str, object]) -> None:
    failed = [name for name, passed in checks.items() if not passed]
    require(not failed, "figure validation failed: " + ", ".join(failed))
    sealed = bool(facts["sourceCommitAssigned"])
    validation = {
        "schemaVersion": "r073o-kolmogorov-spectrum-figure-validation-v1",
        "createdUtc": utc_now(),
        "status": "passed",
        "allChecksPass": True,
        "visualQaConfirmed": True,
        "checks": checks,
        "facts": facts,
    }
    (HERE / "validation.json").write_text(canonical(validation), encoding="utf-8")

    qa = (
        "# R0.73O figure QA report\n\n"
        + ("Status: **PASS - source sealed**\n\n" if sealed else
           "Status: **PASS - visual and programmatic QA; source seal pending**\n\n")
        + "- The corrected final-size color raster is legible and unclipped.\n"
        + "- The grayscale raster preserves line-style and marker distinctions.\n"
        + "- The independently rasterized PDF agrees with the PNG layout.\n"
        + "- The PDF and SVG contain no raster image objects; SVG text is preserved.\n"
        + "- Panel A separates the finite crossing, critical marker, and target legend.\n"
        + "- Panel B retains the finite value, physical scaling, and residual.\n"
        + "- The finite/illustrative footer and all exclusion claims remain visible.\n\n"
        + "Programmatic facts:\n\n"
        + "```json\n" + canonical({
            "pngPixels": facts["pngPixels"],
            "pngDpi": facts["pngDpi"],
            "qaPixels": facts["qaPixels"],
            "pdfMillimetres": facts["pdfMillimetres"],
            "pdfRasterImageXObjects": facts["pdfRasterImageXObjects"],
            "svgRasterImages": facts["svgRasterImages"],
            "sourceRows": facts["sourceRows"],
            "sourceCommit": facts["sourceCommit"],
        }) + "```\n"
    )
    (HERE / "qa-report.md").write_text(qa, encoding="utf-8")

    manifest_names = sorted(PACKAGE_FILES - {"manifest.json", "SHA256SUMS"})
    manifest = {
        "schemaVersion": "r073o-kolmogorov-spectrum-figure-manifest-v1",
        "createdUtc": utc_now(),
        "status": "sealed" if sealed else "validated-unsealed",
        "allPrerequisiteChecksPass": True,
        "visualQaConfirmed": True,
        "sourceCommitAssigned": sealed,
        "sourceCommit": facts["sourceCommit"],
        "sourceBindings": facts["sourceBindings"],
        "files": [record(HERE / name) for name in manifest_names],
    }
    (HERE / "manifest.json").write_text(canonical(manifest), encoding="utf-8")
    (HERE / "SHA256SUMS").write_text(expected_sums(), encoding="utf-8")


def verify_outputs(checks: dict[str, bool], facts: dict[str, object]) -> None:
    require(all(checks.values()), "live figure checks no longer pass")
    validation = load_json(HERE / "validation.json")
    manifest = load_json(HERE / "manifest.json")
    require(validation.get("status") == "passed"
            and validation.get("allChecksPass") is True
            and validation.get("visualQaConfirmed") is True,
            "validation status drift")
    require(validation.get("checks") == checks and validation.get("facts") == facts,
            "validation payload is stale")
    require(manifest.get("allPrerequisiteChecksPass") is True
            and manifest.get("visualQaConfirmed") is True,
            "manifest status drift")
    manifest_names = sorted(PACKAGE_FILES - {"manifest.json", "SHA256SUMS"})
    require(manifest.get("files") == [record(HERE / name) for name in manifest_names],
            "manifest file binding drift")
    require((HERE / "SHA256SUMS").read_text(encoding="utf-8") == expected_sums(),
            "SHA256SUMS drift")


def main() -> None:
    args = parse_args()
    verify_inventory(complete=args.verify_only)
    checks, facts = collect_facts(args.source_commit)
    if args.verify_only:
        verify_outputs(checks, facts)
    else:
        require(args.confirm_visual_qa, "visual QA must be explicitly confirmed")
        write_outputs(checks, facts)
        verify_inventory(complete=True)
    print(canonical({
        "status": "passed",
        "allChecksPass": True,
        "sourceCommitAssigned": facts["sourceCommitAssigned"],
        "figureId": FIGURE_ID,
    }), end="")


if __name__ == "__main__":
    main()
