#!/usr/bin/env python3
"""Render the R0.71I double-column journal figure from archived CSV data."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


MM = 1.0 / 25.4
NAVY = "#234a6b"
RUST = "#a34f2b"
CHARCOAL = "#303030"
GREY = "#777777"
LIGHT_GREY = "#dddddd"


def read_rows(path: Path) -> list[dict[str, str | float]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows: list[dict[str, str | float]] = list(csv.DictReader(handle))
    for row in rows:
        row["x"] = float(row["x"])
        row["value"] = float(row["value"])
    return rows


def series(
    rows: list[dict[str, str | float]], panel: str, name: str
) -> tuple[list[float], list[float]]:
    selected = [
        row
        for row in rows
        if row["panel"] == panel and row["series"] == name
    ]
    selected.sort(key=lambda row: float(row["x"]))
    return (
        [float(row["x"]) for row in selected],
        [float(row["value"]) for row in selected],
    )


def normalize_svg(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    path.write_text(
        "\n".join(line.rstrip() for line in text.splitlines()) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("data.csv"))
    parser.add_argument("--output-stem", type=Path, default=Path("figure"))
    args = parser.parse_args()
    rows = read_rows(args.data)

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 7.0,
            "axes.titlesize": 7.8,
            "axes.labelsize": 7.2,
            "legend.fontsize": 6.0,
            "xtick.labelsize": 6.3,
            "ytick.labelsize": 6.3,
            "axes.linewidth": 0.7,
            "lines.linewidth": 1.3,
            "savefig.facecolor": "white",
            "svg.hashsalt": "r071i-joint-volume-gap",
        }
    )

    fig, axes = plt.subplots(2, 2, figsize=(178 * MM, 108 * MM))
    ax_a, ax_b, ax_c, ax_d = axes.flat

    tau, pulse = series(rows, "A", "commonHeatPulse")
    peak_tau, peak_q = series(rows, "A", "pulsePeak")
    ax_a.plot(
        tau,
        pulse,
        color=NAVY,
        label=r"$q(\tau)$",
    )
    ax_a.scatter(
        peak_tau,
        peak_q,
        s=20,
        marker="o",
        facecolors="white",
        edgecolors=RUST,
        linewidths=1.0,
        zorder=4,
        label=r"exact maximum $q_*$",
    )
    ax_a.scatter([0.0], [0.0], s=17, marker="s", facecolors="white", edgecolors=CHARCOAL, zorder=4)
    ax_a.axhline(0.0, color=GREY, linewidth=0.75)
    ax_a.set_xlim(-0.03, 3.0)
    ax_a.set_ylim(-0.0025, 0.062)
    ax_a.set_xlabel(r"viscous time $\tau=\nu K^2t$")
    ax_a.set_ylabel(r"coefficient $q$")
    ax_a.set_title("Common heat: zero-face coefficient pulse", loc="left", fontweight="bold")
    ax_a.legend(frameon=False, loc="upper right")
    ax_a.text(
        0.98,
        0.10,
        r"$q(0)=q(\infty)=0$",
        transform=ax_a.transAxes,
        ha="right",
        va="bottom",
        fontsize=6.2,
        color=CHARCOAL,
    )

    frequency, ratio = series(rows, "B", "traceVolumeRatio")
    ax_b.plot(
        frequency,
        ratio,
        color=RUST,
        marker="s",
        markerfacecolor="white",
        markeredgewidth=0.9,
        markersize=3.2,
        label=r"exact ratio",
    )
    ax_b.set_xscale("log", base=2)
    ax_b.set_yscale("log", base=2)
    ax_b.set_xlim(0.82, 315)
    ax_b.set_ylim(0.20, 3.0e4)
    ax_b.set_xticks([1, 4, 16, 64, 256], labels=["1", "4", "16", "64", "256"])
    ax_b.set_xlabel(r"shell frequency $K$")
    ax_b.set_ylabel(r"$K^{-2}{\rm TV}(q)\,/\,\int K^{-2}\|F\|^2dt$")
    ax_b.set_title(r"Common heat: exact trace-to-volume ratio", loc="left", fontweight="bold")
    ax_b.legend(frameon=False, loc="upper left")
    ax_b.text(
        0.97,
        0.10,
        r"$=\frac{71-17\sqrt{17}}{3}K^2$" + "\n" + r"$(\nu=1;\ {\rm no\ fit})$",
        transform=ax_b.transAxes,
        ha="right",
        va="bottom",
        fontsize=6.3,
        color=CHARCOAL,
    )

    theta, a_zero = series(rows, "C", "A0")
    _, g_zero = series(rows, "C", "G0")
    test_theta, test_a = series(rows, "C", "positiveTestPoint")
    line_a = ax_c.plot(
        theta,
        a_zero,
        color=NAVY,
        label=r"$A_0=Q_0/Y_0$",
    )[0]
    ax_c.scatter(
        test_theta,
        test_a,
        s=18,
        marker="o",
        facecolors="white",
        edgecolors=NAVY,
        linewidths=0.9,
        zorder=4,
    )
    ax_c.set_xlim(0.0, 0.6)
    ax_c.set_ylim(-0.006, 0.205)
    ax_c.set_xlabel(r"viscous time $\theta=\nu K^2t$")
    ax_c.set_ylabel(r"normalized coefficient $A_0$", color=NAVY)
    ax_c.tick_params(axis="y", colors=NAVY)
    ax_c_right = ax_c.twinx()
    line_g = ax_c_right.plot(
        theta,
        g_zero,
        color=RUST,
        linestyle="--",
        label=r"$G_0=\lim\|F_K\|^2/Y$",
    )[0]
    ax_c_right.set_ylim(-0.04, 1.18)
    ax_c_right.set_ylabel(r"heat density $G_0$", color=RUST)
    ax_c_right.tick_params(axis="y", colors=RUST)
    ax_c.set_title("2D3C limit: zero-entry coefficient and heat density", loc="left", fontweight="bold")
    ax_c.legend(
        [line_a, line_g],
        [line_a.get_label(), line_g.get_label()],
        frameon=False,
        loc="upper right",
    )
    ax_c.text(
        0.98,
        0.10,
        r"$A_0(0)=0,\quad A_0(\log2/10)>0$",
        transform=ax_c.transAxes,
        ha="right",
        va="bottom",
        fontsize=6.1,
        color=CHARCOAL,
    )

    delta, aggregate = series(rows, "D", "aggregateCoefficient")
    endpoint_delta, endpoint_value = series(rows, "D", "refreshEndpoint")
    ax_d.plot(
        delta,
        aggregate,
        color=NAVY,
        label=r"$\sum_\pm a_{\delta,\pm}$",
    )
    ax_d.scatter(
        endpoint_delta,
        endpoint_value,
        s=21,
        marker="s",
        facecolors="white",
        edgecolors=RUST,
        linewidths=1.0,
        zorder=4,
        label=r"refresh endpoints",
    )
    ax_d.annotate(
        "",
        xy=(1.045, 0.25),
        xytext=(1.045, 1.0 / 7.0),
        arrowprops={"arrowstyle": "<->", "color": RUST, "linewidth": 1.0},
        annotation_clip=False,
    )
    ax_d.text(
        1.07,
        0.196,
        r"$\Delta_{\rm ref}=3/28$",
        color=RUST,
        rotation=90,
        ha="center",
        va="center",
        fontsize=6.1,
    )
    ax_d.set_xlim(-0.03, 1.14)
    ax_d.set_ylim(0.125, 0.265)
    ax_d.set_xlabel(r"cutoff modulation $\delta$")
    ax_d.set_ylabel(r"aggregate coefficient ($U=1$)")
    ax_d.set_title("Two-cell partition: exact refresh gap", loc="left", fontweight="bold")
    ax_d.legend(frameon=False, loc="upper right")

    for axis in (ax_a, ax_b, ax_c, ax_d):
        axis.grid(color=LIGHT_GREY, linewidth=0.42, alpha=0.78)
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)
    ax_c_right.spines["top"].set_visible(False)
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

    fig.text(
        0.915,
        0.012,
        "closed-form source data; no DNS or fitted exponent",
        ha="right",
        va="bottom",
        fontsize=5.7,
        color=GREY,
    )
    fig.subplots_adjust(
        left=0.085,
        right=0.915,
        bottom=0.105,
        top=0.94,
        wspace=0.43,
        hspace=0.44,
    )

    output = args.output_stem
    title = "R0.71I joint heat evolution and exact trace-to-volume gap"
    fig.savefig(
        output.with_suffix(".pdf"),
        metadata={
            "Title": title,
            "Author": "Chuikuan Zeng",
            "Subject": "Closed-form common-heat and global-smooth 2D3C volume-gap diagnostics",
            "Creator": "Matplotlib",
            "CreationDate": None,
            "ModDate": None,
        },
    )
    fig.savefig(
        output.with_suffix(".svg"),
        metadata={
            "Title": title,
            "Description": "Four-panel closed-form diagnostic figure; no DNS, PDE time stepping, or fitted exponent.",
            "Creator": "Matplotlib",
            "Date": None,
        },
    )
    normalize_svg(output.with_suffix(".svg"))
    fig.savefig(
        output.with_suffix(".png"),
        dpi=600,
        metadata={
            "Title": title,
            "Description": "Four-panel closed-form diagnostic figure; no DNS, PDE time stepping, or fitted exponent.",
            "Software": "Matplotlib",
        },
    )
    plt.close(fig)


if __name__ == "__main__":
    main()
