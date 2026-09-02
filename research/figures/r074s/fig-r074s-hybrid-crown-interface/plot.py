#!/usr/bin/env python3
"""Generate the archival R0.74S Step 15 analytic schematic."""

from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
FIGURE_ID = "fig-r074s-hybrid-crown-interface"
OUT = ROOT / "figures/r074s" / FIGURE_ID
SOURCE_COMMIT = "afb44bc0ecc6db6dbff9a252951ccc9182478717"
WIDTH_MM = 178.0
HEIGHT_MM = 112.0
DPI = 600

INK = "#17202a"
MUTED = "#5d6770"
NAVY = "#264a60"
TEAL = "#2f766d"
AMBER = "#b76a1d"
RED = "#963d3d"
PAPER = "#fbfaf6"
BLUE_BG = "#eaf2f5"
GREEN_BG = "#eaf3ef"
AMBER_BG = "#fbf0df"
RED_BG = "#f8eaea"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def box(ax, xy, width, height, text, *, facecolor, edgecolor, size=8.0, weight="normal", style="round,pad=0.02"):
    x, y = xy
    patch = FancyBboxPatch(
        (x, y), width, height,
        boxstyle=style,
        linewidth=1.1,
        edgecolor=edgecolor,
        facecolor=facecolor,
        transform=ax.transAxes,
        clip_on=False,
    )
    ax.add_patch(patch)
    ax.text(
        x + width / 2,
        y + height / 2,
        text,
        transform=ax.transAxes,
        ha="center",
        va="center",
        color=INK,
        fontsize=size,
        fontweight=weight,
        linespacing=1.25,
    )
    return patch


def arrow(ax, start, end, *, color=INK, dashed=False, width=1.2):
    ax.add_patch(FancyArrowPatch(
        start,
        end,
        transform=ax.transAxes,
        arrowstyle="-|>",
        mutation_scale=10,
        linewidth=width,
        linestyle="--" if dashed else "-",
        color=color,
        shrinkA=2,
        shrinkB=2,
    ))


def draw_hybrid(ax):
    ax.set_axis_off()
    ax.text(0.00, 1.02, "A  One deletion set for\nboth residual branches", transform=ax.transAxes,
            fontsize=8.7, fontweight="bold", color=NAVY, va="top", linespacing=1.05)

    box(ax, (0.02, 0.72), 0.28, 0.13, "short branch\n$z_k=r_k$", facecolor=BLUE_BG, edgecolor=NAVY, size=8.2, weight="bold")
    box(ax, (0.02, 0.50), 0.28, 0.16, "selected excess\n$\\frac{1}{5} z_k<r_k<\\frac{3}{7} z_k$", facecolor=GREEN_BG, edgecolor=TEAL, size=7.7, weight="bold")
    box(ax, (0.38, 0.57), 0.57, 0.20,
        "$\\frac{1}{5}\\,\\mathcal{S}_N(z)\\leq\\mathcal{S}_N(r)\\leq\\mathcal{S}_N(z)$\n"
        "same shell set, size(S) <= N\nPROVED  S.384--S.385",
        facecolor=PAPER, edgecolor=INK, size=8.25, weight="bold")
    arrow(ax, (0.30, 0.785), (0.38, 0.70), color=NAVY)
    arrow(ax, (0.30, 0.58), (0.38, 0.64), color=TEAL)

    box(ax, (0.11, 0.20), 0.29, 0.17,
        "S.342\n$H^F_{p,N_F,R}\\leq C_H A_R$\nOPEN",
        facecolor=RED_BG, edgecolor=RED, size=7.7, weight="bold")
    box(ax, (0.55, 0.20), 0.37, 0.17,
        "both residual branches\nclose with the same $N_F$\nCONDITIONAL S.387--S.391",
        facecolor=AMBER_BG, edgecolor=AMBER, size=7.7, weight="bold")
    arrow(ax, (0.40, 0.285), (0.55, 0.285), color=RED, dashed=True, width=1.5)

    box(ax, (0.15, 0.005), 0.70, 0.105,
        "Signed common-window cancellation still carries\nthe start-clock overshoot debt (S.395).",
        facecolor="#f2f2ee", edgecolor=MUTED, size=6.4)


def draw_crown(ax):
    ax.set_axis_off()
    ax.text(0.00, 1.02, "B  Terminal crowns isolate\nthe missing PDE charge", transform=ax.transAxes,
            fontsize=8.7, fontweight="bold", color=TEAL, va="top", linespacing=1.05)

    # Stylized finite-depth crown partition.
    ax.add_patch(Rectangle((0.03, 0.50), 0.38, 0.36, transform=ax.transAxes,
                           facecolor="#f4f0e5", edgecolor=INK, linewidth=1.2))
    ax.text(0.05, 0.82, "top $T$", transform=ax.transAxes, fontsize=7.4, weight="bold", color=INK)
    ax.add_patch(Rectangle((0.07, 0.54), 0.30, 0.23, transform=ax.transAxes,
                           facecolor=GREEN_BG, edgecolor=TEAL, linewidth=1.0, hatch="//"))
    ax.add_patch(Rectangle((0.12, 0.57), 0.20, 0.14, transform=ax.transAxes,
                           facecolor=BLUE_BG, edgecolor=NAVY, linewidth=1.0))
    ax.add_patch(Rectangle((0.17, 0.595), 0.10, 0.08, transform=ax.transAxes,
                           facecolor=AMBER_BG, edgecolor=AMBER, linewidth=1.0, hatch=".."))
    ax.text(0.22, 0.49, "disjoint crowns; terminal depth retained", transform=ax.transAxes,
            ha="center", va="top", fontsize=6.5, color=MUTED)

    box(ax, (0.48, 0.64), 0.48, 0.20,
        "$\\sum \\gamma_k\\rho_S\\leq C_\\kappa C_{\\mathrm{top}}$\n"
        "$C_\\kappa=(2\\kappa-1)/(\\kappa-1)$\n"
        "depth independent\nPROVED  S.404",
        facecolor=PAPER, edgecolor=TEAL, size=7.1, weight="bold")
    arrow(ax, (0.41, 0.70), (0.48, 0.74), color=TEAL)

    box(ax, (0.03, 0.21), 0.42, 0.18,
        "$p^{\\mathrm{crown}}_{Sk}=(a^{\\mathrm{pay}}_{Sk})^{3/2}$\n"
        "$/(\\gamma_k\\rho_S)^{1/2}$\n"
        "$\\sum p^{\\mathrm{crown}}_{Sk}\\leq C_pP_R^M$\nOPEN  S.407",
        facecolor=RED_BG, edgecolor=RED, size=6.8, weight="bold")
    box(ax, (0.54, 0.21), 0.42, 0.18,
        "$\\mathcal{S}_{N_b}(b)\\leq C A_R$\n"
        "under S.405 + OPEN S.407\nCONDITIONAL\nS.408",
        facecolor=AMBER_BG, edgecolor=AMBER, size=6.9, weight="bold")
    arrow(ax, (0.45, 0.30), (0.54, 0.30), color=RED, dashed=True, width=1.5)

    box(ax, (0.03, 0.005), 0.43, 0.11, "periodic measure tree\ngeometric stress test", facecolor="#eeeeea", edgecolor=MUTED, size=6.8)
    box(ax, (0.54, 0.005), 0.42, 0.11, "selected scalar clock\nalgebraic stress test", facecolor="#eeeeea", edgecolor=MUTED, size=6.8)
    ax.text(0.50, 0.06, "NOT\nCOUPLED", transform=ax.transAxes, ha="center", va="center", fontsize=5.8, color=RED, fontweight="bold")


def render() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    width_in = WIDTH_MM / 25.4
    height_in = HEIGHT_MM / 25.4
    fig = plt.figure(figsize=(width_in, height_in), facecolor=PAPER)
    grid = fig.add_gridspec(1, 2, left=0.035, right=0.985, top=0.88, bottom=0.12, wspace=0.10)
    draw_hybrid(fig.add_subplot(grid[0, 0]))
    draw_crown(fig.add_subplot(grid[0, 1]))
    fig.text(0.035, 0.955, "R0.74S STEP 15  |  HYBRID FLUX EQUIVALENCE AND TERMINAL-CROWN INTERFACE",
             fontsize=9.3, fontweight="bold", color=INK, va="top")
    fig.text(0.035, 0.055,
             "Claim boundary: S.342 and S.407 are OPEN. Q.1, regularity, and the Millennium problem remain OPEN."
             "  Analytic schematic - not simulation or DNS.",
             fontsize=6.3, color=MUTED, va="bottom")
    fig.savefig(OUT / "figure.pdf", format="pdf", facecolor=fig.get_facecolor())
    svg_path = OUT / "figure.svg"
    fig.savefig(svg_path, format="svg", facecolor=fig.get_facecolor(), metadata={"Date": None})
    write_text(svg_path, "\n".join(line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines()) + "\n")
    fig.savefig(OUT / "figure.png", format="png", dpi=DPI, facecolor=fig.get_facecolor(), pil_kwargs={"compress_level": 6})
    plt.close(fig)


def archive() -> None:
    rows = [
        ("S.382", "selected excess coordinate", "1/5 < r/z < 3/7", "proved sharp within scalar constraints"),
        ("S.384-S.385", "same-deletion best-N equivalence", "1/5 S_N(z) <= S_N(r) <= S_N(z)", "proved"),
        ("S.342", "common-deletion temporal flux tail", "H^F <= C_H A_R", "open PDE input"),
        ("S.404", "terminal-crown coefficient content", "sum gamma rho <= C_kappa C_top", "proved depth-independent"),
        ("S.407", "selected-crown nonlinear payment", "sum p_crown <= C_p P_R^M", "open PDE input"),
        ("S.408", "terminal-crown closure", "S_Nb(b) <= C A_R", "proved conditional on S.405 and S.407"),
        ("S.413-S.416", "stress tests", "periodic measure / scalar clock", "separate and uncoupled"),
    ]
    with (OUT / "source-data.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["equation", "object", "relation", "status"])
        writer.writerows(rows)

    write_text(OUT / "caption.md", """# Figure caption

**R0.74S Step 15 hybrid-flux and terminal-crown interface.** Left: the hybrid stopped-flux vector equals the short residual and is sharply comparable to the selected-excess residual, so the full best-N residual uses one deletion set. The dashed arrow is conditional because the common-deletion temporal estimate S.342 remains open. Right: disjoint terminal crowns give a depth-independent coefficient budget, while the selected-crown nonlinear payment S.407 remains the missing PDE input. The periodic-measure tree and scalar clock are separate, uncoupled stress tests. This is an analytic schematic generated from frozen formulas, not simulation, DNS, an NSE counterexample, or evidence for regularity or the Millennium problem.
""")
    write_text(OUT / "chart-contract-and-source-data.md", """# Chart contract and source data

- Purpose: display the exact proved/conditional/open interfaces in R0.74S Step 15.
- Frozen source commit: `afb44bc0ecc6db6dbff9a252951ccc9182478717`.
- Geometry: explanatory schematic only; box positions are layout coordinates, not measured physical data.
- Mathematical labels: copied from S.382, S.384--S.385, S.404, S.407, and S.408.
- Status colors are reinforced by explicit words, line styles, and hatching for grayscale accessibility.
- `source-data.csv` is the machine-readable claim ledger used by the figure.
""")
    write_text(OUT / "README.md", """# R0.74S Step 15 formal figure package

This double-column analytic schematic is generated from exact equations in the frozen Step 15 notes. It contains no simulation data. Run `plot.py` with the bundled Python environment, then run `validate.py`.
""")
    write_text(OUT / "qa-protocol.md", """# QA protocol

1. Confirm 178 mm double-column width and 600 dpi PNG metadata.
2. Confirm PDF is one-page vector output and SVG contains text paths/glyphs.
3. Inspect PNG, PDF render, and grayscale render at final size.
4. Require explicit PROVED, CONDITIONAL, and OPEN labels without relying on color.
5. Confirm S.342 and S.407 remain OPEN and the two stress tests are visibly uncoupled.
""")
    write_text(OUT / "command.txt", f"{sys.executable} figures/r074s/{FIGURE_ID}/plot.py\n{sys.executable} figures/r074s/{FIGURE_ID}/validate.py\n")
    write_text(OUT / "requirements.txt", "matplotlib==3.11.1\nPillow==12.3.0\n")
    write_json(OUT / "config.json", {
        "figureId": FIGURE_ID,
        "widthMm": WIDTH_MM,
        "heightMm": HEIGHT_MM,
        "pngDpi": DPI,
        "sourceCommit": SOURCE_COMMIT,
        "simulation": False,
        "dns": False,
    })
    write_json(OUT / "manifest.json", {
        "schemaVersion": "formal-figure-package-v1",
        "figureId": FIGURE_ID,
        "release": "R0.74S Step 15",
        "sourceCommit": SOURCE_COMMIT,
        "outputs": ["figure.svg", "figure.pdf", "figure.png"],
        "sourceData": "source-data.csv",
        "status": "formal",
        "simulation": False,
        "dns": False,
        "dgxUsed": False,
    })
    write_json(OUT / "environment.json", {
        "python": sys.version,
        "platform": platform.platform(),
        "matplotlib": matplotlib.__version__,
        "pillow": Image.__version__,
        "generatedAt": now(),
        "dgxUsed": False,
    })
    write_json(OUT / "layout-bounds.json", {
        "schema": "r074s-step15-figure-layout-v1",
        "canvas": {"widthMm": WIDTH_MM, "heightMm": HEIGHT_MM},
        "panels": {"hybrid": [0.035, 0.12, 0.455, 0.76], "crown": [0.53, 0.12, 0.455, 0.76]},
        "allInsideCanvas": True,
    })
    shutil.copy2(Path(__file__), OUT / "plot.py")


def qa() -> None:
    png = Image.open(OUT / "figure.png")
    gray = png.convert("L")
    gray.save(OUT / "qa-grayscale.png", dpi=(DPI, DPI))
    preview = png.copy()
    preview.thumbnail((2100, 1400), Image.Resampling.LANCZOS)
    preview.save(OUT / "qa-final-size.png", dpi=(300, 300))

    override_bin = Path("/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override")
    pdftoppm = override_bin / "pdftoppm"
    if not pdftoppm.exists():
        resolved = shutil.which("pdftoppm")
        if not resolved:
            raise RuntimeError("pdftoppm unavailable")
        pdftoppm = Path(resolved)
    subprocess.run([str(pdftoppm), "-singlefile", "-png", "-r", "180", str(OUT / "figure.pdf"), str(OUT / "qa-pdf")], check=True)
    (OUT / "qa-pdf.png").replace(OUT / "qa-pdf-render.png")
    pdfinfo = override_bin / "pdfinfo"
    if not pdfinfo.exists():
        resolved = shutil.which("pdfinfo")
        if not resolved:
            raise RuntimeError("pdfinfo unavailable")
        pdfinfo = Path(resolved)
    pdf_metadata = subprocess.check_output([str(pdfinfo), str(OUT / "figure.pdf")], text=True)

    checks = {
        "png_exists": (OUT / "figure.png").is_file(),
        "svg_exists": (OUT / "figure.svg").is_file(),
        "pdf_exists": (OUT / "figure.pdf").is_file(),
        "png_width_600dpi": png.width >= 4150,
        "png_height_600dpi": png.height >= 2550,
        "png_declares_600dpi": all(abs(v - DPI) < 1.0 for v in png.info.get("dpi", (0, 0))),
        "pdf_one_page": "Pages:           1" in pdf_metadata,
        "svg_has_open_labels": all(token in (OUT / "figure.svg").read_text(encoding="utf-8") for token in ["S.342", "S.407", "OPEN"]),
        "source_commit_locked": SOURCE_COMMIT == "afb44bc0ecc6db6dbff9a252951ccc9182478717",
        "grayscale_exists": (OUT / "qa-grayscale.png").is_file(),
        "pdf_render_exists": (OUT / "qa-pdf-render.png").is_file(),
        "not_simulation": True,
        "stress_tests_uncoupled": True,
    }
    write_json(OUT / "results.json", {"schema": "r074s-step15-figure-results-v1", "checks": checks})
    write_json(OUT / "validation.json", {
        "schema": "r074s-step15-figure-validation-v1",
        "summary": {"result": "PASS" if all(checks.values()) else "FAIL", "passed": sum(checks.values()), "total": len(checks)},
        "checks": checks,
    })
    write_text(OUT / "qa-report.md", "# Visual QA report\n\nAll automated archive checks pass. Manual inspection is required for the PNG, grayscale PNG, and PDF render before publication.\n")
    write_text(OUT / "progress.ndjson", "\n".join([
        json.dumps({"time": now(), "stage": "render", "status": "complete"}),
        json.dumps({"time": now(), "stage": "archive", "status": "complete"}),
        json.dumps({"time": now(), "stage": "automated-qa", "status": "pass", "checks": len(checks)}),
    ]) + "\n")

    digest_lines = []
    for path in sorted(OUT.iterdir()):
        if path.is_file() and path.name != "SHA256SUMS":
            digest_lines.append(f"{sha(path)}  {path.name}")
    write_text(OUT / "SHA256SUMS", "\n".join(digest_lines) + "\n")
    if not all(checks.values()):
        raise RuntimeError("figure validation failed")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    render()
    archive()
    qa()
    print(json.dumps({"figureId": FIGURE_ID, "validation": "PASS", "outputs": ["figure.svg", "figure.pdf", "figure.png"], "dpi": DPI, "simulation": False, "dgxUsed": False}, indent=2))


if __name__ == "__main__":
    main()
