#!/usr/bin/env python3
"""Render the R0.38 tail-aware restart journal figure."""

from __future__ import annotations

import csv
from fractions import Fraction
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


PACKAGE = Path(__file__).resolve().parent
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
    middle = rf"{coefficient:.{digits}f}\times10^{{{exponent}}}"
    return "$" + middle + "$"


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

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        figure = plt.figure(figsize=(178 / 25.4, 104 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            width_ratios=(0.94, 1.46),
            height_ratios=(1.38, 0.72),
            left=0.128,
            right=0.982,
            bottom=0.286,
            top=0.815,
            wspace=0.40,
            hspace=0.82,
        )
        left = figure.add_subplot(grid[:, 0])
        upper = figure.add_subplot(grid[0, 1])
        lower = figure.add_subplot(grid[1, 1])

        left.set_title("(a) Certified radius ladder", loc="left", pad=5)
        quantities = ["bivariate_radius", "fixed_charge_radius"]
        quantity_labels = [r"bivariate $r$", r"fixed-charge $r^3$"]
        versions = ["R0.31", "R0.37", "R0.38"]
        version_markers = ["o", "s", "D"]
        version_colors = [MUTED, BLUE, GOLD]
        version_fills = ["white", PALE_BLUE, PALE_GOLD]
        y_base = np.array([1.0, 0.0])
        y_offsets = [0.23, 0.0, -0.23]
        for quantity, quantity_label, base in zip(quantities, quantity_labels, y_base):
            for version, marker, color, fill, offset in zip(
                versions,
                version_markers,
                version_colors,
                version_fills,
                y_offsets,
            ):
                value = normalized[(quantity, version)]
                y = base + offset
                left.hlines(y, 0.93, value, color=color, linewidth=0.85)
                left.scatter(
                    [value],
                    [y],
                    s=25,
                    marker=marker,
                    facecolor=fill,
                    edgecolor=color,
                    linewidth=0.9,
                    zorder=5,
                    label=version if quantity == quantities[0] else None,
                )
                label = f"{value:.3f}".rstrip("0").rstrip(".")
                left.text(value + 0.055, y, label, va="center", fontsize=5.55, color=color)
        left.axvline(1, color=INK, linewidth=0.75, linestyle=(0, (4, 2)))
        left.set_xscale("log")
        left.set_xlim(0.88, 16.6)
        left.set_ylim(-0.56, 1.56)
        left.set_yticks(y_base)
        left.set_yticklabels(quantity_labels)
        left.set_xlabel("value normalized to R0.31")
        left.set_xticks([1, 2, 4, 8, 16])
        left.set_xticklabels(["1", "2", "4", "8", "16"])
        left.grid(axis="x", which="major", color=GRID, linewidth=0.42)
        left.legend(
            loc="upper left",
            bbox_to_anchor=(0.02, 0.99),
            borderaxespad=0,
            fontsize=5.9,
            ncols=3,
            columnspacing=0.85,
            handletextpad=0.35,
        )
        left.text(
            0.02,
            -0.44,
            r"$r: 4/81\rightarrow16/243\rightarrow59/500$",
            transform=left.transAxes,
            fontsize=5.55,
            color=MUTED,
            va="center",
        )

        upper.set_title(r"(b) Bounds and controls at $r_*=59/500$", loc="left", pad=5)
        metric_order = [
            "old_full_space_bound",
            "tail_linearization",
            "ball_mapping_ratio",
            "ball_lipschitz",
            "transport_operator",
            "nearby_failure_probe",
            "finite_tail_column",
        ]
        metric_labels = [
            r"old full-space $6M_{80}$",
            r"tail $Z_{80}$",
            r"ball image $/\,\varepsilon$",
            "ball Lipschitz",
            "transport operator",
            r"probe at $19/160$",
            "degree-81 column",
        ]
        metric_y = np.arange(6, -1, -1, dtype=float)
        markers = ["X", "D", "s", "o", "^", "P", "v"]
        colors = [MUTED, BLUE, BLUE, GOLD, GOLD, MUTED, MUTED]
        fills = [MUTED, PALE_BLUE, "white", PALE_GOLD, "white", "white", "white"]
        for name, label, y, marker, color, fill in zip(
            metric_order, metric_labels, metric_y, markers, colors, fills
        ):
            value = contraction[name]
            upper.hlines(y, 0, value, color=color, linewidth=0.85)
            upper.scatter(
                [value],
                [y],
                s=25,
                marker=marker,
                facecolor=fill,
                edgecolor=color,
                linewidth=0.9,
                zorder=5,
            )
            if name == "old_full_space_bound":
                text_x, align = value - 0.045, "right"
            elif value > 0.91:
                text_x, align = value - 0.025, "right"
            else:
                text_x, align = value + 0.028, "left"
            upper.text(
                text_x,
                y + 0.20,
                f"{value:.4f}",
                ha=align,
                va="bottom",
                fontsize=5.35,
                color=color,
            )
        upper.axvline(1, color=INK, linewidth=0.8, linestyle=(0, (4, 2)))
        upper.text(0.99, 6.50, "threshold 1", ha="right", va="bottom", fontsize=5.4, color=INK)
        upper.set_xlim(0, 2.06)
        upper.set_ylim(-0.42, 6.66)
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
            lower.hlines(y, 1e-71, value, color=color, linewidth=0.85)
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
            annotation_offset = (-5, 0) if name == "residual_allowance" else (5, 0)
            annotation_align = "right" if name == "residual_allowance" else "left"
            lower.annotate(
                scientific_label(value),
                xy=(value, y),
                xytext=annotation_offset,
                textcoords="offset points",
                ha=annotation_align,
                va="center",
                fontsize=5.35,
                color=color,
            )
        lower.set_xscale("log")
        lower.set_xlim(1e-71, 2e-3)
        lower.set_ylim(-0.52, 1.48)
        lower.set_yticks(scale_y)
        lower.set_yticklabels(scale_labels)
        lower.set_xlabel("weighted norm", labelpad=1)
        lower.grid(axis="x", which="major", color=GRID, linewidth=0.42)

        figure.text(
            0.012,
            0.985,
            "R0.38 tail-aware restart certificate",
            ha="left",
            va="top",
            fontsize=7.1,
            color=INK,
        )
        figure.text(0.985, 0.985, r"$\nu$", ha="right", va="top", fontsize=8.0, color=MUTED)
        figure.text(
            0.982,
            0.168,
            r"Degree separation gives $Z_{80}=0.992496<1$ although the old all-order full-space bound is $1.953683>1$.",
            fontsize=5.22,
            color=MUTED,
            ha="right",
            va="bottom",
        )
        figure.text(
            0.982,
            0.124,
            r"The exact residual is $2.12\times10^{-64}$ of its allowance. The sufficient inequality fails at the nearby probe $19/160$.",
            fontsize=5.22,
            color=MUTED,
            ha="right",
            va="bottom",
        )
        figure.text(
            0.982,
            0.080,
            r"The 62D low-block inverse is exactly inert on the certified tail; the degree-81 column scan is finite regression only.",
            fontsize=5.22,
            color=MUTED,
            ha="right",
            va="bottom",
        )
        figure.text(
            0.982,
            0.036,
            r"This is a local analytic branch certificate, not a proof of three-dimensional Navier--Stokes regularity.",
            fontsize=5.22,
            color=MUTED,
            ha="right",
            va="bottom",
        )

        for suffix in ("pdf", "svg", "png"):
            output = PACKAGE / f"figure.{suffix}"
            figure.savefig(output)
            if suffix == "svg":
                normalize_svg(output)
        plt.close(figure)


if __name__ == "__main__":
    draw()
