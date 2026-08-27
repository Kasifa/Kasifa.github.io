#!/usr/bin/env python3
"""Build the formal R0.72L moderate strong-coupling figure."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import platform
import resource
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from matplotlib.patches import Ellipse


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def rss_mb() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        return float(value) / (1024.0 * 1024.0)
    return float(value) / 1024.0


def append_ndjson(path: Path, payload: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def add_row(
    rows: list[dict[str, Any]],
    *,
    panel: str,
    route: str,
    series: str,
    x: float,
    y: float,
    raw_value: float,
    auxiliary: float | str,
    pointer: str,
    note: str,
) -> None:
    rows.append(
        {
            "panel": panel,
            "route": route,
            "series": series,
            "x": x,
            "y": y,
            "rawValue": raw_value,
            "auxiliary": auxiliary,
            "source": "research/r072l_report-source.md",
            "pointer": pointer,
            "note": note,
        }
    )


def ledger_values(r_value: float, p_value: float, epsilon: float) -> dict[str, float]:
    ell = 1.0 + math.log(r_value)
    u0 = epsilon ** (4.0 / 3.0) * p_value ** (4.0 / 3.0)
    w_value = (
        epsilon ** (1.0 / 3.0)
        * p_value ** (1.0 / 3.0)
        * r_value ** (-1.0 / 3.0)
        * ell ** (-0.5)
    )
    u_value = epsilon ** (7.0 / 3.0) * p_value ** (4.0 / 3.0)
    v_value = epsilon ** (1.0 / 3.0) * p_value ** (1.0 / 3.0) * r_value
    h_value = u_value / v_value
    z_value = (
        epsilon**2
        * p_value**2
        * r_value ** (2.0 / 3.0)
        * (1.0 + epsilon) ** (-2.0 / 3.0)
        * (1.0 + math.log(2.0 + r_value**2 * (1.0 + epsilon)))
    )
    return {"U0": u0, "W": w_value, "U": u_value, "V": v_value, "H": h_value, "Z": z_value}


def rk4_step(
    derivative: Callable[[float, tuple[float, float]], tuple[float, float]],
    y_value: float,
    state: tuple[float, float],
    step: float,
) -> tuple[float, float]:
    k1 = derivative(y_value, state)
    k2 = derivative(y_value + 0.5 * step, (state[0] + 0.5 * step * k1[0], state[1] + 0.5 * step * k1[1]))
    k3 = derivative(y_value + 0.5 * step, (state[0] + 0.5 * step * k2[0], state[1] + 0.5 * step * k2[1]))
    k4 = derivative(y_value + step, (state[0] + step * k3[0], state[1] + step * k3[1]))
    return (
        state[0] + step * (k1[0] + 2.0 * k2[0] + 2.0 * k3[0] + k4[0]) / 6.0,
        state[1] + step * (k1[1] + 2.0 * k2[1] + 2.0 * k3[1] + k4[1]) / 6.0,
    )


def galerkin_case(r_value: int, sigma: float) -> dict[str, float | int]:
    steps = max(20_000, int(math.ceil(40.0 * sigma)))
    step = 1.0 / steps
    inv_r2 = 1.0 / float(r_value**2)

    def derivative(y_value: float, state: tuple[float, float]) -> tuple[float, float]:
        coupling = sigma * math.exp(-y_value)
        return (
            -inv_r2 * state[0] - coupling * state[1],
            coupling * state[0] - (1.0 + inv_r2) * state[1],
        )

    state = (1.0 / math.sqrt(2.0), 1.0 / math.sqrt(2.0))
    y_value = 0.0
    root_mass = 0.0
    cubic_integral = 0.0
    mixed_integral = 0.0
    root_count = 0
    previous_u, previous_v = state
    previous_cubic = abs(previous_u * previous_v)
    previous_mixed = previous_v**2
    for _ in range(steps):
        next_state = rk4_step(derivative, y_value, state, step)
        next_y = y_value + step
        next_u, next_v = next_state
        next_cubic = math.exp(-3.0 * next_y) * abs(next_u * next_v)
        next_mixed = math.exp(-2.0 * next_y) * next_v**2
        cubic_integral += 0.5 * step * (previous_cubic + next_cubic)
        mixed_integral += 0.5 * step * (previous_mixed + next_mixed)
        if previous_u == 0.0 or previous_u * next_u < 0.0:
            fraction = abs(previous_u) / (abs(previous_u) + abs(next_u))
            root_y = y_value + fraction * step
            root_v = previous_v + fraction * (next_v - previous_v)
            root_mass += math.exp(-2.0 * root_y) * root_v**2
            root_count += 1
        state = next_state
        y_value = next_y
        previous_u, previous_v = state
        previous_cubic = next_cubic
        previous_mixed = next_mixed
    return {
        "sigma": sigma,
        "steps": steps,
        "rootCount": root_count,
        "G": root_mass,
        "C": sigma * cubic_integral,
        "EQ": 2.0 * mixed_integral,
    }


def prepare_data(config: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any], list[Path]]:
    rows: list[dict[str, Any]] = []
    panel_a = config["panels"]["A"]
    r_grid = np.geomspace(float(panel_a["rMin"]), float(panel_a["rMax"]), int(panel_a["samples"]))
    for index, r_value in enumerate(r_grid):
        ell = 1.0 + math.log(float(r_value))
        for series, p_value in (("p = 1", 1.0), ("p = R^-1/2", float(r_value) ** -0.5)):
            epsilon_max = p_value ** (2.0 / 3.0) * float(r_value) ** (2.0 / 3.0) * ell
            add_row(rows, panel="A", route="analytic", series=series, x=float(r_value), y=epsilon_max, raw_value=epsilon_max, auxiliary=p_value, pointer=f"equation (0.9), sample {index}", note="analytic window upper edge; equality gives boundedness, little-o gives decay")

    panel_b = config["panels"]["B"]
    r_b = float(panel_b["R"])
    p_b = r_b ** -0.5
    k_b = float(panel_b["K"])
    ell_b = 1.0 + math.log(r_b)
    epsilon_max_b = p_b ** (2.0 / 3.0) * r_b ** (2.0 / 3.0) * ell_b
    q_grid = np.geomspace(float(panel_b["qMin"]), float(panel_b["qMax"]), int(panel_b["samples"]))
    for index, q_value in enumerate(q_grid):
        epsilon = float(q_value) * epsilon_max_b
        parts = ledger_values(r_b, p_b, epsilon)
        terms = {
            "first-root term": parts["U0"] / (k_b + parts["Z"]),
            "mixed-row term": parts["W"] / math.sqrt(k_b + parts["Z"]),
            "true-cubic term": parts["U"] / (k_b + max(parts["H"], parts["Z"])),
        }
        for series, value in terms.items():
            add_row(rows, panel="B", route="scaling diagnostic", series=series, x=float(q_value), y=float(value), raw_value=epsilon, auxiliary=parts["Z"], pointer=f"equations (0.4), (0.7), (0.8), sample {index}", note="suppressed absolute constants normalized to one; not a sharp numerical bound")
        add_row(rows, panel="B", route="scaling diagnostic", series="three-term sum", x=float(q_value), y=float(sum(terms.values())), raw_value=epsilon, auxiliary=parts["Z"], pointer=f"equation (0.8), sample {index}", note="sum of the three normalized diagnostic components")

    panel_c = config["panels"]["C"]
    r_c = int(panel_c["R"])
    galerkin_rows: list[dict[str, float | int]] = []
    for sigma in panel_c["sigmaValues"]:
        case = galerkin_case(r_c, float(sigma))
        galerkin_rows.append(case)
        for series, key in (("G_Gal / a^2", "G"), ("C_x,Gal / a^2", "C"), ("E_Q,Gal / a^2", "EQ")):
            add_row(rows, panel="C", route="finite projected ODE", series=series, x=float(sigma), y=float(case[key]), raw_value=float(case[key]), auxiliary=int(case["rootCount"]), pointer="equations (6.3)-(6.6)", note="deterministic RK4 finite diagnostic; projected ODE is not a full-lattice subsystem")

    for application, support, series in ((0.0, [0.0], "launch support"), (1.0, [-1.0, 1.0], "retained support"), (2.0, [0.0], "retained support"), (2.0, [-2.0, 2.0], "omitted-shell support")):
        for normalized_index in support:
            add_row(rows, panel="D", route="exact identity", series=series, x=application, y=normalized_index, raw_value=normalized_index, auxiliary="1/sqrt(2)" if series == "omitted-shell support" else "", pointer="equations (6.7)-(6.9)", note="support schematic; omitted-to-retained norm ratio is exact")

    tail = galerkin_rows[-4:]
    log_sigma = np.log([float(row["sigma"]) for row in tail])
    slopes = {
        key: float(np.polyfit(log_sigma, np.log([float(row[key]) for row in tail]), 1)[0])
        for key in ("G", "C", "EQ")
    }
    summary = {
        "rowCount": len(rows),
        "panelBEpsilonMax": epsilon_max_b,
        "panelCGalerkinR": r_c,
        "panelCSlopesLastFour": slopes,
        "panelCRootCounts": [int(row["rootCount"]) for row in galerkin_rows],
        "outsideOverInside": 1.0 / math.sqrt(2.0),
        "newPdeEvolution": False,
        "finiteProjectedOdeOnly": True,
    }
    source_paths = [
        REPOSITORY / config["analyticSource"],
        ROOT / "config.json",
        ROOT / "contract.json",
        ROOT / "figure-contract.md",
        ROOT / "caption.md",
    ]
    return rows, summary, source_paths


def write_data(rows: list[dict[str, Any]]) -> None:
    with (ROOT / "data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def blossom(fig: mpl.figure.Figure, color: str) -> None:
    center = (0.968, 0.972)
    for angle in range(0, 360, 72):
        fig.add_artist(Ellipse(center, width=0.020, height=0.008, angle=angle, facecolor="none", edgecolor=color, linewidth=0.65, transform=fig.transFigure, zorder=20))


def style_axes(ax: mpl.axes.Axes, palette: dict[str, str], *, grid: bool = True) -> None:
    ax.set_facecolor(palette["paper"])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(palette["muted"])
    ax.spines["bottom"].set_color(palette["muted"])
    ax.tick_params(colors=palette["ink"], labelsize=7, length=2.5, width=0.6)
    if grid:
        ax.grid(True, color=palette["grid"], linewidth=0.45, alpha=0.75)
    else:
        ax.grid(False)
    ax.set_axisbelow(True)


def panel_label(ax: mpl.axes.Axes, label: str, palette: dict[str, str]) -> None:
    ax.text(-0.10, 1.02, label, transform=ax.transAxes, fontsize=10, fontweight="bold", color=palette["ink"], va="bottom")


def panel_rows(rows: list[dict[str, Any]], panel: str, series: str) -> list[dict[str, Any]]:
    selected = [row for row in rows if row["panel"] == panel and row["series"] == series]
    return sorted(selected, key=lambda row: float(row["x"]))


def draw_figure(rows: list[dict[str, Any]], config: dict[str, Any], summary: dict[str, Any]) -> None:
    palette = config["palette"]
    width = float(config["figure"]["widthMillimetres"]) / 25.4
    height = float(config["figure"]["heightMillimetres"]) / 25.4
    mpl.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 7.5,
        "axes.titlesize": 8.2,
        "axes.labelsize": 7.5,
        "legend.fontsize": 6.2,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "hatch.linewidth": 0.45,
    })
    fig, axes = plt.subplots(2, 2, figsize=(width, height), constrained_layout=False)
    fig.patch.set_facecolor(palette["paper"])
    fig.subplots_adjust(left=0.085, right=0.975, bottom=0.105, top=0.855, wspace=0.34, hspace=0.46)
    fig.suptitle("Moderate strong-coupling window and full-lattice boundary", x=0.085, y=0.965, ha="left", fontsize=9.8, fontweight="bold", color=palette["ink"])
    fig.text(0.085, 0.912, "Analytic scaling from report equations; projected-ODE points are finite diagnostics, not a PDE embedding", ha="left", fontsize=6.7, color=palette["muted"])
    blossom(fig, palette["ochre"])

    ax = axes[0, 0]
    style_axes(ax, palette)
    panel_label(ax, "A", palette)
    p_one = panel_rows(rows, "A", "p = 1")
    p_worst = panel_rows(rows, "A", "p = R^-1/2")
    r_values = np.array([float(row["x"]) for row in p_one])
    y_one = np.array([float(row["y"]) for row in p_one])
    y_worst = np.array([float(row["y"]) for row in p_worst])
    ceiling = y_one.max() * 5.0
    ax.fill_between(r_values, 1.0, y_worst, color=palette["blueLight"], alpha=0.75, linewidth=0)
    ax.fill_between(r_values, y_worst, y_one, facecolor=palette["ochreLight"], alpha=0.55, hatch="////", edgecolor=palette["ochre"], linewidth=0.0)
    ax.fill_between(r_values, y_one, ceiling, facecolor=palette["paper"], hatch="....", edgecolor=palette["muted"], linewidth=0.0)
    ax.plot(r_values, y_one, color=palette["ochre"], linewidth=1.25, label=r"$p=1$")
    ax.plot(r_values, y_worst, color=palette["blue"], linestyle="--", linewidth=1.25, label=r"$p=R^{-1/2}$")
    ax.axhline(1.0, color=palette["ink"], linestyle=":", linewidth=0.9)
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_ylim(0.7, ceiling)
    ax.set_title("Analytic strong-coupling phase window", loc="left", pad=6)
    ax.set_xlabel("carrier scale R")
    ax.set_ylabel(r"common-band exposure scale $\varepsilon$")
    ax.legend(frameon=False, loc="upper left", handlelength=2.2)
    ax.text(0.98, 0.91, "unresolved extreme", transform=ax.transAxes, ha="right", va="top", fontsize=6.3, color=palette["muted"])
    ax.text(0.04, 0.08, "uniform worst-case window", transform=ax.transAxes, fontsize=6.2, color=palette["blue"])

    ax = axes[0, 1]
    style_axes(ax, palette)
    panel_label(ax, "B", palette)
    styles = {
        "first-root term": (palette["muted"], ":", "^"),
        "mixed-row term": (palette["blue"], "--", "s"),
        "true-cubic term": (palette["ochre"], "-", "o"),
        "three-term sum": (palette["ink"], "-.", None),
    }
    for series, (color, linestyle, marker) in styles.items():
        selected = panel_rows(rows, "B", series)
        ax.plot([float(row["x"]) for row in selected], [float(row["y"]) for row in selected], color=color, linestyle=linestyle, linewidth=1.15 if series != "three-term sum" else 0.85, marker=marker, markevery=32, markersize=3.0, markerfacecolor=palette["open"] if marker == "s" else color, markeredgecolor=color, label=series)
    ax.axvline(1.0, color=palette["ink"], linestyle=":", linewidth=0.9)
    ax.text(1.08, 0.028, r"$q=1$", fontsize=6.2, color=palette["ink"])
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_title("Three terms across the window edge", loc="left", pad=6)
    ax.set_xlabel(r"$q=\varepsilon/\varepsilon_{\max}$")
    ax.set_ylabel("normalized bound component")
    ax.legend(frameon=False, loc="upper left", handlelength=2.2, ncol=1)
    ax.text(0.98, 0.29, r"$R=4096,\ p=R^{-1/2},\ K=1$", transform=ax.transAxes, ha="right", fontsize=6.1, color=palette["muted"], bbox={"facecolor": palette["paper"], "edgecolor": "none", "alpha": 0.90, "pad": 1.2})

    ax = axes[1, 0]
    style_axes(ax, palette)
    panel_label(ax, "C", palette)
    styles_c = {
        "G_Gal / a^2": (palette["blue"], "-", "o"),
        "C_x,Gal / a^2": (palette["ochre"], "--", "s"),
        "E_Q,Gal / a^2": (palette["muted"], ":", "^")
    }
    labels_c = {
        "G_Gal / a^2": r"$G_{\rm Gal}/a^2$",
        "C_x,Gal / a^2": r"$\mathcal{C}_{\times,\mathrm{Gal}}/a^2$",
        "E_Q,Gal / a^2": r"$\mathcal{E}_{Q,\mathrm{Gal}}/a^2$",
    }
    for series, (color, linestyle, marker) in styles_c.items():
        selected = panel_rows(rows, "C", series)
        ax.plot([float(row["x"]) for row in selected], [float(row["y"]) for row in selected], color=color, linestyle=linestyle, linewidth=1.15, marker=marker, markersize=3.5, markerfacecolor=palette["open"] if marker == "s" else color, markeredgecolor=color, label=labels_c[series])
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_title("Finite projected three-mode ODE", loc="left", pad=6)
    ax.set_xlabel(r"projected coupling $\sigma$")
    ax.set_ylabel(r"projected row mass / $a^2$")
    ax.legend(frameon=False, loc="upper left", handlelength=2.2)
    slopes = summary["panelCSlopesLastFour"]
    ax.text(0.98, 0.05, f"tail slopes: G {slopes['G']:.3f}, C {slopes['C']:.3f}, E_Q {slopes['EQ']:.3f}", transform=ax.transAxes, ha="right", fontsize=6.1, color=palette["muted"])
    ax.text(0.98, 0.17, "projection only; not full lattice", transform=ax.transAxes, ha="right", fontsize=6.2, color=palette["ochre"])

    ax = axes[1, 1]
    style_axes(ax, palette, grid=False)
    panel_label(ax, "D", palette)
    ax.axhspan(-1.45, 1.45, color=palette["blueLight"], alpha=0.48, zorder=0)
    ax.axhspan(1.45, 2.55, facecolor=palette["ochreLight"], alpha=0.45, hatch="////", edgecolor=palette["ochre"], linewidth=0.0, zorder=0)
    ax.axhspan(-2.55, -1.45, facecolor=palette["ochreLight"], alpha=0.45, hatch="////", edgecolor=palette["ochre"], linewidth=0.0, zorder=0)
    for start, end in (((0, 0), (1, 1)), ((0, 0), (1, -1)), ((1, 1), (2, 0)), ((1, -1), (2, 0)), ((1, 1), (2, 2)), ((1, -1), (2, -2))):
        outside = abs(end[1]) > 1.1
        ax.annotate("", xy=end, xytext=start, arrowprops={"arrowstyle": "->", "color": palette["ochre"] if outside else palette["blue"], "lw": 0.9, "linestyle": "--" if outside else "-"}, zorder=2)
    ax.scatter([0, 1, 1, 2], [0, 1, -1, 0], s=30, color=palette["blue"], edgecolor=palette["ink"], linewidth=0.5, zorder=4, label="retained sector")
    ax.scatter([2, 2], [2, -2], s=35, marker="s", facecolor=palette["open"], edgecolor=palette["ochre"], linewidth=1.0, zorder=5, label="omitted shell")
    ax.set_xlim(-0.15, 2.75)
    ax.set_ylim(-2.55, 2.55)
    ax.set_xticks([0, 1, 2], [r"$F$", r"$W_RF$", r"$W_R^2F$"])
    ax.set_yticks([-2, -1, 0, 1, 2], [r"$-2R$", r"$-R$", "0", r"$R$", r"$2R$"])
    ax.set_title("Exact first leakage beyond three modes", loc="left", pad=6)
    ax.set_ylabel("Fourier index")
    ax.legend(frameon=False, loc="upper left", handletextpad=0.4)
    ax.text(0.97, 0.56, r"$\|\mathrm{outside}\|/\|\mathrm{inside}\|=1/\sqrt{2}$", transform=ax.transAxes, ha="right", fontsize=7.0, color=palette["ink"], bbox={"facecolor": palette["paper"], "edgecolor": "none", "alpha": 0.88, "pad": 1.0})
    ax.text(0.97, 0.43, "no finite support is invariant", transform=ax.transAxes, ha="right", fontsize=6.2, color=palette["ochre"], bbox={"facecolor": palette["paper"], "edgecolor": "none", "alpha": 0.88, "pad": 1.0})
    ax.text(0.97, 0.08, r"$\varepsilon/\varepsilon_{\max}>1$: unresolved", transform=ax.transAxes, ha="right", fontsize=6.3, color=palette["muted"], bbox={"facecolor": palette["paper"], "edgecolor": palette["muted"], "linewidth": 0.5, "pad": 2.0})

    fig.savefig(ROOT / "figure.pdf", facecolor=palette["paper"])
    fig.savefig(ROOT / "figure.svg", facecolor=palette["paper"])
    svg_path = ROOT / "figure.svg"
    svg_path.write_text("\n".join(line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines()) + "\n", encoding="utf-8")
    fig.savefig(ROOT / "figure.png", dpi=int(config["figure"]["pngDpi"]), facecolor=palette["paper"])
    plt.close(fig)


def main() -> int:
    started = time.perf_counter()
    progress_path = ROOT / "progress.ndjson"
    resource_path = ROOT / "resource-log.ndjson"
    progress_path.write_text("", encoding="utf-8")
    resource_path.write_text("", encoding="utf-8")
    append_ndjson(progress_path, {"time": utc_now(), "event": "figure_build_start"})
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    rows, summary, source_paths = prepare_data(config)
    write_data(rows)
    append_ndjson(progress_path, {"time": utc_now(), "event": "data_prepared", "rows": len(rows), "summary": summary})
    draw_figure(rows, config, summary)
    elapsed = time.perf_counter() - started
    output_hashes = {name: sha256(ROOT / name) for name in ("data.csv", "figure.pdf", "figure.svg", "figure.png")}
    source_hashes = {str(path.relative_to(REPOSITORY)): sha256(path) for path in source_paths}
    results = {
        "schemaVersion": 1,
        "figureId": "R0.72L-1",
        "status": "built",
        "generatedAt": utc_now(),
        "summary": summary,
        "outputSha256": output_hashes,
        "sourceSha256": source_hashes,
        "elapsedSeconds": elapsed,
        "maxRssMb": rss_mb(),
        "newPdeEvolution": False,
        "finiteProjectedOdeOnly": True,
    }
    (ROOT / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    environment = {
        "generatedAt": utc_now(),
        "python": sys.version.replace("\n", " "),
        "matplotlib": mpl.__version__,
        "numpy": np.__version__,
        "platform": platform.platform(),
        "cpuCount": os.cpu_count(),
        "maxRssMb": rss_mb(),
    }
    (ROOT / "environment.txt").write_text("\n".join(f"{key}={value}" for key, value in environment.items()) + "\n", encoding="utf-8")
    append_ndjson(resource_path, {"time": utc_now(), "elapsedSeconds": elapsed, "maxRssMb": rss_mb(), "rows": len(rows)})
    append_ndjson(progress_path, {"time": utc_now(), "event": "figure_build_complete", "elapsedSeconds": elapsed, "outputs": output_hashes})
    print(json.dumps({"status": "built", "rows": len(rows), "elapsedSeconds": elapsed, "summary": summary}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
