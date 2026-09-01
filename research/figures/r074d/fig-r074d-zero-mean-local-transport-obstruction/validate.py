#!/usr/bin/env python3
"""Independent structural validator for the R0.74D journal package."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path

from PIL import Image
from pypdf import PdfReader


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SOURCE_COMMIT = "ff80370fe33094f1423d312b817dfec0bf42d664"
SOURCE_NOTE = "research/r074d_zero_mean_local_transport_obstruction.md"
SOURCE_SHA = "bc9f7557e27bb86d5730273985b60f7135ccea3adc2fc99b2daf7778e70c9124"
CERTIFICATE = "research/r074d_zero_mean_transport_certificate.json"
CERTIFICATE_SHA = "69eecc7884a153bc5d4936c7d3dee9d3c736f5db69c20ba59b486165be96dec9"

NAMES = {
    "README.md", "SHA256SUMS", "caption.md", "chart-contract-and-source-data.md",
    "command.txt", "config.json", "contract.json", "environment.json", "figure.pdf",
    "figure.png", "figure.svg", "manifest.json", "plot.py", "progress.ndjson",
    "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png", "qa-protocol.md",
    "qa-report.md", "requirements.txt", "resource-log.ndjson", "results.json",
    "source-data.csv", "validate.py", "validation.json",
}


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def resolve(value):
    return value.get_object() if hasattr(value, "get_object") else value


def embedded_fonts(page) -> tuple[int, bool]:
    resources = resolve(page.get("/Resources", {}))
    fonts = resolve(resources.get("/Font", {}))
    if not fonts:
        return 0, False
    flags = []
    for reference in fonts.values():
        font = resolve(reference)
        descriptor = font.get("/FontDescriptor")
        if descriptor is None and font.get("/DescendantFonts"):
            descendant = resolve(resolve(font["/DescendantFonts"])[0])
            descriptor = descendant.get("/FontDescriptor")
        descriptor = resolve(descriptor) if descriptor is not None else {}
        flags.append(any(key in descriptor for key in
                         ("/FontFile", "/FontFile2", "/FontFile3")))
    return len(flags), all(flags)


def main() -> None:
    checks: dict[str, bool] = {}
    checks["file_count_and_names"] = {
        path.name for path in HERE.iterdir() if path.is_file()
    } == NAMES

    resolved = subprocess.check_output(
        ["git", "-C", str(REPO), "rev-parse", "ff80370f^{commit}"], text=True,
    ).strip()
    checks["commit_resolves"] = resolved == SOURCE_COMMIT
    proof_bytes = subprocess.check_output(
        ["git", "-C", str(REPO), "show", f"{SOURCE_COMMIT}:{SOURCE_NOTE}"],
    )
    checks["proof_blob_hash"] = hashlib.sha256(proof_bytes).hexdigest() == SOURCE_SHA

    certificate_path = REPO / CERTIFICATE
    checks["certificate_hash"] = sha(certificate_path) == CERTIFICATE_SHA
    certificate = json.loads(certificate_path.read_text(encoding="utf-8"))
    checks["certificate_111_of_111"] = (
        certificate.get("schema_version") == 1
        and certificate.get("status") == "PASS"
        and certificate.get("summary") == {"passed": 111, "total": 111}
    )

    png = Image.open(HERE / "figure.png")
    checks["png_600dpi_size"] = png.size[0] >= 4250 and png.size[1] >= 1936
    checks["png_rgb_or_rgba"] = png.mode in {"RGB", "RGBA"}

    reader = PdfReader(str(HERE / "figure.pdf"))
    checks["pdf_one_page"] = len(reader.pages) == 1
    page = reader.pages[0]
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)
    checks["pdf_180x82mm"] = (
        abs(width - 180 / 25.4 * 72) < 1
        and abs(height - 82 / 25.4 * 72) < 1
    )
    font_count, all_embedded = embedded_fonts(page)
    checks["pdf_fonts_embedded"] = font_count >= 1 and all_embedded

    svg = (HERE / "figure.svg").read_text(encoding="utf-8")
    required = [
        "EXACT NSE", "PROVED", "OPEN", "PRIOR ART", "NOT CLAY", "NO DNS",
        "ZERO GLOBAL MEAN", "d(t,x₃)=B e⁻ᵗ(1−cos x₃) ≤ 0",
        "E[|D| Kᵖᵉʳ(R²;Xₜ)] ≤ C R", "z&lt;0  ⇒  |z+D| ≥ |z|",
        "1/264 − 1/288 = 1/3168 &gt; 0", "X_R / P_R²ᐟ³",
        "local/mollified frame", "explicit entrance-flux payment",
        "No priority claim",
    ]
    for token in required:
        checks["svg_phrase_" + token] = token in svg
    checks["svg_no_raster_image"] = "<image" not in svg
    checks["svg_has_live_text"] = svg.count("<text") >= 45
    base_sizes = [float(value) for value in
                  re.findall(r"font-size: ([0-9.]+)px", svg)]
    checks["svg_minimum_font_6pt"] = bool(base_sizes) and min(base_sizes) >= 6.0

    rows = list(csv.DictReader((HERE / "source-data.csv").open(encoding="utf-8")))
    checks["source_rows_24"] = len(rows) == 24
    checks["source_panels_complete"] = {
        row["panel"] for row in rows
    } == {"A", "B", "C"}
    checks["three_ratio_rows"] = {
        row["record"] for row in rows
        if row["panel"] == "C" and row["category"] == "ratio"
    } == {"background", "local leakage", "exterior residence"}
    checks["two_open_repair_rows"] = {
        row["record"] for row in rows
        if row["panel"] == "C" and row["status"] == "open"
    } == {"local or mollified frame", "explicit entrance flux"}
    checks["prior_art_no_priority_row"] = any(
        row["panel"] == "C"
        and row["status"] == "prior art"
        and "no priority claim" in row["boundary_note"]
        for row in rows
    )
    checks["nonautonomous_order_row"] = any(
        row["panel"] == "B"
        and row["record"] == "accumulated displacement"
        and "t-s" in row["boundary_note"]
        for row in rows
    )
    checks["all_periodic_copies_row"] = any(
        row["panel"] == "B"
        and row["record"] == "periodic lift"
        and "all periodic copies" in row["expression"]
        for row in rows
    )

    contract = json.loads((HERE / "contract.json").read_text(encoding="utf-8"))
    checks["contract_bound"] = (
        contract["sourceCommit"] == SOURCE_COMMIT
        and contract["sourceNoteSha256"] == SOURCE_SHA
        and contract["certificate"]["sha256"] == CERTIFICATE_SHA
        and contract["certificate"]["checks"] == "111/111"
        and contract["expectedFileCount"] == 25
    )
    checks["contract_statuses_complete"] = set(contract["statuses"]) == {
        "PROVED", "EXACT NSE", "OPEN", "PRIOR ART", "NOT CLAY", "NO DNS"
    }
    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    checks["no_dns_contract"] = config["dns"] is False
    checks["no_simulation_contract"] = config["simulation"] is False
    checks["unknown_constants_not_encoded"] = (
        config["unknownConstantsNumericallyEncoded"] is False
    )

    passed = sum(checks.values())
    total = len(checks)
    status = "PASS" if passed == total else "FAIL"
    validation = {
        "certificateSha256": CERTIFICATE_SHA,
        "checks": checks,
        "sourceCommit": SOURCE_COMMIT,
        "sourceNoteSha256": SOURCE_SHA,
        "status": status,
        "summary": {"passed": passed, "total": total},
    }
    (HERE / "validation.json").write_text(
        json.dumps(validation, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (HERE / "qa-report.md").write_text(
        "# QA report\n\n"
        f"**Status:** {status}\n\n"
        f"Independent structural validation: {passed}/{total}. The release command runs generation and validation twice, compares all 25 files byte-for-byte, checks all 20 text files for whitespace defects, and verifies every `SHA256SUMS` entry. Visual/structural QA covers the 180 x 82 mm page, approximately 600 dpi master raster, embedded PDF fonts, live SVG text with no raster image, a 6 pt minimum base label size, grayscale/final-size derivatives, the signed nonautonomous mechanism, seam and all-copy statements, the three distinct ratio rows, and explicit EXACT NSE, PROVED, OPEN, PRIOR ART, NO DNS, and NOT CLAY boundaries. This is a deterministic analytic proof schematic, not interactive browser QA, DNS, or simulation.\n",
        encoding="utf-8",
    )
    (HERE / "results.json").write_text(
        json.dumps({
            "certificateSha256": CERTIFICATE_SHA,
            "checkCount": total,
            "sourceCommit": SOURCE_COMMIT,
            "sourceNoteSha256": SOURCE_SHA,
            "status": status,
        }, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    bound = sorted(name for name in NAMES if name not in {"SHA256SUMS", "manifest.json"})
    manifest = {
        "certificateSha256": CERTIFICATE_SHA,
        "figureId": "fig-r074d-zero-mean-local-transport-obstruction",
        "files": [{"bytes": (HERE / name).stat().st_size, "path": name,
                   "sha256": sha(HERE / name)} for name in bound],
        "sourceCommit": SOURCE_COMMIT,
        "sourceNoteSha256": SOURCE_SHA,
        "status": status,
    }
    (HERE / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8",
    )
    sums = sorted(name for name in NAMES if name != "SHA256SUMS")
    (HERE / "SHA256SUMS").write_text(
        "".join(f"{sha(HERE / name)}  {name}\n" for name in sums),
        encoding="utf-8",
    )

    if status != "PASS":
        failed = [key for key, value in checks.items() if not value]
        raise SystemExit("validation failed: " + str(failed))
    print(f"PASS {passed}/{total}; 25 files")


if __name__ == "__main__":
    main()
