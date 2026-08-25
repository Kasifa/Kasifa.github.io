#!/usr/bin/env python3
"""Render the R0.71H double-column journal figure from archived CSV data."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


MM = 1.0 / 25.4
NAVY = "#234a6b"
RUST = "#a34f2b"
TEAL = "#3d766e"
CHARCOAL = "#303030"
GREY = "#777777"


def read_rows(path: Path) -> list[dict[str, str | float]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows: list[dict[str, str | float]] = list(csv.DictReader(handle))
    for row in rows:
        row["x"] = float(row["x"])
        row["value"] = float(row["value"])
    return rows


def series(
    rows: list[dict[str, str | float]], panel: str, name: str
) -> tuple[np.ndarray, np.ndarray]:
    selected = [row for row in rows if row["panel"] == panel and row["series"] == name]
    selected.sort(key=lambda row: float(row["x"]))
    return (
        np.array([float(row["x"]) for row in selected]),
        np.array([float(row["value"]) for row in selected]),
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
            "font.size": 7.1,
            "axes.titlesize": 8.0,
            "axes.labelsize": 7.3,
            "legend.fontsize": 6.1,
            "xtick.labelsize": 6.5,
            "ytick.labelsize": 6.5,
            "axes.linewidth": 0.7,
            "lines.linewidth": 1.25,
            "savefig.facecolor": "white",
            "svg.hashsalt": "r071h-angular-curvature",
        }
    )

    fig, axes = plt.subplots(2, 2, figsize=(178 * MM, 108 * MM))
    ax_a, ax_b, ax_c, ax_d = axes.flat

    time, payment = series(rows, "A", "rayleighPayment")
    _, angular = series(rows, "A", "angularIntegral")
    _, curvature = series(rows, "A", "curvatureIntegral")
    _, balance = series(rows, "A", "identitySum")
    ax_a.plot(time, payment, color=CHARCOAL, label=r"Rayleigh payment $r(0)-r(t)$")
    ax_a.plot(
        time,
        angular,
        color=RUST,
        linestyle="--",
        marker="o",
        markevery=10,
        markersize=2.5,
        label=r"rotation $\int\|E_t\|^2$",
    )
    ax_a.plot(
        time,
        curvature,
        color=TEAL,
        linestyle=":",
        marker="x",
        markevery=(5, 10),
        markersize=3.1,
        label=r"curvature $\int\|P_{E^\perp}A_0E\|^2$",
    )
    ax_a.plot(
        time[::10],
        balance[::10],
        color=NAVY,
        linestyle="none",
        marker="s",
        markerfacecolor="none",
        markersize=3.2,
        label="sum of both terms",
    )
    ax_a.set_xlim(0.0, 1.5)
    ax_a.set_ylim(-0.03, 1.55)
    ax_a.set_xlabel(r"heat time $t$ ($\nu=1$)")
    ax_a.set_ylabel("cumulative identity terms")
    ax_a.set_title("Pure heat: Rayleigh drop pays rotation", loc="left", fontweight="bold")
    ax_a.legend(frameon=False, loc="lower right")

    frequency, omega = series(rows, "B", "angularSpeed")
    _, source_density = series(rows, "B", "sourceDensity")
    line_omega = ax_b.plot(
        frequency,
        omega,
        color=NAVY,
        marker="o",
        markersize=3.0,
        label=r"$\Omega_K(0)=K/2$",
    )[0]
    ax_b.set_xscale("log", base=2)
    ax_b.set_yscale("log", base=2)
    ax_b.set_xlim(0.85, 300)
    ax_b.set_ylim(0.38, 180)
    ax_b.set_xticks([1, 4, 16, 64, 256], labels=["1", "4", "16", "64", "256"])
    ax_b.set_yticks([0.5, 2, 8, 32, 128], labels=["0.5", "2", "8", "32", "128"])
    ax_b.set_xlabel(r"shell frequency $K$")
    ax_b.set_ylabel(r"angular speed $\Omega_K(0)$", color=NAVY)
    ax_b.tick_params(axis="y", colors=NAVY)
    ax_b_right = ax_b.twinx()
    line_source = ax_b_right.plot(
        frequency,
        source_density,
        color=RUST,
        linestyle="--",
        marker="s",
        markerfacecolor="none",
        markersize=3.0,
        label=r"source density $S_K(0)$",
    )[0]
    limit_line = ax_b_right.axhline(
        9.0 / 4.0,
        color=GREY,
        linestyle=":",
        linewidth=0.9,
        label=r"limit $9/4$",
    )
    ax_b_right.set_ylim(2.0, 6.6)
    ax_b_right.set_ylabel(r"$S_K(0)$", color=RUST)
    ax_b_right.tick_params(axis="y", colors=RUST)
    ax_b.set_title(r"Fixed energy at $t=0$ only: angular speed grows", loc="left", fontweight="bold")
    ax_b.legend(
        [line_omega, line_source, limit_line],
        [line_omega.get_label(), line_source.get_label(), limit_line.get_label()],
        frameon=False,
        loc="upper left",
    )
    ax_b.text(
        0.70,
        0.95,
        r"$\nu=1,\ \|u_0\|_2^2=6,\ a_K=K^{-1}$",
        transform=ax_b.transAxes,
        ha="center",
        va="top",
        fontsize=6.2,
    )

    delta, rayleigh = series(rows, "C", "rayleighQuotient")
    _, projective = series(rows, "C", "projectiveSource")
    line_r = ax_c.plot(
        delta,
        rayleigh,
        color=NAVY,
        marker="o",
        markevery=10,
        markersize=2.8,
        label=r"$R_\delta$",
    )[0]
    ax_c.set_xlim(0.0, 1.0)
    ax_c.set_ylim(0.97, 1.47)
    ax_c.set_xlabel(r"cutoff modulation $\delta$")
    ax_c.set_ylabel(r"Rayleigh ratio $R_\delta$", color=NAVY)
    ax_c.tick_params(axis="y", colors=NAVY)
    ax_c_right = ax_c.twinx()
    line_j = ax_c_right.plot(
        delta,
        projective,
        color=RUST,
        linestyle="--",
        marker="s",
        markerfacecolor="none",
        markevery=(5, 10),
        markersize=2.8,
        label=r"$J_\delta$",
    )[0]
    ax_c_right.set_ylim(-0.01, 0.27)
    ax_c_right.set_ylabel(r"projective source ratio $J_\delta$", color=RUST)
    ax_c_right.tick_params(axis="y", colors=RUST)
    ax_c.set_title("A fixed cutoff gives finite saturation", loc="left", fontweight="bold")
    ax_c.legend(
        [line_r, line_j],
        [line_r.get_label(), line_j.get_label()],
        frameon=False,
        loc="upper left",
    )
    ax_c.text(
        0.98,
        0.05,
        r"$\chi_\delta=(1+\delta\cos Z)/2$",
        transform=ax_c.transAxes,
        ha="right",
        va="bottom",
        fontsize=6.2,
    )

    shell, known_weight = series(rows, "D", "knownHeatWeight")
    _, required_weight = series(rows, "D", "directRequiredWeight")
    ax_d.fill_between(shell, known_weight, required_weight, color="#dddddd", alpha=0.65)
    ax_d.plot(
        shell,
        required_weight,
        color=RUST,
        marker="s",
        markerfacecolor="none",
        markersize=3.0,
        label=r"direct BV/Young weight $1$",
    )
    ax_d.plot(
        shell,
        known_weight,
        color=NAVY,
        linestyle="--",
        marker="o",
        markersize=2.8,
        label=r"known heat-bulk weight $K^{-2}$",
    )
    ax_d.set_xscale("log", base=2)
    ax_d.set_yscale("log")
    ax_d.set_xlim(0.85, 300)
    ax_d.set_ylim(8.0e-6, 2.0)
    ax_d.set_xticks([1, 4, 16, 64, 256], labels=["1", "4", "16", "64", "256"])
    ax_d.set_xlabel(r"shell frequency $K$")
    ax_d.set_ylabel("frequency weight")
    ax_d.set_title(r"Direct Young estimate loses two powers of $K$", loc="left", fontweight="bold")
    ax_d.legend(frameon=False, loc="lower left")
    ax_d.text(
        0.96,
        0.72,
        r"gap ratio $=K^2$" + "\n" + "(scaling comparison)",
        transform=ax_d.transAxes,
        ha="right",
        va="center",
        fontsize=6.4,
    )

    for axis in (ax_a, ax_b, ax_c, ax_d):
        axis.grid(color="#dddddd", linewidth=0.42, alpha=0.75)
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

    fig.subplots_adjust(left=0.085, right=0.915, bottom=0.10, top=0.94, wspace=0.42, hspace=0.43)
    output = args.output_stem
    title = "R0.71H projective heat curvature and remaining angular budget"
    fig.savefig(
        output.with_suffix(".pdf"),
        metadata={
            "Title": title,
            "Author": "Chuikuan Zeng",
            "Subject": "Closed-form projective-curvature and scaling diagnostics",
            "Creator": "Matplotlib",
            "CreationDate": None,
            "ModDate": None,
        },
    )
    fig.savefig(
        output.with_suffix(".svg"),
        metadata={
            "Title": title,
            "Description": "Four-panel closed-form diagnostic figure; no DNS or fitted data.",
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
            "Description": "Four-panel closed-form diagnostic figure; no DNS or fitted data.",
            "Software": "Matplotlib",
        },
    )
    plt.close(fig)


if __name__ == "__main__":
    main()
