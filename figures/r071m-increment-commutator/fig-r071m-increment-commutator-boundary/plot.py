#!/usr/bin/env python3
"""Plot the R0.71M increment-commutator boundary at journal size."""

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


def xy(grouped, panel, series):
    selected = grouped[(panel, series)]
    return (
        np.array([float(row["x"]) for row in selected]),
        np.array([float(row["value"]) for row in selected]),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("data.csv"))
    parser.add_argument("--output-stem", type=Path, default=Path("figure"))
    args = parser.parse_args()
    grouped = load(args.data)
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 7.2,
            "axes.titlesize": 8.0,
            "axes.labelsize": 7.0,
            "legend.fontsize": 6.2,
            "xtick.labelsize": 6.2,
            "ytick.labelsize": 6.2,
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
        }
    )
    fig = plt.figure(figsize=(178 / 25.4, 112 / 25.4))
    fig.set_size_inches(178 / 25.4, 112 / 25.4, forward=False)
    grid = fig.add_gridspec(
        2,
        2,
        left=0.10,
        right=0.975,
        bottom=0.17,
        top=0.87,
        wspace=0.36,
        hspace=0.58,
    )
    ax_a, ax_b, ax_c, ax_d = [
        fig.add_subplot(grid[index // 2, index % 2]) for index in range(4)
    ]
    fig.text(
        0.08,
        0.955,
        "R0.71M  /  exact increment commutator and the four-row tangent boundary",
        fontsize=10.0,
        fontweight="bold",
        color=INK,
    )
    fig.text(
        0.08,
        0.922,
        "Exact identities - deterministic Fourier audit - analytic heat-packet scaling - no DNS",
        fontsize=6.7,
        color=GRAY,
    )

    component_rows = grouped[("A", "signedPairingComponent")]
    total_row = grouped[("A", "signedPairingTotal")][0]
    component_labels = {
        "sourceSquare": "source",
        "viscousCross": "viscous",
        "projectiveSource": "proj. source",
        "projectiveViscous": "proj. viscous",
    }
    labels_a = [component_labels[row["category"]] for row in component_rows] + ["total"]
    values_a = [float(row["value"]) for row in component_rows] + [float(total_row["value"])]
    colors_a = [NAVY, RUST, GOLD, GREEN, INK]
    positions = np.arange(len(values_a))
    bars = ax_a.barh(positions, values_a, color=colors_a, edgecolor=INK, linewidth=0.45)
    bars[-1].set_hatch("//")
    ax_a.set_yticks(positions, labels_a)
    ax_a.invert_yaxis()
    ax_a.set_xscale("symlog", linthresh=1.0e-3)
    ax_a.axvline(0, color=INK, linewidth=0.6)
    ax_a.grid(axis="x", color=GRID, linewidth=0.5)
    ax_a.set_xlabel("signed pairing contribution (diagnostic)")
    ax_a.set_title("A   Exact pairing split on one smooth witness", loc="left", fontweight="bold")
    for bar, value in zip(bars, values_a):
        anchor = value * (1.08 if value > 0 else 1.15)
        ax_a.text(anchor, bar.get_y() + bar.get_height() / 2, f"{value:.2g}", va="center", ha="left" if value > 0 else "right", fontsize=5.7)
    ax_a.text(
        0.02,
        0.02,
        "diagnostic only; no interval sign claim",
        transform=ax_a.transAxes,
        fontsize=5.8,
        color=GRAY,
    )

    row_rows = grouped[("B", "normalizedCriticalRowSquare")]
    support = grouped[("B", "supportDiagnostic")][0]
    label_map = {
        "resolvedTransport": "resolved\ntransport",
        "incrementCommutator": "increment\ncommutator",
        "projectiveGeometry": "projective\ngeometry",
        "viscousMismatch": "viscous\nmismatch",
    }
    labels_b = [label_map[row["category"]] for row in row_rows]
    values_b = np.array([float(row["value"]) for row in row_rows])
    bars_b = ax_b.bar(
        np.arange(4),
        values_b,
        color=[NAVY, RUST, GOLD, GREEN],
        edgecolor=INK,
        linewidth=0.45,
    )
    bars_b[1].set_hatch("//")
    ax_b.set_yscale("log")
    ax_b.set_ylim(1.0e-7, 1.2)
    ax_b.set_xticks(np.arange(4), labels_b)
    ax_b.set_ylabel("fraction of four-row square mass")
    ax_b.grid(axis="y", color=GRID, linewidth=0.5, which="both")
    ax_b.set_title("B   Direct estimate produces four split rows", loc="left", fontweight="bold", fontsize=7.7)
    ax_b.text(
        0.02,
        0.06,
        f"energy above $1.45\\kappa$ in split commutator: {100*float(support['value']):.1f}%",
        transform=ax_b.transAxes,
        fontsize=5.9,
        color=RUST,
        bbox=dict(facecolor=PAPER, edgecolor="none", alpha=0.9, pad=0.5),
    )

    for series, color, marker, label in (
        ("energy", INK, "o", "energy"),
        ("YuQuarticDefect", RUST, "s", r"quartic increment  $r^{-2}$"),
        ("velocityCarleson", NAVY, "^", r"velocity Carleson  $r^{-1}$"),
        ("normalizedLamb", GREEN, "D", r"normalized Lamb  $r^{-1}$"),
    ):
        radius, value = xy(grouped, "C", series)
        order = np.argsort(radius)
        ax_c.loglog(
            radius[order],
            value[order],
            color=color,
            marker=marker,
            markersize=3.1,
            linewidth=1.1,
            label=label,
        )
    ax_c.invert_xaxis()
    ax_c.grid(color=GRID, linewidth=0.5, which="both")
    ax_c.set_xlabel("packet radius  $r$")
    ax_c.set_ylabel("normalized budget")
    ax_c.set_title("C   Energy does not universally pay these envelopes", loc="left", fontweight="bold", fontsize=7.7)
    ax_c.legend(frameon=False, loc="upper left", ncol=1)
    ax_c.text(
        0.98,
        0.04,
        "exact scaling exponents\nheat flows, not NSE solutions",
        transform=ax_c.transAxes,
        ha="right",
        va="bottom",
        fontsize=5.7,
        color=GRAY,
    )

    ax_d.set_axis_off()
    ax_d.set_title(
        "D   Direct-route ledger and the R0.71N gate",
        loc="left",
        fontweight="bold",
        pad=4,
        fontsize=7.7,
    )
    box = dict(boxstyle="square,pad=0.28", facecolor=PAPER, linewidth=0.8)
    nodes = [
        (0.14, 0.76, "Leray energy", NAVY),
        (0.50, 0.76, "quadratic\n$L^2$ increments", GREEN),
        (0.23, 0.42, "known quartic\nincrement defect\n(extra hypothesis)", RUST),
        (0.66, 0.42, "four-row\ncritical ledger", GOLD),
        (0.66, 0.12, "whole-scalar\nsigned fusion", INK),
    ]
    for x_value, y_value, label, color in nodes:
        ax_d.text(
            x_value,
            y_value,
            label,
            transform=ax_d.transAxes,
            bbox={**box, "edgecolor": color},
            ha="center",
            va="center",
            fontsize=6.4,
        )
    arrow = dict(arrowstyle="->", lw=1.0)
    ax_d.annotate("", xy=(0.38, 0.76), xytext=(0.25, 0.76), xycoords="axes fraction", arrowprops={**arrow, "color": GREEN})
    ax_d.text(0.315, 0.88, "energy-paid", transform=ax_d.transAxes, ha="center", fontsize=5.5, color=GREEN)
    ax_d.annotate("", xy=(0.53, 0.42), xytext=(0.36, 0.42), xycoords="axes fraction", arrowprops={**arrow, "color": GOLD, "linestyle": "--"})
    ax_d.text(0.445, 0.42, r"$\times$", transform=ax_d.transAxes, ha="center", va="center", fontsize=8.0, color=RUST, bbox=dict(facecolor=PAPER, edgecolor="none", pad=0.3))
    ax_d.annotate("", xy=(0.66, 0.23), xytext=(0.66, 0.32), xycoords="axes fraction", arrowprops={**arrow, "color": INK})
    ax_d.text(0.78, 0.275, "R0.71N", transform=ax_d.transAxes, ha="center", fontsize=5.8, color=INK)

    fig.text(
        0.08,
        0.025,
        "Scope: fixed cells and a direct absolute envelope. No face, moving-cell, Leray-limit, continuation, regularity, or singularity claim.",
        fontsize=6.1,
        color=GRAY,
    )
    for extension in ("pdf", "svg", "png"):
        fig.savefig(
            args.output_stem.with_suffix(f".{extension}"),
            dpi=600 if extension == "png" else None,
        )
    svg_path = args.output_stem.with_suffix(".svg")
    svg_lines = svg_path.read_text(encoding="utf-8").splitlines()
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_lines) + "\n", encoding="utf-8"
    )
    plt.close(fig)


if __name__ == "__main__":
    main()
