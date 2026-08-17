#!/usr/bin/env python3
"""Plot the R0.20 compact boundary certificates and objective comparison.

Chart contract
--------------
Question: Where are the two exact boundary-strip certificates in compact
coordinates, and how does the certified interior maximum compare with each
codimension-one boundary closure?
Takeaway: The strips cover the only two degeneracy lines, while every boundary
closure maximum stays below the 5.95187 percent interior maximum.
Family: two compact-domain interval diagrams plus one horizontal comparison
bar chart; explicit static Matplotlib export.
Palette: hard two-root cap (blue certificate regions, gold focal maximum),
with hatching, fill state, and marker shape as non-colour distinctions.
Footprint: 178 mm by 82 mm; PDF/SVG plus 600 dpi PNG.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Patch, Rectangle


PACKAGE = Path(__file__).resolve().parent
STYLE = PACKAGE.parents[1] / "journal.mplstyle"
INK = "#27221d"
MUTED = "#6b675f"
BLUE = "#315a76"
BLUE_LIGHT = "#dbe7ed"
GOLD = "#b07b2f"


def load_rows() -> list[dict[str, str]]:
    with (PACKAGE / "data.csv").open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def number(row: dict[str, str], key: str) -> float:
    return float(row[key])


def draw_blossom(figure: plt.Figure) -> None:
    center = (0.985, 0.965)
    radius = 0.006
    for dx, dy in ((0, .012), (.011, .004), (.007, -.010), (-.007, -.010), (-.011, .004)):
        figure.add_artist(
            Circle(
                (center[0] + dx, center[1] + dy),
                radius,
                transform=figure.transFigure,
                facecolor="none",
                edgecolor=GOLD,
                linewidth=.55,
            )
        )


def certificate_panel(
    axis: plt.Axes,
    rows: list[dict[str, str]],
    analytic_label: str,
    core_label: str,
    horizontal_coordinate: str,
    title: str,
) -> None:
    by_label = {row["label"]: row for row in rows if row["record_type"] == "strip"}
    analytic = by_label[analytic_label]
    core = by_label[core_label]
    for row, face, hatch, zorder in (
        (analytic, BLUE_LIGHT, None, 1),
        (core, "none", "////", 2),
    ):
        axis.add_patch(
            Rectangle(
                (number(row, "xmin"), number(row, "ymin")),
                number(row, "xmax") - number(row, "xmin"),
                number(row, "ymax") - number(row, "ymin"),
                facecolor=face,
                edgecolor=BLUE,
                hatch=hatch,
                linewidth=.75,
                zorder=zorder,
            )
        )
    roots = [row for row in rows if row["record_type"] == "root"]
    for row in roots:
        focal = row["label"] == "interior global maximum"
        axis.plot(
            number(row, horizontal_coordinate),
            number(row, "w"),
            marker="*" if focal else "o",
            markersize=6 if focal else 4,
            markerfacecolor=GOLD if focal else "white",
            markeredgecolor=INK,
            markeredgewidth=.65,
            linestyle="none",
            zorder=4,
        )
    axis.set_xlim(0, 1)
    axis.set_ylim(0, 1)
    axis.set_xticks((0, .25, .5, .75, 1))
    axis.set_yticks((0, .25, .5, .75, 1))
    axis.set_xlabel(f"${horizontal_coordinate}$")
    axis.set_ylabel("$w$")
    axis.set_title(title, loc="left", pad=5)
    axis.set_aspect("equal", adjustable="box")


def maxima_panel(axis: plt.Axes, rows: list[dict[str, str]]) -> None:
    maxima = [row for row in rows if row["record_type"] == "maximum"]
    label_map = {
        "positive interior": "Positive interior",
        "q=0 boundary closure": "$q=0$ closure",
        "p=0 boundary closure": "$p=0$ closure",
        "q=infinity boundary closure": "$q=\\infty$ closure",
        "p=infinity boundary closure": "$p=\\infty$ closure",
        "x=0 or x=infinity": "$x=0,\\infty$",
    }
    source_labels = [row["label"] for row in maxima][::-1]
    labels = [label_map[label] for label in source_labels]
    values = [number(row, "target_fraction_percent") for row in maxima][::-1]
    colors = [GOLD if label == "positive interior" else "white" for label in source_labels]
    edges = [INK if label == "positive interior" else BLUE for label in source_labels]
    hatches = [None if label == "positive interior" else "////" for label in source_labels]
    bars = axis.barh(
        range(len(labels)),
        values,
        height=.62,
        color=colors,
        edgecolor=edges,
        linewidth=.7,
    )
    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)
    axis.set_yticks(range(len(labels)), labels)
    axis.set_xlim(0, 6.65)
    axis.set_xlabel("target fraction (%)")
    axis.set_title("(c) Certified closure maxima", loc="left", pad=5)
    axis.axvline(0, color=INK, linewidth=.55)
    for bar, value in zip(bars, values):
        label = "0" if value == 0 else (f"{value:.3f}" if value >= .1 else f"{value:.3f}")
        axis.text(
            max(value + .09, .09),
            bar.get_y() + bar.get_height() / 2,
            label,
            va="center",
            ha="left",
            fontsize=6.2,
            color=INK,
        )
    axis.spines["left"].set_visible(False)
    axis.tick_params(axis="y", length=0)


def main() -> None:
    rows = load_rows()
    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        figure = plt.figure(figsize=(178 / 25.4, 82 / 25.4), layout="none")
        grid = figure.add_gridspec(1, 3, width_ratios=(1, 1, 1.5), wspace=.43)
        zero_axis = figure.add_subplot(grid[0, 0])
        infinity_axis = figure.add_subplot(grid[0, 1])
        maxima_axis = figure.add_subplot(grid[0, 2])
        certificate_panel(
            zero_axis,
            rows,
            "x=0 analytic strip",
            "x=0 dyadic core",
            "u",
            "(a) $x=0$ certificate",
        )
        certificate_panel(
            infinity_axis,
            rows,
            "x=infinity analytic strip",
            "x=infinity dyadic core",
            "v",
            "(b) $x=\\infty$ certificate",
        )
        maxima_panel(maxima_axis, rows)
        legend_handles = [
            Patch(facecolor=BLUE_LIGHT, edgecolor=BLUE, label="exact sign strip"),
            Patch(facecolor="white", edgecolor=BLUE, hatch="////", label="delegated dyadic core"),
            Line2D([], [], marker="*", markersize=6, markerfacecolor=GOLD, markeredgecolor=INK, linestyle="none", label="interior global maximum"),
            Line2D([], [], marker="o", markersize=4, markerfacecolor="white", markeredgecolor=INK, linestyle="none", label="interior saddle"),
        ]
        figure.legend(
            handles=legend_handles,
            loc="upper left",
            bbox_to_anchor=(.005, .925),
            ncol=4,
            columnspacing=1.15,
            handlelength=1.5,
            fontsize=6.3,
        )
        figure.suptitle(
            "R0.20 compact boundary certificates and target-fraction comparison",
            x=.005,
            y=.995,
            ha="left",
            va="top",
            fontsize=8.5,
            color=INK,
        )
        figure.subplots_adjust(left=.055, right=.985, bottom=.17, top=.79, wspace=.48)
        draw_blossom(figure)
        for suffix in ("pdf", "svg", "png"):
            figure.savefig(PACKAGE / f"figure.{suffix}")
        plt.close(figure)


if __name__ == "__main__":
    main()
