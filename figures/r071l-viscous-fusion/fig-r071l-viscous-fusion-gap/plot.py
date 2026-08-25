#!/usr/bin/env python3
"""Plot the R0.71L viscous-fusion figure at journal size."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


NAVY = "#24435f"
RUST = "#a45136"
GOLD = "#b49045"
GREEN = "#4f745e"
INK = "#28231f"
GRAY = "#77716a"
PAPER = "#faf7f0"
GRID = "#d8d1c7"


def load(path):
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    grouped = {}
    for row in rows:
        grouped.setdefault((row["panel"], row["series"]), []).append(row)
    for selected in grouped.values():
        selected.sort(key=lambda row: float(row["x"]))
    return grouped


def values(grouped, panel, series):
    selected = grouped[(panel, series)]
    return np.array([float(row["x"]) for row in selected]), np.array([float(row["value"]) for row in selected])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("data.csv"))
    parser.add_argument("--output-stem", type=Path, default=Path("figure"))
    args = parser.parse_args()
    grouped = load(args.data)
    mpl.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 7.2,
        "axes.titlesize": 8.2,
        "axes.labelsize": 7.2,
        "legend.fontsize": 6.4,
        "xtick.labelsize": 6.4,
        "ytick.labelsize": 6.4,
        "axes.edgecolor": GRAY,
        "axes.labelcolor": INK,
        "xtick.color": INK,
        "ytick.color": INK,
        "text.color": INK,
        "axes.facecolor": PAPER,
        "figure.facecolor": PAPER,
        "savefig.facecolor": PAPER,
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
    })
    fig = plt.figure(figsize=(178 / 25.4, 112 / 25.4))
    fig.set_size_inches(178 / 25.4, 112 / 25.4, forward=False)
    grid = fig.add_gridspec(2, 2, left=0.08, right=0.975, bottom=0.17, top=0.87, wspace=0.36, hspace=0.56)
    ax_a, ax_b, ax_c, ax_d = [fig.add_subplot(grid[index // 2, index % 2]) for index in range(4)]
    fig.text(0.08, 0.955, "R0.71L  /  fixed-cell viscous fusion and the unpaid projective tangent", fontsize=10.1, fontweight="bold", color=INK)
    fig.text(0.08, 0.922, "Exact algebra · deterministic diagnostic · mixed-evidence scale ledger · no DNS", fontsize=6.8, color=GRAY)

    for series, color, style, label in (
        ("localizedLaplacian", NAVY, "-", r"localized $(\Delta+1)C$"),
        ("rawCollarContribution", RUST, "--", r"raw collar contribution"),
        ("fusedViscous", INK, ":", r"fused sum"),
    ):
        x, y = values(grouped, "A", series)
        ax_a.plot(x / np.pi, y, color=color, linestyle=style, linewidth=1.25, label=label)
    ax_a.set_title("A   Two nonzero expanded rows cancel exactly", loc="left", fontweight="bold")
    ax_a.set_xlabel(r"normalized position  $x_1/\pi$")
    ax_a.set_ylabel("exact row value")
    ax_a.set_xlim(-1, 1)
    ax_a.grid(axis="y", color=GRID, linewidth=0.5)
    ax_a.legend(frameon=False, ncol=1, loc="upper right")
    ax_a.text(0.02, 0.05, r"$W=(0,\sin x_1,0)$, $\chi=1+\frac{1}{2}\cos x_1$", transform=ax_a.transAxes, fontsize=6.3, bbox=dict(facecolor=PAPER, edgecolor="none", alpha=0.82, pad=0.5))

    rows_b = grouped[("B", "integratedCoefficient")]
    compact_b = {
        "radial": "radial",
        "heat tangent": "heat tan.",
        "raw collar": "collar",
        "fused tangent": "fused tan.",
        "normalization": "normal.",
        "joint source": "joint",
    }
    labels_b = [compact_b[row["category"]] for row in rows_b]
    values_b = np.array([float(row["value"]) for row in rows_b])
    colors_b = [NAVY, GOLD, RUST, GREEN, NAVY, INK]
    bars = ax_b.bar(np.arange(len(rows_b)), values_b, color=colors_b, edgecolor=INK, linewidth=0.45)
    bars[3].set_hatch("//")
    ax_b.axhline(0, color=INK, linewidth=0.7)
    ax_b.set_xticks(np.arange(len(rows_b)), labels_b, rotation=25, ha="right")
    ax_b.tick_params(axis="x", labelsize=5.6, pad=1)
    ax_b.set_ylabel(r"signed coefficient  $(10^{-7}K^{-2})$")
    ax_b.set_title("B   Partial collar cancellation (diagnostic)", loc="left", fontweight="bold", fontsize=7.7)
    ax_b.grid(axis="y", color=GRID, linewidth=0.5)
    ax_b.text(0.02, 0.93, "diagnostic, not a continuous sign proof", transform=ax_b.transAxes, fontsize=6.2, color=GRAY)

    rows_c = grouped[("C", "scalingExponent")]
    compact_c = {
        "local heat": "local heat",
        "positive creation": "positive",
        "raw collar": "collar",
        "fused tangent": "fused tan.",
        "joint source": "joint",
    }
    labels_c = [compact_c[row["category"]] for row in rows_c]
    values_c = np.array([float(row["value"]) for row in rows_c])
    colors_c = [NAVY, RUST, GOLD, GREEN, INK]
    bars_c = ax_c.bar(np.arange(len(rows_c)), values_c, color=colors_c, edgecolor=INK, linewidth=0.45)
    bars_c[2].set_hatch("..")
    bars_c[3].set_hatch("//")
    for bar, value in zip(bars_c, values_c):
        ax_c.text(bar.get_x() + bar.get_width() / 2, value - 0.14, f"{value:+g}", ha="center", va="top", fontsize=6.3, color=PAPER if value < -2.5 else INK)
    ax_c.set_xticks(np.arange(len(rows_c)), labels_c, rotation=24, ha="right")
    ax_c.tick_params(axis="x", labelsize=5.7, pad=1)
    ax_c.set_ylim(-4.8, 0.3)
    ax_c.set_ylabel(r"power of $K$")
    ax_c.set_title("C   Recorded leading scales (mixed evidence)", loc="left", fontweight="bold", fontsize=7.7)
    ax_c.grid(axis="y", color=GRID, linewidth=0.5)
    ax_c.text(
        0.02,
        0.04,
        "heat: analytic upper scale\nfused tan.: diagnostic; no interval sign certificate",
        transform=ax_c.transAxes,
        fontsize=5.5,
        bbox=dict(facecolor=PAPER, edgecolor="none", alpha=0.9, pad=0.8),
    )

    ax_d.set_axis_off()
    ax_d.set_title("D   Direct Leray estimate stops here", loc="left", fontweight="bold", pad=4, fontsize=7.7)
    box = dict(boxstyle="square,pad=0.32", facecolor=PAPER, linewidth=0.8)
    ax_d.text(0.19, 0.75, "Leray energy\n$\\nu\\int Y\\,dt$", transform=ax_d.transAxes, bbox={**box, "edgecolor": NAVY}, ha="center", va="center", fontsize=6.7)
    ax_d.text(0.72, 0.75, "denominator mass\n$\\sum\\kappa^{-2}d_Q$", transform=ax_d.transAxes, bbox={**box, "edgecolor": GREEN}, ha="center", va="center", fontsize=6.7)
    ax_d.annotate("", xy=(0.56, 0.75), xytext=(0.36, 0.75), xycoords="axes fraction", textcoords="axes fraction", arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.0))
    ax_d.text(0.46, 0.80, "paid", transform=ax_d.transAxes, color=GREEN, fontsize=6.1, ha="center", va="center")
    ax_d.text(0.31, 0.31, "projective tangent\n$|z|\\,|\\langle Px,PM\\rangle|/r_Q$", transform=ax_d.transAxes, bbox={**box, "edgecolor": RUST}, ha="center", va="center", fontsize=6.6)
    ax_d.text(0.78, 0.31, "Cauchy additionally needs\n$\\Gamma_Q$ and $\\nu\\int\\|L\\|_2^2/Y$", transform=ax_d.transAxes, bbox={**box, "edgecolor": GOLD}, ha="center", va="center", fontsize=6.3)
    ax_d.annotate("", xy=(0.28, 0.43), xytext=(0.20, 0.61), xycoords="axes fraction", textcoords="axes fraction", arrowprops=dict(arrowstyle="-[", color=RUST, lw=1.0))
    ax_d.text(0.10, 0.51, "not implied", transform=ax_d.transAxes, color=RUST, fontsize=5.9, ha="center", va="center")
    ax_d.annotate("", xy=(0.61, 0.31), xytext=(0.45, 0.31), xycoords="axes fraction", textcoords="axes fraction", arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.0))
    ax_d.text(0.53, 0.47, "needs extra input", transform=ax_d.transAxes, color=GOLD, fontsize=5.7, ha="center", va="center")
    ax_d.text(0.04, 0.03, "Closed: rowwise absolute raw-collar payment\nOpen: signed fusion / critical increment budget", transform=ax_d.transAxes, fontsize=6.1, color=INK)

    fig.text(0.08, 0.025, "Scope: fixed aligned matched cells. No general face, moving-cell, Leray-limit, continuation, regularity, or singularity claim.", fontsize=6.2, color=GRAY)
    for extension in ("pdf", "svg", "png"):
        fig.savefig(args.output_stem.with_suffix(f".{extension}"), dpi=600 if extension == "png" else None)
    svg_path = args.output_stem.with_suffix(".svg")
    svg_lines = svg_path.read_text(encoding="utf-8").splitlines()
    svg_path.write_text("\n".join(line.rstrip() for line in svg_lines) + "\n", encoding="utf-8")
    plt.close(fig)


if __name__ == "__main__":
    main()
