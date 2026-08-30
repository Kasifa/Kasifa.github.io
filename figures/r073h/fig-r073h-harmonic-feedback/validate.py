#!/usr/bin/env python3
"""Fail-closed validator and QA builder for the R0.73H journal figure."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PACKAGE_RELATIVE = "figures/r073h/fig-r073h-harmonic-feedback"
SOURCE_FILES = (
    "README.md",
    "caption.md",
    "command.txt",
    "config.json",
    "contract.json",
    "plot.py",
    "qa-protocol.md",
    "requirements.txt",
    "validate.py",
)
FIGURE_FILES = ("figure.pdf", "figure.svg", "figure.png")
QA_FILES = ("qa-final-size.png", "qa-grayscale.png", "qa-pdf.png")
FINAL_FILES = tuple(sorted(SOURCE_FILES + FIGURE_FILES + QA_FILES + (
    "SHA256SUMS", "manifest.json", "qa-report.md", "results.json", "validation.json",
)))


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def record(path: Path, relative_to: Path = HERE) -> dict[str, Any]:
    return {
        "bytes": path.stat().st_size,
        "path": str(path.relative_to(relative_to)),
        "sha256": sha256(path),
    }


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def atomic_text(path: Path, payload: str) -> None:
    temporary = path.with_name("." + path.name + ".tmp-r073h")
    try:
        temporary.write_text(payload, encoding="utf-8")
        temporary.replace(path)
    finally:
        temporary.unlink(missing_ok=True)


def strict_json(path: Path) -> dict[str, Any]:
    def reject_constant(value: str) -> object:
        raise ValueError("non-finite JSON constant: " + value)

    def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON key: " + key)
            result[key] = value
        return result

    value = json.loads(
        path.read_text(encoding="utf-8"),
        parse_constant=reject_constant,
        object_pairs_hook=unique_object,
    )
    require(isinstance(value, dict), str(path) + " must contain a JSON object")
    return value


def git_bytes(commit: str, relative: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{relative}"], cwd=ROOT)


def require_commit(commit: str, label: str) -> None:
    result = subprocess.run(
        ["git", "cat-file", "-e", commit + "^{commit}"], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    require(result.returncode == 0, label + " is not a Git commit")


def require_ancestor(older: str, newer: str, message: str) -> None:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", older, newer], cwd=ROOT,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    require(result.returncode == 0, message)


def verify_sources(commit: str) -> list[dict[str, Any]]:
    bindings = []
    for name in SOURCE_FILES:
        relative = f"{PACKAGE_RELATIVE}/{name}"
        current = (ROOT / relative).read_bytes()
        historical = git_bytes(commit, relative)
        require(current == historical, "source blob changed after source commit: " + relative)
        bindings.append({
            "bytes": len(current), "path": relative,
            "sha256": sha256_bytes(current), "sourceCommit": commit,
        })
    return bindings


def verify_inputs(config: dict[str, Any], commit: str) -> list[dict[str, Any]]:
    bindings = []
    for relative in config["inputs"].values():
        current = (ROOT / relative).read_bytes()
        historical = git_bytes(commit, relative)
        require(current == historical, "certificate input changed: " + relative)
        bindings.append({
            "bytes": len(current), "path": relative,
            "sha256": sha256_bytes(current), "sourceCommit": commit,
        })
    return bindings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--renderer-source-commit", required=True)
    parser.add_argument("--certificate-commit", required=True)
    parser.add_argument("--qa-status", choices=("passed",), required=True)
    parser.add_argument("--qa-note", required=True)
    args = parser.parse_args()
    if args.deps:
        sys.path.insert(0, args.deps)

    from PIL import Image, ImageChops, ImageStat
    from pypdf import PdfReader
    import matplotlib
    import numpy
    import PIL
    import pypdf

    require(len(args.qa_note.strip()) >= 60, "QA note is too short")
    require_commit(args.renderer_source_commit, "renderer source commit")
    require_commit(args.certificate_commit, "certificate commit")
    require_ancestor(args.certificate_commit, args.renderer_source_commit,
                     "renderer source commit must descend from certificate commit")
    config = strict_json(HERE / "config.json")
    contract = strict_json(HERE / "contract.json")
    require(config["certificateCommit"] == args.certificate_commit,
            "certificate commit does not match config")
    source_bindings = verify_sources(args.renderer_source_commit)
    input_bindings = verify_inputs(config, args.certificate_commit)

    certificate = strict_json(ROOT / config["inputs"]["certificate"])
    certificate_validation = strict_json(ROOT / config["inputs"]["certificateValidation"])
    results = strict_json(HERE / "results.json")
    require(certificate.get("allChecksPass") is True, "certificate failed")
    require(certificate_validation.get("allChecksPass") is True,
            "certificate validation failed")
    require(results.get("rendererSourceCommit") == args.renderer_source_commit,
            "results renderer-source binding mismatch")
    require(results.get("certificateCommit") == args.certificate_commit,
            "results certificate binding mismatch")
    require(results.get("sourceBindings") == source_bindings,
            "results source bindings mismatch")
    require(results.get("inputBindings") == input_bindings,
            "results input bindings mismatch")
    require(results.get("claimBoundary") == contract["claimBoundary"],
            "results claim boundary mismatch")
    require(contract["claimBoundary"] == {
        "clayProblemSolved": False,
        "exactContinuumQ2EnergySubcertificate": True,
        "finiteCubicSignIsContinuumSaturation": False,
        "finiteCutoffAgreementIsTailProof": False,
        "finiteHarmonicResponseIsContinuumSemigroupEstimate": False,
        "formalJournalFigure": True,
        "generalThreeDimensionalRegularityConclusion": False,
        "naturalSeedOrderOneDepartureEstablishedByFigure": False,
        "threeDimensionalVortexStretchingPresent": False,
    }, "claim boundary is not the exact fail-closed ledger")
    require(certificate["claimLedger"]["fullContinuumHarmonicResolvedSemigroupEstimate"]
            == "OPEN", "continuum semigroup estimate must remain open")
    require(certificate["claimLedger"]["finiteCutoffAgreementAsTailProof"]
            == "NOT_CLAIMED", "finite cutoff agreement was promoted")

    for row in results["outputs"]:
        relative = row["path"]
        path = ROOT / relative
        require(path.is_file() and not path.is_symlink(), "missing figure output: " + relative)
        require(row == {
            "bytes": path.stat().st_size,
            "path": relative,
            "sha256": sha256(path),
        }, "figure output binding mismatch: " + relative)

    reader = PdfReader(HERE / "figure.pdf")
    require(len(reader.pages) == 1, "PDF must contain exactly one page")
    page = reader.pages[0]
    pdf_points = [float(page.mediabox.width), float(page.mediabox.height)]
    expected_points = [float(config["widthMillimetres"]) / 25.4 * 72.0,
                       float(config["heightMillimetres"]) / 25.4 * 72.0]
    require(max(abs(a - b) for a, b in zip(pdf_points, expected_points, strict=True)) < 0.1,
            "PDF physical dimensions are wrong")
    pdf_text = "\n".join((item.extract_text() or "") for item in reader.pages)
    for sentinel in ("Exact doubled-row", "Finite response", "Finite compensated",
                     "Finite numerical", "no continuum saturation"):
        require(sentinel in pdf_text, "PDF text sentinel missing: " + sentinel)

    svg_tree = ET.parse(HERE / "figure.svg")
    svg_root = svg_tree.getroot()
    require(svg_root.tag.endswith("svg"), "SVG root is invalid")
    svg_payload = (HERE / "figure.svg").read_text(encoding="utf-8")
    require("<image" not in svg_payload.lower(), "SVG contains a raster image element")
    require("<text" in svg_payload.lower(), "SVG text was converted to paths")
    svg_width = svg_root.attrib.get("width", "")
    require(svg_width.endswith("pt"), "SVG width has an unexpected unit")
    require(abs(float(svg_width[:-2]) / 72.0 * 25.4
                - float(config["widthMillimetres"])) < 0.1,
            "SVG physical width is not 178 mm")

    with Image.open(HERE / "figure.png") as archival:
        archival.load()
        expected_pixels = (
            round(float(config["widthMillimetres"]) / 25.4 * int(config["pngDpi"])),
            round(float(config["heightMillimetres"]) / 25.4 * int(config["pngDpi"])),
        )
        require(max(abs(a - b) for a, b in zip(archival.size, expected_pixels, strict=True)) <= 2,
                "archival PNG dimensions are wrong")
        dpi = archival.info.get("dpi", (0.0, 0.0))
        require(all(abs(float(value) - int(config["pngDpi"])) < 0.1 for value in dpi),
                "archival PNG is not tagged at 600 dpi")
        final_size = archival.convert("RGB").resize(
            (round(float(config["widthMillimetres"]) * int(config["qaDpi"]) / 25.4),
             round(float(config["heightMillimetres"]) * int(config["qaDpi"]) / 25.4)),
            Image.Resampling.LANCZOS,
        )
        final_size.save(HERE / "qa-final-size.png", dpi=(int(config["qaDpi"]),) * 2)
        grayscale = final_size.convert("L")
        grayscale.save(HERE / "qa-grayscale.png", dpi=(int(config["qaDpi"]),) * 2)
        require(ImageStat.Stat(grayscale).extrema[0][0] < 40,
                "grayscale QA lost dark marks")
        require(ImageStat.Stat(grayscale).extrema[0][1] > 245,
                "grayscale QA lost the paper background")

    pdftoppm = shutil.which("pdftoppm")
    require(pdftoppm is not None, "pdftoppm is unavailable")
    pdf_prefix = HERE / ".qa-pdf-r073h"
    subprocess.run(
        [pdftoppm, "-png", "-singlefile", "-r", "180",
         str(HERE / "figure.pdf"), str(pdf_prefix)],
        check=True, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    generated_pdf_png = pdf_prefix.with_suffix(".png")
    require(generated_pdf_png.is_file(), "PDF raster QA was not generated")
    with Image.open(generated_pdf_png) as rendered:
        rendered.load()
        rendered.convert("RGB").save(HERE / "qa-pdf.png", dpi=(180, 180))
    generated_pdf_png.unlink(missing_ok=True)
    with Image.open(HERE / "qa-pdf.png") as rendered, Image.open(HERE / "qa-final-size.png") as direct:
        resized = rendered.convert("RGB").resize(direct.size, Image.Resampling.LANCZOS)
        difference = ImageChops.difference(resized, direct.convert("RGB"))
        pdf_png_mean_absolute_difference = sum(ImageStat.Stat(difference).mean) / (3.0 * 255.0)
        require(pdf_png_mean_absolute_difference < 0.035,
                "PDF and direct PNG differ too much")

    observations = results["observations"]
    require(observations["exact"] == {
        "crossNormUpper": "27/16",
        "h0Lower": "1/20",
        "hdLower": "1/40",
        "lowBlockLower": "1/5",
        "maximumProfileTime": "1/450",
        "tailLower": "95/4",
    }, "exact observations changed")
    finite = observations["finite"]
    require(abs(finite["quadraticNaturalLogSlope"] - 0.9876043065558459) < 2e-13,
            "quadratic slope changed")
    require(abs(finite["targetCubicNaturalLogSlope"] - 1.9532334940260105) < 2e-13,
            "target-cubic slope changed")
    require(abs(finite["holdoutTotalSignedCompensated"] + 0.6597414810027311) < 2e-15,
            "holdout signed coefficient changed")
    require(finite["profileEndpointStrictlyOutsideTheoremWindow"] is True,
            "finite endpoint was not recorded outside the theorem window")
    require(abs(float(finite["profileEndpoint"]) - 0.01) < 1e-15
            and abs(float(finite["theoremWindowUpper"]) - 1.0 / 450.0) < 1e-15,
            "finite/theorem endpoint ledger changed")
    require(finite["independentFormalSentinelCount"] == 4
            and finite["independentHoldoutCount"] == 1,
            "independent inventory is not four formal sentinels plus one holdout")
    require(float(finite["maximumNormalizedGateRatio"]) < 1.0,
            "a displayed numerical check exceeded its gate")

    qa_report = (
        "# R0.73H figure QA report\n\n"
        "Status: **passed**.\n\n"
        f"Inspection note: {args.qa_note.strip()}\n\n"
        "The validator confirmed the one-page 178 mm by 132 mm PDF, editable "
        "SVG text without raster embedding, 600 dpi PNG metadata, immutable "
        "certificate and renderer-source bindings, and normalized finite checks "
        "below their preregistered gates.  This QA certifies presentation and "
        "provenance only.  It does not turn the finite cubic sign into continuum "
        "saturation, cutoff agreement into a tail proof, or the planar launch "
        "into a three-dimensional regularity result.  All displayed response "
        "ratios use the finite diagnostic endpoint d=0.01, strictly outside "
        "the theorem window D<=1/450; they are not values at d=D.  The independent "
        "inventory is four formal sentinels plus one independently recomputed "
        "holdout.\n"
    )
    atomic_text(HERE / "qa-report.md", qa_report)

    pre_manifest_files = tuple(sorted(SOURCE_FILES + FIGURE_FILES + QA_FILES + (
        "qa-report.md", "results.json",
    )))
    manifest = {
        "schemaVersion": "r073h-formal-figure-manifest-v1",
        "status": "formal",
        "release": "R0.73H",
        "figureId": config["figureId"],
        "createdAt": config["createdAt"],
        "analyticalQuestion": contract["analyticalQuestion"],
        "supportedTakeaway": contract["supportedTakeaway"],
        "claimBoundary": contract["claimBoundary"],
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "certificateCommit": args.certificate_commit,
            "rendererSourceCommit": args.renderer_source_commit,
            "certificateCommitIsAncestorOfRendererSourceCommit": True,
            "outputCommitSelfReferenceIntentionallyAbsent": True,
        },
        "evidence": {
            "exactPanel": "exact rational finite block plus analytic tail/cross/Schur/time-perturbation continuum subcertificate",
            "finitePanels": "binary64 finite Fourier diagnostics only",
            "certificateStatus": "passed",
            "independentCertificateValidationStatus": "passed",
        },
        "inputs": input_bindings,
        "sourceBindings": source_bindings,
        "figure": {
            "profile": "journal-double-column",
            "layout": "four-panel exact-subcertificate and finite-diagnostic comparison",
            "widthMillimetres": config["widthMillimetres"],
            "heightMillimetres": config["heightMillimetres"],
            "pngDpi": config["pngDpi"],
            "outputs": [record(HERE / name) for name in FIGURE_FILES],
        },
        "qa": {
            "status": args.qa_status,
            "note": args.qa_note.strip(),
            "finalSizeDpi": config["qaDpi"],
            "pdfRasterDpi": 180,
            "pdfPngMeanAbsoluteDifference": pdf_png_mean_absolute_difference,
            "artifacts": [record(HERE / name) for name in QA_FILES],
        },
        "observations": observations,
        "environment": {
            "python": sys.version.split()[0],
            "matplotlib": matplotlib.__version__,
            "numpy": numpy.__version__,
            "pillow": PIL.__version__,
            "pypdf": pypdf.__version__,
            "rendererProcesses": 1,
            "rendererThreads": 1,
            "gpu": "not used",
        },
        "caption": {"english": "caption.md"},
        "contract": record(HERE / "contract.json"),
        "results": record(HERE / "results.json"),
        "files": [record(HERE / name) for name in pre_manifest_files],
        "inventoryPolicy": {
            "flatPackage": True,
            "manifestFilesExclude": ["manifest.json", "validation.json", "SHA256SUMS"],
            "expectedFinalFileCount": len(FINAL_FILES),
            "cacheDirectoriesForbidden": True,
        },
    }
    atomic_text(HERE / "manifest.json", canonical(manifest))

    checks = {
        "certificateAndIndependentValidationPassed": True,
        "certificateInputsMatchImmutableCommit": True,
        "claimBoundaryExactAndFailClosed": True,
        "continuumSemigroupEstimateRemainsOpen": True,
        "exactContinuumSubcertificateSentinelsMatch": True,
        "figureOutputBindingsMatch": True,
        "finiteCubicSignNotPromotedToContinuumSaturation": True,
        "finiteObservedValuesRecomputed": True,
        "allNormalizedFiniteChecksBelowOne": True,
        "finiteEndpointStrictlyOutsideTheoremWindow": True,
        "independentInventoryFourFormalPlusOneHoldout": True,
        "onePagePdf": True,
        "pdfPhysicalDimensions": True,
        "pdfTextSentinels": True,
        "png600Dpi": True,
        "rendererSourcesMatchSourceBeforeRunCommit": True,
        "svgEditableVectorTextWithoutRaster": True,
        "visualQaAttested": True,
        "visualQaArtifactsCreated": True,
        "pdfAndDirectPngAgree": True,
    }
    validation = {
        "schemaVersion": "r073h-figure-validation-v1",
        "status": "passed",
        "allChecksPass": all(value is True for value in checks.values()),
        "checks": checks,
        "claimBoundary": contract["claimBoundary"],
        "provenance": {
            "certificateCommit": args.certificate_commit,
            "rendererSourceCommit": args.renderer_source_commit,
            "sourceFileCount": len(SOURCE_FILES),
            "inputFileCount": len(input_bindings),
        },
        "pdfPoints": pdf_points,
        "pngPixels": list(Image.open(HERE / "figure.png").size),
        "qaFinalSizePixels": list(Image.open(HERE / "qa-final-size.png").size),
        "pdfPngMeanAbsoluteDifference": pdf_png_mean_absolute_difference,
        "manifestBinding": record(HERE / "manifest.json"),
        "keyMetrics": observations,
    }
    require(validation["allChecksPass"] is True, "validation ledger contains a failure")
    atomic_text(HERE / "validation.json", canonical(validation))

    ledger_names = tuple(name for name in FINAL_FILES if name != "SHA256SUMS")
    require(all((HERE / name).is_file() and not (HERE / name).is_symlink()
                for name in ledger_names), "final package contains a missing or symlinked file")
    ledger = "".join(f"{sha256(HERE / name)}  {name}\n" for name in ledger_names)
    atomic_text(HERE / "SHA256SUMS", ledger)
    for line, name in zip((HERE / "SHA256SUMS").read_text().splitlines(),
                          ledger_names, strict=True):
        expected_hash, expected_name = line.split("  ", 1)
        require(expected_name == name and expected_hash == sha256(HERE / name),
                "SHA-256 ledger mismatch: " + name)
    current_names = tuple(sorted(path.name for path in HERE.iterdir()))
    require(current_names == FINAL_FILES, "final figure-package inventory mismatch")
    print(canonical(validation), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
