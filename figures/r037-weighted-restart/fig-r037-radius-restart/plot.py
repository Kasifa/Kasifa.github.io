#!/usr/bin/env python3
"""Render the R0.37 weighted-restart journal figure."""

from __future__ import annotations

import csv
from fractions import Fraction
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
STYLE = PACKAGE.parents[1] / "journal.mplstyle"
INK = "#27221d"
MUTED = "#6b675f"
BLUE = "#315a76"
GOLD = "#a16f27"
PALE_BLUE = "#dce6ec"
PALE_GOLD = "#efe1c7"
GRID = "#d5cec0"


def normalize_svg(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(line.rstrip() for line in lines) + "\n", encoding="utf-8")


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def scientific_label(value: float, digits: int = 3) -> str:
    exponent = int(np.floor(np.log10(value)))
    coefficient = value / 10**exponent
    return rf"${coefficient:.{digits}f}\times10^{{{exponent}}}$"


def draw() -> None:
    radius_data = rows("radius-gain.csv")
    normalized = {
        (row["quantity"], row["version"]): float(
            Fraction(row["normalized_to_r031"])
        )
        for row in radius_data
    }
    contraction = {row["metric"]: float(row["decimal"]) for row in rows("contraction.csv")}
    residuals = {row["metric"]: float(row["decimal"]) for row in rows("residual-scales.csv")}
    inverse = {row["name"]: row["exact_or_text"] for row in rows("inverse-metadata.csv")}

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        figure = plt.figure(figsize=(178 / 25.4, 98 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            width_ratios=(0.92, 1.42),
            height_ratios=(1.12, 0.72),
            left=0.125,
            right=0.982,
            bottom=0.275,
            top=0.81,
            wspace=0.38,
            hspace=0.92,
        )
        left = figure.add_subplot(grid[:, 0])
        upper = figure.add_subplot(grid[0, 1])
        lower = figure.add_subplot(grid[1, 1])

        left.set_title("(a) Certified radius gain", loc="left", pad=5)
        quantities = ["bivariate_radius", "fixed_charge_radius"]
        labels = [r"bivariate $r$", r"fixed-charge $r^3$"]
        y_positions = np.array([1.0, 0.0])
        bar_height = 0.26
        for quantity, label, y in zip(quantities, labels, y_positions):
            old_value = normalized[(quantity, "R0.31")]
            new_value = normalized[(quantity, "R0.37")]
            left.barh(
                y + 0.16,
                old_value,
                height=bar_height,
                facecolor="white",
                edgecolor=MUTED,
                linewidth=0.8,
                hatch="////",
                label="R0.31" if quantity == quantities[0] else None,
            )
            left.barh(
                y - 0.16,
                new_value,
                height=bar_height,
                facecolor=PALE_BLUE,
                edgecolor=BLUE,
                linewidth=0.9,
                label="R0.37" if quantity == quantities[0] else None,
            )
            left.text(old_value + 0.045, y + 0.16, "1", va="center", fontsize=5.9, color=MUTED)
            exact_gain = r"$4/3$" if quantity == "bivariate_radius" else r"$64/27$"
            left.text(new_value + 0.045, y - 0.16, exact_gain, va="center", fontsize=5.9, color=BLUE)
        left.axvline(1, color=MUTED, linewidth=0.75, linestyle=(0, (4, 2)))
        left.set_xlim(0, 2.62)
        left.set_ylim(-0.62, 1.62)
        left.set_yticks(y_positions)
        left.set_yticklabels(labels)
        left.set_xlabel("value normalized to R0.31")
        left.grid(axis="x", color=GRID, linewidth=0.42)
        left.legend(loc="lower right", fontsize=6.0)
        left.text(
            0.02,
            -0.48,
            r"$r: 4/81\rightarrow16/243$",
            fontsize=5.8,
            color=MUTED,
            va="center",
        )

        upper.set_title(r"(b) Contraction checks at $r_*=16/243$", loc="left", pad=5)
        metric_order = [
            "active_linearization",
            "ball_mapping_ratio",
            "ball_lipschitz",
            "transport_operator",
        ]
        metric_labels = [
            r"active $\|D\Phi(p_{40})\|$",
            r"ball image $/\,\varepsilon$",
            "ball Lipschitz",
            "transport operator",
        ]
        metric_y = np.arange(3, -1, -1, dtype=float)
        markers = ["D", "s", "o", "^"]
        colors = [BLUE, BLUE, GOLD, GOLD]
        fills = [PALE_BLUE, "white", PALE_GOLD, "white"]
        for name, label, y, marker, color, fill in zip(
            metric_order, metric_labels, metric_y, markers, colors, fills
        ):
            value = contraction[name]
            upper.hlines(y, 0, value, color=color, linewidth=0.9)
            upper.scatter(
                [value],
                [y],
                s=27,
                marker=marker,
                facecolor=fill,
                edgecolor=color,
                linewidth=0.9,
                zorder=5,
            )
            upper.text(
                value - 0.018 if value > 0.72 else value + 0.025,
                y + 0.23,
                f"{value:.4f}",
                ha="right" if value > 0.72 else "left",
                va="bottom",
                fontsize=5.6,
                color=color,
            )
        upper.axvline(1, color=INK, linewidth=0.8, linestyle=(0, (4, 2)))
        upper.text(0.995, 3.48, "threshold 1", ha="right", va="bottom", fontsize=5.5, color=INK)
        upper.set_xlim(0, 1.045)
        upper.set_ylim(-0.42, 3.62)
        upper.set_yticks(metric_y)
        upper.set_yticklabels(metric_labels)
        upper.grid(axis="x", color=GRID, linewidth=0.42)

        lower.set_title("(c) Exact residual versus allowance", loc="left", pad=4)
        scale_names = ["exact_residual_norm", "residual_allowance"]
        scale_labels = ["residual", "allowance"]
        scale_y = [1.0, 0.0]
        scale_markers = ["o", "D"]
        scale_colors = [GOLD, BLUE]
        for name, label, y, marker, color in zip(
            scale_names, scale_labels, scale_y, scale_markers, scale_colors
        ):
            value = residuals[name]
            lower.hlines(y, 1e-48, value, color=color, linewidth=0.85)
            lower.scatter(
                [value],
                [y],
                s=25,
                marker=marker,
                facecolor="white",
                edgecolor=color,
                linewidth=0.9,
                zorder=5,
            )
            lower.annotate(
                scientific_label(value),
                xy=(value, y),
                xytext=(5, 0),
                textcoords="offset points",
                ha="left",
                va="center",
                fontsize=5.5,
                color=color,
            )
        lower.set_xscale("log")
        lower.set_xlim(1e-48, 2e-3)
        lower.set_ylim(-0.52, 1.48)
        lower.set_yticks(scale_y)
        lower.set_yticklabels(scale_labels)
        lower.set_xlabel("weighted norm", labelpad=1)
        lower.grid(axis="x", which="major", color=GRID, linewidth=0.42)

        figure.text(
            0.012,
            0.985,
            "R0.37 weighted-Wiener restart certificate",
            ha="left",
            va="top",
            fontsize=7.1,
            color=INK,
        )
        figure.text(0.985, 0.985, r"$\nu$", ha="right", va="top", fontsize=8.0, color=MUTED)
        figure.text(
            0.982,
            0.135,
            r"One total-degree weight gives $\|\Phi(f)\|\leq3\|f\|^2$ on $q\geq-1$; all four plotted contraction ratios are strictly below one.",
            fontsize=5.35,
            color=MUTED,
            ha="right",
            va="bottom",
        )
        figure.text(
            0.982,
            0.091,
            r"The exact residual is $2.08\times10^{-42}$ of its allowance. The 62D degree-12 inverse is a finite check; the radius theorem is all-order.",
            fontsize=5.35,
            color=MUTED,
            ha="right",
            va="bottom",
        )
        figure.text(
            0.982,
            0.047,
            rf"Boundary infinite-inverse bound: {float(Fraction(inverse['boundary_infinite_inverse_norm_bound'])):.4f}. Exact rational data and hashes are archived with the figure.",
            fontsize=5.35,
            color=MUTED,
            ha="right",
            va="bottom",
        )

        for suffix in ("pdf", "svg", "png"):
            output = PACKAGE / f"figure.{suffix}"
            figure.savefig(output)
            if suffix == "svg":
                normalize_svg(output)
        public_figures = REPOSITORY / "public/figures"
        public_figures.mkdir(parents=True, exist_ok=True)
        for suffix in ("svg", "png"):
            output = public_figures / f"r0-37-radius-restart.{suffix}"
            figure.savefig(output)
            if suffix == "svg":
                normalize_svg(output)
        plt.close(figure)


if __name__ == "__main__":
    draw()
