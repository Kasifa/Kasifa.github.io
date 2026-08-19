#!/usr/bin/env python3
"""Render the R0.40 exact two-endpoint transport journal figure."""

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
    path.write_text(
        "\n".join(line.rstrip() for line in lines) + "\n",
        encoding="utf-8",
    )


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def draw() -> None:
    radius_data = rows("radius-gain.csv")
    normalized = {
        (row["quantity"], row["version"]): float(
            Fraction(row["normalized_to_r031"])
        )
        for row in radius_data
    }
    endpoint_data = rows("endpoint-columns.csv")
    gates = {row["metric"]: row for row in rows("proof-gates.csv")}

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r040-two-endpoint-transport"
        figure = plt.figure(figsize=(178 / 25.4, 110 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            width_ratios=(0.93, 1.47),
            height_ratios=(1.08, 1.02),
            left=0.126,
            right=0.984,
            bottom=0.300,
            top=0.826,
            wspace=0.38,
            hspace=0.78,
        )
        radius_axis = figure.add_subplot(grid[0, 0])
        endpoint_axis = figure.add_subplot(grid[0, 1])
        gate_axis = figure.add_subplot(grid[1, :])

        radius_axis.set_title("(a) Certified radius ladder", loc="left", pad=5)
        quantities = ["common_radius", "fixed_charge_radius"]
        quantity_labels = [r"common $r$", r"fixed-charge $r^3$"]
        versions = ["R0.31", "R0.37", "R0.38", "R0.39", "R0.40"]
        markers = ["o", "s", "D", "P", "X"]
        colors = [MUTED, BLUE, GOLD, MUTED, INK]
        fills = ["white", PALE_BLUE, PALE_GOLD, "white", INK]
        offsets = [0.34, 0.17, 0.0, -0.17, -0.34]
        y_bases = [1.0, 0.0]
        for quantity, y_base in zip(quantities, y_bases):
            for version, marker, color, fill, offset in zip(
                versions,
                markers,
                colors,
                fills,
                offsets,
            ):
                value = normalized[(quantity, version)]
                y = y_base + offset
                radius_axis.hlines(y, 0.92, value, color=color, linewidth=0.82)
                radius_axis.scatter(
                    [value],
                    [y],
                    s=25,
                    marker=marker,
                    facecolor=fill,
                    edgecolor=color,
                    linewidth=0.9,
                    zorder=5,
                )
                label = f"{value:.2f}".rstrip("0").rstrip(".")
                radius_axis.text(
                    value * 1.075,
                    y,
                    f"{version} {label}",
                    va="center",
                    fontsize=5.05,
                    color=color,
                )
        radius_axis.axvline(
            1,
            color=INK,
            linewidth=0.75,
            linestyle=(0, (4, 2)),
        )
        radius_axis.set_xscale("log")
        radius_axis.set_xlim(0.88, 190)
        radius_axis.set_ylim(-0.56, 1.56)
        radius_axis.set_yticks(y_bases)
        radius_axis.set_yticklabels(quantity_labels)
        radius_axis.set_xlabel("normalized to R0.31")
        radius_axis.set_xticks([1, 2, 4, 8, 16, 32, 64, 128])
        radius_axis.set_xticklabels(["1", "2", "4", "8", "16", "32", "64", "128"])
        radius_axis.grid(axis="x", which="major", color=GRID, linewidth=0.42)

        endpoint_axis.set_title(
            r"(b) Exact transport endpoints at $r_*=32/125$",
            loc="left",
            pad=5,
        )
        endpoint_styles = {
            "x=-1": {
                "color": BLUE,
                "linestyle": "-",
                "marker": "o",
                "fill": "white",
                "label": r"$x=-1$ endpoint",
            },
            "x=2": {
                "color": GOLD,
                "linestyle": (0, (4, 2)),
                "marker": "s",
                "fill": PALE_GOLD,
                "label": r"$x=2$ endpoint",
            },
        }
        for endpoint, style in endpoint_styles.items():
            subset = [
                row for row in endpoint_data if row["endpoint"] == endpoint
            ]
            xs = [int(row["input_degree"]) for row in subset]
            ys = [float(row["decimal"]) for row in subset]
            endpoint_axis.plot(
                xs,
                ys,
                color=style["color"],
                linestyle=style["linestyle"],
                linewidth=0.88,
                marker=style["marker"],
                markevery=[0, 1, 4, 19, 40, 60, 80],
                markersize=2.8,
                markerfacecolor=style["fill"],
                markeredgecolor=style["color"],
                markeredgewidth=0.65,
                label=style["label"],
            )
            endpoint_axis.annotate(
                f"{ys[0]:.4f}",
                xy=(xs[0], ys[0]),
                xytext=(7, 1 if endpoint == "x=2" else -8),
                textcoords="offset points",
                ha="left",
                va="center",
                fontsize=5.25,
                color=style["color"],
            )
        old_bound = float(gates["r039_termwise_transport"]["decimal"])
        endpoint_axis.axhline(
            old_bound,
            color=MUTED,
            linewidth=0.78,
            linestyle=(0, (1.4, 1.5)),
        )
        endpoint_axis.text(
            80,
            old_bound - 0.035,
            f"R0.39 termwise {old_bound:.3f}",
            ha="right",
            va="top",
            fontsize=5.1,
            color=MUTED,
        )
        endpoint_axis.axhline(
            1,
            color=INK,
            linewidth=0.78,
            linestyle=(0, (4, 2)),
        )
        endpoint_axis.text(
            80,
            1.018,
            "threshold 1",
            ha="right",
            va="bottom",
            fontsize=5.1,
        )
        endpoint_axis.set_xlim(0, 82)
        endpoint_axis.set_ylim(0.45, 1.44)
        endpoint_axis.set_xticks([1, 20, 40, 60, 81])
        endpoint_axis.set_xlabel(
            r"input degree $j$ (all larger degrees proven lower)"
        )
        endpoint_axis.set_ylabel("exact column ratio")
        endpoint_axis.grid(axis="y", color=GRID, linewidth=0.42)
        endpoint_axis.legend(
            loc="upper right",
            bbox_to_anchor=(0.99, 0.84),
            fontsize=5.2,
            ncols=2,
            columnspacing=0.8,
            handlelength=1.8,
            handletextpad=0.35,
        )

        gate_axis.set_title("(c) Exact proof gates and adjacent control", loc="left", pad=5)
        metric_order = [
            "target_active_tail",
            "r039_termwise_transport",
            "target_transport_x_minus_1",
            "target_transport_x_plus_2",
            "probe_active_tail",
            "probe_polynomial_transport",
        ]
        metric_labels = [
            r"target tail",
            r"R0.39 transport",
            r"target $x=-1$",
            r"target $x=2$",
            r"probe tail $0.257$",
            r"probe transport",
        ]
        y_positions = np.arange(len(metric_order) - 1, -1, -1, dtype=float)
        gate_markers = ["D", "X", "o", "s", "P", "^"]
        gate_colors = [BLUE, MUTED, BLUE, GOLD, MUTED, GOLD]
        gate_fills = [PALE_BLUE, MUTED, "white", PALE_GOLD, "white", "white"]
        for name, label, y, marker, color, fill in zip(
            metric_order,
            metric_labels,
            y_positions,
            gate_markers,
            gate_colors,
            gate_fills,
        ):
            value = float(gates[name]["decimal"])
            gate_axis.hlines(y, 0, value, color=color, linewidth=0.85)
            gate_axis.scatter(
                [value],
                [y],
                s=27,
                marker=marker,
                facecolor=fill,
                edgecolor=color,
                linewidth=0.9,
                zorder=5,
            )
            if value > 1.25:
                text_x, align = value - 0.025, "right"
            elif 0.97 < value < 1.03:
                text_x, align = value + 0.018, "left"
            else:
                text_x, align = value + 0.025, "left"
            digits = 6 if 0.97 < value < 1.03 else 4
            gate_axis.text(
                text_x,
                y + 0.16,
                f"{value:.{digits}f}",
                ha=align,
                va="bottom",
                fontsize=5.25,
                color=color,
            )
        gate_axis.axvline(
            1,
            color=INK,
            linewidth=0.80,
            linestyle=(0, (4, 2)),
        )
        gate_axis.text(
            0.99,
            5.48,
            "threshold 1",
            ha="right",
            va="bottom",
            fontsize=5.25,
        )
        gate_axis.set_xlim(0, 1.48)
        gate_axis.set_ylim(-0.40, 5.62)
        gate_axis.set_yticks(y_positions)
        gate_axis.set_yticklabels(metric_labels)
        gate_axis.set_xlabel("dimensionless upper bound")
        gate_axis.grid(axis="x", color=GRID, linewidth=0.42)

        figure.text(
            0.012,
            0.985,
            "R0.40 exact two-endpoint transport certificate",
            ha="left",
            va="top",
            fontsize=7.1,
            color=INK,
        )
        figure.text(
            0.985,
            0.985,
            r"$\nu$",
            ha="right",
            va="top",
            fontsize=8.0,
            color=MUTED,
        )
        footer = [
            r"Convexity reduces every input slope to $x=-1$ or $x=2$; monotonicity makes $j=1$ the exact polynomial maximum.",
            r"The common certified radius rises from $397/2000$ to $32/125$; the fixed-charge disk grows by $2.14505\times$.",
            r"At $0.256$, transport is $0.862199<1$ and the active tail is $0.994409<1$; at $0.257$, only the tail bound fails.",
            r"Finite columns are regressions only. This reduced-system theorem does not prove three-dimensional Navier--Stokes regularity.",
        ]
        for index, line in enumerate(footer):
            figure.text(
                0.982,
                0.172 - 0.044 * index,
                line,
                fontsize=5.15,
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
