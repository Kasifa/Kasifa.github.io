#!/usr/bin/env python3
"""Validate and seal the R0.74K formal figure package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
CERTIFICATE = REPO / "research/r074k_single_collar_exponent_certificate.json"
PRODUCER = REPO / "scripts/r074k_single_collar_exponent_certificate.py"
BUNDLE = Path("/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies")
PDFINFO = BUNDLE / "bin/override/pdfinfo"

EXPECTED_FILES = {
    "README.md", "SHA256SUMS", "caption.md", "chart-contract-and-source-data.md",
    "command.txt", "config.json", "contract.json", "environment.json",
    "figure.pdf", "figure.png", "figure.svg", "layout-bounds.json",
    "manifest.json", "plot.py", "progress.ndjson", "qa-final-size.png",
    "qa-grayscale.png", "qa-pdf.png", "qa-protocol.md", "qa-report.md",
    "requirements.txt", "results.json", "source-data.csv", "validate.py",
    "validation.json",
}
TEXT_NAMES = {
    name for name in EXPECTED_FILES
    if Path(name).suffix in {".md", ".txt", ".json", ".csv", ".py", ".ndjson"}
} | {"SHA256SUMS"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_text(path: Path, content: str) -> None:
    path.write_text(content.replace("\r\n", "\n").rstrip("\n") + "\n", encoding="utf-8")


def base_checks() -> list[dict]:
    checks: list[dict] = []

    def add(check_id: str, passed: bool, note: str) -> None:
        checks.append({"id": check_id, "pass": bool(passed), "note": note})

    regenerated = subprocess.run([sys.executable, str(PRODUCER)], check=True, capture_output=True).stdout
    add("certificate_byte_identity", regenerated == CERTIFICATE.read_bytes(), "producer stdout equals frozen JSON")
    cert = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    add("certificate_41_of_41", cert.get("summary") == {"passed": 41, "total": 41}, "exact finite rows")
    add("certificate_result", cert.get("result") == "PASS", "finite certificate status")
    add("free_tail_status_boundary", cert.get("status_flags", {}).get("nearest_free_tail") == "FAIL_FREE_TAIL_AS_PROOF_MECHANISM", "failure is method-only")
    add("analytic_open_boundary", cert.get("status_flags", {}).get("conditional_collar_hypothesis") == "OPEN", "missing lemma remains open")
    add("not_clay_boundary", cert.get("status_flags", {}).get("clay_problem") == "NOT_CLAIMED", "claim boundary")

    current = {p.name for p in HERE.iterdir() if p.is_file()}
    add("inventory_subset", current <= EXPECTED_FILES, "no unexpected files")
    add("required_render_files", {"figure.pdf", "figure.png", "figure.svg", "source-data.csv"} <= current, "masters and source data exist")

    rows = list(csv.DictReader((HERE / "source-data.csv").open(encoding="utf-8")))
    add("source_data_row_count", len(rows) == 7, "six shell rows plus positive-volume row")
    add("source_data_adverse_row", rows[-1]["status"] == "FREE_TAIL_PROOF_FAILS", "method boundary visible")
    add("source_data_no_simulation", all("sample" not in str(row).lower() for row in rows), "exact table only")

    png = Image.open(HERE / "figure.png")
    add("png_mode_rgb", png.mode == "RGB", "publication raster is RGB")
    add("png_600dpi_dimensions", png.size == (4205, 2174), f"actual={png.size}")
    add("png_dpi_metadata", all(abs(x - 600) < 1 for x in png.info.get("dpi", (0, 0))), f"actual={png.info.get('dpi')}")
    add("final_size_dimensions", Image.open(HERE / "qa-final-size.png").size == (1402, 724), "final-size QA surface")
    add("grayscale_mode", Image.open(HERE / "qa-grayscale.png").mode == "L", "grayscale QA surface")
    add("pdf_qa_exists", (HERE / "qa-pdf.png").stat().st_size > 10000, "independent PDF raster")

    pdfinfo = subprocess.run([str(PDFINFO), str(HERE / "figure.pdf")], check=True, capture_output=True, text=True).stdout
    add("pdf_one_page", "Pages:           1" in pdfinfo, "single-page vector PDF")
    add("pdf_page_size", "504.567 x 260.787 pts" in pdfinfo or "504.57 x 260.79 pts" in pdfinfo, "178mm x 92mm page")

    svg = (HERE / "figure.svg").read_text(encoding="utf-8")
    add("svg_vector", "<svg" in svg and "<path" in svg, "vector SVG")
    add("svg_panel_title", "inward-shell exponent ledger" in svg, "panel A title embedded")
    add("svg_open_label", "OPEN" in svg and "NOT CLAY" in svg, "claim boundary embedded")

    results = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
    add("results_certificate", results.get("certificate") == "PASS_41_OF_41", "results bound to exact certificate")
    add("results_conditional_open", results.get("conditional_hypothesis") == "OPEN", "open status retained")
    add("results_not_simulation", results.get("simulation") is False, "diagram is not simulation")

    for name in sorted(TEXT_NAMES - {"SHA256SUMS", "manifest.json", "validation.json"}):
        path = HERE / name
        if not path.exists():
            add(f"text_exists_{name}", False, "missing text artifact")
            continue
        payload = path.read_bytes()
        add(f"utf8_lf_{name}", not payload.startswith(b"\xef\xbb\xbf") and b"\r" not in payload and payload.endswith(b"\n") and not payload.endswith(b"\n\n"), "UTF-8/LF/single-EOF policy")

    return checks


def seal(validation: dict) -> None:
    write_text(HERE / "validation.json", json.dumps(validation, indent=2, sort_keys=True))
    manifest_entries = []
    for path in sorted(HERE.iterdir(), key=lambda p: p.name):
        if path.is_file() and path.name not in {"manifest.json", "SHA256SUMS"}:
            manifest_entries.append({"path": path.name, "sha256": sha256(path), "bytes": path.stat().st_size})
    manifest = {
        "schema": "r074k-formal-figure-manifest-v1",
        "figure_id": "fig-r074k-single-inward-collar",
        "entries": manifest_entries,
        "validation": validation["status"],
        "simulation": False,
        "claim_boundary": "OPEN_TRUE_PACKET_LEMMA_NOT_CLAY",
    }
    write_text(HERE / "manifest.json", json.dumps(manifest, indent=2, sort_keys=True))
    rows = []
    for path in sorted(HERE.iterdir(), key=lambda p: p.name):
        if path.is_file() and path.name != "SHA256SUMS":
            rows.append(f"{sha256(path)}  {path.name}")
    write_text(HERE / "SHA256SUMS", "\n".join(rows))


def verify_seals() -> tuple[bool, list[str]]:
    errors = []
    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    for item in manifest["entries"]:
        path = HERE / item["path"]
        if not path.exists() or sha256(path) != item["sha256"] or path.stat().st_size != item["bytes"]:
            errors.append(f"manifest:{item['path']}")
    for line in (HERE / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        if sha256(HERE / name) != digest:
            errors.append(f"sha:{name}")
    return not errors, errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()

    checks = base_checks()
    passed = sum(item["pass"] for item in checks)
    manual_report = (HERE / "qa-report.md").read_text(encoding="utf-8")
    manual_pass = "Manual status: PASS" in manual_report
    manual_state = "PASS" if manual_pass else "PENDING"
    validation = {
        "schema": "r074k-formal-figure-validation-v1",
        "status": "PASS" if passed == len(checks) and manual_pass else "FAIL",
        "checks": checks,
        "summary": {"passed": passed, "total": len(checks)},
        "manual_qa": {
            "source": "qa-report.md",
            "color": manual_state,
            "grayscale": manual_state,
            "final_size": manual_state,
            "pdf_raster": manual_state,
            "claim_boundary": manual_state,
        },
    }
    if args.verify_only:
        stored = json.loads((HERE / "validation.json").read_text(encoding="utf-8"))
        seals_ok, errors = verify_seals()
        ok = validation == stored and seals_ok and validation["status"] == "PASS"
        if not ok:
            raise SystemExit("verify-only FAIL: " + "; ".join(errors or ["validation drift"]))
        print(f"verify-only PASS {passed}/{len(checks)}; {len(EXPECTED_FILES)} files; seals PASS")
        return

    if validation["status"] != "PASS":
        failed = [item["id"] for item in checks if not item["pass"]]
        if not manual_pass:
            failed.append("manual_qa_gate")
        raise SystemExit("validation FAIL: " + ", ".join(failed))
    seal(validation)
    print(f"R074K_FIGURE_VALIDATION=PASS_{passed}_OF_{len(checks)}")
    print(f"R074K_FIGURE_FILES={len(EXPECTED_FILES)}")


if __name__ == "__main__":
    main()
