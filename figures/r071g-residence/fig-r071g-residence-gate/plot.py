#!/usr/bin/env python3
"""Render the R0.71G journal figure from the archived CSV."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


MM = 1.0 / 25.4
COLORS = {
    1.0: "#7b3294",
    0.5: "#c51b7d",
    0.2: "#e66101",
    0.1: "#0571b0",
    0.05: "#1b7837",
}
LINESTYLES = {1.0: (0, (1, 1)), 0.5: "-", 0.2: "--", 0.1: "-.", 0.05: (0, (5, 1, 1, 1))}
MARKERS = {0.5: "o", 0.1: "s", 0.01: "^"}


def normalize_svg_line_endings(path: Path):
    """Keep Matplotlib's SVG content while removing trailing line whitespace."""
    text = path.read_text(encoding="utf-8")
    path.write_text(
        "\n".join(line.rstrip() for line in text.splitlines()) + "\n",
        encoding="utf-8",
    )


def read_rows(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        for key in ("mu", "theta", "value", "aux"):
            row[key] = float(row[key])
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("data.csv"))
    parser.add_argument("--output-stem", type=Path, default=Path("figure"))
    args = parser.parse_args()
    rows = read_rows(args.data)

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 7.2,
            "axes.titlesize": 8.2,
            "axes.labelsize": 7.5,
            "legend.fontsize": 6.4,
            "xtick.labelsize": 6.7,
            "ytick.labelsize": 6.7,
            "axes.linewidth": 0.7,
            "lines.linewidth": 1.25,
            "savefig.facecolor": "white",
        }
    )
    fig, axes = plt.subplots(2, 2, figsize=(178 * MM, 108 * MM))
    ax_a, ax_b, ax_c, ax_d = axes.flat

    sign_rows = [row for row in rows if row["recordType"] == "signExit"]
    sign_exit = {row["mu"]: row["theta"] for row in sign_rows}

    for mu in (0.5, 0.2, 0.1, 0.05):
        profile = [
            row
            for row in rows
            if row["recordType"] == "profile"
            and row["level"] == "H"
            and np.isclose(row["mu"], mu)
            and row["theta"] <= min(10.25, sign_exit[mu] + 0.35)
        ]
        ax_a.plot(
            [row["theta"] for row in profile],
            [row["aux"] for row in profile],
            color=COLORS[mu],
            linestyle=LINESTYLES[mu],
            label=fr"$\mu={mu:g}$",
        )
    ax_a.axhline(0.0, color="#222222", linewidth=0.7)
    ax_a.axhline(1.0, color="#777777", linewidth=0.8, linestyle=":", label=r"$\mu=0$")
    ax_a.set_xlim(0.0, 10.25)
    ax_a.set_ylim(-0.65, 1.1)
    ax_a.set_xlabel(r"dimensionless time $\theta=\nu K^2t$")
    ax_a.set_ylabel(r"rescaled work $e^{4\theta}H_\mu$")
    ax_a.set_title("Sign-only tails outlive one viscous time", loc="left", fontweight="bold")
    ax_a.legend(ncol=2, frameon=False, loc="lower left")
    ax_a.grid(color="#dddddd", linewidth=0.45, alpha=0.7)

    inverse_mu = np.array([row["aux"] for row in sign_rows])
    exits = np.array([row["theta"] for row in sign_rows])
    order = np.argsort(inverse_mu)
    ax_b.plot(
        inverse_mu[order],
        exits[order],
        color="#0571b0",
        marker="o",
        markersize=3.4,
        label="finite chain check",
    )
    guide_x = np.linspace(1.0, 20.0, 100)
    ax_b.plot(
        guide_x,
        0.5 * guide_x,
        color="#666666",
        linestyle="--",
        linewidth=1.0,
        label=r"$0.5\mu^{-1}$ guide",
    )
    ax_b.axhline(1.0, color="#999999", linestyle=":", linewidth=0.8)
    ax_b.set_xlim(0.5, 20.5)
    ax_b.set_ylim(0.0, 10.4)
    ax_b.set_xlabel(r"inverse nonlinearity $\mu^{-1}$")
    ax_b.set_ylabel(r"first sign exit $\theta_{\rm sign}$")
    ax_b.set_title("Checked sign exits grow as coupling weakens", loc="left", fontweight="bold")
    ax_b.legend(frameon=False, loc="upper left")
    ax_b.grid(color="#dddddd", linewidth=0.45, alpha=0.7)

    q_rows = [row for row in rows if row["recordType"] == "qExit"]
    level_colors = {0.5: "#1b7837", 0.1: "#0571b0", 0.01: "#c51b7d"}
    for level in (0.5, 0.1, 0.01):
        selected = [row for row in q_rows if np.isclose(float(row["level"]), level)]
        selected.sort(key=lambda row: row["mu"])
        ax_c.plot(
            [row["mu"] for row in selected],
            [row["theta"] for row in selected],
            color=level_colors[level],
            marker=MARKERS[level],
            markersize=3.2,
            label=fr"$q/q_0={level:g}$",
        )
        exact_limit = -np.log(level) / 6.0
        ax_c.axhline(
            exact_limit,
            color=level_colors[level],
            linestyle=":",
            linewidth=0.9,
            alpha=0.8,
        )
    ax_c.set_xscale("log")
    ax_c.invert_xaxis()
    ax_c.set_xlim(1.15, 0.043)
    ax_c.set_ylim(0.0, 0.82)
    ax_c.set_xlabel(r"coupling $\mu=a/\nu$ (weak limit to the right)")
    ax_c.set_ylabel(r"first relative-$q$ exit $\theta_q$")
    ax_c.set_title("Relative levels stay at the viscous scale", loc="left", fontweight="bold")
    ax_c.legend(frameon=False, loc="upper left")
    ax_c.grid(color="#dddddd", linewidth=0.45, alpha=0.7)

    functional = [row for row in rows if row["recordType"] == "functional"]
    n_values = [int(round(row["theta"])) for row in functional]
    unweighted = [row["value"] for row in functional]
    weighted = [row["aux"] for row in functional]
    line_unweighted = ax_d.plot(
        n_values,
        unweighted,
        color="#b2182b",
        marker="o",
        markersize=3.0,
        label=r"unweighted $\sum_{m\leq n}\int A_m=n$",
    )[0]
    ax_d_right = ax_d.twinx()
    line_weighted = ax_d_right.plot(
        n_values,
        weighted,
        color="#2166ac",
        linestyle="--",
        marker="s",
        markersize=2.8,
        label=r"weighted $\sum_{m\leq n}K_m^{-2}\int A_m$",
    )[0]
    ax_d_right.axhline(1.0 / 3.0, color="#2166ac", linestyle=":", linewidth=0.8)
    ax_d.set_xlim(0.5, 12.5)
    ax_d.set_ylim(0.0, 12.8)
    ax_d_right.set_ylim(0.0, 0.36)
    ax_d.set_xlabel("number of active shells")
    ax_d.set_ylabel("unweighted sum", color="#b2182b")
    ax_d_right.set_ylabel("weighted sum", color="#2166ac")
    ax_d.tick_params(axis="y", colors="#b2182b")
    ax_d_right.tick_params(axis="y", colors="#2166ac")
    ax_d.set_title("Residence alone misses summability", loc="left", fontweight="bold")
    ax_d.legend(
        [line_unweighted, line_weighted],
        [line_unweighted.get_label(), line_weighted.get_label()],
        frameon=False,
        loc="center right",
    )
    ax_d.grid(color="#dddddd", linewidth=0.45, alpha=0.7)

    for label, axis in zip("ABCD", axes.flat):
        axis.text(
            -0.12,
            1.08,
            label,
            transform=axis.transAxes,
            fontsize=9.2,
            fontweight="bold",
            va="top",
        )

    fig.subplots_adjust(left=0.09, right=0.91, bottom=0.10, top=0.94, wspace=0.40, hspace=0.43)
    output = args.output_stem
    fig.savefig(output.with_suffix(".pdf"))
    fig.savefig(output.with_suffix(".svg"))
    normalize_svg_line_endings(output.with_suffix(".svg"))
    fig.savefig(output.with_suffix(".png"), dpi=600)
    plt.close(fig)


if __name__ == "__main__":
    main()
