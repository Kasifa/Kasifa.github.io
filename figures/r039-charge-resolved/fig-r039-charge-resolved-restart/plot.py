#!/usr/bin/env python3
"""Render the R0.39 charge-resolved restart journal figure."""

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


def draw() -> None:
    radius_data = rows("radius-gain.csv")
    normalized = {
        (row["quantity"], row["version"]): float(
            Fraction(row["normalized_to_r031"])
        )
        for row in radius_data
    }
    charge_data = rows("charge-columns.csv")
    large_sector = rows("large-charge-sector.csv")[0]
    gates = {row["metric"]: row for row in rows("proof-gates.csv")}

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r039-charge-resolved"
        figure = plt.figure(figsize=(178 / 25.4, 110 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            width_ratios=(0.92, 1.48),
            height_ratios=(1.08, 1.02),
            left=0.126,
            right=0.984,
            bottom=0.300,
            top=0.826,
            wspace=0.38,
            hspace=0.78,
        )
        radius_axis = figure.add_subplot(grid[0, 0])
        charge_axis = figure.add_subplot(grid[0, 1])
        gate_axis = figure.add_subplot(grid[1, :])

        radius_axis.set_title("(a) Certified radius ladder", loc="left", pad=5)
        quantities = ["common_radius", "fixed_charge_radius"]
        quantity_labels = [r"common $r$", r"fixed-charge $r^3$"]
        versions = ["R0.31", "R0.37", "R0.38", "R0.39"]
        markers = ["o", "s", "D", "P"]
        colors = [MUTED, BLUE, GOLD, INK]
        fills = ["white", PALE_BLUE, PALE_GOLD, "white"]
        offsets = [0.30, 0.10, -0.10, -0.30]
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
                    value * 1.08,
                    y,
                    f"{version} {label}",
                    va="center",
                    fontsize=5.3,
                    color=color,
                )
        radius_axis.axvline(1, color=INK, linewidth=0.75, linestyle=(0, (4, 2)))
        radius_axis.set_xscale("log")
        radius_axis.set_xlim(0.88, 91)
        radius_axis.set_ylim(-0.52, 1.52)
        radius_axis.set_yticks(y_bases)
        radius_axis.set_yticklabels(quantity_labels)
        radius_axis.set_xlabel("normalized to R0.31")
        radius_axis.set_xticks([1, 2, 4, 8, 16, 32, 64])
        radius_axis.set_xticklabels(["1", "2", "4", "8", "16", "32", "64"])
        radius_axis.grid(axis="x", which="major", color=GRID, linewidth=0.42)
        charge_axis.set_title(
            r"(b) All-order tail bound by input charge at $r_*=397/2000$",
            loc="left",
            pad=5,
        )
        charge_values = [
            (int(row["input_charge"]), float(row["decimal"]))
            for row in charge_data
        ]
        residue_styles = [
            ("o", "-", "white"),
            ("s", (0, (4, 2)), PALE_BLUE),
            ("^", (0, (1.2, 1.5)), "white"),
        ]
        for residue, (marker, linestyle, fill) in enumerate(residue_styles):
            subset = [(x, y) for x, y in charge_values if x % 3 == residue]
            xs = [item[0] for item in subset]
            ys = [item[1] for item in subset]
            charge_axis.plot(
                xs,
                ys,
                color=BLUE,
                linestyle=linestyle,
                linewidth=0.75,
                marker=marker,
                markevery=8,
                markersize=2.6,
                markerfacecolor=fill,
                markeredgecolor=BLUE,
                markeredgewidth=0.65,
                label=rf"$s\equiv{residue}\ (\mathrm{{mod}}\ 3)$",
            )
        maximum_row = next(row for row in charge_data if row["is_maximum"] == "True")
        maximum_charge = int(maximum_row["input_charge"])
        maximum_value = float(maximum_row["decimal"])
        charge_axis.scatter(
            [maximum_charge],
            [maximum_value],
            s=34,
            marker="P",
            facecolor=PALE_GOLD,
            edgecolor=GOLD,
            linewidth=0.9,
            zorder=6,
        )
        charge_axis.annotate(
            rf"max $s={maximum_charge}$: {maximum_value:.4f}",
            xy=(maximum_charge, maximum_value),
            xytext=(-5, 8),
            textcoords="offset points",
            ha="right",
            va="bottom",
            fontsize=5.25,
            color=GOLD,
        )
        large_value = float(large_sector["decimal"])
        charge_axis.scatter(
            [248],
            [large_value],
            s=31,
            marker="D",
            facecolor="white",
            edgecolor=GOLD,
            linewidth=0.9,
            zorder=6,
        )
        charge_axis.annotate(
            rf"all $s\geq241$: {large_value:.4f}",
            xy=(248, large_value),
            xytext=(-4, -9),
            textcoords="offset points",
            ha="right",
            va="top",
            fontsize=5.25,
            color=GOLD,
        )
        charge_axis.axhline(1, color=INK, linewidth=0.78, linestyle=(0, (4, 2)))
        charge_axis.text(247, 0.965, "threshold 1", ha="right", va="top", fontsize=5.2)
        charge_axis.set_xlim(-5, 255)
        charge_axis.set_ylim(0, 1.05)
        charge_axis.set_xlabel(r"input charge $s$ (diamond closes the infinite sector)")
        charge_axis.set_ylabel("induced column bound")
        charge_axis.grid(axis="y", color=GRID, linewidth=0.42)
        charge_axis.legend(
            loc="lower right",
            fontsize=5.1,
            ncols=3,
            columnspacing=0.70,
            handlelength=1.6,
            handletextpad=0.3,
        )

        gate_axis.set_title("(c) Exact proof gates and nearby control", loc="left", pad=5)
        metric_order = [
            "old_tail_bound",
            "charge_resolved_tail",
            "ball_mapping_ratio",
            "old_transport_bound",
            "refined_transport_bound",
            "probe_transport_bound",
        ]
        metric_labels = [
            "old tail",
            "new tail",
            r"ball ratio",
            "old transport",
            "new transport",
            r"probe at $0.199$",
        ]
        y_positions = np.arange(len(metric_order) - 1, -1, -1, dtype=float)
        gate_markers = ["X", "D", "s", "X", "o", "P"]
        gate_colors = [MUTED, BLUE, BLUE, MUTED, GOLD, MUTED]
        gate_fills = [MUTED, PALE_BLUE, "white", MUTED, "white", "white"]
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
            if value > 1.70:
                text_x, align = value - 0.035, "right"
            elif 0.94 < value < 1.06:
                text_x, align = value + 0.030, "left"
            else:
                text_x, align = value + 0.035, "left"
            digits = 6 if 0.94 < value < 1.06 else 4
            gate_axis.text(
                text_x,
                y + 0.16,
                f"{value:.{digits}f}",
                ha=align,
                va="bottom",
                fontsize=5.25,
                color=color,
            )
        gate_axis.axvline(1, color=INK, linewidth=0.80, linestyle=(0, (4, 2)))
        gate_axis.text(0.985, 5.48, "threshold 1", ha="right", va="bottom", fontsize=5.25)
        gate_axis.set_xlim(0, 2.12)
        gate_axis.set_ylim(-0.40, 5.62)
        gate_axis.set_yticks(y_positions)
        gate_axis.set_yticklabels(metric_labels)
        gate_axis.set_xlabel("dimensionless upper bound")
        gate_axis.grid(axis="x", color=GRID, linewidth=0.42)

        figure.text(
            0.012,
            0.985,
            "R0.39 charge-resolved restart certificate",
            ha="left",
            va="top",
            fontsize=7.1,
            color=INK,
        )
        figure.text(0.985, 0.985, r"$\nu$", ha="right", va="top", fontsize=8.0, color=MUTED)
        footer = [
            r"The all-order charge-column maximum is $0.689601$ at $s=162$; one analytic sector closes every $s\geq241$ at $0.473943$.",
            r"Charge resolution raises the common certified radius from $59/500$ to $397/2000$; the fixed-charge disk grows by $4.76031\times$.",
            r"Transport is now the binding gate: $0.999410<1$ at the target, while the same sufficient bound is $1.002543>1$ at $0.199$.",
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
