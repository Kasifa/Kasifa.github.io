#!/usr/bin/env python3
"""Fail-closed validation and sealing for the R0.74O formal figure package."""

from __future__ import annotations

import base64
import csv
import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path

from PIL import Image
from pypdf import PdfReader


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
BUNDLE = Path("/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies")
CLAIM = "SCALAR_PAYMENT_ONLY_ENDPOINT_NO_GO_SMOOTH_EXACT_FAMILY_NOT_CLAY"
FIGURE_ID = "fig-r074o-amplitude-endpoint"

EXTERNAL_BINDINGS = [
    REPO / "research/r074o_problem_freeze.md",
    REPO / "research/r074o_amplitude_endpoint_counterexample.md",
    REPO / "research/r074o_amplitude_endpoint_independent_audit.md",
    REPO / "research/r074o_final_source_rebind_audit.md",
    REPO / "research/r074o_gap_matrix.md",
    REPO / "research/r074o_amplitude_endpoint_certificate.json",
    REPO / "research/r074o_amplitude_endpoint_certificate_report.md",
    REPO / "research/r074o_certificate_independent_audit.md",
    REPO / "scripts/r074o_amplitude_endpoint_certificate.py",
    REPO / "scripts/r074o_amplitude_endpoint_certificate_independent.rb",
    REPO / "research/r074o_report-source.md",
    REPO / "research/r074o_bilingual_dictionary.md",
    REPO / "research/r074o_reader_source_independent_audit.md",
    REPO / "research/r074o_primary_literature_boundary.md",
    REPO / "research/r074o_primary_literature_independent_audit.md",
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

    if not all((HERE / name).is_file() for name in required):
        missing = [name for name in required if not (HERE / name).is_file()]
        print("required package inputs missing:", ", ".join(missing))
        raise SystemExit(1)

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
                "scalar-payment-only no-go on a smooth exact family; NOT CLAY",
            ),
            check(
                "analytic_audit_status",
                config["analytic_proof_audit"] == "PASS"
                and results["analytic_proof_audit"] == "PASS",
                "must remain fail-closed until the external analytic audit passes",
            ),
            check(
                "literature_audit_status",
                config["literature_audit"] == "REQUIRED_FAIL_CLOSED"
                and results["literature_audit"] == "PASS",
                "bounded primary-literature boundary requires its independent audit",
            ),
            check(
                "reader_audit_status",
                config["reader_source_audit"] == "REQUIRED_FAIL_CLOSED"
                and results["reader_source_audit"] == "PASS",
                "reader source and dictionary require an independent audit",
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
                "deterministic analytic schematic; no simulation",
            ),
            check(
                "contract_complete",
                contract["data_rows_expected"] == 24
                and contract["renderer"] == "deterministic_reportlab_vector"
                and contract["visual_status"]
                == "analytic_schematic_not_to_scale_no_DNS_no_simulation_no_fitted_data"
                and "direct labels" in contract["non_color_distinction"]
                and contract["palette_policy"] == "hard_two_root_cap_plus_neutrals"
                and contract["component_boundary"]
                == "The lower bound for X_* comes from endpoint energy; no separate lower bound is proved for its dissipation component.",
                "chart contract binds data grain, renderer, visual boundary, and non-color distinction",
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
    expected = {
        "radius_exponent_rho": Fraction(1, 320),
        "annular_weight_exponent_c_gamma": Fraction(8, 3969),
        "energy_decay_d_E": Fraction(98, 29475),
        "net_energy_exponent_e_E": Fraction(17018, 12998475),
        "amplitude_gap_m": Fraction(43, 423360),
        "varkappa_L_power": Fraction(2, 3),
        "varkappa_exp_coefficient": Fraction(43, 1270080),
        "energy_reserve": Fraction(1171, 943200),
        "velocity_packet_background_ratio": Fraction(1),
        "harmonic_L_power": Fraction(-3, 2),
        "payment_B_power": Fraction(3),
        "payment_R_power": Fraction(3),
        "beta_limit": Fraction(1, 128),
        "shear_lower_prefactor": Fraction(8),
        "shear_lower_exp_exponent": Fraction(-8),
        "quadratic_varkappa_power": Fraction(2),
        "observable_L_power": Fraction(1),
        "observable_B_power": Fraction(2),
        "observable_R_power": Fraction(2),
        "power_increment_delta_star": Fraction(86, 11907),
        "frontier_power_q_star": Fraction(8024, 11907),
        "endpoint_log_power": Fraction(1, 2),
        "frontier_log_power": Fraction(7, 6),
        "ratio_log_power": Fraction(2, 3),
    }
    mismatches = []
    for key, value in expected.items():
        if key not in rows:
            mismatches.append({"item": key, "error": "missing"})
            continue
        exact = Fraction(rows[key]["exact_value"])
        numeric = float(rows[key]["numeric_value"])
        if exact != value or abs(numeric - float(value)) > max(5e-15, 5e-15 * abs(float(value))):
            mismatches.append({"item": key, "exact": str(exact), "expected": str(value), "numeric": numeric})
    rho = expected["radius_exponent_rho"]
    c_gamma = expected["annular_weight_exponent_c_gamma"]
    d_e = expected["energy_decay_d_E"]
    e_e = expected["net_energy_exponent_e_E"]
    m = expected["amplitude_gap_m"]
    delta = expected["power_increment_delta_star"]
    checks.extend(
        [
            check(
                "source_row_count",
                len(csv_rows) == 24 and len(rows) == 24 and set(rows) == set(expected),
                "24 unique exact rational rows",
            ),
            check("numeric_columns_match_exact", not mismatches, str(mismatches)),
            check(
                "net_energy_identity",
                d_e - c_gamma == e_e == Fraction(17018, 12998475),
                "e_E = d_E - c_gamma",
            ),
            check(
                "amplitude_gap_identity",
                rho - Fraction(3, 2) * c_gamma == m == Fraction(43, 423360),
                "m = rho - 3 c_gamma / 2 > 0",
            ),
            check(
                "varkappa_exponent_identity",
                m / 3 == expected["varkappa_exp_coefficient"] == Fraction(43, 1270080),
                "varkappa exponential coefficient is m/3",
            ),
            check(
                "energy_reserve_identity",
                e_e - Fraction(2, 3) * m
                == expected["energy_reserve"]
                == Fraction(1171, 943200),
                "amplified energy remains below background scale",
            ),
            check(
                "frontier_power_identity",
                Fraction(2) * m / (Fraction(9) * rho)
                == delta
                == Fraction(86, 11907)
                and Fraction(2, 3) + delta
                == expected["frontier_power_q_star"]
                == Fraction(8024, 11907),
                "delta_* and q_* reconstructed exactly",
            ),
            check(
                "log_power_identity",
                expected["frontier_log_power"] - expected["endpoint_log_power"]
                == expected["ratio_log_power"]
                == Fraction(2, 3),
                "7/6 - 1/2 = 2/3",
            ),
            check(
                "payment_ledger_exact",
                expected["velocity_packet_background_ratio"] == 1
                and expected["harmonic_L_power"] == Fraction(-3, 2)
                and expected["payment_B_power"] == 3
                and expected["payment_R_power"] == 3,
                "G ratio, H decay, and B^3 R^3 payment powers",
            ),
            check(
                "observable_ledger_exact",
                expected["quadratic_varkappa_power"] == 2
                and expected["observable_L_power"] == 1
                and expected["observable_B_power"] == 2
                and expected["observable_R_power"] == 2,
                "varkappa^2 B^2 L R^2 observable powers",
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
    font_names = [str(reference.get_object().get("/BaseFont", "")) for reference in font_resources.values()]
    checks.extend(
        [
            check("pdf_one_page", len(reader.pages) == 1, "one-page vector PDF"),
            check("pdf_unencrypted", not reader.is_encrypted, "PDF is open"),
            check(
                "pdf_metadata",
                metadata.title == "R0.74O passive-amplitude endpoint obstruction"
                and metadata.author == "C. K. Zeng"
                and "Scalar-payment-only endpoint no-go" in metadata.subject
                and "no simulation or DNS" in metadata.subject
                and "NOT CLAY" in metadata.subject,
                "PDF metadata preserves scope and simulation boundary",
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
        ">A<",
        ">B<",
        ">C<",
        ">D<",
        "FREE",
        "varkappa &gt; 0",
        "a_* = varkappa B Gamma^(-1/2)",
        "1171/943200 &gt; 0",
        "packet / background = 1 exactly",
        "L^(-3/2)",
        "P_* ~",
        "varkappa^2 B^2 L R^2",
        "8024/11907",
        "86/11907",
        "SCALAR-PAYMENT-ONLY NO-GO",
        "smooth exact family",
        "NOT CLAY",
        "no DNS/simulation/fitted data",
        "X lower comes from endpoint energy",
        "no separate dissipation lower",
    ]
    payloads = re.findall(r"data:font/ttf;base64,([A-Za-z0-9+/=]+)", svg)
    decoded_payloads = []
    for payload in payloads:
        try:
            decoded_payloads.append(base64.b64decode(payload, validate=True))
        except ValueError:
            decoded_payloads.append(b"")
    font_root = (
        BUNDLE
        / "native/libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/Resources/fonts/truetype"
    )
    expected_font_hashes = {sha256(font_root / name) for name in ["DejaVuSans.ttf", "DejaVuSans-Bold.ttf"]}
    actual_font_hashes = {hashlib.sha256(payload).hexdigest() for payload in decoded_payloads}
    checks.extend(
        [
            check("svg_root", "<svg" in svg and "</svg>" in svg, "valid SVG wrapper"),
            check(
                "svg_vector_only",
                "<image" not in svg
                and svg.count("<path")
                + svg.count("<rect")
                + svg.count("<circle")
                + svg.count("<polygon")
                >= 25,
                "vector geometry and no raster node",
            ),
            check(
                "svg_four_panel_semantics",
                all(token in svg for token in semantic_tokens),
                "four panels, exact margins, quadratic law, frontier, and scope rendered",
            ),
            check(
                "svg_embedded_fonts",
                svg.count("@font-face") == 2
                and svg.count("data:font/ttf;base64,") == 2
                and actual_font_hashes == expected_font_hashes
                and "font-family: 'R074O-Regular'" in svg
                and "font-family: 'R074O-Bold'" in svg,
                f"embedded font hashes={sorted(actual_font_hashes)}",
            ),
            check(
                "analytic_not_simulated",
                "Analytic schematic" in svg
                and "not to scale" in svg
                and "no DNS/simulation/fitted data" in svg
                and "random" not in plot_source.lower()
                and "numpy" not in plot_source.lower(),
                "no DNS, simulation, fitted data, or sampled path",
            ),
        ]
    )

    own_text_files = [
        HERE / name
        for name in [
            "README.md",
            "caption.md",
            "chart-contract-and-source-data.md",
            "config.json",
            "contract.json",
            "plot.py",
            "qa-protocol.md",
            "qa-report.md",
            "results.json",
            "source-data.csv",
        ]
    ]
    wrong_amplitude_symbol = []
    for path in own_text_files:
        text = path.read_text(encoding="utf-8")
        if re.search(r"(?<!var)" + "kap" + "pa", text, flags=re.IGNORECASE):
            wrong_amplitude_symbol.append(path.name)
    checks.append(
        check(
            "varkappa_not_kappa",
            not wrong_amplitude_symbol and "varkappa" in svg,
            f"standalone kappa occurrences={wrong_amplitude_symbol}",
        )
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
        r"\varkappa=L^{2/3}",
        "1171/943200",
        r"L^{-3/2}",
        "8024/11907",
        "86/11907",
        "scalar-payment-only no-go",
        "no DNS",
        "NOT CLAY",
        "independent figure-package audit is not self-claimed",
        "lower bound for \\(X_*\\) comes from endpoint energy",
        "no separate lower bound is proved for its dissipation component",
    ]
    checks.append(
        check(
            "caption_exact_and_bounded",
            all(token in caption for token in caption_tokens) and "\t" not in caption,
            "caption binds exact amplitude, payments, frontier, and claim boundary",
        )
    )

    external_exist = all(path.is_file() for path in EXTERNAL_BINDINGS)
    checks.append(
        check(
            "external_bindings_exist",
            external_exist,
            "core proof, finite certificate, reader chain, and literature chain",
        )
    )
    if external_exist:
        freeze = (REPO / "research/r074o_problem_freeze.md").read_text(encoding="utf-8")
        proof_path = REPO / "research/r074o_amplitude_endpoint_counterexample.md"
        proof = proof_path.read_text(encoding="utf-8")
        analytic_audit_path = REPO / "research/r074o_amplitude_endpoint_independent_audit.md"
        analytic_audit = analytic_audit_path.read_text(encoding="utf-8")
        source_rebind = (REPO / "research/r074o_final_source_rebind_audit.md").read_text(encoding="utf-8")
        gap_matrix = (REPO / "research/r074o_gap_matrix.md").read_text(encoding="utf-8")
        certificate_path = REPO / "research/r074o_amplitude_endpoint_certificate.json"
        certificate = json.loads(certificate_path.read_text(encoding="utf-8"))
        certificate_report = (REPO / "research/r074o_amplitude_endpoint_certificate_report.md").read_text(encoding="utf-8")
        certificate_audit = (REPO / "research/r074o_certificate_independent_audit.md").read_text(encoding="utf-8")
        report_source_path = REPO / "research/r074o_report-source.md"
        report_source = report_source_path.read_text(encoding="utf-8")
        dictionary_path = REPO / "research/r074o_bilingual_dictionary.md"
        dictionary = dictionary_path.read_text(encoding="utf-8")
        reader_audit = (REPO / "research/r074o_reader_source_independent_audit.md").read_text(encoding="utf-8")
        literature_path = REPO / "research/r074o_primary_literature_boundary.md"
        literature_boundary = literature_path.read_text(encoding="utf-8")
        literature_audit = (REPO / "research/r074o_primary_literature_independent_audit.md").read_text(encoding="utf-8")
        checks.extend(
            [
                check(
                    "proof_binding_semantics",
                    sha256(proof_path) == "471158de1db718ac96f38adc729464d8717006f47c8c6bb57834cc4e159bd9bb"
                    and "Theorem 6.1" in proof
                    and "scalar sub-frontier no-go" in proof
                    and "\\varkappa" in proof
                    and "\\kappa=16" in proof
                    and "1171}{943200" in proof
                    and "8024}{11907" in proof
                    and "86}{11907" in proof
                    and "No simulation, DNS, DGX" in proof
                    and "Novelty and priority are not claimed" in proof
                    and "NOT CLAY" in proof,
                    "current proof contains exact smooth family, complete payment, frontier, and NOT CLAY",
                ),
                check(
                    "freeze_and_gap_boundary",
                    "scalar-payment endpoint question" in freeze
                    and "simulation, DNS, DGX" in freeze
                    and "OPEN / NOT CLAIMED" in gap_matrix
                    and "NOT CLAY" in gap_matrix,
                    "problem freeze and gap matrix preserve narrow no-go scope",
                ),
                check(
                    "analytic_audit_pass",
                    "Verdict: PASS" in analytic_audit
                    and sha256(proof_path) in analytic_audit
                    and sha256(REPO / "research/r074o_problem_freeze.md") in analytic_audit
                    and sha256(REPO / "research/r074o_gap_matrix.md") in analytic_audit
                    and "INDEPENDENT MATHEMATICAL AUDIT: PASS; NOT CLAY" in analytic_audit,
                    "external analytic audit binds and independently reconstructs current source",
                ),
                check(
                    "final_source_rebind_pass",
                    "FINAL SOURCE REBIND: PASS" in source_rebind
                    and sha256(proof_path) in source_rebind
                    and sha256(REPO / "research/r074o_problem_freeze.md") in source_rebind
                    and sha256(REPO / "research/r074o_gap_matrix.md") in source_rebind,
                    "final source hash and equation delimiters rebound after repairs",
                ),
                check(
                    "finite_certificate_pass",
                    certificate.get("result") == "PASS"
                    and certificate.get("summary", {}).get("passed") == 245
                    and certificate.get("summary", {}).get("total") == 245
                    and certificate.get("summary", {}).get("unique_ids") == 245
                    and "NOT CLAY" in " ".join(certificate.get("analytic_boundary", []))
                    and "FINITE: PASS, 245/245" in certificate_report,
                    "frozen exact-arithmetic certificate is complete and finite-only",
                ),
                check(
                    "finite_certificate_independent_audit",
                    "PASS 245/245" in certificate_audit
                    and sha256(certificate_path) in certificate_audit
                    and sha256(REPO / "scripts/r074o_amplitude_endpoint_certificate.py") in certificate_audit
                    and sha256(REPO / "scripts/r074o_amplitude_endpoint_certificate_independent.rb") in certificate_audit
                    and "FINITE ONLY; NOT CLAY" in certificate_audit,
                    "independent Ruby Rational reconstruction binds producer and JSON",
                ),
                check(
                    "finite_certificate_adversarial_audit",
                    "PASS 245/245" in certificate_audit
                    and sha256(certificate_path) in certificate_audit
                    and "Fail-closed tamper test" in certificate_audit
                    and "noncanonical rational" in certificate_audit
                    and "FINITE ONLY; NOT CLAY" in certificate_audit,
                    "independent certificate audit includes a fail-closed valid-JSON tamper test",
                ),
                check(
                    "reader_chain_pass",
                    "PASS" in reader_audit
                    and sha256(proof_path) in reader_audit
                    and sha256(analytic_audit_path) in reader_audit
                    and sha256(report_source_path) in reader_audit
                    and sha256(dictionary_path) in reader_audit
                    and "8024/11907" in report_source
                    and "1171/943200" in report_source
                    and "scalar-payment-only estimate" in dictionary
                    and "NOT CLAY" in dictionary,
                    "reader audit binds final corrected report source and bilingual dictionary",
                ),
                check(
                    "literature_boundary_audit_pass",
                    "PASS" in literature_audit
                    and sha256(literature_path) in literature_audit
                    and "not used as evidence of novelty" in literature_audit.lower()
                    and "NOT CLAY" in literature_audit
                    and "finite non-hit is not evidence of novelty" in literature_boundary
                    and "2D3C" in literature_boundary
                    and "no direct hit found" in literature_boundary,
                    "bounded primary-literature non-hit independently audited without priority claim",
                ),
            ]
        )
    else:
        for check_id in [
            "proof_binding_semantics",
            "freeze_and_gap_boundary",
            "analytic_audit_pass",
            "final_source_rebind_pass",
            "finite_certificate_pass",
            "finite_certificate_independent_audit",
            "finite_certificate_adversarial_audit",
            "reader_chain_pass",
            "literature_boundary_audit_pass",
        ]:
            checks.append(check(check_id, False, "required external input missing"))

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
    analytic_pass = next(item for item in checks if item["id"] == "analytic_audit_pass")["pass"]
    literature_pass = next(item for item in checks if item["id"] == "literature_boundary_audit_pass")["pass"]
    reader_pass = next(item for item in checks if item["id"] == "reader_chain_pass")["pass"]
    validation = {
        "analytic_proof_audit": "PASS" if analytic_pass else "FAIL_OR_MISSING",
        "checks": checks,
        "claim_boundary": CLAIM,
        "figure_id": FIGURE_ID,
        "figure_package_independent_audit": "EXTERNAL_SEPARATE_NOT_CLAIMED",
        "literature_audit": "PASS" if literature_pass else "FAIL_OR_MISSING",
        "reader_source_audit": "PASS" if reader_pass else "FAIL_OR_MISSING",
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
        "visual_qa": "PASS"
        if next(item for item in checks if item["id"] == "manual_visual_gate")["pass"]
        else "PENDING_OR_FAIL",
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
        "literature_audit": validation["literature_audit"],
        "reader_source_audit": validation["reader_source_audit"],
        "schema": "r074o-formal-figure-manifest-v1",
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
