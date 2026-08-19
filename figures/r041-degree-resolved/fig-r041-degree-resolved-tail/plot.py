#!/usr/bin/env python3
"""Render the R0.41 degree-resolved tail journal figure."""

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
LIGHT = "#aaa398"
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
    charge_data = rows("charge-columns.csv")
    degree_data = rows("degree-columns.csv")
    gate_data = {row["metric"]: row for row in rows("proof-gates.csv")}

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r041-degree-resolved-tail"
        figure = plt.figure(figsize=(178 / 25.4, 140 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            width_ratios=(0.91, 1.09),
            height_ratios=(1.0, 1.0),
            left=0.132,
            right=0.984,
            bottom=0.250,
            top=0.885,
            wspace=0.42,
            hspace=0.61,
        )
        radius_axis = figure.add_subplot(grid[0, 0])
        charge_axis = figure.add_subplot(grid[0, 1])
        degree_axis = figure.add_subplot(grid[1, 0])
        gate_axis = figure.add_subplot(grid[1, 1])

        radius_axis.set_title("(a) Certified radius ladder", loc="left", pad=5)
        quantities = ["common_radius", "fixed_charge_radius"]
        quantity_labels = [r"common $r$", r"fixed-charge $r^3$"]
        versions = ["R0.31", "R0.37", "R0.38", "R0.39", "R0.40", "R0.41"]
        markers = ["o", "s", "D", "P", "X", "^"]
        colors = [MUTED, BLUE, GOLD, MUTED, BLUE, INK]
        fills = ["white", PALE_BLUE, PALE_GOLD, "white", PALE_BLUE, INK]
        offsets = [0.38, 0.23, 0.08, -0.08, -0.23, -0.38]
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
                radius_axis.hlines(y, 0.93, value, color=color, linewidth=0.78)
                radius_axis.scatter(
                    [value],
                    [y],
                    s=22,
                    marker=marker,
                    facecolor=fill,
                    edgecolor=color,
                    linewidth=0.82,
                    zorder=5,
                )
                label = f"{value:.2f}".rstrip("0").rstrip(".")
                radius_axis.text(
                    value * 1.075,
                    y,
                    f"{version} {label}",
                    va="center",
                    fontsize=4.72,
                    color=color,
                )
        radius_axis.axvline(1, color=INK, linewidth=0.72, linestyle=(0, (4, 2)))
        radius_axis.set_xscale("log")
        radius_axis.set_xlim(0.88, 245)
        radius_axis.set_ylim(-0.56, 1.56)
        radius_axis.set_yticks(y_bases)
        radius_axis.set_yticklabels(quantity_labels)
        radius_axis.set_xlabel("normalized to R0.31")
        radius_axis.set_xticks([1, 2, 4, 8, 16, 32, 64, 128])
        radius_axis.set_xticklabels(["1", "2", "4", "8", "16", "32", "64", "128"])
        radius_axis.grid(axis="x", which="major", color=GRID, linewidth=0.40)

        charge_axis.set_title(
            r"(b) All-order tail sectors at $r_*=9/32$",
            loc="left",
            pad=5,
        )
        finite = [row for row in charge_data if row["kind"] != "large_charge"]
        xs = [int(row["plot_charge"]) for row in finite]
        ys = [float(row["decimal"]) for row in finite]
        charge_axis.plot(
            xs,
            ys,
            color=BLUE,
            linewidth=0.82,
            linestyle="-",
            label=r"finite sectors $-1\leq s\leq240$",
        )
        for charge, marker, fill, annotation, shift in (
            (-1, "o", "white", r"$s=-1$", (6, 4)),
            (162, "s", PALE_BLUE, r"$s=162$", (5, 5)),
        ):
            index = xs.index(charge)
            charge_axis.scatter(
                [charge],
                [ys[index]],
                s=24,
                marker=marker,
                facecolor=fill,
                edgecolor=BLUE,
                linewidth=0.85,
                zorder=5,
            )
            charge_axis.annotate(
                f"{annotation}  {ys[index]:.3f}",
                xy=(charge, ys[index]),
                xytext=shift,
                textcoords="offset points",
                fontsize=4.9,
                color=BLUE,
            )
        large = charge_data[-1]
        large_value = float(large["decimal"])
        charge_axis.scatter(
            [241],
            [large_value],
            s=30,
            marker="D",
            facecolor=PALE_GOLD,
            edgecolor=GOLD,
            linewidth=0.9,
            zorder=6,
        )
        charge_axis.annotate(
            rf"$s\geq241$  {large_value:.3f}",
            xy=(241, large_value),
            xytext=(-5, 7),
            textcoords="offset points",
            ha="right",
            fontsize=4.9,
            color=GOLD,
        )
        legacy = float(gate_data["target_legacy_tail"]["decimal"])
        charge_axis.axhline(
            legacy,
            color=MUTED,
            linewidth=0.75,
            linestyle=(0, (1.4, 1.5)),
        )
        charge_axis.text(
            238,
            legacy - 0.026,
            f"legacy {legacy:.3f}",
            ha="right",
            va="top",
            fontsize=4.85,
            color=MUTED,
        )
        charge_axis.axhline(1, color=INK, linewidth=0.75, linestyle=(0, (4, 2)))
        charge_axis.text(238, 1.018, "threshold 1", ha="right", fontsize=4.85)
        charge_axis.set_xlim(-8, 249)
        charge_axis.set_ylim(0.0, 1.205)
        charge_axis.set_xticks([-1, 60, 120, 162, 200, 241])
        charge_axis.set_xlabel(r"input charge $s$ ($241$ denotes $s\geq241$)")
        charge_axis.set_ylabel("induced column bound")
        charge_axis.grid(axis="y", color=GRID, linewidth=0.40)

        degree_axis.set_title(
            r"(c) Former worst charge $s=162$",
            loc="left",
            pad=5,
        )
        degrees = [int(row["input_degree"]) for row in degree_data]
        exact_values = [float(row["decimal"]) for row in degree_data]
        sector_bound = float(degree_data[0]["all_order_bound_decimal"])
        infinity = float(degree_data[0]["infinite_core_decimal"])
        degree_axis.plot(
            degrees,
            exact_values,
            color=BLUE,
            linewidth=0.86,
            marker="o",
            markersize=3.0,
            markerfacecolor="white",
            markeredgecolor=BLUE,
            markeredgewidth=0.72,
            label="finite exact columns",
        )
        degree_axis.axhline(
            sector_bound,
            color=GOLD,
            linewidth=0.78,
            linestyle=(0, (4, 2)),
            label="all-order sector bound",
        )
        degree_axis.axhline(
            infinity,
            color=MUTED,
            linewidth=0.72,
            linestyle=(0, (1.4, 1.5)),
            label=r"core endpoint $x=0$",
        )
        minimum_index = int(np.argmin(exact_values))
        degree_axis.annotate(
            f"minimum {exact_values[minimum_index]:.3f} at j={degrees[minimum_index]}",
            xy=(degrees[minimum_index], exact_values[minimum_index]),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=4.85,
            color=BLUE,
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.6},
        )
        degree_axis.text(
            1510,
            sector_bound + 0.010,
            f"bound {sector_bound:.3f}",
            ha="right",
            va="bottom",
            fontsize=4.85,
            color=GOLD,
        )
        degree_axis.text(
            1510,
            infinity + 0.008,
            f"$x=0$  {infinity:.3f}",
            ha="right",
            va="bottom",
            fontsize=4.85,
            color=MUTED,
        )
        degree_axis.set_xscale("log")
        degree_axis.set_xlim(72, 1850)
        degree_axis.set_ylim(0.265, 0.615)
        degree_axis.set_xticks([81, 162, 324, 810, 1620])
        degree_axis.set_xticklabels(["81", "162", "324", "810", "1620"])
        degree_axis.set_xlabel(r"input degree $j$ (finite regressions)")
        degree_axis.set_ylabel("exact column ratio")
        degree_axis.grid(axis="y", color=GRID, linewidth=0.40)

        gate_axis.set_title(
            "(d) Acceptance, target, and adjacent control",
            loc="left",
            pad=5,
        )
        metric_order = [
            "acceptance_legacy_tail",
            "acceptance_resolved_tail",
            "acceptance_transport",
            "target_legacy_tail",
            "target_resolved_tail",
            "target_transport",
            "probe_resolved_tail",
            "probe_transport",
        ]
        metric_labels = [
            "0.257 legacy tail",
            "0.257 resolved tail",
            "0.257 transport",
            "0.28125 legacy tail",
            "0.28125 resolved tail",
            "0.28125 transport",
            "0.282 resolved tail",
            "0.282 transport",
        ]
        y_positions = np.array([8.0, 7.0, 6.0, 4.5, 3.5, 2.5, 1.0, 0.0])
        styles = {
            "legacy tail": (MUTED, "X", MUTED),
            "resolved tail": (BLUE, "o", "white"),
            "transport": (GOLD, "s", PALE_GOLD),
        }
        for name, label, y in zip(metric_order, metric_labels, y_positions):
            row = gate_data[name]
            value = float(row["decimal"])
            color, marker, fill = styles[row["gate"]]
            gate_axis.hlines(y, 0.62, value, color=color, linewidth=0.82)
            gate_axis.scatter(
                [value],
                [y],
                s=25,
                marker=marker,
                facecolor=fill,
                edgecolor=color,
                linewidth=0.88,
                zorder=5,
            )
            if value > 1.10:
                text_x, align = value - 0.012, "right"
            else:
                text_x, align = value + 0.014, "left"
            digits = 6 if 0.98 < value < 1.02 else 3
            gate_axis.text(
                text_x,
                y + 0.17,
                f"{value:.{digits}f}",
                ha=align,
                va="bottom",
                fontsize=4.8,
                color=color,
            )
        gate_axis.axvline(1, color=INK, linewidth=0.78, linestyle=(0, (4, 2)))
        gate_axis.text(0.995, 8.43, "threshold 1", ha="right", fontsize=4.85)
        gate_axis.axhline(5.25, color=GRID, linewidth=0.45)
        gate_axis.axhline(1.75, color=GRID, linewidth=0.45)
        gate_axis.set_xlim(0.61, 1.185)
        gate_axis.set_ylim(-0.45, 8.58)
        gate_axis.set_yticks(y_positions)
        gate_axis.set_yticklabels(metric_labels)
        gate_axis.set_xlabel("dimensionless upper bound")
        gate_axis.grid(axis="x", color=GRID, linewidth=0.40)

        figure.text(
            0.012,
            0.985,
            "R0.41 degree-resolved active-tail certificate",
            ha="left",
            va="top",
            fontsize=7.2,
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
            r"For each $2\leq s\leq240$, convexity of the complete core in $x=s/j$ reduces every $j>80$ to two common endpoints.",
            r"The old $0.257$ failure passes; the common radius reaches $9/32$, where tail $=0.778542$ and transport $=0.996211$.",
            r"At $0.282$, the active fixed point still closes but transport is $1.000375>1$: this is a sufficient-bound failure only.",
            r"Finite degree points are regressions. The reduced-system theorem does not prove three-dimensional Navier--Stokes regularity.",
        ]
        for index, line in enumerate(footer):
            figure.text(
                0.982,
                0.164 - 0.038 * index,
                line,
                fontsize=4.95,
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
