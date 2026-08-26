#!/usr/bin/env python3
"""Render the four-panel R0.71V fixed-target boundary-layer figure."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
import json
import os
from pathlib import Path
import resource
import time
from zoneinfo import ZoneInfo

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
import numpy as np


ROOT = Path(__file__).resolve().parent
TIMEZONE = ZoneInfo("Asia/Shanghai")
PAPER = "#FBF9F4"
INK = "#252422"
BLUE = "#355C7D"
OCHRE = "#B8792B"
GRAY = "#77736C"
LIGHT = "#D8D3C8"
PALE_BLUE = "#91A6B8"


def append_log(path: Path, payload: dict[str, object]) -> None:
    payload = {
        "timestamp": datetime.now(TIMEZONE).isoformat(timespec="milliseconds"),
        **payload,
    }
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(payload, sort_keys=True) + "\n")


def configure() -> None:
    mpl.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 7.05,
        "axes.titlesize": 7.9,
        "axes.labelsize": 6.95,
        "xtick.labelsize": 6.2,
        "ytick.labelsize": 6.2,
        "legend.fontsize": 5.7,
        "axes.edgecolor": INK,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": INK,
        "ytick.color": INK,
        "axes.facecolor": PAPER,
        "figure.facecolor": PAPER,
        "savefig.facecolor": PAPER,
        "axes.linewidth": 0.72,
        "lines.linewidth": 1.22,
        "pdf.fonttype": 42,
        "svg.fonttype": "none",
        "svg.hashsalt": "r071v-zero-level-boundary",
    })


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def select(
    rows: list[dict[str, str]], panel: str, series: str, q_value: str | None = None
) -> list[dict[str, str]]:
    selected = [
        row for row in rows
        if row["panel"] == panel
        and row["series"] == series
        and (q_value is None or row["q"] == q_value)
    ]
    return sorted(selected, key=lambda row: float(row["x"]))


def xy(rows: list[dict[str, str]]) -> tuple[np.ndarray, np.ndarray]:
    return (
        np.asarray([float(row["x"]) for row in rows], dtype=float),
        np.asarray([float(row["y"]) for row in rows], dtype=float),
    )


def blossom(fig: plt.Figure) -> None:
    center_x, center_y = 0.979, 0.965
    for index, color in enumerate((BLUE, OCHRE, BLUE, OCHRE, BLUE)):
        angle = 2.0 * np.pi * index / 5.0 + np.pi / 2.0
        fig.add_artist(Circle(
            (center_x + 0.009 * np.cos(angle), center_y + 0.009 * np.sin(angle)),
            0.0062,
            transform=fig.transFigure,
            facecolor=color,
            edgecolor=PAPER,
            linewidth=0.35,
            alpha=0.82,
            zorder=20,
        ))
    fig.add_artist(Circle(
        (center_x, center_y),
        0.0048,
        transform=fig.transFigure,
        facecolor=INK,
        edgecolor=PAPER,
        linewidth=0.35,
        zorder=21,
    ))


def panel_title(axis: plt.Axes, letter: str, title: str) -> None:
    axis.set_title(f"{letter}   {title}", loc="left", fontweight="bold", pad=4.7)


def common_log_axis(axis: plt.Axes) -> None:
    axis.set_xscale("log", base=2)
    axis.set_yscale("log")
    axis.set_xticks([8, 16, 32, 64, 128, 256])
    axis.set_xticklabels(["8", "16", "32", "64", "128", "256"])
    axis.grid(True, which="major", color=LIGHT, linewidth=0.38)
    axis.grid(True, which="minor", axis="y", color=LIGHT, linewidth=0.25, alpha=0.45)
    axis.set_xlabel(r"auxiliary-frequency factor $q$")


def add_power_guide(
    axis: plt.Axes,
    q_values: np.ndarray,
    values: np.ndarray,
    power: float,
    label: str,
    color: str,
    vertical_factor: float = 1.0,
) -> None:
    start_index = 3
    guide_x = q_values[start_index:]
    anchor = values[start_index] * vertical_factor
    guide_y = anchor * (guide_x / guide_x[0]) ** power
    axis.plot(
        guide_x,
        guide_y,
        color=color,
        linewidth=0.72,
        linestyle=(0, (1.4, 1.5)),
        alpha=0.68,
        zorder=1,
    )
    axis.annotate(
        label,
        xy=(guide_x[-1], guide_y[-1]),
        xytext=(-2, 1.5),
        textcoords="offset points",
        ha="right",
        va="bottom",
        fontsize=5.2,
        color=color,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-stem", type=Path, required=True)
    arguments = parser.parse_args()
    started = time.perf_counter()
    rows = load_rows(arguments.data)
    results = json.loads(arguments.results.read_text(encoding="utf-8"))
    config = json.loads(arguments.config.read_text(encoding="utf-8"))
    configure()
    append_log(ROOT / "progress.ndjson", {"stage": "plot-start"})

    # Matplotlib 3.11 quantizes figure inches internally; use the journal's
    # audited 0.01-inch representation (7.01 by 5.28 inches).
    width = round(float(config["figure"]["widthMillimetres"]) / 25.4, 2)
    height = round(float(config["figure"]["heightMillimetres"]) / 25.4, 2)
    fig, axes = plt.subplots(2, 2, figsize=(width, height), constrained_layout=False)
    fig.subplots_adjust(
        left=0.086,
        right=0.985,
        bottom=0.145,
        top=0.868,
        wspace=0.30,
        hspace=0.39,
    )
    axa, axb, axc, axd = axes.ravel()
    fig.suptitle(
        "Fixed-target zero-level boundary layer",
        x=0.086,
        y=0.963,
        ha="left",
        fontsize=10.15,
        fontweight="bold",
    )
    fig.text(
        0.086,
        0.923,
        r"exact $N=2$ tangent  ·  $\nu=.02$  ·  $K_y=K_z=\kappa_*=m_*=1$  ·  $d=8$  ·  roots $(.1,.2)/q^2$  ·  $\ell=.5$  ·  $Q=4$, $B=.25$",
        ha="left",
        fontsize=6.55,
        color=GRAY,
    )
    blossom(fig)

    profile_styles = (
        ("8", PALE_BLUE, (0, (2.0, 1.5)), r"$q=8$"),
        ("32", OCHRE, "--", r"$q=32$"),
        ("256", BLUE, "-", r"$q=256$"),
        ("limit", INK, ":", r"$\Gamma$"),
    )
    profile_cache: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    for q_text, color, line_style, label in profile_styles:
        series = "limiting target profile" if q_text == "limit" else "rescaled target profile"
        x_values, y_values = xy(select(rows, "A", series, q_text))
        profile_cache[q_text] = (x_values, y_values)
        axa.plot(x_values, y_values, color=color, linestyle=line_style, label=label)
    axa.axhline(0.0, color=GRAY, linewidth=0.52)
    for root, marker in zip(config["scaledRoots"], ("o", "s"), strict=True):
        axa.axvline(root, color=LIGHT, linewidth=0.55, linestyle=(0, (1.2, 1.6)))
        axa.scatter(
            [root],
            [0.0],
            marker=marker,
            s=18,
            facecolors=PAPER,
            edgecolors=INK,
            linewidths=0.75,
            zorder=6,
        )
    axa.set_xlim(0.05, 1.25)
    axa.set_xlabel(r"scaled relative time $r=q^2\theta$")
    axa.set_ylabel(r"$q^2\gamma_q(r/q^2)$")
    axa.grid(True, color=LIGHT, linewidth=0.38)
    axa.legend(loc="upper left", frameon=False, ncol=2, columnspacing=0.85, handlelength=2.2)
    zoom = inset_axes(axa, width="42%", height="43%", loc="center right", borderpad=0.75)
    for q_text, color, line_style, _ in profile_styles:
        x_values, y_values = profile_cache[q_text]
        zoom.plot(x_values, y_values, color=color, linestyle=line_style, linewidth=0.86)
    zoom.axhline(0.0, color=GRAY, linewidth=0.42)
    for root in config["scaledRoots"]:
        zoom.axvline(root, color=LIGHT, linewidth=0.45, linestyle=":")
    zoom.set_xlim(0.05, 0.245)
    zoom.set_ylim(-0.0054, 0.0045)
    zoom.tick_params(labelsize=4.5, pad=1.0, length=2.0)
    zoom.grid(True, color=LIGHT, linewidth=0.25)
    mark_inset(axa, zoom, loc1=2, loc2=4, fc="none", ec=GRAY, linewidth=0.35)
    panel_title(axa, "A", "Rescaled two-root profiles")

    q_values = np.asarray(config["qValues"], dtype=float)
    panel_b_styles = (
        ("second-root atom", BLUE, "-", "o", r"second-root atom $M_{2,q}$", -4.0, r"$q^{-4}$"),
        ("target-shell first row", OCHRE, "--", "s", r"$(2/\ell)\mathcal{B}^{(*)}_{1,q}$", -6.0, r"$q^{-6}$"),
        ("target-shell second row", INK, "-.", "^", r"$(7\ell/3)\mathcal{B}^{(*)}_{2,q}$", -2.0, r"$q^{-2}$"),
        ("terminal H square", GRAY, ":", "D", r"terminal $H_E^2$", -8.0, r"$q^{-8}$"),
    )
    for index, (series, color, line_style, marker, label, power, guide) in enumerate(panel_b_styles):
        x_values, y_values = xy(select(rows, "B", series))
        axb.loglog(
            x_values,
            y_values,
            color=color,
            linestyle=line_style,
            marker=marker,
            markersize=3.35,
            markerfacecolor=PAPER if index in (1, 3) else color,
            markeredgecolor=color,
            markeredgewidth=0.65,
            label=label,
            zorder=3,
        )
        add_power_guide(axb, x_values, y_values, power, guide, color)
    common_log_axis(axb)
    axb.set_ylabel("tangent coefficient or excursion charge")
    axb.legend(loc="lower left", frameon=False, ncol=2, columnspacing=0.75, handlelength=2.1)
    axb.text(
        0.98,
        0.79,
        "atom = second prescribed root only\nrows = singleton target shell",
        transform=axb.transAxes,
        ha="right",
        va="top",
        fontsize=5.3,
        color=GRAY,
    )
    panel_title(axb, "B", "Second-root atom and jet ledger")

    panel_c_styles = (
        (
            "second-root atom over first row",
            BLUE,
            "-",
            "o",
            r"$M_{2,q}/[(2/\ell)\mathcal{B}^{(*)}_{1,q}]$",
            2.0,
            r"$q^{2}$",
        ),
        (
            "second-root atom over second row",
            OCHRE,
            "--",
            "s",
            r"$M_{2,q}/[(7\ell/3)\mathcal{B}^{(*)}_{2,q}]$",
            -2.0,
            r"$q^{-2}$",
        ),
        (
            "second-root atom over terminal H square",
            INK,
            ":",
            "D",
            r"$M_{2,q}/H_{E,\mathrm{term}}^2$",
            4.0,
            r"$q^{4}$",
        ),
    )
    for index, (series, color, line_style, marker, label, power, guide) in enumerate(panel_c_styles):
        x_values, y_values = xy(select(rows, "C", series))
        axc.loglog(
            x_values,
            y_values,
            color=color,
            linestyle=line_style,
            marker=marker,
            markersize=3.5,
            markerfacecolor=PAPER if index == 1 else color,
            markeredgecolor=color,
            markeredgewidth=0.65,
            label=label,
            zorder=3,
        )
        add_power_guide(axc, x_values, y_values, power, guide, color)
    axc.axhline(1.0, color=GRAY, linewidth=0.6, linestyle=(0, (2.5, 2.0)))
    common_log_axis(axc)
    axc.set_ylabel("dimensionless ratio")
    axc.legend(loc="upper left", frameon=False, handlelength=2.2)
    axc.text(
        0.98,
        0.34,
        "first root may be paid separately;\nthe second-root ratio still diverges",
        transform=axc.transAxes,
        ha="right",
        va="bottom",
        fontsize=5.35,
        color=GRAY,
    )
    panel_title(axc, "C", "Necessity ratios at the second root")

    panel_d_styles = (
        ("internal D", BLUE, "-", "o", r"internal $D_E$", -2.0, r"$q^{-2}$"),
        ("terminal D", OCHRE, "--", "s", r"terminal $D_E$", -4.0, r"$q^{-4}$"),
    )
    for index, (series, color, line_style, marker, label, power, guide) in enumerate(panel_d_styles):
        x_values, y_values = xy(select(rows, "D", series))
        axd.loglog(
            x_values,
            y_values,
            color=color,
            linestyle=line_style,
            marker=marker,
            markersize=3.6,
            markerfacecolor=PAPER if index else color,
            markeredgecolor=color,
            markeredgewidth=0.65,
            label=label,
            zorder=3,
        )
        add_power_guide(axd, x_values, y_values, power, guide, color)
    common_log_axis(axd)
    axd.set_ylabel(r"$D_E=h_E^2Y(t_E)/(\ell Y_E\|C_t(t_E)\|_2^2)$")
    axd.legend(loc="upper right", frameon=False)
    powers = results["fittedExponentsTailFour"]
    axd.text(
        0.03,
        0.065,
        "tail-four slopes\n"
        + rf"internal {powers['internalD']:.3f}; terminal {powers['terminalD']:.3f}",
        transform=axd.transAxes,
        ha="left",
        va="bottom",
        fontsize=5.4,
        color=GRAY,
    )
    panel_title(axd, "D", "Excursion non-collapse factors")

    fig.text(
        0.5,
        0.027,
        "Fixed target, multiplier, shell scale and macroscopic window; exact IFT tangent only — no nonlinear integration, no DNS, no covariant dilation.",
        ha="center",
        fontsize=6.0,
        color=GRAY,
    )
    metadata = {
        "Title": "R0.71V fixed-target zero-level boundary layer",
        "Subject": "Second-root atom versus target-shell first and second time-jet rows",
        "Author": "Kasifa",
        "Keywords": "Navier-Stokes, recurrence, zero-level atom, temporal jet, excursion",
    }
    arguments.output_stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(arguments.output_stem.with_suffix(".pdf"), metadata=metadata)
    svg_path = arguments.output_stem.with_suffix(".svg")
    fig.savefig(
        svg_path,
        metadata={"Title": metadata["Title"], "Description": metadata["Subject"]},
    )
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines())
        + "\n",
        encoding="utf-8",
    )
    fig.savefig(
        arguments.output_stem.with_suffix(".png"),
        dpi=int(config["figure"]["pngDpi"]),
        metadata={"Title": metadata["Title"]},
    )
    plt.close(fig)
    elapsed = time.perf_counter() - started
    usage = resource.getrusage(resource.RUSAGE_SELF)
    append_log(ROOT / "progress.ndjson", {
        "stage": "plot-complete",
        "outputs": ["figure.pdf", "figure.svg", "figure.png"],
        "elapsedSeconds": elapsed,
    })
    append_log(ROOT / "resource-log.ndjson", {
        "stage": "plot-complete",
        "elapsedSeconds": elapsed,
        "pid": os.getpid(),
        "processUserCpuSeconds": usage.ru_utime,
        "processSystemCpuSeconds": usage.ru_stime,
        "maximumResidentSetRaw": usage.ru_maxrss,
    })
    print(json.dumps({
        "status": "passed",
        "outputs": ["figure.pdf", "figure.svg", "figure.png"],
        "elapsedSeconds": elapsed,
    }, indent=2))


if __name__ == "__main__":
    main()
