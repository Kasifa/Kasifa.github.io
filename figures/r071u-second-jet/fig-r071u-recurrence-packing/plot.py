#!/usr/bin/env python3
"""Render the 178 mm four-panel R0.71U recurrence figure."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle
import numpy as np


PAPER = "#FBF9F4"
INK = "#252422"
BLUE = "#355C7D"
OCHRE = "#B8792B"
GRAY = "#77736C"
LIGHT = "#D8D3C8"


def load(path: Path) -> list[dict[str, str]]:
    return list(csv.DictReader(path.open(encoding="utf-8")))


def select(
    rows: list[dict[str, str]], panel: str, series: str, case: str | None = None
) -> list[dict[str, str]]:
    return [
        item for item in rows
        if item["panel"] == panel
        and item["series"] == series
        and (case is None or item["case"] == case)
    ]


def configure() -> None:
    mpl.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 7.2,
        "axes.titlesize": 8.0,
        "axes.labelsize": 7.1,
        "xtick.labelsize": 6.35,
        "ytick.labelsize": 6.35,
        "legend.fontsize": 5.9,
        "axes.edgecolor": INK,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": INK,
        "ytick.color": INK,
        "axes.facecolor": PAPER,
        "figure.facecolor": PAPER,
        "savefig.facecolor": PAPER,
        "axes.linewidth": 0.72,
        "lines.linewidth": 1.25,
        "pdf.fonttype": 42,
        "svg.fonttype": "none",
        "svg.hashsalt": "r071u-recurrence-packing",
    })


def blossom(fig: plt.Figure) -> None:
    center_x, center_y = 0.979, 0.964
    radius = 0.0062
    for index, color in enumerate((BLUE, OCHRE, BLUE, OCHRE, BLUE)):
        angle = 2.0 * np.pi * index / 5.0 + np.pi / 2.0
        petal = Circle(
            (center_x + 0.009 * np.cos(angle), center_y + 0.009 * np.sin(angle)),
            radius,
            transform=fig.transFigure,
            facecolor=color,
            edgecolor=PAPER,
            linewidth=0.35,
            alpha=0.82,
            zorder=20,
        )
        fig.add_artist(petal)
    fig.add_artist(Circle(
        (center_x, center_y), 0.0048, transform=fig.transFigure,
        facecolor=INK, edgecolor=PAPER, linewidth=0.35, zorder=21,
    ))


def panel_title(axis: plt.Axes, letter: str, title: str) -> None:
    axis.set_title(f"{letter}   {title}", loc="left", fontweight="bold", pad=5.0)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--output-stem", type=Path, required=True)
    args = parser.parse_args()
    rows = load(args.data)
    configure()
    fig, axes = plt.subplots(
        2,
        2,
        # Matplotlib 3.11 quantizes figsize to 0.01 in; 7.01 in is 178.05 mm.
        figsize=(7.01, 5.28),
        constrained_layout=False,
    )
    fig.subplots_adjust(left=0.082, right=0.985, bottom=0.135, top=0.875, wspace=0.29, hspace=0.37)
    axa, axb, axc, axd = axes.ravel()
    fig.suptitle(
        "Prescribed returns in a modular exact-NSE lattice",
        x=0.082, y=0.965, ha="left", fontsize=10.1, fontweight="bold",
    )
    fig.text(
        0.082,
        0.925,
        r"$u=(f,0,v)$  ·  $\nu=0.02$  ·  $K=L=1$  ·  $d=8$  ·  $p_1=0.002$  ·  primary $m_{\rm cut}=24$, independent 36",
        ha="left",
        fontsize=6.75,
        color=GRAY,
    )
    blossom(fig)

    real_rows = sorted(select(rows, "A", "real target"), key=lambda item: float(item["x"]))
    imag_rows = sorted(select(rows, "A", "imaginary target"), key=lambda item: float(item["x"]))
    time = np.asarray([float(item["x"]) for item in real_rows])
    real = np.asarray([float(item["y"]) for item in real_rows])
    imag = np.asarray([float(item["y"]) for item in imag_rows])
    axa.plot(time, 1e7 * real, color=BLUE, label=r"$10^7\,\mathrm{Re}\,a_0$")
    axa.plot(time, 1e9 * imag, color=OCHRE, linestyle="--", label=r"$10^9\,\mathrm{Im}\,a_0$")
    axa.axhline(0.0, color=INK, lw=0.62)
    root_rows = sorted(select(rows, "A", "prescribed root"), key=lambda item: float(item["time"]))
    markers = ("o", "s", "D")
    slope_values: list[float] = []
    for index, (item, marker) in enumerate(zip(root_rows, markers, strict=True), start=1):
        root_time = float(item["time"])
        slope_values.append(float(item["value"]))
        axa.axvline(root_time, color=GRAY, lw=0.65, linestyle=(0, (1.5, 2.1)))
        axa.scatter(
            [root_time], [0.0], marker=marker, s=23,
            facecolors=PAPER, edgecolors=INK, linewidths=0.9, zorder=5,
        )
    axa.set_xlim(0.0, 0.08)
    axa.set_ylim(-3.25, 6.45)
    axa.set_xlabel("time")
    axa.set_ylabel("scaled target coefficient")
    axa.grid(True, color=LIGHT, lw=0.4)
    axa.legend(loc="upper left", frameon=False, ncol=2, columnspacing=1.0, handlelength=2.2)
    axa.text(
        0.98,
        0.06,
        r"$|a_0'(t_m)|=(6.60,\,9.72,\,38.9)\times10^{-6}$",
        transform=axa.transAxes,
        ha="right",
        fontsize=5.9,
        color=GRAY,
    )
    panel_title(axa, "A", "Three prescribed target returns")

    styles = (
        ("t1", BLUE, "-", "o", r"$t_1=0.01$"),
        ("t2", OCHRE, "--", "s", r"$t_2=0.03$"),
        ("t3", INK, ":", "D", r"$t_3=0.07$"),
    )
    for case, color, linestyle, marker, label in styles:
        segment = sorted(select(rows, "B", "complex passage", case), key=lambda item: float(item["time"]))
        x = 1e8 * np.asarray([float(item["x"]) for item in segment])
        y = 1e9 * np.asarray([float(item["y"]) for item in segment])
        axb.plot(x, y, color=color, linestyle=linestyle, label=label)
        middle = int(np.argmin(np.abs(np.asarray([float(item["value"]) for item in segment]))))
        left = min(len(x) - 1, middle + 8)
        right = min(len(x) - 1, middle + 28)
        axb.annotate(
            "",
            xy=(x[right], y[right]),
            xytext=(x[left], y[left]),
            arrowprops={"arrowstyle": "-|>", "color": color, "lw": 0.8, "mutation_scale": 6.0},
            zorder=4,
        )
        root = select(rows, "B", "complex root", case)[0]
        marker_size = {"t1": 52, "t2": 32, "t3": 16}[case]
        axb.scatter(
            [1e8 * float(root["x"])], [1e9 * float(root["y"])],
            marker=marker, s=marker_size, facecolors=PAPER, edgecolors=color,
            linewidths=1.0, zorder=5,
        )
    axb.axhline(0.0, color=GRAY, lw=0.55)
    axb.axvline(0.0, color=GRAY, lw=0.55)
    axb.set_xlabel(r"$10^8\,\mathrm{Re}\,a_0$")
    axb.set_ylabel(r"$10^9\,\mathrm{Im}\,a_0$")
    axb.grid(True, color=LIGHT, lw=0.4)
    axb.legend(loc="upper left", frameon=False)
    axb.text(
        0.98, 0.06, "arrows show increasing time\nlocal windows: |t − tₘ| ≤ 0.004",
        transform=axb.transAxes, ha="right", fontsize=5.75, color=GRAY,
    )
    panel_title(axb, "B", "Complex-plane origin passages")

    cstyles = (
        ("t1", BLUE, "-", "o", r"$t_1$"),
        ("t2", OCHRE, "--", "s", r"$t_2$"),
        ("t3", INK, ":", "D", r"$t_3$"),
    )
    for case, color, linestyle, marker, label in cstyles:
        atom_rows = sorted(select(rows, "C", "jet atom", case), key=lambda item: float(item["x"]))
        x = np.asarray([float(item["x"]) for item in atom_rows])
        y = np.asarray([float(item["y"]) for item in atom_rows])
        axc.loglog(
            x, y, color=color, linestyle=linestyle, marker=marker,
            ms=3.3, markerfacecolor=color, markeredgewidth=0.5, label=label,
        )
        trace_rows = sorted(select(rows, "C", "quarter first-jet trace", case), key=lambda item: float(item["x"]))
        axc.loglog(
            [float(item["x"]) for item in trace_rows],
            [float(item["y"]) for item in trace_rows],
            linestyle="none", marker=marker, ms=5.0,
            markerfacecolor="none", markeredgecolor=color, markeredgewidth=0.65,
        )
    guide_x = np.asarray([2.5e-4, 2.0e-3])
    guide_y = 1.55e-16 * (guide_x / guide_x[0]) ** 2
    axc.loglog(guide_x, guide_y, color=GRAY, lw=0.8, linestyle=(0, (4, 2)), label=r"guide $p_1^2$")
    axc.set_xlabel(r"curve coordinate $p_1$")
    axc.set_ylabel(r"jet atom $J_*(t_m)$")
    axc.grid(True, which="both", color=LIGHT, lw=0.38)
    handles, labels = axc.get_legend_handles_labels()
    handles.append(Line2D([], [], color=GRAY, marker="o", linestyle="none", markerfacecolor="none", ms=5.0))
    labels.append(r"open: $P(t_m)/4$")
    axc.legend(handles, labels, loc="upper left", frameon=False, ncol=2, columnspacing=0.8)
    axc.text(
        0.98,
        0.055,
        "sampled exponents: 2.008, 2.001, 2.000\n" + r"$P=\kappa_*^{-6}\|C_{*,t}\|_2^2/Y$,  $J=P/4$",
        transform=axc.transAxes,
        ha="right",
        fontsize=5.65,
        color=GRAY,
    )
    panel_title(axc, "C", r"Atoms collapse as $O(p_1^2)$")

    residual_rows = sorted(select(rows, "D", "prescribed-time residual"), key=lambda item: float(item["x"]))
    slope_rows = sorted(select(rows, "D", "slope relative error"), key=lambda item: float(item["x"]))
    cutoffs = np.asarray([float(item["x"]) for item in residual_rows])
    residual = np.asarray([float(item["y"]) for item in residual_rows])
    slope_error = np.asarray([float(item["y"]) for item in slope_rows])
    axd.semilogy(cutoffs, np.maximum(residual, 1e-22), color=BLUE, marker="o", ms=3.3, label=r"max $|a_0(t_m)|$")
    axd.semilogy(
        cutoffs, np.maximum(slope_error, 1e-22), color=OCHRE,
        linestyle="--", marker="s", ms=3.4, markerfacecolor="none",
        label="max relative slope error vs 36",
    )
    independent_row = select(rows, "D", "independent root residual")[0]
    axd.scatter(
        [float(independent_row["x"])], [max(float(independent_row["y"]), 1e-22)],
        marker="D", s=29, facecolors=PAPER, edgecolors=INK, linewidths=0.95,
        zorder=5, label="independent reshoot at 36",
    )
    axd.axvline(24, color=BLUE, lw=0.58, linestyle=":")
    axd.axvline(36, color=INK, lw=0.58, linestyle=":")
    axd.set_xticks(cutoffs.astype(int))
    axd.set_ylim(5e-23, 5e-8)
    axd.set_xlabel(r"lattice cutoff $m_{\rm cut}$")
    axd.set_ylabel("residual or relative difference")
    axd.grid(True, which="both", color=LIGHT, lw=0.38)
    axd.legend(loc="upper right", frameon=False)
    axd.text(
        0.03,
        0.07,
        r"$m=24\to36$:  $\Delta a_0=9.45\times10^{-21}$" + "\n"
        + r"relative $\Delta a_0'=3.29\times10^{-14}$" + "\n"
        + r"analytic gap: $R_*=3<d-K=7$, next radius $\sqrt{50}$" + "\n"
        + r"zero reference at $m=36$ is shown at the $10^{-22}$ floor",
        transform=axd.transAxes,
        ha="left",
        fontsize=5.35,
        color=GRAY,
    )
    panel_title(axd, "D", "Cutoff and residual convergence")

    fig.text(
        0.5,
        0.025,
        "Finite Fourier–Galerkin corroboration with PDE time stepping; not DNS and not a continuum truncation proof.",
        ha="center",
        fontsize=6.15,
        color=GRAY,
    )
    metadata = {
        "Title": "R0.71U modular exact-NSE recurrence packing",
        "Subject": "Finite Fourier-Galerkin corroboration with analytic claim boundary",
        "Author": "Kasifa",
        "Keywords": "Navier-Stokes, recurrence, Fourier lattice, jet atom",
    }
    args.output_stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output_stem.with_suffix(".pdf"), metadata=metadata)
    fig.savefig(args.output_stem.with_suffix(".svg"), metadata={"Title": metadata["Title"], "Description": metadata["Subject"]})
    fig.savefig(args.output_stem.with_suffix(".png"), dpi=600, metadata={"Title": metadata["Title"]})
    plt.close(fig)


if __name__ == "__main__":
    main()
