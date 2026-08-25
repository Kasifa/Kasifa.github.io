#!/usr/bin/env python3
"""Plot R0.71O soft-denominator faces at double-column journal size."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle


BLUE = "#355C7D"
ORANGE = "#C76B3C"
INK = "#252422"
GRAY = "#77736C"
LIGHT_GRAY = "#D9D5CD"
PALE_BLUE = "#DDE7EF"
PALE_ORANGE = "#F4E1D5"
PAPER = "#FBF9F4"


def load(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault((row["panel"], row["series"]), []).append(row)
    return rows, grouped


def add_blossom(fig) -> None:
    center_x, center_y = 0.955, 0.946
    radius = 0.0058
    offsets = ((-0.006, 0), (0.006, 0), (0, -0.007), (0, 0.007))
    colors = (BLUE, ORANGE, BLUE, ORANGE)
    for (dx, dy), color in zip(offsets, colors, strict=True):
        fig.add_artist(
            Circle(
                (center_x + dx, center_y + dy),
                radius,
                transform=fig.transFigure,
                facecolor="none",
                edgecolor=color,
                linewidth=0.7,
            )
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("data.csv"))
    parser.add_argument("--output-stem", type=Path, default=Path("figure"))
    args = parser.parse_args()
    _, grouped = load(args.data)

    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 7.0,
            "axes.titlesize": 7.8,
            "axes.labelsize": 6.7,
            "legend.fontsize": 5.7,
            "xtick.labelsize": 5.9,
            "ytick.labelsize": 5.9,
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

    fig = plt.figure(figsize=(178 / 25.4, 118 / 25.4))
    fig.set_size_inches(178 / 25.4, 118 / 25.4, forward=False)
    grid = fig.add_gridspec(
        2,
        2,
        left=0.075,
        right=0.975,
        bottom=0.145,
        top=0.865,
        wspace=0.34,
        hspace=0.56,
    )
    ax_a = fig.add_subplot(grid[0, 0])
    ax_b = fig.add_subplot(grid[0, 1])
    ax_c = fig.add_subplot(grid[1, 0])
    ax_d = fig.add_subplot(grid[1, 1])

    fig.text(
        0.065,
        0.955,
        "R0.71O  /  soft denominator layers and one-sided face measures",
        fontsize=9.7,
        fontweight="bold",
        color=INK,
    )
    fig.text(
        0.065,
        0.922,
        "Exact finite-order profiles - abstract budget separation - one genuine NSE initial jet",
        fontsize=6.5,
        color=GRAY,
    )
    add_blossom(fig)

    # Panel A: normalized soft profiles and the one-sided atom directions.
    profiles: dict[str, list[tuple[float, float]]] = {}
    for row in grouped[("A", "softProfile")]:
        profiles.setdefault(row["case"], []).append(
            (float(row["x"]), float(row["value"]))
        )
    odd = sorted(profiles["odd m=1, b>0"])
    even = sorted(profiles["even m=2, b>0"])
    ax_a.plot(
        [item[0] for item in odd],
        [item[1] for item in odd],
        color=BLUE,
        linewidth=1.45,
        label=r"odd $m=1$: $A_-=0$, $A_+=A$",
    )
    ax_a.plot(
        [item[0] for item in even],
        [item[1] for item in even],
        color=ORANGE,
        linewidth=1.35,
        linestyle="--",
        label=r"even $m=2$: $A_-=A_+=A$",
    )
    ax_a.axvline(0.0, color=INK, linewidth=0.55)
    ax_a.annotate(
        "",
        xy=(0.14, 0.34),
        xytext=(0.14, 0.035),
        arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.15),
    )
    ax_a.text(0.27, 0.34, r"$+A_+\delta_{t_0}$", color=BLUE, fontsize=5.7, va="center")
    ax_a.annotate(
        "",
        xy=(-0.14, 0.035),
        xytext=(-0.14, 0.34),
        arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=1.15),
    )
    ax_a.text(-0.27, 0.39, r"$-A_-\delta_{t_0}$", color=ORANGE, fontsize=5.7, ha="right")
    ax_a.set_xlim(-4.0, 4.0)
    ax_a.set_ylim(-0.02, 1.08)
    ax_a.set_xlabel(r"inner coordinate $s=(t-t_0)/\delta_\varepsilon$")
    ax_a.set_ylabel(r"$a_\varepsilon/A$")
    ax_a.set_title(
        "A   Odd and even finite-order soft profiles",
        loc="left",
        fontweight="bold",
    )
    ax_a.grid(color=LIGHT_GRAY, linewidth=0.45)
    ax_a.legend(
        frameon=True,
        facecolor=PAPER,
        edgecolor="none",
        framealpha=0.88,
        loc="lower left",
        handlelength=2.0,
    )

    # Panel B: signed derivative measure versus relaxed/Jordan face cost.
    ledger = {
        (row["case"], row["component"]): float(row["value"])
        for row in grouped[("B", "faceLedger")]
    }
    cases = ("odd m=1", "even m=2")
    y_positions = np.array([1.0, 0.0])
    offset = 0.16
    height = 0.27
    signed_values = [ledger[(case, "signedAtom")] for case in cases]
    jordan_values = [ledger[(case, "relaxedJordan")] for case in cases]
    hard_values = [ledger[(case, "hardBVJump")] for case in cases]
    signed_bars = ax_b.barh(
        y_positions + offset,
        signed_values,
        height=height,
        color=BLUE,
        edgecolor=INK,
        linewidth=0.45,
        label=r"signed atom $A_+-A_-$",
    )
    jordan_bars = ax_b.barh(
        y_positions - offset,
        jordan_values,
        height=height,
        color=PALE_ORANGE,
        edgecolor=ORANGE,
        linewidth=0.85,
        hatch="///",
        label=r"relaxed/Jordan $A_++A_-$",
    )
    for index, case in enumerate(cases):
        ax_b.plot(
            hard_values[index],
            y_positions[index],
            marker="D",
            markersize=4.2,
            markerfacecolor=PAPER,
            markeredgecolor=INK,
            markeredgewidth=0.85,
            zorder=5,
        )
        ax_b.text(
            hard_values[index] + 0.06,
            y_positions[index] + 0.015,
            f"hard BV {hard_values[index]:.0f}",
            fontsize=5.1,
            va="center",
            ha="left",
        )
    for bars, values in ((signed_bars, signed_values), (jordan_bars, jordan_values)):
        for bar, value in zip(bars, values, strict=True):
            ax_b.text(
                value + 0.045,
                bar.get_y() + bar.get_height() / 2,
                f"{value:.0f}",
                va="center",
                ha="left",
                fontsize=5.5,
                fontweight="bold",
            )
    ax_b.axvline(0, color=INK, linewidth=0.6)
    ax_b.set_xlim(-0.12, 2.42)
    ax_b.set_ylim(-0.55, 1.55)
    ax_b.set_yticks(y_positions, ("odd $m=1$", "even $m=2$"))
    ax_b.set_xlabel("normalized face mass (A=1)")
    ax_b.grid(axis="x", color=LIGHT_GRAY, linewidth=0.45)
    ax_b.set_title(
        "B   Signed atom versus relaxed face cost",
        loc="left",
        fontweight="bold",
    )
    ax_b.legend(frameon=False, loc="upper right", handlelength=1.7)
    ax_b.text(
        0.985,
        0.035,
        r"even: $-A\delta_{t_0}+A\delta_{t_0}\rightharpoonup0$, but Jordan mass $=2A$",
        transform=ax_b.transAxes,
        ha="right",
        fontsize=5.3,
        color=GRAY,
    )

    # Panel C: exact oscillatory separation on logarithmic axes.
    c_series = {}
    for series in ("softFaceTV", "denominatorMass", "CtSquareMass"):
        c_series[series] = sorted(
            (int(row["N"]), float(row["value"]))
            for row in grouped[("C", series)]
        )
    styles = (
        ("softFaceTV", BLUE, "o", "-", r"soft face TV $\sim2N$"),
        ("denominatorMass", ORANGE, "s", "--", r"$\int d_Ndt=\pi/N^2$"),
        ("CtSquareMass", GRAY, "D", ":", r"$\int\|C_{N,t}\|^2dt=\pi$"),
    )
    for series, color, marker, linestyle, label in styles:
        pairs = c_series[series]
        ax_c.plot(
            [pair[0] for pair in pairs],
            [pair[1] for pair in pairs],
            color=color,
            marker=marker,
            linestyle=linestyle,
            linewidth=1.25,
            markersize=3.8,
            markerfacecolor=color if series == "softFaceTV" else PAPER,
            markeredgecolor=color,
            markeredgewidth=0.8,
            label=label,
        )
    ax_c.set_xscale("log", base=2)
    ax_c.set_yscale("log")
    ax_c.set_xlim(0.82, 82)
    ax_c.set_ylim(4.0e-4, 2.2e2)
    ax_c.set_xticks([1, 2, 4, 8, 16, 32, 64], ["1", "2", "4", "8", "16", "32", "64"])
    ax_c.set_xlabel("oscillation count N")
    ax_c.set_ylabel("exact positive quantity (log scale)")
    ax_c.grid(which="both", color=LIGHT_GRAY, linewidth=0.42)
    ax_c.set_title(
        r"C   Oscillatory separation at $\varepsilon_N=N^{-4}$",
        loc="left",
        fontweight="bold",
    )
    ax_c.legend(frameon=False, loc="upper left", handlelength=2.4)
    ax_c.text(
        0.985,
        0.035,
        "abstract smooth Hilbert path; not a coupled NSE observable",
        transform=ax_c.transAxes,
        ha="right",
        fontsize=5.35,
        color=GRAY,
    )

    # Panel D: exact four-mode NSE initial jet and its one-sided trace.
    ax_d.set_axis_off()
    ax_d.set_title(
        "D   One genuine NSE initial entry face",
        loc="left",
        fontweight="bold",
        pad=4,
    )
    mode_ax = ax_d.inset_axes([0.015, 0.17, 0.45, 0.70])
    info_ax = ax_d.inset_axes([0.48, 0.05, 0.51, 0.84])
    info_ax.set_axis_off()
    mode_rows = grouped[("D", "targetMode")]
    positive = [row for row in mode_rows if row["component"].endswith("I/4") and not row["component"].endswith("-I/4")]
    negative = [row for row in mode_rows if row not in positive]
    mode_ax.scatter(
        [float(row["x"]) for row in positive],
        [float(row["y"]) for row in positive],
        s=28,
        marker="o",
        facecolor=BLUE,
        edgecolor=INK,
        linewidth=0.55,
        label=r"$\widehat F_3=+i/4$",
        zorder=4,
    )
    mode_ax.scatter(
        [float(row["x"]) for row in negative],
        [float(row["y"]) for row in negative],
        s=30,
        marker="s",
        facecolor=PAPER,
        edgecolor=ORANGE,
        linewidth=1.0,
        label=r"$\widehat F_3=-i/4$",
        zorder=4,
    )
    for row in mode_rows:
        x_value, y_value = float(row["x"]), float(row["y"])
        mode_ax.text(
            x_value + 0.08,
            y_value + 0.08,
            f"({int(x_value):+d},{int(y_value):+d},0)",
            fontsize=4.8,
        )
    mode_ax.axhline(0, color=GRAY, linewidth=0.5)
    mode_ax.axvline(0, color=GRAY, linewidth=0.5)
    mode_ax.set_xlim(-1.55, 1.55)
    mode_ax.set_ylim(-1.55, 1.55)
    mode_ax.set_aspect("equal")
    mode_ax.set_xticks((-1, 0, 1))
    mode_ax.set_yticks((-1, 0, 1))
    mode_ax.set_xlabel(r"$k_1$")
    mode_ax.set_ylabel(r"$k_2$")
    mode_ax.set_title(r"target modes at $k_3=0$", fontsize=6.1)
    mode_ax.grid(color=LIGHT_GRAY, linewidth=0.4)
    mode_ax.legend(
        frameon=False,
        loc="center",
        bbox_to_anchor=(0.50, 0.49),
        ncol=1,
        handletextpad=0.35,
        fontsize=4.55,
    )

    metrics = {
        row["component"]: float(row["value"])
        for row in grouped[("D", "nseMetric")]
    }
    info_ax.text(
        0.02,
        0.96,
        "u0 = (0, cos x1, 0)\n     + (0, 0, cos x2)",
        fontsize=4.45,
        fontweight="bold",
        va="top",
        linespacing=1.25,
    )
    info_ax.text(
        0.02,
        0.56,
        "\n".join(
            (
                rf"$Y(0)={metrics['Y0']:.0f}$,   $d(0)=0$",
                rf"$B_t(0)={metrics['Bt']:.1f}$",
                rf"$\|C_t(0)\|_2^2={metrics['Ct2']:.0f}$",
            )
        ),
        fontsize=5.2,
        linespacing=1.35,
    )
    info_ax.text(
        0.50,
        0.29,
        rf"$a(0+)={metrics['rightTrace']:.2f}=1/4$",
        fontsize=7.0,
        fontweight="bold",
        color=BLUE,
        ha="center",
        va="center",
        bbox=dict(
            boxstyle="round,pad=0.30",
            facecolor=PALE_BLUE,
            edgecolor=BLUE,
            linewidth=0.85,
        ),
    )
    info_ax.text(
        0.02,
        0.015,
        "one-sided initial jet; no time step\nno internal or unbounded NSE face count\nno continuation or regularity claim",
        fontsize=3.95,
        color=GRAY,
        linespacing=1.22,
    )

    fig.text(
        0.065,
        0.028,
        "Scope: fixed cell and Y>0. Panel C is abstract. Panel D is one NSE initial jet only; no internal face-count, continuation, singularity, or regularity theorem.",
        fontsize=5.75,
        color=GRAY,
    )

    for extension in ("pdf", "svg", "png"):
        fig.savefig(
            args.output_stem.with_suffix(f".{extension}"),
            dpi=600 if extension == "png" else None,
        )
    svg_path = args.output_stem.with_suffix(".svg")
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_text = re.sub(r'width="[^"]+"', 'width="178mm"', svg_text, count=1)
    svg_text = re.sub(r'height="[^"]+"', 'height="118mm"', svg_text, count=1)
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n",
        encoding="utf-8",
    )
    plt.close(fig)


if __name__ == "__main__":
    main()
