#!/usr/bin/env python3
"""Render the R0.71J double-column journal figure from archived CSV data."""

from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Patch


MM = 1.0 / 25.4
INK = "#28231f"
MUTED = "#6b675f"
NAVY = "#315a76"
RUST = "#8b4d43"
GOLD = "#a27a3f"
PALE_NAVY = "#e6edf1"
PALE_RUST = "#f1e4df"
GRID = "#d5cec0"
WHITE = "#ffffff"


def read_rows(path: Path) -> list[dict[str, str | float]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows: list[dict[str, str | float]] = list(csv.DictReader(handle))
    for row in rows:
        row["x"] = float(row["x"])
        row["value"] = float(row["value"])
    return rows


def selected(rows: list[dict[str, str | float]], panel: str, name: str) -> list[dict[str, str | float]]:
    values = [row for row in rows if row["panel"] == panel and row["series"] == name]
    values.sort(key=lambda row: (float(row["x"]), str(row["category"])))
    return values


def series(rows: list[dict[str, str | float]], panel: str, name: str) -> tuple[list[float], list[float]]:
    values = selected(rows, panel, name)
    return [float(row["x"]) for row in values], [float(row["value"]) for row in values]


def normalize_svg(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    path.write_text("\n".join(line.rstrip() for line in text.splitlines()) + "\n", encoding="utf-8")


def blossom(figure: plt.Figure) -> None:
    """Locked research blossom at the top-right header anchor."""

    center = (0.970, 0.958)
    for dx, dy, angle in ((0.0, 0.010, 0.0), (0.0, -0.010, 0.0), (0.008, 0.0, 90.0), (-0.008, 0.0, 90.0)):
        figure.add_artist(
            Ellipse(
                (center[0] + dx, center[1] + dy),
                0.010,
                0.018,
                angle=angle,
                transform=figure.transFigure,
                facecolor="#ead9b8",
                edgecolor=GOLD,
                linewidth=0.35,
            )
        )


def style_axis(axis: plt.Axes) -> None:
    axis.grid(color=GRID, linewidth=0.42, alpha=0.78, zorder=0)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)


def panel_label(axis: plt.Axes, letter: str) -> None:
    axis.text(-0.13, 1.08, letter, transform=axis.transAxes, fontsize=9.2, fontweight="bold", va="top")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("data.csv"))
    parser.add_argument("--output-stem", type=Path, default=Path("figure"))
    args = parser.parse_args()
    rows = read_rows(args.data)

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 6.8,
            "axes.titlesize": 7.7,
            "axes.labelsize": 6.9,
            "legend.fontsize": 5.45,
            "xtick.labelsize": 6.0,
            "ytick.labelsize": 6.0,
            "axes.linewidth": 0.65,
            "lines.linewidth": 1.25,
            "savefig.facecolor": "white",
            "svg.hashsalt": "r071j-full-frame-gap",
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
        }
    )

    figure = plt.figure(figsize=(178 * MM, 112 * MM))
    grid = figure.add_gridspec(
        2,
        2,
        left=0.080,
        right=0.935,
        bottom=0.130,
        top=0.865,
        wspace=0.38,
        hspace=0.42,
    )
    axis_a = figure.add_subplot(grid[0, 0])
    axis_b = figure.add_subplot(grid[0, 1])
    axis_c = figure.add_subplot(grid[1, 0])
    grid_d = grid[1, 1].subgridspec(2, 1, height_ratios=(1.65, 1.0), hspace=0.70)
    axis_d = figure.add_subplot(grid_d[0, 0])
    axis_support = figure.add_subplot(grid_d[1, 0])

    # Panel A: exact positive-defect decomposition at theta*.
    term_values = {
        name: float(selected(rows, "A", name)[0]["value"]) * 1.0e4
        for name in ("positiveCreation", "timeDerivative", "viscousMass", "negativeDefect")
    }
    axis_a.bar(
        [0],
        [term_values["positiveCreation"]],
        width=0.56,
        facecolor=PALE_NAVY,
        edgecolor=NAVY,
        linewidth=1.0,
        hatch="///",
        zorder=3,
    )
    bottom = 0.0
    component_styles = (
        ("timeDerivative", NAVY, PALE_NAVY, "///", r"$\partial_\theta A_0$"),
        ("viscousMass", RUST, PALE_RUST, "\\\\", r"$32A_0$"),
        ("negativeDefect", MUTED, WHITE, "..", r"$2s_-$"),
    )
    legend_patches: list[Patch] = []
    for name, edge, face, hatch, label in component_styles:
        height = term_values[name]
        if height > 0.0:
            axis_a.bar([1], [height], bottom=[bottom], width=0.56, facecolor=face, edgecolor=edge, linewidth=0.9, hatch=hatch, zorder=3)
        bottom += height
        legend_patches.append(Patch(facecolor=face, edgecolor=edge, hatch=hatch, label=label, linewidth=0.8))
    axis_a.scatter([1], [0], marker="x", color=MUTED, s=20, linewidths=0.9, zorder=5)
    for x_value, height in ((0, term_values["positiveCreation"]), (1, bottom)):
        axis_a.text(x_value, height + 0.22, f"{height:.3f}", ha="center", va="bottom", color=INK, fontsize=6.2)
    axis_a.text(1.19, 0.12, r"$2s_-=0$", color=MUTED, fontsize=5.8, va="bottom")
    axis_a.set_xticks([0, 1], ["left side\n" + r"$2s_+$", "right side\ncomponent sum"])
    axis_a.set_xlim(-0.62, 1.62)
    axis_a.set_ylim(0.0, max(term_values["positiveCreation"], bottom) * 1.25)
    axis_a.set_ylabel(r"dimensionless term $\times10^4$")
    axis_a.set_title(r"Positive-defect identity at $\theta_* = \log2/18$", loc="left", fontweight="bold")
    axis_a.legend(handles=legend_patches, frameon=False, loc="upper right", ncol=1, handlelength=1.3)
    axis_a.text(
        0.02,
        0.97,
        r"$2s_+=\partial_\theta A_0+32A_0+2s_-$",
        transform=axis_a.transAxes,
        ha="left",
        va="top",
        color=INK,
        fontsize=6.0,
    )
    style_axis(axis_a)

    # Panel B: normalized pure-heat profiles.
    profile_styles = (
        ("Bnormalized", NAVY, "-", "o", r"$B_0/B_0(\theta_*)$"),
        ("Dnormalized", RUST, "--", "s", r"$D_0/D_0(0)$"),
        ("Ynormalized", MUTED, "-.", "^", r"$Y_0/Y_0(0)$"),
        ("anormalized", NAVY, ":", "D", r"$A_0/A_*$"),
    )
    for name, color, linestyle, marker, label in profile_styles:
        theta, values = series(rows, "B", name)
        axis_b.plot(
            theta,
            values,
            color=color,
            linestyle=linestyle,
            marker=marker,
            markerfacecolor=WHITE,
            markeredgecolor=color,
            markeredgewidth=0.6,
            markersize=2.2,
            markevery=(0, 25),
            label=label,
        )
    theta_star = math.log(2.0) / 18.0
    axis_b.axvline(theta_star, color=RUST, linewidth=0.65, linestyle=(0, (2, 2)))
    axis_b.scatter([theta_star], [1.0], marker="o", facecolor=WHITE, edgecolor=RUST, linewidth=0.8, s=17, zorder=5)
    axis_b.text(theta_star + 0.006, 3.98, r"$\theta_*$", color=RUST, fontsize=5.8)
    axis_b.set_xlim(0.0, 0.4)
    axis_b.set_ylim(-0.08, 4.35)
    axis_b.set_xlabel(r"viscous time $\theta=\nu K^2t$")
    axis_b.set_ylabel("normalized profile")
    axis_b.set_title("Selected-parent pure-heat profiles", loc="left", fontweight="bold")
    axis_b.legend(frameon=False, loc="upper right", ncol=2, columnspacing=0.8, handlelength=2.1)
    style_axis(axis_b)

    # Panel C: algebraic full-frame bounds.
    frequency, z_lower = series(rows, "C", "Zlower")
    _, h_upper = series(rows, "C", "Hupper")
    axis_c.plot(
        frequency,
        z_lower,
        color=NAVY,
        marker="o",
        markerfacecolor=WHITE,
        markeredgecolor=NAVY,
        markeredgewidth=0.7,
        markersize=2.8,
        label=r"$A_*/(64K^2)$  (creation lower coefficient)",
    )
    axis_c.plot(
        frequency,
        h_upper,
        color=RUST,
        linestyle="--",
        marker="s",
        markerfacecolor=WHITE,
        markeredgecolor=RUST,
        markeredgewidth=0.7,
        markersize=2.8,
        label=r"$(1-2^{-1/9})/(2K^4)$  (heat upper bound)",
    )
    axis_c.set_xscale("log", base=2)
    axis_c.set_yscale("log")
    axis_c.set_xlim(6.5, 1.02e4)
    axis_c.set_ylim(3.0e-18, 2.0e-5)
    axis_c.set_xticks([8, 32, 128, 512, 2048, 8192], labels=["8", "32", "128", "512", "2048", "8192"])
    axis_c.set_xlabel(r"dyadic frequency $K$  (reference grid; $K_0$ not quantified)")
    axis_c.set_ylabel(r"weighted time integral, $\nu=1$")
    axis_c.set_title("Parent-frame asymptotic comparison bounds", loc="left", fontweight="bold")
    axis_c.legend(frameon=False, loc="lower left", handlelength=2.5)
    axis_c.text(0.96, 0.91, r"slopes $-2$ and $-4$", transform=axis_c.transAxes, ha="right", va="top", color=INK, fontsize=6.0)
    axis_c.text(0.96, 0.77, r"$Z/H\geq c\nu K^2$ for large dyadic $K$", transform=axis_c.transAxes, ha="right", va="top", color=MUTED, fontsize=5.8)
    style_axis(axis_c)

    # Panel D: exact initial-time group ledger.
    groups, b_group = series(rows, "D", "Bgroup")
    _, f_group = series(rows, "D", "F2group")
    _, d_group = series(rows, "D", "dgroup")
    bar_colors = [NAVY, RUST, MUTED]
    bars = axis_d.bar(groups, b_group, width=0.58, color=[PALE_NAVY, PALE_RUST, WHITE], edgecolor=bar_colors, linewidth=0.95, hatch=["///", "\\\\", ".."], zorder=3)
    axis_d.axhline(0.0, color=INK, linewidth=0.65)
    axis_d.scatter([2.0], [0.0], marker="o", facecolor=WHITE, edgecolor=MUTED, linewidth=0.8, s=18, zorder=5)
    for index, (bar, f_value, d_value) in enumerate(zip(bars, f_group, d_group)):
        y_value = b_group[index]
        if y_value < 0:
            label_y = -27.0
            vertical = "center"
        else:
            label_y = y_value + 2.2
            vertical = "bottom"
        axis_d.text(bar.get_x() + bar.get_width() / 2.0, label_y, rf"$F^2={int(f_value)},\ d={int(d_value)}$", ha="center", va=vertical, fontsize=5.5, color=INK)
    axis_d.set_xticks(groups, [r"$|m|=0$", r"$|m|=1$", r"$|m|=2$"])
    axis_d.set_ylim(-48, 48)
    axis_d.set_ylabel(r"$B$ group / $K^3$")
    axis_d.set_title(r"Initial mode ledger: $36-36+0=0$", loc="left", fontweight="bold")
    style_axis(axis_d)

    # Panel D lower strip: flat-top parent support for all Lamb modes.
    radius_rows = selected(rows, "D", "frameRadius")
    axis_support.axvspan(1.0, math.sqrt(2.0), facecolor=PALE_NAVY, edgecolor=NAVY, linewidth=0.55, alpha=0.75)
    for channel, marker, color in (("n=4", "o", NAVY), ("n=5", "s", RUST)):
        channel_rows = [row for row in radius_rows if row["category"] == channel]
        axis_support.scatter(
            [float(row["value"]) for row in channel_rows],
            [float(row["x"]) for row in channel_rows],
            marker=marker,
            facecolor=WHITE,
            edgecolor=color,
            linewidth=0.75,
            s=17,
            label=rf"${channel}$",
            zorder=4,
        )
    axis_support.set_xlim(0.965, 1.445)
    axis_support.set_ylim(-0.42, 2.42)
    axis_support.set_yticks([0, 1, 2], [r"$|m|=0$", r"$1$", r"$2$"])
    axis_support.set_xticks([1.0, 1.2, math.sqrt(2.0)], ["1", "1.2", r"$\sqrt{2}$"])
    axis_support.set_xlabel(r"normalized radius $|\xi|/(4K)$")
    axis_support.set_title(r"All listed Lamb modes satisfy $m_j(\xi)=1$", loc="left", fontsize=6.6, fontweight="bold", pad=2)
    axis_support.legend(frameon=False, loc="upper left", ncol=2, handletextpad=0.3, columnspacing=0.7)
    style_axis(axis_support)

    for letter, axis in (("A", axis_a), ("B", axis_b), ("C", axis_c), ("D", axis_d)):
        panel_label(axis, letter)

    figure.text(0.045, 0.965, "R0.71J  /  full-frame positive-creation and heat-payment audit", ha="left", va="top", fontsize=9.0, fontweight="bold", color=INK)
    figure.text(0.045, 0.925, r"parent-only broad frame  ·  global cell $\chi=1$  ·  heat height $s=0$  ·  closed-form 2D3C limit", ha="left", va="top", fontsize=5.6, color=MUTED)
    figure.text(0.935, 0.010, "exact formula evaluation; no DNS, fitted exponent, regularity, or singularity claim", ha="right", va="bottom", fontsize=5.35, color=MUTED)
    blossom(figure)

    output = args.output_stem
    title = "R0.71J parent-only full-frame positive creation and heat-payment gap"
    figure.savefig(
        output.with_suffix(".pdf"),
        metadata={
            "Title": title,
            "Author": "Chuikuan Zeng",
            "Subject": "Closed-form parent-frame positive-defect, heat-profile, scaling, and mode-ledger diagnostics",
            "Creator": "Matplotlib",
            "CreationDate": None,
            "ModDate": None,
        },
    )
    figure.savefig(
        output.with_suffix(".svg"),
        metadata={
            "Title": title,
            "Description": "Four-panel closed-form parent-only broad-frame diagnostic; no DNS or finite-K PDE trajectory.",
            "Creator": "Matplotlib",
            "Date": None,
        },
    )
    normalize_svg(output.with_suffix(".svg"))
    figure.savefig(
        output.with_suffix(".png"),
        dpi=600,
        metadata={
            "Title": title,
            "Description": "Four-panel closed-form parent-only broad-frame diagnostic; no DNS or finite-K PDE trajectory.",
            "Software": "Matplotlib",
        },
    )
    plt.close(figure)


if __name__ == "__main__":
    main()
