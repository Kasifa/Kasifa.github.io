#!/usr/bin/env python3
"""Generate the deterministic R0.74C three-panel journal package."""
from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle
from PIL import Image, ImageOps
import pypdfium2 as pdfium


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SOURCE_COMMIT = "d6c59e31c4a10800a1e091390a25ad5672dc17d5"
SOURCE_NOTE = "research/r074c_advected_shear_large_payment_obstruction.md"
SOURCE_SHA = "b300e7c32f9d944be36813530c5ffd1d7bc7463d161bba829284b4ab2d3e2c09"
CERTIFICATE = "research/r074c_advected_shear_certificate.json"
CERTIFICATE_SHA = "96e58ab63941d26afa0b5df8bf66f61e2b8698c2a314679d115e83a5dceb45d1"
FROZEN_UTC = "2026-09-01T00:00:00+00:00"

NAVY = "#174A7E"
BLUE = "#DCEAF5"
GREY = "#555B63"
LIGHT = "#F4F5F6"
RED = "#B64635"
AMBER = "#B98217"
GREEN = "#367342"
PURPLE = "#765A9A"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def rounded_box(ax, x, y, w, h, text, *, edge=NAVY, face="white", fs=6.4,
                lw=0.8, linestyle="-", weight="normal", align="center"):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        edgecolor=edge, facecolor=face, linewidth=lw, linestyle=linestyle,
    )
    ax.add_patch(patch)
    tx = x + w / 2 if align == "center" else x + 0.025
    ax.text(tx, y + h / 2, text, ha=align, va="center", fontsize=fs,
            color="#20242A", fontweight=weight, linespacing=1.25)


def arrow(ax, start, end, *, color=NAVY, linestyle="-", lw=0.9, scale=8):
    ax.add_patch(FancyArrowPatch(
        start, end, arrowstyle="-|>", mutation_scale=scale,
        linewidth=lw, color=color, linestyle=linestyle,
    ))


def badge(ax, x, y, text, color, *, linestyle="-", fs=6.1):
    ax.text(
        x, y, text, ha="left", va="center", fontsize=fs, fontweight="bold",
        color=color,
        bbox=dict(boxstyle="round,pad=.18", fc="white", ec=color,
                  lw=.7, ls=linestyle),
    )


def source_rows() -> list[list[object]]:
    return [
        ["A", "geometry", "fixed core", "|x| < 8R", "local buffer", "proved", "not to scale"],
        ["A", "geometry", "target annulus", "(2/3)MR <= |x| < (4/3)MR", "A_m(R)", "proved", "M=3*2^(m-1)"],
        ["A", "trajectory", "entrance centre", "q(t_-)=q*=1/2", "remote strip", "proved", "local buffer sees Gaussian tail"],
        ["A", "trajectory", "endpoint centre", "q(t_0)=MR", "target strip", "proved", "strong derivative-kernel strip"],
        ["A", "local leakage", "quadratic", "A^2 R^2 Pi(M) exp(-M^2/264)", "payment row", "proved", "strictly faster decay than target weight"],
        ["A", "target", "lower bound", "A^2 M^2 R^2 exp(-M^2/288)", "X_R lower bound", "proved", "positive-measure endpoint interval"],
        ["B", "payment", "constant background", "R^(-2)", "P_R^(2/3)", "proved", "ratio after substitution: M^2"],
        ["B", "payment", "local heat leakage", "A^2 R^2 Pi(M) exp(-M^2/264)", "P_R^(2/3)", "proved", "ratio: M^2/Pi(M) exp(M^2(1/264-1/288))"],
        ["B", "payment", "exterior residence", "A^2 R^(8/3) M^(-2/3)", "P_R^(2/3)", "proved", "ratio: M^(8/3) exp(M^2/288)"],
        ["B", "sequence", "radius", "R=exp(-M^2/96)", "test sequence", "proved", "M tends to infinity"],
        ["B", "sequence", "amplitude", "A=R^(-2) exp(M^2/576)", "test sequence", "proved", "finite for each M"],
        ["B", "conclusion", "fixed-centre endpoint", "X_R/P_R^(2/3) -> infinity", "theorem", "proved", "exact smooth periodic NSE"],
        ["C", "boundary", "fixed centre", "pure P^(2/3) endpoint fails", "negative theorem", "proved", "specific frozen R0.74B ledger"],
        ["C", "boundary", "co-moving mean subtraction", "present family becomes non-advected", "mechanism test", "proved", "removes this counterexample only"],
        ["C", "boundary", "co-moving pure closure", "unknown", "revised positive question", "open", "no theorem claimed"],
        ["C", "literature", "witness class and moving/skewed frames", "known frameworks", "prior art", "bounded statement", "no priority claim"],
        ["C", "scope", "Millennium problem", "unresolved", "not a Clay result", "boundary", "no regularity or blow-up theorem"],
    ]


def draw() -> None:
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "pdf.fonttype": 42,
        "svg.fonttype": "none",
        "svg.hashsalt": "r074c-d6c59e31-b300e7c3",
    })
    fig = plt.figure(figsize=(180 / 25.4, 82 / 25.4), dpi=600, facecolor="white")
    grid = fig.add_gridspec(1, 3, left=.024, right=.985, bottom=.105, top=.91, wspace=.075)
    axes = [fig.add_subplot(grid[0, index]) for index in range(3)]
    for index, ax in enumerate(axes):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.text(0, 1.035, chr(65 + index), fontsize=10, fontweight="bold", va="top")

    # Panel A: exact transport geometry, deliberately schematic across an axis break.
    ax = axes[0]
    ax.text(.08, 1.02, "Advected strip / fixed centre", fontsize=7.7,
            fontweight="bold", va="top")
    badge(ax, .69, .96, "EXACT NSE", NAVY)
    y_axis = .48
    ax.plot([.07, .93], [y_axis, y_axis], color="#30343A", lw=.7)
    arrow(ax, (.91, y_axis), (.09, y_axis), color=PURPLE, lw=1.2, scale=9)
    ax.text(.50, .525, "constant transport V", ha="center", fontsize=6.2, color=PURPLE)

    # Fixed centre and nested buffer.
    ax.add_patch(Rectangle((.08, .39), .12, .18, fc=LIGHT, ec=GREY, lw=.7))
    ax.add_patch(Rectangle((.095, .415), .035, .13, fc="#DDE1E5", ec=GREY, lw=.6))
    ax.text(.14, .345, "fixed x₀\nB₂R ⊂ B₈R", ha="center", va="top", fontsize=6.1)
    ax.text(.14, .605, "Gaussian tail only", ha="center", fontsize=6.1, color=GREY)

    # Endpoint annular band and derivative heat-kernel strip.
    ax.add_patch(Rectangle((.39, .35), .30, .26, fc="#FFF3DA", ec=AMBER,
                           lw=.7, hatch="///"))
    ax.text(.57, .315, "Aₘ(R): ⅔MR ≤ |x| < ⁴⁄₃MR", ha="center", fontsize=6.0)
    ax.add_patch(Rectangle((.515, .37), .044, .22, fc=BLUE, ec=NAVY, lw=.9))
    ax.plot([.537, .537], [.38, .58], color=NAVY, lw=1.3)
    ax.text(.537, .635, "q(t₀)=MR", ha="center", fontsize=6.3, color=NAVY)
    ax.text(.537, .235, "strong |∂₂Kᵖᵉʳ| strip", ha="center", fontsize=6.1, color=NAVY)

    # Entrance marker beyond a visible scale break.
    ax.plot([.735, .755], [.455, .505], color=GREY, lw=.8)
    ax.plot([.755, .775], [.455, .505], color=GREY, lw=.8)
    ax.add_patch(Rectangle((.855, .37), .045, .22, fc="#E9E2F1", ec=PURPLE, lw=.9))
    ax.text(.878, .635, "q(t₋)=q*=½", ha="center", fontsize=6.2, color=PURPLE)
    ax.text(.755, .43, "axis break", ha="center", fontsize=6.0, color=GREY)

    rounded_box(ax, .07, .065, .86, .13,
                "B₈R leakage: A²R²Π(M) exp(−M²/264)\n"
                "target: A²M²R² exp(−M²/288)\n"
                "schematic geometry; no DNS",
                edge=NAVY, face=BLUE, fs=6.05)
    badge(ax, .07, .018, "PROVED", GREEN)
    badge(ax, .35, .018, "ALL PERIODIC COPIES", GREY, linestyle="--", fs=6.0)

    # Panel B: the exact exponent / power ledger.
    ax = axes[1]
    ax.text(.08, 1.02, "Three losing payment rows", fontsize=7.7,
            fontweight="bold", va="top")
    badge(ax, .70, .96, "ANALYTIC", NAVY)
    rounded_box(ax, .06, .80, .88, .10,
                "Target L = A²M²R² exp(−M²/288)",
                edge=NAVY, face=BLUE, fs=6.8, weight="bold")
    ax.text(.06, .755, "P²ᐟ³ upper rows", fontsize=6.2, fontweight="bold", color=GREY)

    row_specs = [
        (.62, "background", "R⁻²", "L / row = M²  → ∞", GREEN),
        (.46, "local heat tail", "A²R²Π(M) exp(−M²/264)",
         "L / row = [M²/Π(M)] exp[M²(1/264−1/288)]  → ∞", GREEN),
        (.30, "exterior residence", "A²R⁸ᐟ³M⁻²ᐟ³",
         "L / row = M⁸ᐟ³ exp(M²/288)  → ∞", GREEN),
    ]
    for y, title, formula, ratio, color in row_specs:
        rounded_box(ax, .05, y, .90, .115, f"{title}:  {formula}\n{ratio}",
                    edge=color, face="#EFF6F0", fs=6.05, align="left")
    rounded_box(ax, .10, .13, .80, .10,
                "R = exp(−M²/96)\nA = R⁻² exp(M²/576)",
                edge=PURPLE, face="#F2EEF7", fs=6.15)
    rounded_box(ax, .14, .025, .72, .075,
                "X_R / P_R²ᐟ³  → ∞  as M → ∞",
                edge=RED, face="#FAECE8", fs=7.0, weight="bold")

    # Panel C: exact conclusion and the intentionally open boundary.
    ax = axes[2]
    ax.text(.08, 1.02, "Fixed vs co-moving endpoint", fontsize=7.45,
            fontweight="bold", va="top")
    badge(ax, .70, .96, "SCOPE", GREY)
    rounded_box(ax, .07, .78, .86, .11,
                "FIXED CENTRE\nDelete +P from frozen R0.74B endpoint",
                edge=RED, face="#FAECE8", fs=6.5)
    arrow(ax, (.50, .78), (.50, .705), color=RED)
    rounded_box(ax, .18, .61, .64, .085,
                "FAILS — exact NSE witness",
                edge=RED, face="white", fs=6.8, weight="bold")

    rounded_box(ax, .06, .435, .88, .105,
                "MEAN-SUBTRACTED CO-MOVING FRAME\n"
                "u−ū,  x_c(t)=x₀+ū(t−t₀)",
                edge=NAVY, face=BLUE, fs=6.25)
    arrow(ax, (.50, .61), (.50, .54), color=NAVY)
    rounded_box(ax, .07, .265, .86, .12,
                "Present family becomes non-advected.\n"
                "This obstruction is neutralized;\n"
                "the closure problem is not solved.",
                edge=GREEN, face="#EFF6F0", fs=6.0)
    arrow(ax, (.50, .435), (.50, .375), color=GREEN)
    rounded_box(ax, .12, .13, .76, .075,
                "Pure co-moving P²ᐟ³ closure: OPEN",
                edge=AMBER, face="#FFF6E5", fs=6.65, weight="bold")
    arrow(ax, (.50, .265), (.50, .205), color=AMBER)
    ax.text(.50, .09, "Witness + moving frames are prior art; no priority claim.",
            ha="center", fontsize=6.0, color=GREY)
    badge(ax, .06, .025, "OPEN", AMBER)
    badge(ax, .35, .025, "NOT CLAY", GREY)
    badge(ax, .68, .025, "NO DNS", GREY, linestyle="--")

    fig.text(
        .5, .035,
        "Exact smooth periodic NSE family • deterministic proof schematic • unknown constants are not encoded numerically",
        ha="center", fontsize=6.25, color=GREY,
    )

    fixed_dt = datetime(2026, 9, 1, tzinfo=timezone.utc)
    fig.savefig(
        HERE / "figure.svg",
        metadata={"Date": FROZEN_UTC,
                  "Description": f"SourceCommit={SOURCE_COMMIT}; SourceSHA256={SOURCE_SHA}"},
    )
    fig.savefig(
        HERE / "figure.pdf",
        metadata={"Title": "R0.74C advected-shear obstruction",
                  "Subject": f"{SOURCE_COMMIT}; {SOURCE_SHA}",
                  "CreationDate": fixed_dt, "ModDate": fixed_dt},
    )
    fig.savefig(HERE / "figure.png", dpi=600)
    plt.close(fig)

    svg_path = HERE / "figure.svg"
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines()) + "\n",
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
    source.resize((2126, 969), Image.Resampling.LANCZOS).save(HERE / "qa-final-size.png")
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
    assert certificate["status"] == "PASS"
    assert certificate["summary"] == {"passed": 83, "total": 83}

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
        "figureId": "fig-r074c-advected-shear-obstruction",
        "panels": ["A", "B", "C"],
        "sourceCommit": SOURCE_COMMIT,
        "sourceNoteSha256": SOURCE_SHA,
        "unknownConstantsNumericallyEncoded": False,
    }
    contract = {
        "certificate": {"checks": "83/83", "schemaVersion": 1,
                        "sha256": CERTIFICATE_SHA},
        "expectedFileCount": 25,
        "figureClaims": {
            "A": "Exact advected derivative-periodic-heat-kernel geometry; schematic, not DNS.",
            "B": "Frozen lower bound and the three P^(2/3) payment comparisons.",
            "C": "Fixed-centre failure, present-obstruction neutralization, and open co-moving closure.",
        },
        "schema": "r074c-figure-contract-v1",
        "sourceCommit": SOURCE_COMMIT,
        "sourceNoteSha256": SOURCE_SHA,
        "statuses": ["PROVED", "EXACT NSE", "OPEN", "PRIOR ART", "NOT CLAY", "NO DNS"],
    }
    (HERE / "config.json").write_text(canonical(config), encoding="utf-8")
    (HERE / "contract.json").write_text(canonical(contract), encoding="utf-8")
    (HERE / "caption.md").write_text(
        "Figure X. Advected-shear obstruction to the frozen R0.74B large-payment endpoint. "
        "(A) An exact derivative-periodic-heat-kernel strip is transported by a large constant mean velocity from a remote entrance position to the fixed-centre target annulus; the buffered local ball sees only its Gaussian tail. "
        "(B) With R=exp(-M^2/96) and A=R^(-2)exp(M^2/576), the target lower bound dominates separately the constant-background, local-leakage, and exterior-residence rows of P_R^(2/3). Hence X_R/P_R^(2/3) tends to infinity along exact smooth periodic Navier--Stokes solutions. "
        "(C) This disproves only deletion of +P in the frozen fixed-centre endpoint. Mean subtraction and a co-moving centre neutralize this particular construction; whether a pure co-moving P^(2/3) closure holds remains OPEN. The exact transverse-wave witness class and moving/skewed frames are prior art. No DNS. NOT CLAY.\n",
        encoding="utf-8",
    )
    (HERE / "README.md").write_text(
        "# R0.74C advected-shear obstruction figure\n\n"
        f"Reproducible 25-file journal package frozen to analytic commit {SOURCE_COMMIT}. "
        "Run `plot.py`, then `validate.py`; `command.txt` performs the two-run byte audit.\n",
        encoding="utf-8",
    )
    (HERE / "chart-contract-and-source-data.md").write_text(
        "# Chart contract and source data\n\n"
        "`source-data.csv` records every geometry, exponent, power, asymptotic ratio, and scope statement shown in the figure. Panel A uses an explicit axis break and is a proof schematic, not a scaled numerical trajectory. Panel B records symbolic analytic comparisons only. Panel C separates the proved fixed-centre no-go, neutralization of this one mechanism, prior art, and the still-open positive question. Unknown constants are labels only and are never plotted as data.\n",
        encoding="utf-8",
    )
    (HERE / "qa-protocol.md").write_text(
        "# QA protocol\n\n"
        "Verify the analytic commit, note hash, certificate hash and 83/83 status; exact 25-file inventory; 180 x 82 mm one-page PDF; approximately 600 dpi master PNG; embedded PDF fonts; SVG text with no raster image; base label size at least 6 pt; complete panel/status phrases; 17 closed-form source rows; grayscale and final-size legibility; and explicit no-DNS, prior-art, OPEN, and NOT CLAY boundaries. Run generation and validation twice and compare every byte.\n",
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
        canonical({"cpuOnly": True, "dgxUsed": False, "dns": False,
                   "simulation": False}).strip() + "\n",
        encoding="utf-8",
    )
    (HERE / "results.json").write_text(canonical({
        "certificateSha256": CERTIFICATE_SHA,
        "rows": len(rows),
        "sourceCommit": SOURCE_COMMIT,
        "sourceNoteSha256": SOURCE_SHA,
        "status": "PREVALIDATION",
    }), encoding="utf-8")
    (HERE / "qa-report.md").write_text("# QA report\n\nPending validator.\n", encoding="utf-8")
    (HERE / "validation.json").write_text(canonical({"status": "PENDING"}), encoding="utf-8")
    (HERE / "manifest.json").write_text(canonical({
        "certificateSha256": CERTIFICATE_SHA,
        "figureId": config["figureId"],
        "files": [],
        "sourceCommit": SOURCE_COMMIT,
        "sourceNoteSha256": SOURCE_SHA,
    }), encoding="utf-8")
    (HERE / "SHA256SUMS").write_text("", encoding="utf-8")


if __name__ == "__main__":
    write_package()
    draw()
    render_qa()
