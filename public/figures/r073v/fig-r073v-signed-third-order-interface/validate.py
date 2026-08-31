#!/usr/bin/env python3
"""Fail-closed validation and artifact seal for the R0.73V formal figure."""

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
import xml.etree.ElementTree as ET


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

from plot import (  # type: ignore  # noqa: E402
    CSV_FIELDS, certificate_pair, generate_rows, load_json as plot_load_json,
)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FIGURE_ID = "fig-r073v-signed-third-order-interface"
CERTIFICATE_SOURCE_COMMIT = "7c445c522a241bdc8b867b6fce0f0fed9b82e97d"
CERTIFICATE_PACKAGE_COMMIT = "b34d91ea96c257b943f11d134e8024138e5f3cb0"
REPOSITORY_URL = "https://github.com/Kasifa/Kasifa.github.io.git"
PRIMARY_RELATIVE = "research/certificates/r073v/results.json"
INDEPENDENT_RELATIVE = "research/certificates/r073v/independent-results.json"
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
    parser.add_argument("--confirm-visual-qa", action="store_true")
    parser.add_argument("--figure-source-commit", default="")
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


def record(path: Path, schema: str | None = None, relative: str | None = None) -> dict[str, object]:
    result: dict[str, object] = {
        "bytes": path.stat().st_size,
        "path": relative if relative is not None else path.name,
        "sha256": sha256(path),
    }
    if schema is not None:
        result["schema"] = schema
    return result


def add(checks: list[dict[str, object]], check_id: str, passed: bool, **details: object) -> None:
    checks.append({"id": check_id, "pass": bool(passed), **details})
    require(bool(passed), "check failed: " + check_id)


def git_blob(commit: str, relative: str) -> bytes:
    completed = subprocess.run(
        ["git", "cat-file", "blob", f"{commit}:{relative}"], cwd=ROOT,
        capture_output=True, check=False,
    )
    require(completed.returncode == 0, "git blob absent: " + relative)
    return completed.stdout


def certificate_bindings(contract: dict[str, Any]) -> list[dict[str, object]]:
    cert = contract["certificate"]
    require(cert["sourceCommit"] == CERTIFICATE_SOURCE_COMMIT, "certificate source commit drift")
    require(cert["packageCommit"] == CERTIFICATE_PACKAGE_COMMIT, "certificate package commit drift")
    bindings = []
    for relative, expected in (
        (PRIMARY_RELATIVE, cert["primarySha256"]),
        (INDEPENDENT_RELATIVE, cert["independentSha256"]),
    ):
        path = ROOT / relative
        payload = path.read_bytes()
        require(hashlib.sha256(payload).hexdigest() == expected, "certificate hash drift: " + relative)
        require(git_blob(CERTIFICATE_PACKAGE_COMMIT, relative) == payload,
                "certificate blob drift from package commit: " + relative)
        bindings.append({
            "bytes": len(payload), "path": relative, "sha256": expected,
            "sourceClass": "sealed-two-path-exact-certificate",
        })
    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all", "--",
         "research/certificates/r073v"], cwd=ROOT, capture_output=True, check=False,
    )
    require(status.returncode == 0 and not status.stdout, "certificate scope is dirty")
    return bindings


def figure_source_bindings(commit: str | None) -> list[dict[str, object]]:
    if commit is None:
        return []
    require(re.fullmatch(r"[0-9a-f]{40}", commit) is not None,
            "figure source commit must be full lowercase 40-hex")
    completed = subprocess.run(
        ["git", "cat-file", "-e", commit + "^{commit}"], cwd=ROOT,
        capture_output=True, check=False,
    )
    require(completed.returncode == 0, "figure source commit does not resolve")
    bindings = []
    scoped_paths = []
    for name in sorted(SOURCE_FILES | RAW_FILES):
        path = HERE / name
        relative = path.relative_to(ROOT).as_posix()
        payload = path.read_bytes()
        require(git_blob(commit, relative) == payload,
                "figure source blob drift from commit: " + relative)
        bindings.append({
            "bytes": len(payload), "path": relative, "sha256": hashlib.sha256(payload).hexdigest(),
            "sourceClass": "immutable-figure-source-or-raw-artifact",
        })
        scoped_paths.append(relative)
    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all", "--", *scoped_paths],
        cwd=ROOT, capture_output=True, check=False,
    )
    require(status.returncode == 0 and not status.stdout,
            "final figure source/raw scope is dirty")
    require(len(bindings) == 21, "figure source binding inventory drift")
    return bindings


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        return list(reader.fieldnames or []), rows


def read_ndjson(path: Path) -> list[dict[str, Any]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        value = json.loads(line, object_pairs_hook=reject_duplicate_keys)
        require(isinstance(value, dict), "NDJSON row is not an object: " + path.name)
        rows.append(value)
    require(bool(rows), "NDJSON is empty: " + path.name)
    return rows


def find_row(rows: list[dict[str, str]], panel: str, series: str, record_name: str) -> dict[str, str]:
    matches = [row for row in rows if row["panel"] == panel and row["series"] == series
               and row["record"] == record_name]
    require(len(matches) == 1, f"row lookup not unique: {panel}/{series}/{record_name}")
    return matches[0]


def reconstruct_checks(
    visual_confirmed: bool, figure_source_commit: str | None = None,
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    actual_entries = list(HERE.iterdir())
    actual_files = {path.name for path in actual_entries if path.is_file()}
    require(actual_files <= PACKAGE_FILES,
            "unexpected figure files: " + repr(sorted(actual_files - PACKAGE_FILES)))
    require(all(path.is_file() for path in actual_entries), "unexpected figure subdirectory or special entry")
    require((SOURCE_FILES | RAW_FILES) <= actual_files,
            "missing source/raw files: " + repr(sorted((SOURCE_FILES | RAW_FILES) - actual_files)))
    config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    environment = load_json(HERE / "environment.json")
    results = load_json(HERE / "results.json")
    bindings = certificate_bindings(contract)
    figure_bindings = figure_source_bindings(figure_source_commit)
    primary, independent = certificate_pair(contract)
    checks: list[dict[str, object]] = []

    add(checks, "source-inventory", len(SOURCE_FILES) == 10)
    add(checks, "raw-inventory", len(RAW_FILES) == 11)
    add(checks, "package-inventory", len(PACKAGE_FILES) == 25)
    add(checks, "manifest-bound-inventory", len(MANIFEST_BOUND_FILES) == 23)
    add(checks, "regular-source-and-raw-files", all(
        (HERE / name).is_file() and not (HERE / name).is_symlink()
        for name in SOURCE_FILES | RAW_FILES
    ))
    add(checks, "config-schema",
        config.get("schemaVersion") == "r073v-signed-third-order-interface-figure-config-v1")
    add(checks, "contract-schema",
        contract.get("schemaVersion") == "r073v-signed-third-order-interface-figure-contract-v1")
    add(checks, "results-schema",
        results.get("schemaVersion") == "r073v-signed-third-order-interface-figure-results-v1")
    add(checks, "identity-cross-binding",
        config.get("figureId") == FIGURE_ID and contract.get("figureId") == FIGURE_ID
        and contract.get("release") == "R0.73V" and results.get("figureId") == FIGURE_ID)
    add(checks, "certificate-source-commit-pin",
        contract["certificate"].get("sourceCommit") == CERTIFICATE_SOURCE_COMMIT)
    add(checks, "certificate-package-commit-pin",
        contract["certificate"].get("packageCommit") == CERTIFICATE_PACKAGE_COMMIT)
    add(checks, "certificate-binding-count", len(bindings) == 2)
    add(checks, "two-path-common-core-equality", primary["commonCore"] == independent["commonCore"])
    add(checks, "two-path-independent-import-flag",
        independent["independence"].get("importsPrimaryProducer") is False)
    add(checks, "two-path-primary-arithmetic",
        primary.get("arithmetic")
        == "fractions.Fraction Gaussian rationals and finite q-polynomials; no floating point")
    add(checks, "two-path-independent-polynomial-representation",
        independent["independence"].get("polynomialRepresentation") == "trimmed dense coefficient tuples")
    add(checks, "common-core-digest-result",
        results["certificate"].get("commonCoreSha256") == contract["certificate"]["commonCoreSha256"])
    add(checks, "complete-table-digest-result",
        results["certificate"].get("completeTableDigest") == contract["certificate"]["completeTableDigest"])
    add(checks, "two-path-result-flag", results["certificate"].get("commonCoreByteIdentical") is True)

    claim = contract["claimBoundary"]
    add(checks, "claim-exact-certificate", claim.get("exactFiniteCertificate") is True)
    add(checks, "claim-two-path", claim.get("twoIndependentImplementationsAgree") is True)
    add(checks, "claim-coefficientwise-only", claim.get("coefficientwiseNonRecoveryOnly") is True)
    add(checks, "claim-selected-quartic-only", claim.get("quarticStatementSelectedCoefficientOnly") is True)
    add(checks, "claim-curve-not-fit", claim.get("analyticCurveIsRendererSampleNotFit") is True)
    for key in (
        "informationTheoreticMinimalityEstablished", "wholeFieldNonRecoveryEstablished",
        "finiteHierarchyNoGoEstablished", "fourthOrderNonClosureEstablished",
        "pdeClosureEstablished", "navierStokesSimulation",
        "fittedScalingLaw", "singularSolution", "regularityCriterionImproved",
        "globalRegularityEstablished", "clayProblemSolved",
    ):
        add(checks, "claim-false-" + key, claim.get(key) is False)
    add(checks, "results-claim-boundary", results.get("claimBoundary") == claim)
    add(checks, "local-translation-path",
        contract["compute"].get("ordinaryTranslationPath") == "LOCAL_DIRECT_NO_DGX"
        and environment["execution"].get("ordinaryTranslationPath") == "LOCAL_DIRECT_NO_DGX")
    add(checks, "no-dgx",
        contract["compute"].get("dgxUsed") is False and environment["execution"].get("dgxUsed") is False)
    add(checks, "no-gpu",
        contract["compute"].get("gpu") == "not used" and environment["execution"].get("gpu") == "not used")
    add(checks, "no-network", environment["execution"].get("network") == "not used")

    expected_rows = generate_rows(config, contract, primary, independent)
    fields, actual_rows = read_csv(HERE / "source-data.csv")
    add(checks, "csv-fields", fields == list(CSV_FIELDS))
    add(checks, "csv-row-count", len(actual_rows) == 158 and len(expected_rows) == 158)
    add(checks, "csv-exact-reconstruction", actual_rows == expected_rows)
    add(checks, "csv-primary-hash-propagated",
        all(row["primary_sha256"] == contract["certificate"]["primarySha256"] for row in actual_rows))
    add(checks, "csv-independent-hash-propagated",
        all(row["independent_sha256"] == contract["certificate"]["independentSha256"] for row in actual_rows))
    add(checks, "csv-source-paths-present",
        all(row["source_primary_path"] and row["source_independent_path"] for row in actual_rows))
    add(checks, "csv-renderer-sample-count",
        sum(row["series"] == "quarticProfile" for row in actual_rows) == 101)
    sample_rows = [row for row in actual_rows if row["series"] == "quarticProfile"]
    add(checks, "csv-renderer-samples-finite", all(
        math.isfinite(float(row["x"])) and math.isfinite(float(row["y"])) for row in sample_rows
    ))
    add(checks, "csv-renderer-sample-formula", all(
        math.isclose(float(row["y"]), 2 * math.exp(-2 * float(row["x"]))
                     * (1 - math.exp(-2 * float(row["x"]))) ** 2,
                     rel_tol=0.0, abs_tol=2e-16)
        for row in sample_rows
    ))

    core = primary["commonCore"]
    compressed = core["compressedTarget"]
    add(checks, "compressed-ccal-11", compressed["Ccal"][0][0]["coefficients"] == {"5": "2"})
    add(checks, "compressed-resolved-11", compressed["resolved"][0][0]["coefficients"] == {"3": "2"})
    add(checks, "compressed-chi-11", compressed["chi"][0][0]["coefficients"] == {"3": "-2", "5": "2"})
    add(checks, "compressed-chi-12", compressed["chi"][0][1]["coefficients"] == {"3": "1", "5": "-1"})
    add(checks, "compressed-chi-order", compressed["chi"][0][0]["smallS"] == {"order": 1, "leadingCoefficient": "-4"})
    add(checks, "compressed-sign-pair-12",
        compressed["signPairDifference"][0][1]["coefficients"] == {"3": "2", "5": "-2"})
    add(checks, "compressed-csv-formula",
        find_row(actual_rows, "A", "chi", "chi-11")["q_polynomial"] == "(q^3-q^5)*K")

    four = core["fourSiteTarget"]
    expected_four = {
        ("localKappaFlux", 0, 0): ({"3": "4", "5": "-6", "9": "2"}, 2, "24"),
        ("localKappaFlux", 0, 1): ({"3": "-6", "5": "9", "9": "-3"}, 2, "-36"),
        ("localKappaFlux", 1, 1): ({"3": "8", "5": "-12", "9": "4"}, 2, "48"),
        ("pressureDiffusion", 0, 0): ({"3": "4", "5": "-4"}, 1, "8"),
        ("pressureDiffusion", 0, 1): ({"3": "2", "5": "-2"}, 1, "4"),
        ("pressureDiffusion", 1, 1): ({"3": "-8", "5": "8"}, 1, "-16"),
        ("pressureStrainXi", 0, 0): ({"3": "-4", "5": "4"}, 1, "-8"),
        ("pressureStrainXi", 0, 1): ({}, "infinity", "0"),
        ("pressureStrainXi", 1, 1): ({"3": "4", "5": "-4"}, 1, "8"),
    }
    for (series, i, j), (coefficients, order, leading) in expected_four.items():
        entry = four[series][i][j]
        add(checks, f"four-{series}-{i + 1}{j + 1}-coefficients", entry["coefficients"] == coefficients)
        add(checks, f"four-{series}-{i + 1}{j + 1}-order", entry["smallS"]["order"] == order)
        add(checks, f"four-{series}-{i + 1}{j + 1}-leading", entry["smallS"]["leadingCoefficient"] == leading)
    add(checks, "four-combined-pressure-11-zero",
        find_row(actual_rows, "B", "combinedPressure", "combinedPressure-11")["coefficient_map"] == "{}")
    add(checks, "four-combined-pressure-12",
        find_row(actual_rows, "B", "combinedPressure", "combinedPressure-12")["coefficient_map"] == '{"3":"2","5":"-2"}')
    add(checks, "four-combined-pressure-22",
        find_row(actual_rows, "B", "combinedPressure", "combinedPressure-22")["coefficient_map"] == '{"3":"-4","5":"4"}')
    add(checks, "four-order-gap-exact",
        four["localKappaFlux"][0][0]["smallS"]["order"] == 2
        and four["pressureDiffusion"][0][0]["smallS"]["order"] == 1)

    six = core["sixSiteZeroMode"]
    add(checks, "six-contracted-kappa-all-zero",
        all(not six["contractedKappaFlux"][i][j]["coefficients"] for i in range(3) for j in range(3)))
    add(checks, "six-pressure-diffusion-all-zero",
        all(not six["pressureDiffusion"][i][j]["coefficients"] for i in range(3) for j in range(3)))
    add(checks, "six-xi-11", six["pressureStrainXi"][0][0]["coefficients"] == {"0": "-48", "4": "48"})
    add(checks, "six-xi-22", six["pressureStrainXi"][1][1]["coefficients"] == {"0": "48", "4": "-48"})
    add(checks, "six-xi-order", six["pressureStrainXi"][0][0]["smallS"] == {"order": 1, "leadingCoefficient": "-192"})
    add(checks, "six-group-one-zero", all(
        not six["pressureStrainXiByInputNormSquared"]["1"][i][j]["coefficients"]
        for i in range(3) for j in range(3)
    ))
    add(checks, "six-group-two-equals-xi",
        six["pressureStrainXiByInputNormSquared"]["2"] == six["pressureStrainXi"])

    quartic = core["quarticSelected"]
    add(checks, "quartic-index", quartic["index"] == "kappa112")
    add(checks, "quartic-mode", quartic["mode"] == [0, 2, 0])
    add(checks, "quartic-polynomial",
        quartic["coefficient"]["coefficients"] == {"2": "2*i", "4": "-4*i", "6": "2*i"})
    add(checks, "quartic-order",
        quartic["coefficient"]["smallS"] == {"order": 2, "leadingCoefficient": "8*i"})
    add(checks, "quartic-finite-epsilon",
        quartic["finiteEpsilonAtQHalf"]["extractedLinearCoefficient"] == "9/32*i")
    add(checks, "quartic-finite-samples",
        quartic["finiteEpsilonAtQHalf"]["samples"] == {
            "0": "0", "1": "9/32*i", "2": "9/16*i", "3": "27/32*i",
        })
    add(checks, "quartic-dilation-source",
        primary["dilation"]["quarticSelected"] == "2*i*L*q^2*(1-q^2)^2 at mode L*(0,2,0)")
    add(checks, "compressed-dilation-source",
        primary["compressedLift"]["dilationAtSThetaOverLSquaredFrobeniusSignDifference"]
        == "2*sqrt(6)*L*(exp(-3*theta)-exp(-5*theta))")

    add(checks, "result-row-count", results.get("rowCount") == 158)
    add(checks, "result-series-total", results.get("series", {}).get("total") == 158)
    add(checks, "result-exact-four-order", results["exactConstants"].get("fourSiteKappaOrder") == 2)
    add(checks, "result-exact-pressure-order", results["exactConstants"].get("fourSitePressureOrder") == 1)
    add(checks, "result-exact-six-xi",
        results["exactConstants"].get("sixSitePressureStrain") == "(1-q^4)*diag(-48,48,0)")
    add(checks, "result-exact-quartic",
        results["exactConstants"].get("quarticSelected") == "2*i*q^2*(1-q^2)^2")

    add(checks, "figure-width-mm", config.get("widthMillimetres") == 178.0)
    add(checks, "figure-height-mm", config.get("heightMillimetres") == 118.0)
    add(checks, "figure-png-dpi-config", config.get("pngDpi") == 600)
    allowed_palette = {value.lower() for value in config["palette"].values()} | {"#000000", "#ffffff"}
    add(checks, "palette-two-root", config["palette"].get("blue") == "#285f8f"
        and config["palette"].get("gold") == "#a86f00")

    with Image.open(HERE / "figure.png") as image:
        expected_pixels = (
            int(float(config["widthMillimetres"]) / 25.4 * int(config["pngDpi"])),
            int(float(config["heightMillimetres"]) / 25.4 * int(config["pngDpi"])),
        )
        add(checks, "png-pixel-dimensions", image.size == expected_pixels,
            expected=list(expected_pixels), actual=list(image.size))
        dpi = image.info.get("dpi")
        add(checks, "png-dpi-metadata", isinstance(dpi, tuple)
            and all(abs(float(value) - 600.0) < 0.02 for value in dpi))
        add(checks, "png-mode", image.mode in {"RGB", "RGBA"})
        expected_final = image.copy()
        expected_final.thumbnail((int(config["qaMaximumWidthPixels"]), 1400))
        expected_final = expected_final.convert("RGB")
        with Image.open(HERE / "qa-final-size.png") as qa_final:
            add(checks, "qa-final-size-exact",
                ImageChops.difference(expected_final, qa_final.convert("RGB")).getbbox() is None)
        expected_grey = expected_final.convert("L")
        with Image.open(HERE / "qa-grayscale.png") as qa_grey:
            add(checks, "qa-grayscale-exact",
                ImageChops.difference(expected_grey, qa_grey.convert("L")).getbbox() is None)

    reader = PdfReader(str(HERE / "figure.pdf"))
    add(checks, "pdf-page-count", len(reader.pages) == 1)
    box = reader.pages[0].mediabox
    width_mm = float(box.width) * 25.4 / 72.0
    height_mm = float(box.height) * 25.4 / 72.0
    add(checks, "pdf-width-mm", abs(width_mm - 178.0) < 0.03, actual=width_mm)
    add(checks, "pdf-height-mm", abs(height_mm - 118.0) < 0.03, actual=height_mm)
    add(checks, "pdf-title", reader.metadata is not None
        and reader.metadata.get("/Title") == "R0.73V | Pressure-aware signed third-order heat-lift interface")
    document = pdfium.PdfDocument(str(HERE / "figure.pdf"))
    add(checks, "pdfium-page-count", len(document) == 1)
    page = document[0]
    regenerated_pdf = page.render(scale=3.0).to_pil().convert("RGB")
    page.close()
    document.close()
    with Image.open(HERE / "qa-pdf.png") as stored_pdf:
        add(checks, "qa-pdf-raster-exact",
            ImageChops.difference(regenerated_pdf, stored_pdf.convert("RGB")).getbbox() is None)

    svg_text = (HERE / "figure.svg").read_text(encoding="utf-8")
    svg_root = ET.fromstring(svg_text)
    add(checks, "svg-root", svg_root.tag.endswith("svg"))
    add(checks, "svg-width", svg_root.attrib.get("width", "").endswith("pt"))
    add(checks, "svg-height", svg_root.attrib.get("height", "").endswith("pt"))
    view_box = [float(item) for item in svg_root.attrib.get("viewBox", "").split()]
    add(checks, "svg-viewbox", len(view_box) == 4 and view_box[2] > 500 and view_box[3] > 330)
    add(checks, "svg-no-remote-href",
        re.search(r'(?:href|xlink:href)=["\']https?://', svg_text, flags=re.IGNORECASE) is None)
    svg_colours = {match.lower() for match in re.findall(r"#[0-9a-fA-F]{6}", svg_text)}
    add(checks, "svg-declared-palette-only", svg_colours <= allowed_palette,
        colours=sorted(svg_colours))
    add(checks, "svg-panel-labels", all(label in svg_text for label in (
        "Exact pressure-aware interface", "Four-site mode decomposition",
        "Six-site zero-mode witness", "Selected quartic remainder",
    )))
    add(checks, "svg-claim-boundary-text", "NOT CLAY" in svg_text and "coefficientwise" in svg_text)

    for name, expected in EXPECTED_DEPENDENCIES.items():
        add(checks, "dependency-" + name,
            environment["packages"].get(name) == expected and package_version(name) == expected)
    add(checks, "python-version-cross-check",
        environment["execution"].get("python") == platform_python_version())
    add(checks, "execution-processes", environment["execution"].get("processes") == 1)
    add(checks, "execution-threads", environment["execution"].get("threadsPerProcess") == 1)
    add(checks, "execution-memory-positive",
        isinstance(environment["execution"].get("memoryGiB"), (int, float))
        and float(environment["execution"]["memoryGiB"]) > 0)

    progress = read_ndjson(HERE / "progress.ndjson")
    resources = read_ndjson(HERE / "resource-log.ndjson")
    add(checks, "progress-stage-start", progress[0].get("stage") == "start")
    add(checks, "progress-stage-two-path", any(row.get("stage") == "two-path-certificate-validated" for row in progress))
    add(checks, "progress-stage-complete", progress[-1].get("stage") == "complete")
    add(checks, "progress-monotone", all(
        float(progress[i]["elapsedSeconds"]) <= float(progress[i + 1]["elapsedSeconds"])
        for i in range(len(progress) - 1)
    ))
    add(checks, "resource-stage-count", len(resources) == len(progress))
    add(checks, "resource-local-only", all(
        row.get("dgxUsed") is False and row.get("gpu") == "not used"
        and row.get("ordinaryTranslationPath") == "LOCAL_DIRECT_NO_DGX"
        for row in resources
    ))
    add(checks, "visual-qa-confirmed", visual_confirmed is True)
    return checks, bindings, figure_bindings


def platform_python_version() -> str:
    import platform
    return platform.python_version()


def elapsed_seconds() -> float:
    rows = read_ndjson(HERE / "progress.ndjson")
    return max(float(row["elapsedSeconds"]) for row in rows)


def write_qa_report(checks: list[dict[str, object]]) -> None:
    text = f"""# R0.73V formal-figure QA report

**Status:** PASS — EXACT CERTIFICATE / ARTIFACT SEAL

**Checks:** {len(checks)}/{len(checks)}

The primary sparse-polynomial producer and independent dense-polynomial
producer have identical complete `commonCore` objects. Their frozen hashes,
common-core digest, complete-table digest, and immutable certificate commit
bindings passed before source-data reconstruction.

Exact compressed-lift coefficients, all displayed four-site matrices and
small-s orders, six-site zero/nonzero rows, the selected quartic coefficient,
finite-epsilon extraction, and parabolic dilation passed. The plotted profile
was reconstructed pointwise from the exact formula and was not used as a fit.

SVG/PDF/600-dpi PNG integrity, dimensions, declared palette, final-size raster,
grayscale conversion, and independently regenerated PDF raster passed. Visual
inspection confirmed legible panel titles, equations, matrices, direct labels,
curve annotation, and claim-boundary footnotes in color, grayscale, final-size,
and PDF renderings.

The package is coefficientwise and selected-coefficient in scope. It does not
claim whole-field information non-recovery, finite-hierarchy nonclosure,
singularity, global regularity, or a Clay result.

`navierStokesSimulation=false`; `fittedScalingLaw=false`; `dgxUsed=false`;
`ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX`; `NOT CLAY`.
"""
    (HERE / "qa-report.md").write_text(text, encoding="utf-8")


def build_manifest(
    checks: list[dict[str, object]], bindings: list[dict[str, object]],
    figure_bindings: list[dict[str, object]], figure_source_commit: str | None,
) -> dict[str, object]:
    contract = load_json(HERE / "contract.json")
    environment = load_json(HERE / "environment.json")
    created = utc_now()
    return {
        "schemaVersion": "research-figure-manifest-v1",
        "figureSchemaVersion": "r073v-signed-third-order-interface-manifest-v1",
        "figureId": FIGURE_ID,
        "release": "R0.73V",
        "status": "formal",
        "publicationStatus": "staged",
        "analyticalQuestion": contract["analyticalQuestion"],
        "supportedClaim": contract["supportedClaim"],
        "createdAt": created,
        "git": {
            "certificateCommit": CERTIFICATE_PACKAGE_COMMIT,
            "certificateSourceCommit": CERTIFICATE_SOURCE_COMMIT,
            "dirtyAtCertifiedRun": False,
            "dirtyScope": ([item["path"] for item in figure_bindings]
                           if figure_source_commit else [PRIMARY_RELATIVE, INDEPENDENT_RELATIVE]),
            "figureSourceCommit": figure_source_commit,
            "repository": REPOSITORY_URL,
            "sourceCommit": figure_source_commit or CERTIFICATE_SOURCE_COMMIT,
            "sourceCommitMeaning": (
                "immutable commit containing byte-identical figure source and raw artifacts"
                if figure_source_commit else
                "immutable exact-certificate source commit; figure-source commit is assigned by the release transaction"
            ),
        },
        "seal": {
            "artifactHashBound": True,
            "certificateCommitBound": True,
            "certificateCommonCoreByteIdentical": True,
            "figureSourceBindings": figure_bindings,
            "figureSourceCommit": figure_source_commit,
            "figureSourceCommitAssigned": figure_source_commit is not None,
            "requiresParentFigureSourceCommitFinalReseal": figure_source_commit is None,
            "state": ("formal-figure-source-seal" if figure_source_commit
                      else "formal-artifact-prepublication-seal"),
        },
        "certificate": {
            "bindings": bindings,
            "commonCoreSha256": contract["certificate"]["commonCoreSha256"],
            "completeTableDigest": contract["certificate"]["completeTableDigest"],
            "twoIndependentImplementationsAgree": True,
        },
        "computation": {
            "configuration": "config.json",
            "formalCommand": "python plot.py --render-preseal; python validate.py --confirm-visual-qa; python validate.py --verify-only",
            "kind": "exact-formula-audit",
            "monitoring": {
                "enabled": True,
                "progressLog": "progress.ndjson",
                "resourceLog": "resource-log.ndjson",
            },
            "precision": "exact Gaussian-rational q-polynomials with deterministic analytic renderer samples",
            "scientificWallTimeSeconds": elapsed_seconds(),
            "solver": "closed-form two-path finite Fourier certificate",
        },
        "compute": {
            "cpu": environment["execution"]["cpu"],
            "dgxUsed": False,
            "gpu": "not used",
            "host": environment["execution"]["host"],
            "memoryGiB": environment["execution"]["memoryGiB"],
            "operatingSystem": environment["execution"]["operatingSystem"],
            "processes": 1,
            "threadsPerProcess": 1,
        },
        "environment": {
            "packages": environment["packages"],
            "packagesLock": "requirements.txt",
            "python": environment["execution"]["python"],
        },
        "data": [
            record(HERE / "source-data.csv", "r073v-signed-third-order-interface-source-v1"),
            record(HERE / "results.json", "r073v-signed-third-order-interface-figure-results-v1"),
            record(HERE / "validation.json", "r073v-signed-third-order-interface-validation-v1"),
            record(HERE / "progress.ndjson", "progress-ndjson-v1"),
            record(HERE / "resource-log.ndjson", "resource-log-ndjson-v1"),
        ],
        "sourceData": [
            record(ROOT / PRIMARY_RELATIVE, "r073v-primary-exact-certificate-v1", PRIMARY_RELATIVE),
            record(ROOT / INDEPENDENT_RELATIVE, "r073v-independent-exact-certificate-v1", INDEPENDENT_RELATIVE),
        ],
        "figure": {
            "heightMillimetres": 118.0,
            "outputs": [
                record(HERE / "figure.pdf"),
                record(HERE / "figure.svg"),
                {**record(HERE / "figure.png"), "dpi": 600},
            ],
            "widthMillimetres": 178.0,
        },
        "caption": {"english": "caption.md"},
        "qa": {
            "status": "passed",
            "validationChecks": len(checks),
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "dataCrossChecked": True,
            "qaArtifacts": [
                record(HERE / "qa-pdf.png", "qa-raster-v1"),
                record(HERE / "qa-final-size.png", "qa-raster-v1"),
                record(HERE / "qa-grayscale.png", "qa-raster-v1"),
            ],
        },
        "claimBoundary": contract["claimBoundary"],
        "computePolicy": contract["compute"],
    }


def write_sums() -> None:
    names = sorted(MANIFEST_BOUND_FILES | {"manifest.json"})
    lines = [f"{sha256(HERE / name)}  {name}" for name in names]
    (HERE / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")


def verify_metadata(expected_checks: list[dict[str, object]], figure_source_commit: str | None) -> None:
    validation = load_json(HERE / "validation.json")
    manifest = load_json(HERE / "manifest.json")
    require(validation.get("schemaVersion") == "r073v-signed-third-order-interface-validation-v1",
            "validation schema drift")
    require(validation.get("status") == "PASS", "validation status drift")
    require(validation.get("passed") == len(expected_checks)
            and validation.get("required") == len(expected_checks), "validation count drift")
    require(validation.get("checks") == expected_checks, "validation check reconstruction drift")
    require(manifest.get("schemaVersion") == "research-figure-manifest-v1", "manifest schema drift")
    require(manifest.get("figureSchemaVersion") == "r073v-signed-third-order-interface-manifest-v1",
            "figure manifest schema drift")
    require(manifest.get("figureId") == FIGURE_ID and manifest.get("release") == "R0.73V",
            "manifest identity drift")
    require(manifest.get("status") == "formal" and manifest.get("publicationStatus") == "staged",
            "manifest state drift")
    require(manifest["qa"].get("validationChecks") == len(expected_checks)
            and manifest["qa"].get("status") == "passed", "manifest QA drift")
    require(manifest["seal"].get("figureSourceCommitAssigned") is (figure_source_commit is not None)
            and manifest["seal"].get("requiresParentFigureSourceCommitFinalReseal")
            is (figure_source_commit is None)
            and manifest["seal"].get("figureSourceCommit") == figure_source_commit,
            "figure source seal boundary drift")
    for section in ("data", "sourceData"):
        for item in manifest[section]:
            path = (HERE / item["path"]) if section == "data" else (ROOT / item["path"])
            require(path.is_file() and sha256(path) == item["sha256"],
                    "manifest hash drift: " + str(item["path"]))
    for item in manifest["figure"]["outputs"]:
        path = HERE / item["path"]
        require(path.is_file() and sha256(path) == item["sha256"],
                "manifest figure hash drift: " + str(item["path"]))
    for item in manifest["qa"]["qaArtifacts"]:
        path = HERE / item["path"]
        require(path.is_file() and sha256(path) == item["sha256"],
                "manifest QA hash drift: " + str(item["path"]))
    sums = {}
    for line in (HERE / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        require(name not in sums, "duplicate SHA256SUMS path: " + name)
        sums[name] = digest
    expected_names = MANIFEST_BOUND_FILES | {"manifest.json"}
    require(set(sums) == expected_names, "SHA256SUMS inventory drift")
    for name, digest in sums.items():
        require(sha256(HERE / name) == digest, "SHA256SUMS mismatch: " + name)


def main() -> int:
    args = parse_args()
    if args.verify_only:
        manifest = load_json(HERE / "manifest.json")
        visual_confirmed = manifest.get("qa", {}).get("status") == "passed"
        assigned = manifest.get("seal", {}).get("figureSourceCommitAssigned") is True
        figure_source_commit = manifest.get("seal", {}).get("figureSourceCommit") if assigned else None
        require(figure_source_commit is None or isinstance(figure_source_commit, str),
                "manifest figure source commit type drift")
        checks, _, _ = reconstruct_checks(
            visual_confirmed=visual_confirmed, figure_source_commit=figure_source_commit,
        )
        verify_metadata(checks, figure_source_commit)
        print(canonical({
            "checks": len(checks), "figureId": FIGURE_ID, "mode": "verify-only",
            "status": "PASS",
        }), end="")
        return 0
    require(args.confirm_visual_qa, "write pass requires --confirm-visual-qa")
    figure_source_commit = args.figure_source_commit or None
    checks, bindings, figure_bindings = reconstruct_checks(
        visual_confirmed=True, figure_source_commit=figure_source_commit,
    )
    validation = {
        "schemaVersion": "r073v-signed-third-order-interface-validation-v1",
        "createdUtc": utc_now(),
        "checks": checks,
        "passed": len(checks),
        "required": len(checks),
        "status": "PASS",
        "visualQaConfirmed": True,
    }
    (HERE / "validation.json").write_text(canonical(validation), encoding="utf-8")
    write_qa_report(checks)
    manifest = build_manifest(checks, bindings, figure_bindings, figure_source_commit)
    (HERE / "manifest.json").write_text(canonical(manifest), encoding="utf-8")
    write_sums()
    verify_metadata(checks, figure_source_commit)
    print(canonical({
        "checks": len(checks), "figureId": FIGURE_ID, "mode": "write-seal",
        "publicationStatus": "staged", "status": "PASS",
    }), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
