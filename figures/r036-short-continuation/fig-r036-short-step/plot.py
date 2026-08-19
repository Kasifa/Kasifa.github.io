#!/usr/bin/env python3
"""Render the R0.36 orbit-safe short-continuation figure."""

from __future__ import annotations

import csv
from fractions import Fraction
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
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
    path.write_text(
        "\n".join(line.rstrip() for line in lines) + "\n",
        encoding="utf-8",
    )


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def scientific_label(value: float) -> str:
    exponent = int(np.floor(np.log10(value)))
    coefficient = value / (10**exponent)
    return rf"$ {coefficient:.3f}\times10^{{{exponent}}}$"


def draw() -> None:
    geometry = {record["name"]: record for record in rows("geometry.csv")}
    scales = {record["name"]: record for record in rows("certificate-scales.csv")}
    jacobian = {record["name"]: record["exact_or_text"] for record in rows("jacobian.csv")}

    normalized = {
        name: float(Fraction(record["normalized_by_r031"]))
        for name, record in geometry.items()
    }
    scale_order = [
        "all_order_residual_upper_bound",
        "outer_tail_bound",
        "inner_inclusion_radius",
        "finite_exact_residual_norm",
    ]
    values = {name: float(scales[name]["decimal"]) for name in scale_order}

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        figure, (left, right) = plt.subplots(
            1,
            2,
            figsize=(178 / 25.4, 84 / 25.4),
            gridspec_kw={"width_ratios": (1.00, 1.12)},
            layout="none",
        )

        left.set_title("(a) Orbit-safe local geometry", loc="left", pad=5)
        center = normalized["center_modulus"]
        domain = Circle(
            (0, 0),
            normalized["r031_radius"],
            fill=False,
            edgecolor=MUTED,
            linewidth=0.9,
            linestyle=(0, (5, 2)),
            label=r"R0.31 domain $\rho_*$",
        )
        outer = Circle(
            (center, 0),
            normalized["outer_local_radius"],
            facecolor=PALE_BLUE,
            edgecolor=BLUE,
            linewidth=0.9,
            alpha=0.72,
            label=r"outer disc $R=5\rho_*/7$",
        )
        orbit = Circle(
            (center, 0),
            normalized["inner_affine_orbit_extent"],
            fill=False,
            edgecolor=GOLD,
            linewidth=1.05,
            linestyle=(0, (4, 2)),
            label=r"affine orbit envelope $3\rho_*/7$",
        )
        inner = Circle(
            (center, 0),
            normalized["inner_local_radius"],
            facecolor=PALE_GOLD,
            edgecolor=INK,
            linewidth=0.95,
            label=r"inner disc $r=\rho_*/7$",
        )
        for patch in (domain, outer, orbit, inner):
            left.add_patch(patch)
        left.scatter([center], [0], s=18, marker="x", color=INK, linewidth=0.9, zorder=6)
        left.annotate(
            r"$c_Z=\rho_*/7$",
            xy=(center, 0),
            xytext=(0.33, -0.26),
            arrowprops={"arrowstyle": "->", "color": MUTED, "lw": 0.65},
            color=MUTED,
            fontsize=6.15,
        )
        left.annotate(
            r"strict outer margin $\rho_*/7$",
            xy=(6 / 7, 0),
            xytext=(0.58, -0.72),
            arrowprops={"arrowstyle": "-[", "color": BLUE, "lw": 0.65},
            color=BLUE,
            fontsize=6.0,
            ha="center",
        )
        left.text(
            -0.98,
            -1.07,
            r"$W$-plane geometry is reflected: $c_W=-\rho_*/7$.",
            color=MUTED,
            fontsize=5.95,
            va="top",
        )
        left.axhline(0, color=GRID, linewidth=0.45, zorder=0)
        left.axvline(0, color=GRID, linewidth=0.45, zorder=0)
        left.set_xlabel(r"$\operatorname{Re}(Z)/\rho_*$")
        left.set_ylabel(r"$\operatorname{Im}(Z)/\rho_*$")
        left.set_xlim(-1.08, 1.08)
        left.set_ylim(-1.16, 1.08)
        left.set_aspect("equal", adjustable="box")
        left.set_xticks([-1, -0.5, 0, 0.5, 1])
        left.set_yticks([-1, -0.5, 0, 0.5, 1])
        left.legend(loc="upper left", bbox_to_anchor=(0.0, 0.995), fontsize=6.05)

        right.set_title("(b) Certified enclosure scales", loc="left", pad=5)
        y_positions = np.array([3, 2, 1, 0], dtype=float)
        markers = ["D", "^", "s", "o"]
        colors = [BLUE, BLUE, BLUE, GOLD]
        line_styles = [(0, (5, 2)), (0, (5, 2)), (0, (5, 2)), "solid"]
        for name, y, marker, color, line_style in zip(
            scale_order, y_positions, markers, colors, line_styles
        ):
            value = values[name]
            right.hlines(y, 1e-80, value, color=color, linewidth=0.85, linestyle=line_style)
            right.scatter(
                [value],
                [y],
                s=28,
                marker=marker,
                facecolor="white" if name != "finite_exact_residual_norm" else PALE_GOLD,
                edgecolor=color,
                linewidth=0.9,
                zorder=5,
            )
            if name in {"all_order_residual_upper_bound", "outer_tail_bound"}:
                right.annotate(
                    scientific_label(value),
                    xy=(value, y),
                    xytext=(-6, 0),
                    textcoords="offset points",
                    ha="right",
                    va="center",
                    color=color,
                    fontsize=5.8,
                )
            else:
                right.annotate(
                    scientific_label(value),
                    xy=(value, y),
                    xytext=(5, 0),
                    textcoords="offset points",
                    ha="left",
                    va="center",
                    color=color,
                    fontsize=5.8,
                )
        right.set_xscale("log")
        right.set_xlim(1e-80, 3e-6)
        right.set_ylim(-0.65, 3.62)
        right.set_yticks(y_positions)
        right.set_yticklabels(
            [
                "residual upper bound",
                "outer tail (N=40)",
                "inner inclusion radius",
                "finite exact residual",
            ]
        )
        right.set_xlabel("norm scale")
        right.grid(axis="x", which="major", color=GRID, linewidth=0.42)
        right.text(
            1.1e-79,
            3.43,
            "ALL-ORDER CERTIFICATES",
            color=BLUE,
            fontsize=5.55,
            fontweight="bold",
            va="top",
        )
        right.text(
            1.1e-79,
            0.42,
            "FINITE EXACT DIAGNOSTIC",
            color=GOLD,
            fontsize=5.55,
            fontweight="bold",
            va="bottom",
        )
        right.text(
            1.1e-79,
            -0.48,
            rf"$J_8$: {jacobian['dimension']}D;  $\|J_8^{{-1}}\|_1={jacobian['maximum_unweighted_column_l1_norm']}$",
            color=MUTED,
            fontsize=5.9,
            va="bottom",
        )

        figure.text(
            0.012,
            0.986,
            "R0.36 one-step continuation certificate",
            ha="left",
            va="top",
            fontsize=7.1,
            color=INK,
        )
        figure.text(0.985, 0.986, r"$\nu$", ha="right", va="top", fontsize=8.0, color=MUTED)
        figure.text(
            0.985,
            0.052,
            r"$c=(\rho_*/7,-\rho_*/7)$, $r=\rho_*/7$, $R=5\rho_*/7$; after conjugacy $s/S=1/2$ and $C=121/48$.",
            fontsize=5.45,
            color=MUTED,
            ha="right",
            va="bottom",
        )
        figure.text(
            0.985,
            0.016,
            "All-order tail and residual bounds cover omitted degrees; the 42D inverse is a finite regression test, not an infinite inverse.",
            fontsize=5.45,
            color=MUTED,
            ha="right",
            va="bottom",
        )
        figure.subplots_adjust(left=0.076, right=0.985, bottom=0.22, top=0.82, wspace=0.36)

        for suffix in ("pdf", "svg", "png"):
            output = PACKAGE / f"figure.{suffix}"
            figure.savefig(output)
            if suffix == "svg":
                normalize_svg(output)
        public_figures = REPOSITORY / "public/figures"
        public_figures.mkdir(parents=True, exist_ok=True)
        for suffix in ("svg", "png"):
            output = public_figures / f"r0-36-short-step.{suffix}"
            figure.savefig(output)
            if suffix == "svg":
                normalize_svg(output)
        plt.close(figure)


if __name__ == "__main__":
    draw()
