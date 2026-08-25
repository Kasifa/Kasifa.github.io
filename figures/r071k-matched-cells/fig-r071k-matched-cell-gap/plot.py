#!/usr/bin/env python3
"""Plot the R0.71K matched-cell figure at journal size."""

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
INK = "#28231f"
GRAY = "#77716a"
PAPER = "#faf7f0"
GRID = "#d8d1c7"


def load(path: Path):
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
    return (
        np.array([float(row["x"]) for row in selected]),
        np.array([float(row["value"]) for row in selected]),
    )


def panel_label(axis, letter):
    axis.text(-0.12, 1.08, letter, transform=axis.transAxes, fontsize=10, fontweight="bold", color=INK, va="top")


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
    # Some interactive backends quantize the initial canvas to whole pixels.
    # Restore the exact journal dimensions before any export.
    fig.set_size_inches(178 / 25.4, 112 / 25.4, forward=False)
    grid = fig.add_gridspec(2, 2, left=0.08, right=0.975, bottom=0.17, top=0.88, wspace=0.30, hspace=0.43)
    ax_a = fig.add_subplot(grid[0, 0])
    ax_b = fig.add_subplot(grid[0, 1])
    ax_c = fig.add_subplot(grid[1, 0])
    ax_d = fig.add_subplot(grid[1, 1])

    fig.text(0.08, 0.955, "R0.71K  /  fixed matched cells and the localized heat-payment gap", fontsize=10.2, fontweight="bold", color=INK)
    fig.text(0.08, 0.922, "Exact translated-cell algebra · deterministic partition · no DNS", fontsize=6.8, color=GRAY)

    line_specs = [
        ("leftAtom", NAVY, "--", "left atom"),
        ("centerAtom", RUST, "-", "center atom"),
        ("rightAtom", GOLD, ":", "right atom"),
        ("partitionSum", INK, "-.", "sum"),
    ]
    for series, color, style, label in line_specs:
        x, y = values(grouped, "A", series)
        ax_a.plot(x / np.pi, y, color=color, linestyle=style, linewidth=1.25 if series == "partitionSum" else 1.0, label=label)
    ax_a.set_title("Fixed smooth translated partition", loc="left", fontweight="bold")
    ax_a.set_xlabel(r"normalized position  $y/\pi$")
    ax_a.set_ylabel("partition weight")
    ax_a.set_xlim(-1, 1)
    ax_a.set_ylim(-0.03, 1.08)
    ax_a.grid(axis="y", color=GRID, linewidth=0.5, alpha=0.8)
    ax_a.legend(frameon=False, ncol=2, loc="upper center")
    ax_a.text(0.02, 0.08, r"$\sum_Q\chi_Q=1$   ·   overlap $\leq8$", transform=ax_a.transAxes, fontsize=6.6, color=INK)
    panel_label(ax_a, "A")

    x, y = values(grouped, "B", "globalAmplitude")
    ax_b.plot(x, y, color=NAVY, linewidth=1.35, label=r"global $A_0/A_*$")
    xg, yg = values(grouped, "B", "globalEndpoint")
    xl, yl = values(grouped, "B", "localTemplateEndpoint")
    ax_b.scatter(xg, yg, s=25, marker="o", color=RUST, zorder=4, label=r"global at $\theta_*$")
    ax_b.scatter(xl, yl, s=30, marker="s", facecolors=PAPER, edgecolors=RUST, linewidths=1.1, zorder=5, label="local template audit")
    ax_b.axvline(float(xg[0]), color=GRAY, linestyle=":", linewidth=0.8)
    ax_b.set_title("Zero entry becomes a positive cell endpoint", loc="left", fontweight="bold")
    ax_b.set_xlabel(r"parabolic time  $\theta=\nu K^2t$")
    ax_b.set_ylabel(r"amplitude  /  $A_*$")
    ax_b.set_xlim(0, 0.12)
    ax_b.set_ylim(-0.08, max(yl[0] * 1.18, y.max() * 1.05))
    ax_b.grid(axis="y", color=GRID, linewidth=0.5, alpha=0.8)
    ax_b.legend(frameon=False, loc="upper right")
    ax_b.text(0.02, 0.08, r"$A_0(0)=0$;  $A_{\rm loc}(\theta_*)>0$", transform=ax_b.transAxes, fontsize=6.6)
    panel_label(ax_b, "B")

    for series, color, style, marker, label in (
        ("creationPower", RUST, "-", "o", r"normalized creation  $K^{-2}$"),
        ("heatPower", NAVY, "--", "s", r"normalized heat  $K^{-4}$"),
    ):
        x, y = values(grouped, "C", series)
        ax_c.loglog(x, y, color=color, linestyle=style, marker=marker, markersize=3.2, markerfacecolor=PAPER if marker == "s" else color, linewidth=1.15, label=label)
    ax_c.set_title("Matched localization retains two powers", loc="left", fontweight="bold")
    ax_c.set_xlabel(r"dyadic frequency  $K$  (reference grid)")
    ax_c.set_ylabel("constant-normalized bound")
    ax_c.grid(which="both", color=GRID, linewidth=0.45, alpha=0.7)
    ax_c.legend(frameon=False, loc="lower left")
    ax_c.text(0.58, 0.80, r"ratio $\gtrsim K^2$", transform=ax_c.transAxes, fontsize=7.1, fontweight="bold", color=INK)
    ax_c.text(0.58, 0.70, r"$K_0$ not quantified", transform=ax_c.transAxes, fontsize=6.2, color=GRAY)
    panel_label(ax_c, "C")

    rows = grouped[("D", "scalingExponent")]
    labels = [row["category"] for row in rows]
    exponents = np.array([float(row["value"]) for row in rows])
    colors = [NAVY, NAVY, NAVY, NAVY, RUST, NAVY, GOLD, RUST]
    bars = ax_d.bar(np.arange(len(labels)), exponents, color=colors, edgecolor=INK, linewidth=0.45)
    for index, bar in enumerate(bars):
        if labels[index] == "collar":
            bar.set_hatch("//")
        if labels[index] == "H_loc":
            bar.set_hatch("..")
        offset = 0.16 if exponents[index] >= 0 else -0.28
        ax_d.text(bar.get_x() + bar.get_width() / 2, exponents[index] + offset, f"{exponents[index]:+g}", ha="center", va="bottom" if exponents[index] >= 0 else "top", fontsize=6.2)
    ax_d.axhline(0, color=INK, linewidth=0.7)
    ax_d.set_xticks(np.arange(len(labels)), labels, rotation=35, ha="right")
    ax_d.set_ylabel(r"power of $K$")
    ax_d.set_ylim(-4.8, 2.8)
    ax_d.set_title("Cell ledger and the leading collar", loc="left", fontweight="bold")
    ax_d.grid(axis="y", color=GRID, linewidth=0.5, alpha=0.8)
    ax_d.text(0.02, 0.92, r"collar and $Z_{\rm loc}$: same $K^{-2}$ scale", transform=ax_d.transAxes, fontsize=6.4, color=INK)
    panel_label(ax_d, "D")

    fig.text(0.08, 0.025, "Scope: one fixed aligned matched partition; the collar-paid, face-paid, moving-cell, and Leray-limit problems remain open.", fontsize=6.2, color=GRAY)
    for extension in ("pdf", "svg", "png"):
        fig.savefig(args.output_stem.with_suffix(f".{extension}"), dpi=600 if extension == "png" else None)
    plt.close(fig)


if __name__ == "__main__":
    main()
