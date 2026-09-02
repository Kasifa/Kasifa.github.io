#!/usr/bin/env python3
"""Fail-closed validation and sealing for the R0.74N formal figure package."""

from __future__ import annotations

import base64
import csv
import hashlib
import json
import re
import subprocess
from fractions import Fraction
from pathlib import Path

from PIL import Image
from pypdf import PdfReader


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
BUNDLE = Path("/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies")
PYTHON = BUNDLE / "python/bin/python3"
RUBY = Path("/usr/bin/ruby")
CLAIM = "FAMILYWISE_ALL_SHELL_SYNTHESIS_NOT_CLAY"
FIGURE_ID = "fig-r074n-all-shell-synthesis"

EXTERNAL_BINDINGS = [
    REPO / "research/r074n_problem_freeze.md",
    REPO / "research/r074n_all_shell_synthesis.md",
    REPO / "research/r074n_all_shell_certificate.json",
    REPO / "research/r074n_all_shell_certificate_report.md",
    REPO / "research/r074n_all_shell_independent_audit.md",
    REPO / "research/r074n_crossnote_implication_independent_audit.md",
    REPO / "research/r074n_gap_matrix.md",
    REPO / "research/r074n_report-source.md",
    REPO / "research/r074n_bilingual_dictionary.md",
    REPO / "research/r074n_reader_source_independent_audit.md",
    REPO / "research/r074n_certificate_independent_audit.md",
    REPO / "research/r074n_certificate_adversarial_audit.md",
    REPO / "research/r074n_final_source_rebind_audit.md",
    REPO / "research/r074n_primary_literature_boundary.md",
    REPO / "research/r074n_primary_literature_independent_audit.md",
    REPO / "scripts/r074n_all_shell_certificate.py",
    REPO / "scripts/r074n_all_shell_certificate_independent.rb",
    REPO / "research/r074l_forward_bridge_bv_reduction.md",
    REPO / "research/r074l_main_collar_independent_audit.md",
    REPO / "research/r074m_final_segment_expulsion.md",
    REPO / "research/r074m_nearest_inward_independent_audit.md",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(check_id: str, passed: bool, note: str) -> dict:
    return {"id": check_id, "note": note, "pass": bool(passed)}


def image_info(path: Path) -> dict:
    with Image.open(path) as image:
        return {
            "dpi": list(image.info.get("dpi", (0, 0))),
            "mode": image.mode,
            "size": [image.width, image.height],
        }


def get_pdf_images(page) -> list[str]:
    resources = page.get("/Resources")
    if resources is None:
        return []
    resources = resources.get_object()
    xobjects = resources.get("/XObject")
    if xobjects is None:
        return []
    found = []
    for name, reference in xobjects.get_object().items():
        obj = reference.get_object()
        if obj.get("/Subtype") == "/Image":
            found.append(str(name))
    return found


def main() -> None:
    checks: list[dict] = []
    required = [
        "README.md",
        "caption.md",
        "chart-contract-and-source-data.md",
        "command.txt",
        "config.json",
        "contract.json",
        "environment.json",
        "figure.pdf",
        "figure.png",
        "figure.svg",
        "plot.py",
        "progress.ndjson",
        "qa-final-size.png",
        "qa-grayscale.png",
        "qa-pdf.png",
        "qa-svg-quicklook.png",
        "qa-protocol.md",
        "qa-report.md",
        "requirements.txt",
        "results.json",
        "source-data.csv",
        "validate.py",
    ]
    for name in required:
        checks.append(check(f"exists_{name}", (HERE / name).is_file(), name))

    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    contract = json.loads((HERE / "contract.json").read_text(encoding="utf-8"))
    results = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
    checks.extend(
        [
            check(
                "claim_boundary",
                config["claim_boundary"] == CLAIM
                and contract["claim_boundary"] == CLAIM
                and results["claim_boundary"] == CLAIM,
                "familywise all-shell theorem only; NOT CLAY",
            ),
            check(
                "analytic_audit_status",
                config["analytic_proof_audit"] == "PASS"
                and results["analytic_proof_audit"] == "PASS",
                "must remain fail-closed until the external analytic audit passes",
            ),
            check(
                "figure_audit_separate",
                config["figure_package_independent_audit"] == "EXTERNAL_SEPARATE_NOT_CLAIMED"
                and results["figure_package_independent_audit"] == "EXTERNAL_SEPARATE_NOT_CLAIMED",
                "package does not self-certify its independent figure audit",
            ),
            check(
                "simulation_false",
                config["simulation"] is False
                and contract["simulation"] is False
                and results["simulation"] is False,
                "deterministic schematic; no simulation",
            ),
            check(
                "contract_complete",
                contract["data_rows_expected"] == 20
                and contract["renderer"] == "deterministic_reportlab_vector"
                and contract["visual_status"] == "schematic_not_to_scale_no_DNS_no_sampled_path"
                and "direct labels" in contract["non_color_distinction"],
                "chart contract binds data grain, renderer, boundary, and non-color distinction",
            ),
            check(
                "output_hashes",
                results["outputs"]["pdf_sha256"] == sha256(HERE / "figure.pdf")
                and results["outputs"]["png_sha256"] == sha256(HERE / "figure.png")
                and results["outputs"]["svg_sha256"] == sha256(HERE / "figure.svg"),
                "results bind every publication master",
            ),
        ]
    )

    with (HERE / "source-data.csv").open(newline="", encoding="utf-8") as handle:
        csv_rows = list(csv.DictReader(handle))
    rows = {row["item"]: row for row in csv_rows}
    mismatches = []
    for key, row in rows.items():
        exact = float(Fraction(row["exact_value"]))
        numeric = float(row["numeric_value"])
        if abs(exact - numeric) > max(5e-15, 5e-15 * abs(exact)):
            mismatches.append({"item": key, "exact": exact, "numeric": numeric})
    rho = Fraction(rows["radius_exponent_rho"]["exact_value"])
    c_gamma = Fraction(rows["annular_weight_exponent_c_gamma"]["exact_value"])
    checks.extend(
        [
            check("source_row_count", len(csv_rows) == 20 and len(rows) == 20, "20 unique exact rows"),
            check("numeric_columns_match_exact", not mismatches, str(mismatches)),
            check(
                "geometry_identity",
                Fraction(3, 5) - Fraction(32, 63) - Fraction(1, 16)
                == Fraction(rows["geometry_gap"]["exact_value"])
                == Fraction(149, 5040),
                "one padded inward tube has positive asymptotic room",
            ),
            check(
                "bad_event_reserve",
                Fraction(1, 16) - rho - c_gamma
                == Fraction(rows["bad_event_reserve"]["exact_value"])
                == Fraction(72851, 1270080),
                "bad path pays one inverse R and Gamma_j",
            ),
            check(
                "outer_exponent_reserve",
                3 * c_gamma - rho
                == Fraction(rows["outer_exponent_reserve"]["exact_value"])
                == Fraction(1237, 423360),
                "outer Gamma ratio pays one inverse R",
            ),
            check(
                "outer_gamma_gap",
                3 * c_gamma
                == Fraction(rows["gamma_forward_gap"]["exact_value"])
                == Fraction(8, 1323),
                "Gamma_(j+1)/Gamma_j exponent",
            ),
            check(
                "outer_discrete_ledger",
                Fraction(rows["outer_volume_base"]["exact_value"]) == 4
                and Fraction(rows["geometric_tail_ratio_bound"]["exact_value"]) == Fraction(1, 2)
                and Fraction(rows["outer_L_squared_prefactor"]["exact_value"])
                == Fraction(4096, 3969),
                "collar volume, eventual ratio, and dyadic L conversion",
            ),
        ]
    )

    master = image_info(HERE / "figure.png")
    final = image_info(HERE / "qa-final-size.png")
    gray = image_info(HERE / "qa-grayscale.png")
    pdf_raster = image_info(HERE / "qa-pdf.png")
    svg_quicklook = image_info(HERE / "qa-svg-quicklook.png")
    checks.extend(
        [
            check("png_dimensions", master["size"] == [4205, 2363], "178 mm by 100 mm at 600 dpi"),
            check("png_rgb", master["mode"] == "RGB", "publication color mode"),
            check("png_dpi", min(master["dpi"]) >= 599, f"metadata dpi={master['dpi']}"),
            check("final_dimensions", final["size"] == [1402, 788], "200-dpi final-size QA"),
            check("gray_mode", gray["mode"] == "L", "grayscale QA"),
            check("pdf_raster_dimensions", pdf_raster["size"] == [2103, 1182], "300-dpi PDF QA"),
            check(
                "svg_quicklook_raster",
                svg_quicklook["mode"] == "RGB" and svg_quicklook["size"] == [2103, 2103],
                f"Quick Look SVG raster size={svg_quicklook['size']}",
            ),
        ]
    )

    reader = PdfReader(str(HERE / "figure.pdf"))
    page = reader.pages[0]
    metadata = reader.metadata
    width_pt = float(page.mediabox.width)
    height_pt = float(page.mediabox.height)
    pdf_images = get_pdf_images(page)
    font_resources = page["/Resources"].get_object().get("/Font").get_object()
    font_names = [
        str(reference.get_object().get("/BaseFont", "")) for reference in font_resources.values()
    ]
    checks.extend(
        [
            check("pdf_one_page", len(reader.pages) == 1, "one-page vector PDF"),
            check("pdf_unencrypted", not reader.is_encrypted, "PDF is open"),
            check(
                "pdf_metadata",
                metadata.title == "R0.74N exact all-shell synthesis"
                and metadata.author == "C. K. Zeng"
                and "NOT CLAY" in metadata.subject
                and "no simulation" in metadata.subject,
                "PDF metadata preserves status and simulation boundary",
            ),
            check(
                "pdf_physical_size",
                abs(width_pt - 504.5669291338583) < 0.01
                and abs(height_pt - 283.46456692913387) < 0.01,
                f"media box={width_pt:.6f}x{height_pt:.6f} pt",
            ),
            check("pdf_vector_no_images", not pdf_images, f"image XObjects={pdf_images}"),
            check(
                "pdf_embedded_font_names",
                any("DejaVuSans" in value for value in font_names)
                and any("DejaVuSans-Bold" in value for value in font_names),
                f"font resources={font_names}",
            ),
        ]
    )

    svg = (HERE / "figure.svg").read_text(encoding="utf-8")
    plot_source = (HERE / "plot.py").read_text(encoding="utf-8")
    semantic_tokens = [
        "INWARD UNION",
        "1 &lt;= k &lt;= j-1",
        "k = j",
        "k &gt;= j+1",
        "Dbar_&lt;",
        "R0.74M expulsion in the same tube",
        "R0.74L absolute",
        "super-Gaussian outer tail",
        "sum_(k&gt;=j+1) 4^k Gamma_k",
        "ratio &lt;= 1/2 eventually",
        "1237/423360 &gt; 0",
        "Gamma_j L R^5",
        "not to scale",
        "no DNS",
        "NOT CLAY",
    ]
    payloads = re.findall(r"data:font/ttf;base64,([A-Za-z0-9+/=]+)", svg)
    decoded_payloads = []
    for payload in payloads:
        try:
            decoded_payloads.append(base64.b64decode(payload, validate=True))
        except ValueError:
            decoded_payloads.append(b"")
    expected_font_hashes = {sha256(path) for path in [
        BUNDLE
        / "native/libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/Resources/fonts/truetype/DejaVuSans.ttf",
        BUNDLE
        / "native/libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/Resources/fonts/truetype/DejaVuSans-Bold.ttf",
    ]}
    actual_font_hashes = {hashlib.sha256(payload).hexdigest() for payload in decoded_payloads}
    checks.extend(
        [
            check("svg_root", "<svg" in svg and "</svg>" in svg, "valid SVG wrapper"),
            check(
                "svg_vector_only",
                "<image" not in svg
                and svg.count("<path") + svg.count("<rect") + svg.count("<circle") >= 30,
                "vector geometry and no raster node",
            ),
            check("svg_semantics", all(token in svg for token in semantic_tokens), "all shell ranges, mechanisms, target, and boundary rendered"),
            check(
                "svg_embedded_fonts",
                svg.count("@font-face") == 2
                and svg.count("data:font/ttf;base64,") == 2
                and actual_font_hashes == expected_font_hashes
                and "font-family: 'R074N-Regular'" in svg
                and "font-family: 'R074N-Bold'" in svg,
                f"embedded font hashes={sorted(actual_font_hashes)}",
            ),
            check(
                "schematic_not_simulated",
                "ordinal shell symbols" in svg
                and "not quantitative data" in svg
                and "Schematic" in svg
                and "random" not in plot_source.lower()
                and "numpy" not in plot_source.lower(),
                "no numerical shell data or sampled path",
            ),
        ]
    )

    qa_protocol = (HERE / "qa-protocol.md").read_text(encoding="utf-8")
    qa_report = (HERE / "qa-report.md").read_text(encoding="utf-8")
    checks.append(
        check(
            "manual_visual_gate",
            "Manual status: PASS" in qa_protocol
            and "Manual status: PASS" in qa_report
            and "Quick Look" in qa_protocol
            and "Quick Look" in qa_report
            and "independent figure-package audit" in qa_protocol
            and "independent figure-package audit" in qa_report,
            "five-surface internal visual QA completed without self-audit claim",
        )
    )

    caption = (HERE / "caption.md").read_text(encoding="utf-8")
    caption_tokens = [
        r"k\le j-1",
        r"k\ge j+1",
        "72851/1270080",
        "1237/423360",
        "not to scale",
        "no DNS",
        "NOT CLAY",
        "independent analytic audit with result PASS",
    ]
    checks.append(
        check(
            "caption_exact_and_bounded",
            all(token in caption for token in caption_tokens) and "\t" not in caption,
            "caption binds exact partition, margins, and claim boundary",
        )
    )

    external_exist = all(path.is_file() for path in EXTERNAL_BINDINGS)
    checks.append(
        check(
            "external_bindings_exist",
            external_exist,
            "problem, proof, finite certificates, audits, literature boundary, and inherited L/M lemmas",
        )
    )
    if external_exist:
        proof = (REPO / "research/r074n_all_shell_synthesis.md").read_text(encoding="utf-8")
        analytic_audit = (REPO / "research/r074n_all_shell_independent_audit.md").read_text(encoding="utf-8")
        crossnote_audit = (REPO / "research/r074n_crossnote_implication_independent_audit.md").read_text(encoding="utf-8")
        gap_matrix = (REPO / "research/r074n_gap_matrix.md").read_text(encoding="utf-8")
        report_source = (REPO / "research/r074n_report-source.md").read_text(encoding="utf-8")
        dictionary = (REPO / "research/r074n_bilingual_dictionary.md").read_text(encoding="utf-8")
        reader_audit = (REPO / "research/r074n_reader_source_independent_audit.md").read_text(encoding="utf-8")
        finite_audit = (REPO / "research/r074n_certificate_independent_audit.md").read_text(encoding="utf-8")
        adversarial_audit = (REPO / "research/r074n_certificate_adversarial_audit.md").read_text(encoding="utf-8")
        source_rebind = (REPO / "research/r074n_final_source_rebind_audit.md").read_text(encoding="utf-8")
        literature_boundary = (REPO / "research/r074n_primary_literature_boundary.md").read_text(encoding="utf-8")
        literature_audit = (REPO / "research/r074n_primary_literature_independent_audit.md").read_text(encoding="utf-8")
        checks.extend(
            [
                check(
                    "proof_binding_semantics",
                    "Theorem 6.1" in proof
                    and "exact all-shell synthesis" in proof
                    and "3c_\\gamma-\\rho" in proof
                    and "Corollary 6.2" in proof
                    and "cT_j\\le\\mathcal U_j\\le X_j\\le CT_j" in proof
                    and "0\\le\\mathcal D_j\\le CT_j" in proof
                    and "does not give a matching lower bound for \\(\\mathcal D_j\\)" in proof
                    and "NOT CLAY" in proof,
                    "current source contains shell theorem, cross-note X law, component boundary, and NOT CLAY",
                ),
                check(
                    "analytic_audit_pass",
                    "PASS" in analytic_audit
                    and "NOT CLAY" in analytic_audit
                    and "r074n_all_shell_synthesis.md" in analytic_audit,
                    "external analytic audit explicitly passes the bound source",
                ),
                check(
                    "crossnote_audit_pass",
                    "Verdict: PASS" in crossnote_audit
                    and "cT_j\\le\\mathcal U_j\\le X_j\\le CT_j" in crossnote_audit
                    and "no lower bound \\(\\mathcal D_j\\ge cT_j\\)" in crossnote_audit
                    and "universal square-root-log endpoint estimate" in crossnote_audit
                    and "FAMILYWISE ONLY; NOT CLAY" in crossnote_audit,
                    "cross-note audit proves exact-family X, keeps D lower and universal endpoint open",
                ),
                check(
                    "reader_chain_pass",
                    "Verdict: PASS" in reader_audit
                    and sha256(REPO / "research/r074n_all_shell_synthesis.md") in reader_audit
                    and sha256(REPO / "research/r074n_all_shell_independent_audit.md") in reader_audit
                    and sha256(REPO / "research/r074n_crossnote_implication_independent_audit.md") in reader_audit
                    and sha256(REPO / "research/r074n_final_source_rebind_audit.md") in reader_audit
                    and sha256(REPO / "research/r074n_report-source.md") in reader_audit
                    and sha256(REPO / "research/r074n_bilingual_dictionary.md") in reader_audit
                    and "global regularity remain OPEN" in reader_audit
                    and "PROVED FAMILYWISE / CROSS-NOTE AUDITED" in gap_matrix
                    and "OPEN / NOT CLAIMED" in gap_matrix
                    and "X_j\\asymp\\mathfrak C_j" in report_source
                    and "OPEN" in dictionary,
                    "reader, dictionary, report, and gap matrix preserve final exact-family and OPEN boundaries",
                ),
                check(
                    "finite_audit_pass",
                    "PASS" in finite_audit and "NOT CLAY" in finite_audit,
                    "external exact-arithmetic audit explicitly passes",
                ),
                check(
                    "finite_adversarial_audit_pass",
                    "PASS, with the stated finite-only scope" in adversarial_audit
                    and "inherit the producer's `PASS` flag as evidence" in adversarial_audit
                    and "FINITE ONLY; NOT CLAY" in adversarial_audit,
                    "adversarial finite audit reconstructs and tampers valid JSON fail-closed",
                ),
                check(
                    "final_source_rebind_pass",
                    "FINAL SOURCE REBIND: PASS" in source_rebind
                    and sha256(REPO / "research/r074n_all_shell_synthesis.md") in source_rebind
                    and sha256(REPO / "research/r074n_all_shell_independent_audit.md") in source_rebind,
                    "final source and analytic audit hashes rebound after audited cross-note repairs",
                ),
                check(
                    "literature_boundary_audit_pass",
                    "Verdict: **PASS**" in literature_audit
                    and sha256(REPO / "research/r074n_primary_literature_boundary.md") in literature_audit
                    and "no direct theorem in the screened" in literature_audit
                    and "no novelty search" in literature_audit
                    and "NOT CLAY" in literature_boundary,
                    "bounded primary-literature non-hit independently audited without novelty claim",
                ),
            ]
        )

        certificate_run = subprocess.run(
            [str(PYTHON), str(REPO / "scripts/r074n_all_shell_certificate.py")],
            check=False,
            capture_output=True,
            text=True,
        )
        try:
            certificate = json.loads(certificate_run.stdout)
            finite_python_pass = (
                certificate_run.returncode == 0
                and certificate["result"] == "PASS"
                and certificate["summary"]["passed"] == certificate["summary"]["total"]
            )
        except (json.JSONDecodeError, KeyError, TypeError):
            finite_python_pass = False
        checks.append(check("finite_python_certificate", finite_python_pass, "Python exact certificate independently rerun"))

        ruby_run = subprocess.run(
            [str(RUBY), str(REPO / "scripts/r074n_all_shell_certificate_independent.rb")],
            check=False,
            capture_output=True,
            text=True,
        )
        checks.append(
            check(
                "finite_ruby_reconstruction",
                ruby_run.returncode == 0 and "PASS" in ruby_run.stdout,
                "independent Ruby Rational reconstruction rerun",
            )
        )
    else:
        checks.extend(
            [
                check("proof_binding_semantics", False, "external inputs missing"),
                check("analytic_audit_pass", False, "external inputs missing"),
                check("crossnote_audit_pass", False, "external inputs missing"),
                check("reader_chain_pass", False, "external inputs missing"),
                check("finite_audit_pass", False, "external inputs missing"),
                check("finite_adversarial_audit_pass", False, "external inputs missing"),
                check("final_source_rebind_pass", False, "external inputs missing"),
                check("literature_boundary_audit_pass", False, "external inputs missing"),
                check("finite_python_certificate", False, "external inputs missing"),
                check("finite_ruby_reconstruction", False, "external inputs missing"),
            ]
        )

    text_files = [
        path
        for path in HERE.iterdir()
        if path.is_file() and path.suffix.lower() in {".md", ".py", ".json", ".csv", ".txt", ".svg"}
    ]
    forbidden = []
    for path in text_files:
        for byte in path.read_bytes():
            if byte < 32 and byte not in (10, 13):
                forbidden.append((path.name, byte))
    checks.append(check("no_forbidden_controls", not forbidden, str(forbidden)))

    passed = sum(1 for item in checks if item["pass"])
    validation = {
        "analytic_proof_audit": "PASS" if next(item for item in checks if item["id"] == "analytic_audit_pass")["pass"] else "FAIL_OR_MISSING",
        "checks": checks,
        "claim_boundary": CLAIM,
        "figure_id": FIGURE_ID,
        "figure_package_independent_audit": "EXTERNAL_SEPARATE_NOT_CLAIMED",
        "result": "PASS" if passed == len(checks) else "FAIL",
        "summary": {"passed": passed, "total": len(checks)},
    }
    (HERE / "validation.json").write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    layout = {
        "final_size_dimensions": final["size"],
        "master_dimensions": master["size"],
        "page_mm": [178, 100],
        "pdf_raster_dimensions": pdf_raster["size"],
        "quicklook_dimensions": svg_quicklook["size"],
        "visual_qa": "PASS" if next(item for item in checks if item["id"] == "manual_visual_gate")["pass"] else "PENDING_OR_FAIL",
    }
    (HERE / "layout-bounds.json").write_text(json.dumps(layout, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    external = [
        {"path": str(path.relative_to(REPO)), "sha256": sha256(path)}
        for path in EXTERNAL_BINDINGS
        if path.is_file()
    ]
    excluded = {"manifest.json", "SHA256SUMS"}
    entries = [
        {"bytes": path.stat().st_size, "path": path.name, "sha256": sha256(path)}
        for path in sorted(HERE.iterdir())
        if path.is_file() and path.name not in excluded
    ]
    manifest = {
        "analytic_proof_audit": validation["analytic_proof_audit"],
        "claim_boundary": CLAIM,
        "entries": entries,
        "external_bindings": external,
        "figure_id": FIGURE_ID,
        "figure_package_independent_audit": "EXTERNAL_SEPARATE_NOT_CLAIMED",
        "schema": "r074n-formal-figure-manifest-v1",
        "simulation": False,
        "validation": validation["result"],
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    seal_paths = [path for path in sorted(HERE.iterdir()) if path.is_file() and path.name != "SHA256SUMS"]
    (HERE / "SHA256SUMS").write_text(
        "".join(f"{sha256(path)}  {path.name}\n" for path in seal_paths), encoding="utf-8"
    )

    print(f"verify-only {validation['result']} {passed}/{len(checks)}; {len(entries)} package entries")
    if validation["result"] != "PASS":
        print("failed:", ", ".join(item["id"] for item in checks if not item["pass"]))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
