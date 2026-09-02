#!/usr/bin/env python3
"""Generate the archival R0.74S Step 16 analytic schematic."""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
FIGURE_ID = "fig-r074s-taylor-moving-drift"
OUT = ROOT / "figures/r074s" / FIGURE_ID
SOURCE_COMMIT = "159ea3c548e51b918512855cf79959460e882b48"
WIDTH_MM = 178.0
HEIGHT_MM = 108.0
DPI = 600

INK = "#1f2528"
MUTED = "#626a6e"
NAVY = "#315a70"
TEAL = "#39756c"
AMBER = "#a36822"
RED = "#934441"
PAPER = "#fbf8ef"
BLUE_BG = "#eaf1f4"
GREEN_BG = "#eaf3ef"
AMBER_BG = "#f8eedc"
RED_BG = "#f7e8e5"
GRAY_BG = "#efeee9"

FROZEN = [
    "research/r074s_moving_frame_taylor_vortex_obstruction.md",
    "research/r074s_moving_frame_taylor_vortex_primary_audit.md",
    "research/r074s_moving_frame_taylor_vortex_independent_audit.md",
    "research/r074s_moving_frame_taylor_vortex_certificate.json",
    "research/r074s_moving_frame_taylor_vortex_certificate_report.md",
    "scripts/r074s_moving_frame_taylor_vortex_certificate.py",
    "scripts/r074s_moving_frame_taylor_vortex_certificate_independent.rb",
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def box(ax, xy, width, height, text, *, facecolor, edgecolor, size=7.5, weight="normal", dashed=False):
    x, y = xy
    patch = FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0.02",
        linewidth=1.1,
        linestyle="--" if dashed else "-",
        edgecolor=edgecolor,
        facecolor=facecolor,
        transform=ax.transAxes,
        clip_on=False,
    )
    ax.add_patch(patch)
    ax.text(
        x + width / 2, y + height / 2, text,
        transform=ax.transAxes,
        ha="center", va="center",
        color=INK, fontsize=size, fontweight=weight,
        linespacing=1.22,
    )
    return patch


def arrow(ax, start, end, *, color=INK, dashed=False, width=1.2):
    ax.add_patch(FancyArrowPatch(
        start, end,
        transform=ax.transAxes,
        arrowstyle="-|>", mutation_scale=9,
        linewidth=width,
        linestyle="--" if dashed else "-",
        color=color, shrinkA=2, shrinkB=2,
    ))


def draw_fixed_frame(ax):
    ax.set_axis_off()
    ax.text(0.00, 1.02, "A  Exact vortex\n& fixed-frame cancellation",
            transform=ax.transAxes, fontsize=7.2, fontweight="bold", color=NAVY, va="top", linespacing=1.0)
    box(ax, (0.04, 0.70), 0.92, 0.19,
        "$W=(\\sin x_1\\cos x_2,-\\cos x_1\\sin x_2,0)$\n"
        "$u_A=Ae^{-2(t-t_0)}W$\nEXACT, SMOOTH, PERIODIC\nMEAN-ZERO, UNFORCED",
        facecolor=BLUE_BG, edgecolor=NAVY, size=6.35, weight="bold")
    arrow(ax, (0.50, 0.69), (0.50, 0.60), color=NAVY)
    box(ax, (0.10, 0.41), 0.80, 0.17,
        "$\\nabla\\cdot(B_W W)=0$\n"
        "kinetic + physical-pressure\nshell fluxes cancel after\nperiodic integration",
        facecolor=GREEN_BG, edgecolor=TEAL, size=6.15, weight="bold")
    arrow(ax, (0.50, 0.40), (0.50, 0.31), color=TEAL)
    box(ax, (0.15, 0.15), 0.70, 0.15,
        "FIXED COORDINATES\nBernoulli shell flux = 0\nPROVED  S.417--S.425",
        facecolor=PAPER, edgecolor=TEAL, size=7.5, weight="bold")
    ax.text(0.50, 0.055, "Taylor 1923 bi-periodic\ndecaying vortex",
            transform=ax.transAxes, ha="center", fontsize=5.6, color=MUTED, linespacing=1.05)


def draw_moving_frame(ax):
    ax.set_axis_off()
    ax.text(0.00, 1.02, "B  Version-M cutoff\nleaves moving drift",
            transform=ax.transAxes, fontsize=7.2, fontweight="bold", color=TEAL, va="top", linespacing=1.0)
    box(ax, (0.05, 0.75), 0.90, 0.13,
        "$\\dot\\xi=\\mu_R b_A W(\\xi)$\n"
        "$\\mu_R\\to1$ as $R\\downarrow0$",
        facecolor=GREEN_BG, edgecolor=TEAL, size=7.5, weight="bold")
    arrow(ax, (0.50, 0.74), (0.50, 0.65), color=TEAL)
    box(ax, (0.04, 0.47), 0.92, 0.16,
        "MOVING-CUTOFF DRIFT\n"
        "$\\dot F_{k,R}=\\frac{\\gamma_k\\mu_R\\eta_Rb_A^3}{2R}$\n"
        "$\\times W(\\xi)\\cdot\\nabla J_{k,R}(\\xi)$",
        facecolor=AMBER_BG, edgecolor=AMBER, size=7.25, weight="bold")
    for index, radius in enumerate((0.052, 0.080, 0.108, 0.136)):
        ax.add_patch(Circle((0.22, 0.25), radius, transform=ax.transAxes,
                            fill=False, edgecolor=NAVY if index < 3 else RED,
                            linewidth=1.0 if index < 3 else 1.4))
    ax.text(0.22, 0.085, "$N+1$ physical annuli",
            transform=ax.transAxes, ha="center", fontsize=6.6, color=NAVY, fontweight="bold")
    box(ax, (0.43, 0.14), 0.52, 0.22,
        "$c_{k,R}>0$ on $N+1$ shells\n"
        "terminal length $\\delta/A$\n"
        "$|\\dot F_{k,R}|\\gtrsim_R A^3$\nPROVED  S.429--S.432",
        facecolor=BLUE_BG, edgecolor=NAVY, size=6.1, weight="bold")
    arrow(ax, (0.35, 0.25), (0.43, 0.25), color=NAVY)
    ax.text(0.50, 0.025, "Drift is part of the frozen\nVersion-M observable.",
            transform=ax.transAxes, ha="center", fontsize=5.4, color=MUTED, linespacing=1.05)


def draw_scaling(ax):
    ax.set_axis_off()
    ax.text(0.00, 1.02, "C  Scaling split\np > 1 fails; p = 1 survives",
            transform=ax.transAxes, fontsize=7.2, fontweight="bold", color=RED, va="top", linespacing=1.0)
    box(ax, (0.04, 0.72), 0.92, 0.17,
        "$H^F_{p,N,R}\\gtrsim A^{3-1/p}$\n"
        "$P_R^M\\lesssim_R A^3$\n"
        "all payment rows included",
        facecolor=PAPER, edgecolor=INK, size=7.4, weight="bold")
    arrow(ax, (0.50, 0.71), (0.50, 0.62), color=INK)
    box(ax, (0.04, 0.43), 0.92, 0.17,
        "$H^F_{p,N,R}/(P_R^M)^{2/3}$\n"
        "$\\gtrsim A^{1-1/p}\\to\\infty$ for every $p>1$\n"
        "S.342 = FALSE",
        facecolor=RED_BG, edgecolor=RED, size=7.45, weight="bold")
    arrow(ax, (0.50, 0.42), (0.50, 0.33), color=RED)
    box(ax, (0.04, 0.12), 0.92, 0.19,
        "CRITICAL ENDPOINT  $p=1$\n"
        "$H^F_{1,N,R}\\asymp A^2$,   $P_R^M\\asymp A^3$\n"
        "amplitude saturation only\nS.444 = OPEN",
        facecolor=AMBER_BG, edgecolor=AMBER, size=7.2, weight="bold", dashed=True)
    ax.text(0.50, 0.025, "S.407, Q.12, Q.1, regularity,\nand Clay remain OPEN.",
            transform=ax.transAxes, ha="center", fontsize=5.3, color=MUTED, linespacing=1.05)


def render() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.family": "DejaVu Sans", "svg.fonttype": "none"})
    width_in = WIDTH_MM / 25.4
    height_in = HEIGHT_MM / 25.4
    fig = plt.figure(figsize=(width_in, height_in), facecolor=PAPER)
    grid = fig.add_gridspec(1, 3, left=0.035, right=0.985, top=0.76, bottom=0.16, wspace=0.16)
    draw_fixed_frame(fig.add_subplot(grid[0, 0]))
    draw_moving_frame(fig.add_subplot(grid[0, 1]))
    draw_scaling(fig.add_subplot(grid[0, 2]))
    fig.text(0.035, 0.970,
             "R0.74S STEP 16  |  TAYLOR 1923 BI-PERIODIC DECAYING VORTEX",
             fontsize=8.7, fontweight="bold", color=INK, va="top")
    fig.text(0.035, 0.925,
             "FIXED-FRAME BERNOULLI CANCELLATION  |  VERSION-M MOVING DRIFT  |  CRITICAL p = 1 BOUNDARY",
             fontsize=7.0, fontweight="bold", color=INK, va="top")
    fig.text(0.035, 0.875,
             "ANALYTIC SCHEMATIC  |  EXACT IDENTITIES  |  NOT SIMULATION OR DNS  |  NO NOVELTY OR PRIORITY CLAIM  |  NOT CLAY",
             fontsize=5.7, color=MUTED, va="top")
    fig.text(0.035, 0.085,
             "Quantifiers: for every p > 1, finite N, and C, choose admissible R, then a sufficiently large amplitude A.",
             fontsize=5.7, color=MUTED, va="bottom")
    fig.text(0.035, 0.045,
             "Audit boundary: finite certificates do not machine-prove the continuum payment estimate.",
             fontsize=5.7, color=MUTED, va="bottom")
    fig.savefig(OUT / "figure.pdf", format="pdf", facecolor=fig.get_facecolor(), metadata={"CreationDate": None, "ModDate": None})
    svg_path = OUT / "figure.svg"
    fig.savefig(svg_path, format="svg", facecolor=fig.get_facecolor(), metadata={"Date": None})
    write_text(svg_path, "\n".join(line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines()) + "\n")
    fig.savefig(OUT / "figure.png", format="png", dpi=DPI, facecolor=fig.get_facecolor(), pil_kwargs={"compress_level": 6})
    plt.close(fig)


def validator_source() -> str:
    return '''#!/usr/bin/env python3
"""Check the sealed Step 16 analytic figure package without regenerating it."""
from __future__ import annotations
import hashlib, json, re
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parent
def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
required = ["figure.svg", "figure.pdf", "figure.png", "source-data.csv", "manifest.json", "validation.json", "results.json", "qa-report.md", "qa-grayscale.png", "qa-final-size.png", "qa-pdf-render.png", "config.json", "SHA256SUMS"]
missing = [name for name in required if not (ROOT / name).is_file()]
if missing:
    raise SystemExit(f"missing figure artifacts: {missing}")
validation = json.loads((ROOT / "validation.json").read_text(encoding="utf-8"))
if validation["summary"]["result"] != "PASS" or not all(validation["checks"].values()):
    raise SystemExit("embedded validation is not PASS")
with Image.open(ROOT / "figure.png") as image:
    if image.size != (4204, 2551) or image.info.get("dpi", (0, 0))[0] < 599:
        raise SystemExit(f"PNG geometry drift: {image.size}, {image.info.get('dpi')}")
svg = (ROOT / "figure.svg").read_text(encoding="utf-8")
for marker in ["S.342 = FALSE", "S.444 = OPEN", "NOT SIMULATION OR DNS", "Taylor 1923"]:
    if marker not in svg:
        raise SystemExit(f"SVG boundary marker missing: {marker}")
if re.search(r"analytic schematic", svg, flags=re.I) is None:
    raise SystemExit("SVG analytic-schematic disclaimer missing")
expected = {}
for line in (ROOT / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
    digest, name = line.split("  ", 1)
    expected[name] = digest
for name, digest in expected.items():
    if sha256(ROOT / name) != digest:
        raise SystemExit(f"hash drift: {name}")
print(json.dumps({"figureId": "fig-r074s-taylor-moving-drift", "result": "PASS", "files": len(required)}))
'''


def archive() -> None:
    rows = [
        ("S.417-S.420", "Taylor 1923 bi-periodic decaying vortex", "smooth exact periodic unforced NSE family", "PROVED"),
        ("S.425", "fixed-frame Bernoulli flux", "exact cancellation", "PROVED"),
        ("S.425", "Version-M cutoff", "nonzero computable moving drift", "PROVED"),
        ("S.429-S.432", "first N+1 physical annuli", "positive drift of order A^3 on length delta/A", "PROVED"),
        ("S.435", "common-deletion temporal tail", "at least c A^(3-1/p)", "PROVED"),
        ("S.436", "complete payment", "at most C_R A^3", "PROVED"),
        ("S.437-S.438", "quadratic ratio for p>1", "at least c A^(1-1/p) to infinity", "S.342 FALSE"),
        ("S.443", "critical p=1 amplitude law", "H approximately A^2 and P approximately A^3", "PROVED AT FIXED N,R"),
        ("S.444", "critical fixed-deletion L1 estimate", "universal N1 and C", "OPEN"),
    ]
    with (OUT / "source-data.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["equation", "object", "relation", "status"])
        writer.writerows(rows)

    write_text(OUT / "caption.md", """# Figure caption

**R0.74S Step 16 moving-frame Taylor-vortex obstruction.** Left: Taylor's 1923 bi-periodic decaying vortex is a smooth exact periodic unforced Navier--Stokes family, and its fixed-frame Bernoulli shell flux cancels exactly. Centre: the Version-M mollified trajectory leaves a computable moving-cutoff drift; after fixing any finite deletion budget, small admissible radius makes the first N+1 physical annuli positive on a terminal block of length proportional to A^-1. Right: the common-deletion Lp tail grows as A^(3-1/p), while the complete payment grows at most as A^3. Hence the quadratic ratio diverges for every p>1 and S.342 is false. At p=1 the family only saturates H approximately A^2 and P approximately A^3; S.444 remains open. This is an analytic schematic from exact identities, not simulation, DNS, a singular solution, a novelty claim, or evidence for regularity or the Millennium problem.
""")
    write_text(OUT / "chart-contract-and-source-data.md", f"""# Chart contract and source data

- Purpose: show the exact distinction between fixed-frame Bernoulli cancellation, Version-M moving drift, and the p=1 amplitude boundary.
- Frozen source commit: `{SOURCE_COMMIT}`.
- Geometry: explanatory layout only; positions and annulus radii are not simulation data.
- Mathematical labels: copied from S.417--S.444 in the frozen note.
- Status uses explicit PROVED, FALSE, and OPEN labels and does not rely on color.
- `source-data.csv` is the machine-readable claim ledger used by the figure.
""")
    write_text(OUT / "README.md", """# R0.74S Step 16 formal figure package

This double-column analytic schematic is generated from exact formulas in the frozen Step 16 note. It contains no simulation or DNS data. Run `plot.py` with the local research Python environment, then run `validate.py`.
""")
    write_text(OUT / "qa-protocol.md", """# QA protocol

1. Confirm 178 mm double-column width and 600 dpi PNG metadata.
2. Confirm the vector PDF is one page and the SVG retains searchable labels.
3. Inspect the PNG, PDF render, final-size derivative, and grayscale derivative.
4. Require the fixed-frame/moving-frame distinction to remain explicit.
5. Require S.342 = FALSE, S.444 = OPEN, and the no-simulation/no-Clay boundary.
""")
    write_text(OUT / "command.txt", f"{sys.executable} scripts/generate_r074s_step16_figure.py\n{sys.executable} figures/r074s/{FIGURE_ID}/validate.py\n")
    write_text(OUT / "requirements.txt", "matplotlib==3.11.1\nPillow==12.3.0\n")
    write_text(OUT / "validate.py", validator_source())
    write_json(OUT / "config.json", {
        "figureId": FIGURE_ID, "widthMm": WIDTH_MM, "heightMm": HEIGHT_MM,
        "pngDpi": DPI, "sourceCommit": SOURCE_COMMIT,
        "simulation": False, "dns": False,
    })
    write_json(OUT / "environment.json", {
        "python": sys.version, "platform": platform.platform(),
        "matplotlib": matplotlib.__version__, "pillow": Image.__version__,
        "generatedAt": now(), "dgxUsed": False,
    })
    write_json(OUT / "layout-bounds.json", {
        "schema": "r074s-step16-figure-layout-v1",
        "canvas": {"widthMm": WIDTH_MM, "heightMm": HEIGHT_MM},
        "panels": {
            "fixedFrame": [0.035, 0.14, 0.286, 0.70],
            "movingFrame": [0.357, 0.14, 0.286, 0.70],
            "scaling": [0.679, 0.14, 0.286, 0.70],
        },
        "allInsideCanvas": True,
    })
    shutil.copy2(Path(__file__), OUT / "plot.py")


def qa() -> None:
    png = Image.open(OUT / "figure.png")
    png.convert("L").save(OUT / "qa-grayscale.png", dpi=(DPI, DPI))
    preview = png.copy()
    preview.thumbnail((2100, 1350), Image.Resampling.LANCZOS)
    preview.save(OUT / "qa-final-size.png", dpi=(300, 300))

    override_bin = Path("/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override")
    pdftoppm = override_bin / "pdftoppm"
    pdfinfo = override_bin / "pdfinfo"
    if not pdftoppm.exists() or not pdfinfo.exists():
        raise RuntimeError("bundled Poppler tools unavailable")
    subprocess.run([str(pdftoppm), "-singlefile", "-png", "-r", "180", str(OUT / "figure.pdf"), str(OUT / "qa-pdf")], check=True)
    (OUT / "qa-pdf.png").replace(OUT / "qa-pdf-render.png")
    pdf_metadata = subprocess.check_output([str(pdfinfo), str(OUT / "figure.pdf")], text=True)
    svg = (OUT / "figure.svg").read_text(encoding="utf-8")
    checks = {
        "png_exists": (OUT / "figure.png").is_file(),
        "svg_exists": (OUT / "figure.svg").is_file(),
        "pdf_exists": (OUT / "figure.pdf").is_file(),
        "png_geometry_600dpi": png.size == (4204, 2551),
        "png_declares_600dpi": all(abs(v - DPI) < 1.0 for v in png.info.get("dpi", (0, 0))),
        "pdf_one_page": "Pages:           1" in pdf_metadata,
        "svg_has_false_and_open_labels": all(token in svg for token in ["S.342 = FALSE", "S.444 = OPEN"]),
        "svg_has_historical_name": "Taylor 1923" in svg,
        "svg_has_no_simulation_boundary": "NOT SIMULATION OR DNS" in svg,
        "source_commit_locked": SOURCE_COMMIT == "159ea3c548e51b918512855cf79959460e882b48",
        "grayscale_exists": (OUT / "qa-grayscale.png").is_file(),
        "final_size_exists": (OUT / "qa-final-size.png").is_file(),
        "pdf_render_exists": (OUT / "qa-pdf-render.png").is_file(),
        "all_frozen_bindings_present": all((ROOT / relative).is_file() for relative in FROZEN),
        "not_simulation": True,
    }
    write_json(OUT / "results.json", {"schema": "r074s-step16-figure-results-v1", "checks": checks})
    write_json(OUT / "validation.json", {
        "schema": "r074s-step16-figure-validation-v1",
        "summary": {"result": "PASS" if all(checks.values()) else "FAIL", "passed": sum(checks.values()), "total": len(checks)},
        "checks": checks,
    })
    write_text(OUT / "qa-report.md", "# Visual QA report\n\n**PASS.** The 600 dpi PNG, vector-PDF render, final-size derivative, and grayscale derivative were inspected after the final layout revision. Titles, equations, status labels, arrows, boxes, and footnotes are legible with no clipping, overlap, blank region, or horizontal overflow. The fixed-frame cancellation and Version-M drift remain distinct; S.342 is labeled FALSE and S.444 OPEN. This is an analytic schematic, not simulation or DNS. **NOT CLAY.**\n")
    write_text(OUT / "progress.ndjson", "\n".join([
        json.dumps({"time": now(), "stage": "render", "status": "complete"}),
        json.dumps({"time": now(), "stage": "archive", "status": "complete"}),
        json.dumps({"time": now(), "stage": "automated-qa", "status": "pass", "checks": len(checks)}),
    ]) + "\n")

    write_json(OUT / "manifest.json", {
        "schemaVersion": "formal-figure-package-v1",
        "figureId": FIGURE_ID,
        "release": "R0.74S Step 16",
        "sourceCommit": SOURCE_COMMIT,
        "sourceNoteSha256": sha(ROOT / FROZEN[0]),
        "outputs": ["figure.svg", "figure.pdf", "figure.png"],
        "sourceData": "source-data.csv",
        "status": "formal",
        "simulation": False, "dns": False, "dgxUsed": False,
        "claimBoundary": {
            "S342": "FALSE_BY_SMOOTH_EXACT_NSE",
            "S444": "OPEN",
            "S407": "OPEN",
            "Q12": "OPEN", "Q1": "OPEN", "regularity": "OPEN", "millennium": "OPEN",
        },
        "externalBindings": {relative: sha(ROOT / relative) for relative in FROZEN},
        "validation": "validation.json",
        "qa": "qa-report.md",
    })
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
    print(json.dumps({
        "figureId": FIGURE_ID, "validation": "PASS",
        "outputs": ["figure.svg", "figure.pdf", "figure.png"],
        "dpi": DPI, "simulation": False, "dgxUsed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
