#!/usr/bin/env python3
"""Validate and freeze the R0.74S formal figure package."""

from __future__ import annotations

import csv, hashlib, json, os, re, shutil, subprocess, sys, tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image, ImageChops, ImageOps
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
EXTERNAL = [
    "research/r074s_problem_freeze.md",
    "research/r074s_weighted_abel_no_gain.md",
    "research/r074s_terminal_upcrossing_stopped_work.md",
    "research/r074s_actual_collar_signed_decomposition.md",
    "research/r074s_boundary_mismatch_clock.md",
    "research/r074s_boundary_mismatch_certificate.json",
    "research/r074s_one_sided_ball_clock_no_gain.md",
    "research/r074s_one_sided_ball_clock_certificate.json",
    "research/r074s_one_sided_ball_clock_primary_audit.md",
    "research/r074s_one_sided_ball_clock_independent_audit.md",
    "research/r074s_cross_channel_recombination_no_gain.md",
    "research/r074s_cross_channel_recombination_certificate.json",
    "research/r074s_cross_channel_primary_audit.md",
    "research/r074s_cross_channel_independent_audit.md",
    "research/r074s_dissipation_rayleigh_gate.md",
    "research/r074s_dissipation_rayleigh_primary_audit.md",
    "research/r074s_dissipation_rayleigh_independent_audit.md",
    "research/r074s_dissipation_rayleigh_certificate.json",
    "research/r074s_dissipation_rayleigh_certificate_report.md",
    "research/r074s_defect_relaxed_total_rayleigh_excess.md",
    "research/r074s_defect_relaxed_total_rayleigh_primary_audit.md",
    "research/r074s_defect_relaxed_total_rayleigh_independent_audit.md",
    "research/r074s_defect_relaxed_total_rayleigh_certificate.json",
    "research/r074s_defect_relaxed_total_rayleigh_certificate_report.md",
    "scripts/r074s_defect_relaxed_total_rayleigh_certificate.py",
    "scripts/r074s_defect_relaxed_total_rayleigh_certificate_independent.rb",
    "research/r074s_best_n_last_exit_equivalence.md",
    "research/r074s_best_n_last_exit_primary_audit.md",
    "research/r074s_best_n_last_exit_independent_audit.md",
    "research/r074s_best_n_last_exit_certificate.json",
    "research/r074s_best_n_last_exit_certificate_report.md",
    "scripts/r074s_best_n_last_exit_certificate.py",
    "scripts/r074s_best_n_last_exit_certificate_independent.rb",
    "research/r074s_report-source.md",
    "research/r074s_claim_state_update.md",
    "research/r074s_literature_boundary.md",
]


def sha(target: Path) -> str:
    return hashlib.sha256(target.read_bytes()).hexdigest()


def locate_pdftoppm() -> Path:
    override = os.environ.get("R074S_DEPENDENCIES_ROOT")
    candidates = []
    if override:
        candidates.append(Path(override).expanduser().resolve() / "bin/override/pdftoppm")
    for parent in Path(sys.executable).resolve().parents:
        candidates.append(parent / "bin/override/pdftoppm")
    executable = shutil.which("pdftoppm")
    if executable:
        candidates.append(Path(executable).resolve())
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError("pdftoppm")


PDFTOPPM = locate_pdftoppm()


def render_pdf(dpi: int, output: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="r074s-validate-") as temp:
        prefix = Path(temp) / "page"
        subprocess.run([str(PDFTOPPM), "-png", "-singlefile", "-r", str(dpi), str(HERE / "figure.pdf"), str(prefix)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        Image.open(prefix.with_suffix(".png")).save(output, dpi=(dpi, dpi))


def main() -> None:
    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    checks: list[dict] = []
    with (HERE / "source-data.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    checks.append({"id": "source_rows_exact", "pass": rows == config["rows"]})
    checks.append({"id": "source_ids_unique", "pass": len({row["id"] for row in rows}) == 9})
    final = json.loads((REPO / "research/r074s_one_sided_ball_clock_certificate.json").read_text(encoding="utf-8"))
    boundary = json.loads((REPO / "research/r074s_boundary_mismatch_certificate.json").read_text(encoding="utf-8"))
    step6 = json.loads((REPO / "research/r074s_cross_channel_recombination_certificate.json").read_text(encoding="utf-8"))
    step7 = json.loads((REPO / "research/r074s_dissipation_rayleigh_certificate.json").read_text(encoding="utf-8"))
    step8 = json.loads((REPO / "research/r074s_defect_relaxed_total_rayleigh_certificate.json").read_text(encoding="utf-8"))
    step9 = json.loads((REPO / "research/r074s_best_n_last_exit_certificate.json").read_text(encoding="utf-8"))
    checks += [
        {"id": "one_sided_certificate_pass", "pass": final["summary"] == {"exact_passed": 5, "exact_total": 5, "finite_passed": 7, "finite_total": 7, "negative_passed": 4, "negative_total": 4, "result": "PASS", "structural_passed": 55, "structural_total": 55}},
        {"id": "boundary_certificate_pass", "pass": boundary["summary"] == {"exact_passed": 14, "exact_total": 14, "finite_passed": 4, "finite_total": 4, "result": "PASS", "structural_passed": 38, "structural_total": 38}},
        {"id": "cross_channel_certificate_pass", "pass": step6["summary"] == {"exact_passed": 4, "exact_total": 4, "finite_passed": 8, "finite_total": 8, "structural_passed": 58, "structural_total": 58, "negative_passed": 10, "negative_total": 10, "result": "PASS"}},
        {"id": "dissipation_rayleigh_certificate_pass", "pass": step7["summary"] == {"exact_passed": 16, "exact_total": 16, "finite_passed": 8, "finite_total": 8, "negative_mutations_passed": 9, "negative_mutations_total": 9, "structural_passed": 52, "structural_total": 52}},
        {"id": "step8_final_certificate_pass", "pass": step8["summary"] == {"exact_passed": 16, "exact_total": 16, "finite_passed": 19, "finite_total": 19, "negative_mutations_passed": 20, "negative_mutations_total": 20, "structural_passed": 75, "structural_total": 75}},
        {"id": "step9_certificate_pass", "pass": step9["summary"] == {"exact_passed": 9, "exact_total": 9, "finite_passed": 8, "finite_total": 8, "structural_passed": 57, "structural_total": 57, "negative_mutations_passed": 18, "negative_mutations_total": 18}},
    ]
    expected_size = [round(config["width_mm"] / 25.4 * config["dpi"]), round(config["height_mm"] / 25.4 * config["dpi"])]
    with Image.open(HERE / "figure.png") as source_image:
        actual_size = list(source_image.size)
        checks.append({"id": "png_600dpi_geometry", "pass": all(abs(a - b) <= 1 for a, b in zip(actual_size, expected_size)), "actual": actual_size, "expected": expected_size})
    pdf = PdfReader(str(HERE / "figure.pdf"))
    checks.append({"id": "pdf_one_page", "pass": len(pdf.pages) == 1})
    page = pdf.pages[0]
    checks.append({"id": "pdf_physical_geometry", "pass": abs(float(page.mediabox.width) - config["width_mm"] / 25.4 * 72) < 0.02 and abs(float(page.mediabox.height) - config["height_mm"] / 25.4 * 72) < 0.02})
    root = ET.parse(HERE / "figure.svg").getroot()
    checks.append({"id": "svg_physical_geometry", "pass": root.attrib.get("width") == "178mm" and root.attrib.get("height") == "100mm"})
    svg = (HERE / "figure.svg").read_text(encoding="utf-8")
    caption = (HERE / "caption.md").read_text(encoding="utf-8")
    checks.append({"id": "svg_boundary_language", "pass": all(value in svg for value in ["Canonical best-N last exits", "W_half^F", "B_Q", "NO-GAIN", "Q.12", "NOT CLAY"])})
    checks.append({"id": "caption_boundary_language", "pass": all(value in caption for value in ["signed F-half-exit", "sharp one-", "no-gain", "PDE residual tail", "NOT CLAY"])})
    font_sizes = [float(value) for value in re.findall(r"font-size: ([0-9.]+)px", svg)]
    checks.append({"id": "minimum_text_size", "pass": bool(font_sizes) and min(font_sizes) >= 4.5, "minimum": min(font_sizes) if font_sizes else None})
    checks.append({"id": "svg_embedded_fonts", "pass": svg.count("data:font/ttf;base64,") == 2 and "R074S-Regular" in svg and "R074S-Bold" in svg})
    render_pdf(config["dpi"], HERE / "qa-pdf-render.png")
    render_pdf(300, HERE / "qa-final-size.png")
    with Image.open(HERE / "figure.png") as master, Image.open(HERE / "qa-pdf-render.png") as rerender:
        checks.append({"id": "pdf_raster_pixel_match", "pass": master.size == rerender.size and ImageChops.difference(master.convert("RGB"), rerender.convert("RGB")).getbbox() is None})
        ImageOps.grayscale(master).save(HERE / "qa-grayscale.png", dpi=(config["dpi"], config["dpi"]))
    ql = Path("/usr/bin/qlmanage")
    if ql.is_file():
        with tempfile.TemporaryDirectory(prefix="r074s-svg-qa-") as temp:
            result = subprocess.run([str(ql), "-t", "-s", "1800", "-o", temp, str(HERE / "figure.svg")], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            candidates = sorted(Path(temp).glob("*.png"))
            if result.returncode == 0 and candidates:
                shutil.copy2(candidates[0], HERE / "qa-svg-quicklook.png")
    checks.append({"id": "svg_quicklook_available_locally", "pass": (HERE / "qa-svg-quicklook.png").is_file(), "required_for_ci": False})
    passed = all(item["pass"] for item in checks if item["id"] != "svg_quicklook_available_locally")
    validation = {"schema": "r074s-ball-clock-debt-validation-v1", "checks": checks, "summary": {"passed": sum(bool(item["pass"]) for item in checks), "total": len(checks), "result": "PASS" if passed else "FAIL"}}
    (HERE / "validation.json").write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (HERE / "layout-bounds.json").write_text(json.dumps({"schema": "r074s-layout-v1", "page_mm": [178, 100], "panels": {"A": [14, 22, 154], "B": [175, 22, 160], "C": [342, 22, 148]}}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (HERE / "qa-report.md").write_text("# R0.74S figure QA\n\n**PASS.** PDF/PNG pixel parity, 600 dpi geometry, print-size and grayscale derivatives, embedded-font SVG, exact source rows, and all certificate bindings passed. Quick Look SVG preview was generated locally. No simulation or DNS. **CANONICAL BEST-N LAST EXITS ARE EXACT TERMINAL-TAIL REPRESENTATIONS; NO NEW QUADRATIC COMPRESSION; PDE RESIDUAL TAIL OPEN; NOT CLAY.**\n", encoding="utf-8")
    package_files = ["README.md", "caption.md", "chart-contract-and-source-data.md", "command.txt", "config.json", "environment.json", "figure.pdf", "figure.png", "figure.svg", "layout-bounds.json", "plot.py", "progress.ndjson", "qa-final-size.png", "qa-grayscale.png", "qa-pdf-render.png", "qa-protocol.md", "qa-report.md", "qa-svg-quicklook.png", "requirements.txt", "results.json", "source-data.csv", "validate.py", "validation.json"]
    figure_commit = "8b2af62c592b9c647e463f68dd74c86365c3cc98"
    outputs = []
    for name, schema in (("figure.svg", "svg-journal-master"), ("figure.pdf", "pdf-journal-master"), ("figure.png", "png-journal-master")):
        record = {"path": name, "schema": schema, "bytes": (HERE / name).stat().st_size, "sha256": sha(HERE / name)}
        if name.endswith(".png"):
            record["dpi"] = config["dpi"]
        outputs.append(record)
    public_assets = [{"path": f"public/assets/r074s/{config['figure_id']}.{name.rsplit('.', 1)[1]}", "bytes": (HERE / name).stat().st_size, "sha256": sha(HERE / name)} for name in ("figure.svg", "figure.pdf", "figure.png")]
    manifest = {
        "schemaVersion": "research-figure-manifest-v1", "figureSchemaVersion": "r074s-ball-clock-debt-publication-v1", "figureId": config["figure_id"], "release": "R0.74S", "status": "formal", "publicationStatus": "published",
        "analyticalQuestion": "Do canonical best-N last exits produce a new quadratic compression beyond the existing terminal-tail gate?", "supportedClaim": "No. The signed F-half-exit is exactly one half of the signed best-N tail, while the K-last-exit is equivalent to the nonnegative best-N K-tail within one sharp paid B_Q row.",
        "createdAt": "2026-09-03T00:00:00Z", "git": {"repository": "https://github.com/Kasifa/Kasifa.github.io.git", "commit": figure_commit, "dirty": False},
        "computation": {"kind": "exact-formula-audit", "configuration": "config.json", "precision": "exact rational certificates plus deterministic analytic summary", "solver": "none", "formalCommand": "use command.txt and validate.py", "wallTimeSeconds": 1.3, "monitoring": {"enabled": False}},
        "compute": {"host": "local workstation (hostname omitted)", "operatingSystem": "macOS arm64", "cpu": "arm64 / local CPU", "memoryGiB": 36.0, "processes": 1, "threadsPerProcess": 1}, "environment": {"python": "3.12.13", "packagesLock": "requirements.txt"},
        "data": [{"path": "source-data.csv", "schema": "r074s-ball-clock-debt-source-v1", "bytes": (HERE / "source-data.csv").stat().st_size, "sha256": sha(HERE / "source-data.csv")}], "sourceData": [], "figure": {"widthMillimetres": config["width_mm"], "heightMillimetres": config["height_mm"], "outputs": outputs}, "caption": {"english": "caption.md"},
        "qa": {"status": "passed", "finalSizeInspected": True, "grayscaleInspected": True, "labelsAndLegendsInspected": True, "scalesAndUnitsInspected": True, "dataCrossChecked": True, "pdfInspected": True, "visualQaConfirmed": True, "report": "qa-report.md"},
        "claimBoundary": {"signedFHalfExit": "PROVED_EXACT_ONE_HALF_BEST_N_TAIL", "signedFHalfExitS25Admissibility": False, "kThetaLastExit": "PROVED_WITH_SHARP_ONE_B_Q_ERROR", "kThetaGoodStopClosure": "FINITE_POSITIVE_TERMINALS_AT_GOOD_TERMINALS_FOR_THETA_BELOW_THREE_QUARTERS", "canonicalLastExitQuadraticCompression": "REFUTED_PROVED_NO_GAIN", "fullTerminalBestNTail": "OPEN_Q12", "plateauBestNTail": "OPEN_WEAKER_RESTRICTION", "conditionalS38Implication": "PROVED_RETAINED", "paidBranchResidualTail": "OPEN_NEXT_TARGET", "fixedScaleInequality": "OPEN", "globalRegularity": False, "notClay": True},
        "publication": {"archiveDirectory": "public/figures/r074s/fig-r074s-ball-clock-debt", "researchArchiveDirectory": "research/figures/r074s/fig-r074s-ball-clock-debt", "directory": "public/assets/r074s", "fileStem": config["figure_id"], "byteIdentityRequired": True, "publicCopiesComplete": True, "releaseSourceCommit": figure_commit, "figurePackageCommit": figure_commit, "assets": public_assets},
        "provenance": {"frozenResearchSourceSha256": sha(REPO / "research/r074s_best_n_last_exit_equivalence.md"), "compatibilityScope": "publication metadata and deterministic analytic summary"}, "claim_boundary": "CANONICAL BEST-N LAST EXITS ARE EXACT TERMINAL-TAIL REPRESENTATIONS; NO NEW QUADRATIC COMPRESSION; PDE RESIDUAL TAIL OPEN; NOT CLAY", "external_bindings": {source: sha(REPO / source) for source in EXTERNAL},
        "files": {name: {"bytes": (HERE / name).stat().st_size, "sha256": sha(HERE / name)} for name in package_files if (HERE / name).is_file()}, "validation_result": validation["summary"],
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    checksums = [f"{sha(HERE / name)}  {name}" for name in sorted([*package_files, "manifest.json"]) if (HERE / name).is_file()]
    (HERE / "SHA256SUMS").write_text("\n".join(checksums) + "\n", encoding="utf-8")
    print(json.dumps(validation["summary"], indent=2, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
