#!/usr/bin/env python3
"""Generate the deterministic R0.74D three-panel journal package."""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle
from PIL import Image, ImageOps
import pypdfium2 as pdfium


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SOURCE_COMMIT = "ff80370fe33094f1423d312b817dfec0bf42d664"
SOURCE_NOTE = "research/r074d_zero_mean_local_transport_obstruction.md"
SOURCE_SHA = "bc9f7557e27bb86d5730273985b60f7135ccea3adc2fc99b2daf7778e70c9124"
CERTIFICATE = "research/r074d_zero_mean_transport_certificate.json"
CERTIFICATE_SHA = "69eecc7884a153bc5d4936c7d3dee9d3c736f5db69c20ba59b486165be96dec9"
CERTIFICATE_CHECKS = {"passed": 111, "total": 111}
FROZEN_UTC = "2026-09-01T00:00:00+00:00"

NAVY = "#174A7E"
BLUE = "#DCEAF5"
GREY = "#555B63"
LIGHT = "#F4F5F6"
RED = "#A84436"
AMBER = "#A87412"
GREEN = "#356E43"
PURPLE = "#765A9A"
INK = "#20242A"


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def rounded_box(ax, x, y, w, h, text, *, edge=NAVY, face="white", fs=6.2,
                lw=0.8, linestyle="-", weight="normal", align="center"):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        edgecolor=edge, facecolor=face, linewidth=lw, linestyle=linestyle,
    )
    ax.add_patch(patch)
    tx = x + w / 2 if align == "center" else x + 0.025
    ax.text(tx, y + h / 2, text, ha=align, va="center", fontsize=fs,
            color=INK, fontweight=weight, linespacing=1.22)


def arrow(ax, start, end, *, color=NAVY, linestyle="-", lw=0.9, scale=8):
    ax.add_patch(FancyArrowPatch(
        start, end, arrowstyle="-|>", mutation_scale=scale,
        linewidth=lw, color=color, linestyle=linestyle,
    ))


def badge(ax, x, y, text, color, *, linestyle="-", fs=6.0):
    ax.text(
        x, y, text, ha="left", va="center", fontsize=fs, fontweight="bold",
        color=color,
        bbox=dict(boxstyle="round,pad=.18", fc="white", ec=color,
                  lw=.7, ls=linestyle),
    )


def blossom(ax, x, y, radius=.010):
    for dx, dy in ((0, radius * 1.7), (radius * 1.6, radius * .5),
                   (radius, -radius * 1.4), (-radius, -radius * 1.4),
                   (-radius * 1.6, radius * .5)):
        ax.add_patch(Circle((x + dx, y + dy), radius, fill=False,
                            edgecolor=NAVY, linewidth=.55))
    ax.add_patch(Circle((x, y), radius * .55, facecolor=AMBER,
                        edgecolor=NAVY, linewidth=.45))


def source_rows() -> list[list[object]]:
    return [
        ["A", "exact family", "velocity", "u=(AF,B exp(-t) cos(x3),0); p=0", "exact smooth periodic NSE", "proved", "analytic formula; no DNS"],
        ["A", "mean", "global spatial mean", "u_bar=0", "Version-A frame", "proved", "constant-global-mean centre remains fixed"],
        ["A", "centre", "Version-A centre", "x_c(t)=0", "fixed observation centre", "proved", "global-mean subtraction is the identity"],
        ["A", "trajectory", "reference endpoints", "Q(R^2)=q*=1/2; Q(65R^2)=q_m=M R", "local packet path", "proved", "reference path in x3=0 plane"],
        ["A", "packet", "initial profile", "R^3 d_2 K_R^2(x2-q_pre) K_R^2(x3)", "localized derivative-heat packet", "proved", "scale R in x2 and x3; invariant in x1"],
        ["A", "geometry", "target annulus", "(2/3)M R <= |x| < (4/3)M R", "A_m(R)", "proved", "positive-measure endpoint slab"],
        ["B", "drift", "residual coefficient", "d=B exp(-t)(1-cos(x3)) <= 0", "one-sided mechanism", "proved", "B<0"],
        ["B", "drift", "accumulated displacement", "D=integral d(t-s,X_s) ds <= 0", "time-reversed diffusion", "proved", "nonautonomous order is t-s"],
        ["B", "target bridge", "weighted first moment", "E[|D| K_R^2(X_t)] <= C R", "target perturbation", "proved", "unknown C not plotted"],
        ["B", "target", "lower bound", "A^2 M R^2 exp(-M^2/288)", "X_R lower bound", "proved", "endpoint interval has positive measure"],
        ["B", "leakage", "one-sided separation", "z<0 implies |z+D| >= |z|", "fixed-centre Gaussian suppression", "proved", "central chart; no periodic wrap"],
        ["B", "leakage", "quadratic row", "A^2 R^2 Pi(M) exp(-M^2/264)", "buffered local energy", "proved", "Pi(M)=(1+M)^18 after relaxation"],
        ["B", "exponent", "strict margin", "1/264-1/288=1/3168>0", "target versus leakage", "proved", "exponential margin beats fixed polynomial"],
        ["B", "copies", "periodic lift", "all annuli and all periodic copies", "effective weights", "proved", "no copy truncation"],
        ["C", "sequence", "radius", "R=exp(-M^2/96)", "explicit divergence sequence", "proved", "M tends to infinity"],
        ["C", "sequence", "amplitude", "A=R^(-2) exp(M^2/576)", "explicit divergence sequence", "proved", "finite for each M"],
        ["C", "ratio", "background", "L/R^(-2)=M", "P_R^(2/3) row", "proved", "tends to infinity"],
        ["C", "ratio", "local leakage", "M/Pi(M) exp(M^2(1/264-1/288))", "P_R^(2/3) row", "proved", "tends to infinity"],
        ["C", "ratio", "exterior residence", "M^(7/3) exp(M^2/288)", "P_R^(2/3) row", "proved", "tends to infinity"],
        ["C", "conclusion", "global-mean Version A", "X_R/P_R^(2/3) -> infinity", "negative theorem", "proved", "specific frozen annular ledger"],
        ["C", "boundary", "local or mollified frame", "unknown", "transport-aware repair", "open", "no theorem claimed"],
        ["C", "boundary", "explicit entrance flux", "unknown", "fixed-centre repair", "open", "no theorem claimed"],
        ["C", "literature", "2D3C/shear/moving-frame mechanisms", "known frameworks", "known-framework boundary", "prior art", "no priority claim"],
        ["C", "scope", "Millennium problem", "unresolved", "not a Clay result", "boundary", "no regularity or blow-up theorem"],
    ]


CHART_CONTRACT = """# Chart contract and source data

**Analytical question.** Why does subtracting only the constant global mean fail to restore the frozen Version-A pure \\(P_R^{2/3}\\) endpoint, even for an exact zero-total-mean smooth periodic Navier--Stokes family?

**One-sentence takeaway.** A zero-global-mean decaying shear transports a localized derivative-heat packet toward a fixed Version-A centre; the one-sided residual drift preserves the target while suppressing fixed-centre leakage, and the resulting target dominates all three frozen payment rows along the explicit analytic sequence.

**Surface and format.** One static, journal-width, three-panel proof schematic; Matplotlib renderer; 180 x 82 mm; live-text SVG, one-page embedded-font PDF, and approximately 600 dpi RGB PNG. Grayscale and final-size derivatives are mandatory. This is a closed-form analytic figure, not DNS, a numerical trajectory, or a simulation.

**Panel contract.** Panel A shows the exact zero-global-mean field \\(u=(AF,B_Re^{-t}\\cos x_3,0)\\), the fixed Version-A centre, the reference path from \\(q_*=1/2\\) to \\(q_m=M_mR\\), and the scale-\\(R\\) packet. Panel B shows the signed residual drift \\(d=B_Re^{-t}(1-\\cos x_3)\\le0\\), the target bridge error \\(O(R)\\), the seam-safe one-sided Gaussian mechanism, and the strict exponent margin \\(1/264>1/288\\). Panel C shows separately the background, local-leakage, and exterior-residence ratios tending to infinity, followed by the exact narrow conclusion and the still-open local/mollified-frame or explicit-flux repairs.

**Canonical source grain.** `source-data.csv` contains one row per displayed geometry identity, stochastic/sign mechanism, exponent, payment row, asymptotic ratio, or scope boundary. Every quantitative row is copied from the frozen theorem at commit `ff80370fe33094f1423d312b817dfec0bf42d664`, SHA-256 `bc9f7557e27bb86d5730273985b60f7135ccea3adc2fc99b2daf7778e70c9124`. Unknown constants are labels only and are never encoded as numerical observations.

**Certificate gate.** Certificate provenance is bound only after `research/r074d_zero_mean_transport_certificate.json` has a stable `PASS` hash and check count. Plotting and validation must refuse a mismatched theorem or certificate hash.

**Palette and non-color distinction.** Single blue root for exact/proved mechanisms, amber for open boundaries, deep red only for the rejected frozen endpoint, and neutral greys for prior-art/scope text. Solid versus dashed strokes, open versus filled boxes, hatching, direct labels, and panel separation preserve meaning in grayscale; color is never the sole encoding.

**Required visible labels.** `EXACT NSE`, `PROVED`, `OPEN`, `PRIOR ART`, `NO DNS`, and `NOT CLAY` must appear as live SVG text. The figure must state that local/mollified frames and an explicit entrance-flux payment remain open, and it must make no priority claim.

**QA contract.** Exact 25-file inventory; two complete generate/validate runs with 25/25 byte identity; all text files free of whitespace defects; all `SHA256SUMS` entries verified; one 180 x 82 mm PDF page with embedded fonts; at least 4250 x 1936 pixels for the master PNG; live SVG text with no raster image and no base label below 6 pt; visual inspection of the master, PDF render, grayscale render, and final-size derivative.
"""


def draw() -> None:
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "pdf.fonttype": 42,
        "svg.fonttype": "none",
        "svg.hashsalt": "r074d-ff80370f-bc9f7557-69eecc78",
    })
    fig = plt.figure(figsize=(180 / 25.4, 82 / 25.4), dpi=600, facecolor="white")
    grid = fig.add_gridspec(1, 3, left=.022, right=.985, bottom=.108,
                            top=.91, wspace=.072)
    axes = [fig.add_subplot(grid[0, index]) for index in range(3)]
    for index, ax in enumerate(axes):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.text(0, 1.035, chr(65 + index), fontsize=10, fontweight="bold", va="top")
    blossom(axes[2], .955, 1.012, .008)

    # Panel A: exact zero-mean shear and local packet path.
    ax = axes[0]
    ax.text(.07, 1.02, "Zero-mean shear / fixed centre", fontsize=7.45,
            fontweight="bold", va="top")
    badge(ax, .68, .96, "EXACT NSE", NAVY)
    ax.text(.08, .895, "b(t,x₃)=B e⁻ᵗ cos x₃,   ∫ b dx₃=0", fontsize=6.05,
            color=INK)
    for y, label, direction in ((.81, "x₃=+π", 1), (.735, "x₃=0", -1),
                                (.66, "x₃=−π", 1)):
        ax.plot([.20, .91], [y, y], color="#D5D9DD", lw=.55)
        ax.text(.07, y, label, fontsize=6.0, va="center", color=GREY)
        start, end = ((.34, y), (.82, y)) if direction > 0 else ((.82, y), (.34, y))
        arrow(ax, start, end, color=NAVY if direction < 0 else GREY,
              lw=1.05, scale=8)

    ax.add_patch(Rectangle((.075, .36), .115, .19, fc=LIGHT, ec=GREY, lw=.7))
    ax.add_patch(Rectangle((.092, .385), .035, .14, fc="#DDE1E5", ec=GREY, lw=.6))
    ax.text(.04, .325, "Version-A centre\nx_c(t)=0  (ū=0)", ha="left",
            va="top", fontsize=6.0, linespacing=1.2)
    ax.add_patch(Rectangle((.27, .365), .25, .18, fc="#FFF3DA", ec=AMBER,
                           lw=.7, hatch="///"))
    ax.text(.94, .325, "Aₘ(R)\n⅔MR ≤ |x| < ⁴⁄₃MR", ha="right", va="top",
            fontsize=6.0, linespacing=1.2)
    ax.add_patch(Rectangle((.365, .382), .038, .145, fc=BLUE, ec=NAVY, lw=.9))
    ax.text(.384, .57, "qₘ=MR", ha="center", fontsize=6.0, color=NAVY)
    ax.add_patch(Rectangle((.855, .382), .038, .145, fc="#E9E2F1", ec=PURPLE, lw=.9))
    ax.text(.874, .57, "q*=½", ha="center", fontsize=6.0, color=PURPLE)
    ax.plot([.64, .66], [.425, .485], color=GREY, lw=.8)
    ax.plot([.66, .68], [.425, .485], color=GREY, lw=.8)
    arrow(ax, (.84, .455), (.42, .455), color=PURPLE, lw=1.15, scale=9)
    ax.text(.63, .495, "Q(R²) → Q(65R²)", ha="center", fontsize=6.0, color=PURPLE)
    ax.text(.66, .40, "axis break", ha="center", fontsize=6.0, color=GREY)
    rounded_box(ax, .06, .075, .88, .13,
                "u=(AF, B e⁻ᵗ cos x₃, 0),  p=0\n"
                "F₀=R³ ∂₂Kᵖᵉʳ(R²;x₂−qₚᵣₑ) Kᵖᵉʳ(R²;x₃)\n"
                "scale-R packet; invariant in x₁",
                edge=NAVY, face=BLUE, fs=6.0)
    badge(ax, .06, .018, "PROVED", GREEN)
    badge(ax, .36, .018, "ZERO GLOBAL MEAN", GREY, linestyle="--", fs=6.0)

    # Panel B: signed residual and strict Gaussian exponent margin.
    ax = axes[1]
    ax.text(.07, 1.02, "Signed bridge / leakage", fontsize=7.45,
            fontweight="bold", va="top")
    badge(ax, .70, .96, "PROVED", GREEN)
    rounded_box(ax, .055, .81, .89, .095,
                "d(t,x₃)=B e⁻ᵗ(1−cos x₃) ≤ 0\n"
                "D=∫d(t−s,X_s)ds ≤ 0",
                edge=NAVY, face=BLUE, fs=6.2, weight="bold")
    arrow(ax, (.50, .81), (.50, .745), color=NAVY)
    rounded_box(ax, .055, .64, .89, .095,
                "TARGET BRIDGE\nE[|D| Kᵖᵉʳ(R²;Xₜ)] ≤ C R",
                edge=GREEN, face="#EFF6F0", fs=6.2)
    arrow(ax, (.50, .64), (.50, .575), color=GREEN)
    rounded_box(ax, .055, .47, .89, .095,
                "z<0  ⇒  |z+D| ≥ |z|\ncentral half-chart; no periodic wrap",
                edge=PURPLE, face="#F2EEF7", fs=6.15)

    ax.text(.07, .405, "Exact exponential comparison", fontsize=6.1,
            fontweight="bold", color=GREY)
    rounded_box(ax, .06, .285, .88, .085,
                "target:   exp(−M²/288)", edge=NAVY, face="white",
                fs=6.35, align="left")
    rounded_box(ax, .06, .18, .88, .085,
                "leakage: exp(−M²/264) × Π(M)", edge=GREY, face=LIGHT,
                fs=6.35, linestyle="--", align="left")
    rounded_box(ax, .10, .075, .80, .075,
                "1/264 − 1/288 = 1/3168 > 0",
                edge=GREEN, face="#EFF6F0", fs=6.45, weight="bold")
    badge(ax, .06, .025, "ALL COPIES", GREY, linestyle="--")
    badge(ax, .42, .025, "NO DNS", GREY, linestyle="--")

    # Panel C: three ratio rows and the exact open boundary.
    ax = axes[2]
    ax.text(.07, 1.02, "Ratios / exact boundary", fontsize=7.45,
            fontweight="bold", va="top")
    rounded_box(ax, .06, .82, .88, .085,
                "R=exp(−M²/96),   A=R⁻² exp(M²/576)",
                edge=PURPLE, face="#F2EEF7", fs=6.35, weight="bold")
    row_specs = [
        (.69, .095, "background", "M  → ∞"),
        (.535, .12, "local leakage", "[M/Π(M)]\n× exp[M²(1/264−1/288)]  → ∞"),
        (.40, .095, "exterior residence", "M⁷ᐟ³ exp(M²/288)  → ∞"),
    ]
    for y, height, title, ratio in row_specs:
        rounded_box(ax, .055, y, .89, height, f"{title}\nL / row = {ratio}",
                    edge=GREEN, face="#EFF6F0", fs=6.0, align="left")
    rounded_box(ax, .10, .285, .80, .075,
                "X_R / P_R²ᐟ³  → ∞",
                edge=RED, face="#FAECE8", fs=7.0, weight="bold")
    rounded_box(ax, .05, .145, .90, .105,
                "OPEN: local/mollified frame\n"
                "or explicit entrance-flux payment",
                edge=AMBER, face="#FFF6E5", fs=6.25, weight="bold")
    ax.text(.50, .105, "2D3C / shear / moving-frame mechanisms: PRIOR ART",
            ha="center", fontsize=6.0, color=GREY)
    ax.text(.50, .076, "No priority claim; the frozen ledger result is narrow.",
            ha="center", fontsize=6.0, color=GREY)
    badge(ax, .05, .025, "OPEN", AMBER)
    badge(ax, .31, .025, "PRIOR ART", GREY, linestyle="--")
    badge(ax, .68, .025, "NOT CLAY", GREY)

    fig.text(
        .5, .038,
        "Exact smooth periodic NSE • analytic source formulas only • fixed global-mean frame fails • no simulation",
        ha="center", fontsize=6.15, color=GREY,
    )

    fixed_dt = datetime(2026, 9, 1, tzinfo=timezone.utc)
    fig.savefig(
        HERE / "figure.svg",
        metadata={"Date": FROZEN_UTC,
                  "Description": f"SourceCommit={SOURCE_COMMIT}; SourceSHA256={SOURCE_SHA}; CertificateSHA256={CERTIFICATE_SHA}"},
    )
    fig.savefig(
        HERE / "figure.pdf",
        metadata={"Title": "R0.74D zero-mean local-transport obstruction",
                  "Subject": f"{SOURCE_COMMIT}; {SOURCE_SHA}; {CERTIFICATE_SHA}",
                  "CreationDate": fixed_dt, "ModDate": fixed_dt},
    )
    fig.savefig(HERE / "figure.png", dpi=600)
    plt.close(fig)

    svg_path = HERE / "figure.svg"
    svg_path.write_text(
        "\n".join(line.rstrip() for line in
                  svg_path.read_text(encoding="utf-8").splitlines()) + "\n",
        encoding="utf-8", newline="\n",
    )


def render_qa() -> None:
    document = pdfium.PdfDocument(str(HERE / "figure.pdf"))
    page = document[0]
    image = page.render(scale=4252 / page.get_size()[0]).to_pil().convert("RGB")
    image.save(HERE / "qa-pdf.png")
    page.close()
    document.close()

    source = Image.open(HERE / "figure.png").convert("RGB")
    source.resize((2126, 969), Image.Resampling.LANCZOS).save(
        HERE / "qa-final-size.png"
    )
    ImageOps.grayscale(source).convert("RGB").save(HERE / "qa-grayscale.png")


def write_package() -> None:
    proof_bytes = subprocess.run(
        ["git", "-C", str(REPO), "show", f"{SOURCE_COMMIT}:{SOURCE_NOTE}"],
        check=True, capture_output=True,
    ).stdout
    assert hashlib.sha256(proof_bytes).hexdigest() == SOURCE_SHA
    certificate_path = REPO / CERTIFICATE
    assert sha(certificate_path) == CERTIFICATE_SHA
    certificate = json.loads(certificate_path.read_text(encoding="utf-8"))
    assert certificate.get("schema_version") == 1
    assert certificate.get("status") == "PASS"
    assert certificate.get("summary") == CERTIFICATE_CHECKS

    rows = source_rows()
    with (HERE / "source-data.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["panel", "category", "record", "expression", "role",
                         "status", "boundary_note"])
        writer.writerows(rows)

    config = {
        "canvasMm": [180, 82],
        "certificateSha256": CERTIFICATE_SHA,
        "dns": False,
        "dpi": 600,
        "figureId": "fig-r074d-zero-mean-local-transport-obstruction",
        "panels": ["A", "B", "C"],
        "simulation": False,
        "sourceCommit": SOURCE_COMMIT,
        "sourceNoteSha256": SOURCE_SHA,
        "unknownConstantsNumericallyEncoded": False,
    }
    contract = {
        "certificate": {"checks": "111/111", "schemaVersion": 1,
                        "sha256": CERTIFICATE_SHA},
        "expectedFileCount": 25,
        "figureClaims": {
            "A": "Exact zero-global-mean decaying shear, fixed Version-A centre, and localized packet reference path.",
            "B": "Signed residual drift, O(R) target bridge, seam-safe one-sided leakage, and strict exponent margin.",
            "C": "Three divergent payment ratios, narrow global-mean-frame failure, and open transport-aware repairs.",
        },
        "schema": "r074d-figure-contract-v1",
        "sourceCommit": SOURCE_COMMIT,
        "sourceNoteSha256": SOURCE_SHA,
        "statuses": ["PROVED", "EXACT NSE", "OPEN", "PRIOR ART", "NOT CLAY", "NO DNS"],
    }
    (HERE / "config.json").write_text(canonical(config), encoding="utf-8")
    (HERE / "contract.json").write_text(canonical(contract), encoding="utf-8")
    (HERE / "caption.md").write_text(
        "Figure X. Zero-global-mean local-transport obstruction to the frozen Version-A endpoint. "
        "(A) The exact smooth periodic field u=(AF,B exp(-t) cos(x3),0), p=0 has zero total spatial mean, so the global-mean Version-A centre remains fixed. Its localized derivative-heat packet follows the reference path from q*=1/2 to q_m=MR. "
        "(B) In reference-centred coordinates the nonautonomous residual drift d=B exp(-t)(1-cos(x3)) is nonpositive. The target-weighted displacement is O(R), whereas on the observation side z<0 implies |z+D|>=|z|. Thus the local quadratic leakage carries exp(-M^2/264), strictly faster than the target weight exp(-M^2/288). All periodic copies are included. "
        "(C) For R=exp(-M^2/96) and A=R^(-2)exp(M^2/576), the target separately dominates the background, local-leakage, and exterior-residence rows of P_R^(2/3), proving X_R/P_R^(2/3) tends to infinity for the frozen global-mean frame. A local or mollified frame and a formulation retaining explicit entrance flux remain OPEN. The 2D3C, shear, and moving-frame mechanisms are PRIOR ART; no priority claim. Analytic formulas only; NO DNS. NOT CLAY.\n",
        encoding="utf-8",
    )
    (HERE / "README.md").write_text(
        "# R0.74D zero-mean local-transport obstruction figure\n\n"
        f"Reproducible 25-file journal package frozen to analytic commit {SOURCE_COMMIT} "
        f"and certificate {CERTIFICATE_SHA} (111/111). Run `plot.py`, then "
        "`validate.py`; `command.txt` performs the two-run byte audit.\n",
        encoding="utf-8",
    )
    (HERE / "chart-contract-and-source-data.md").write_text(
        CHART_CONTRACT, encoding="utf-8"
    )
    (HERE / "qa-protocol.md").write_text(
        "# QA protocol\n\n"
        "Verify the analytic commit, note hash, certificate hash and 111/111 status; exact 25-file inventory; 180 x 82 mm one-page PDF; approximately 600 dpi master PNG; embedded PDF fonts; live SVG text with no raster image; base label size at least 6 pt; complete panel/status phrases; 24 closed-form source rows; grayscale and final-size legibility; the three distinct ratio rows; nonautonomous sign, seam, all-copy, open-repair, prior-art, no-DNS, and NOT CLAY boundaries. Run generation and validation twice and compare every byte.\n",
        encoding="utf-8",
    )
    (HERE / "requirements.txt").write_text(
        "matplotlib==3.10.6\npillow==12.3.0\npypdf==6.10.0\npypdfium2==5.13.0\n",
        encoding="utf-8",
    )
    (HERE / "environment.json").write_text(canonical({
        "dgxUsed": False,
        "frozenUtc": FROZEN_UTC,
        "networkUsed": False,
        "python": sys.version,
    }), encoding="utf-8")
    (HERE / "progress.ndjson").write_text(
        canonical({"event": "rendered", "utc": FROZEN_UTC}).strip() + "\n",
        encoding="utf-8",
    )
    (HERE / "resource-log.ndjson").write_text(
        canonical({"analyticSourceOnly": True, "cpuOnly": True,
                   "dgxUsed": False, "dns": False, "simulation": False}).strip() + "\n",
        encoding="utf-8",
    )
    (HERE / "results.json").write_text(canonical({
        "certificateSha256": CERTIFICATE_SHA,
        "rows": len(rows),
        "sourceCommit": SOURCE_COMMIT,
        "sourceNoteSha256": SOURCE_SHA,
        "status": "PREVALIDATION",
    }), encoding="utf-8")
    (HERE / "qa-report.md").write_text(
        "# QA report\n\nPending validator.\n", encoding="utf-8"
    )
    (HERE / "validation.json").write_text(
        canonical({"status": "PENDING"}), encoding="utf-8"
    )
    (HERE / "manifest.json").write_text(canonical({
        "certificateSha256": CERTIFICATE_SHA,
        "figureId": config["figureId"],
        "files": [],
        "sourceCommit": SOURCE_COMMIT,
        "sourceNoteSha256": SOURCE_SHA,
    }), encoding="utf-8")
    (HERE / "SHA256SUMS").write_text("", encoding="utf-8")
    (HERE / "command.txt").write_text(
        "set -e\n"
        "export PYTHONPATH=/Users/kasifa/.cache/codex-runtimes/r073s-figure-python\n"
        "PY=/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3\n"
        "$PY -B plot.py\n"
        "$PY -B validate.py\n"
        "snapshot_dir=$(mktemp -d /private/tmp/r074d-byte-snapshot.XXXXXX)\n"
        "cp -p * \"$snapshot_dir\"/\n"
        "$PY -B plot.py\n"
        "$PY -B validate.py\n"
        "diff -rq \"$snapshot_dir\" .\n"
        "text_files=(README.md caption.md chart-contract-and-source-data.md command.txt config.json contract.json environment.json figure.svg manifest.json plot.py progress.ndjson qa-protocol.md qa-report.md requirements.txt resource-log.ndjson results.json SHA256SUMS source-data.csv validate.py validation.json)\n"
        "for text_file in $text_files; do\n"
        "  whitespace=$(git diff --no-index --check /dev/null \"$text_file\" 2>&1 || true)\n"
        "  test -z \"$whitespace\"\n"
        "done\n"
        "shasum -a 256 -c SHA256SUMS >/dev/null\n"
        "echo \"DETERMINISM PASS: 25/25 files byte-identical; text whitespace PASS: 20/20\"\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    write_package()
    draw()
    render_qa()
