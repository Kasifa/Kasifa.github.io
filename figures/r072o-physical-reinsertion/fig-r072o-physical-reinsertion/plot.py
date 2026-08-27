#!/usr/bin/env python3
"""Build the R0.72O physical-reinsertion journal figure.

The dense curves evaluate formulas stated in the analytic report. Producer
and independent certificate rows appear only as exact-arithmetic audit
anchors. This script does not solve a PDE, regress an exponent, or infer an
unconditional multi-carrier theorem.
"""

from __future__ import annotations

import csv
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import resource
import sys
import time
from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np


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


def max_rss_mb() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024.0 * 1024.0) if sys.platform == "darwin" else value / 1024.0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def as_float(row: dict[str, str], key: str) -> float:
    value = float(row[key])
    if not math.isfinite(value):
        raise ValueError(f"non-finite {key} in {row}")
    return value


def append_ndjson(path: Path, value: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(value, sort_keys=True) + "\n")


def expected_key(row: dict[str, str]) -> tuple[int, str, float]:
    return (int(row["R"]), row["regime"], float(row["level"]))


def validate_inputs(
    config: dict[str, Any],
) -> tuple[
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
    dict[str, Any],
]:
    certificate = REPOSITORY / config["certificateDirectory"]
    names = config["certificates"]
    producer = read_csv(certificate / names["producerWindow"])
    independent = read_csv(certificate / names["independentWindow"])
    producer_deg = read_csv(certificate / names["producerDegeneracy"])
    independent_deg = read_csv(certificate / names["independentDegeneracy"])
    crosscheck = json.loads(
        (certificate / names["crosscheck"]).read_text(encoding="utf-8")
    )
    expected = {
        (r_value, regime, float(level))
        for r_value in config["expectedR"]
        for regime in ("oneCarrier", "worstCommonBand")
        for level in config["expectedLevels"]
    }
    if {expected_key(row) for row in producer} != expected:
        raise RuntimeError("producer window grid differs from the figure contract")
    if {expected_key(row) for row in independent} != expected:
        raise RuntimeError("independent window grid differs from the figure contract")
    if [expected_key(row) for row in producer] != [expected_key(row) for row in independent]:
        raise RuntimeError("producer and independent window row order differs")
    if [int(row["R"]) for row in producer_deg] != config["expectedR"]:
        raise RuntimeError("producer degeneracy grid differs from the figure contract")
    if [int(row["R"]) for row in independent_deg] != config["expectedR"]:
        raise RuntimeError("independent degeneracy grid differs from the figure contract")
    if crosscheck.get("status") != "passed":
        raise RuntimeError("R0.72O producer-independent crosscheck did not pass")
    tolerance = float(config["validation"]["crossRouteRelativeTolerance"])
    if any(float(value) > tolerance for value in crosscheck["maximumRelativeDifferences"].values()):
        raise RuntimeError("R0.72O crosscheck exceeds the figure tolerance")
    return producer, independent, producer_deg, independent_deg, crosscheck


def l_r(r_value: np.ndarray | float) -> np.ndarray | float:
    return 1.0 + np.log(r_value)


def l_repsilon(r_value: np.ndarray | float, epsilon: np.ndarray | float) -> np.ndarray | float:
    return 1.0 + np.log(2.0 + r_value * r_value * (1.0 + epsilon))


def z_exact(r_value: float, epsilon: np.ndarray, p_value: float = 1.0) -> np.ndarray:
    return (
        epsilon**2
        * p_value**2
        * r_value ** (2.0 / 3.0)
        * (1.0 + epsilon) ** (-2.0 / 3.0)
        * l_repsilon(r_value, epsilon)
    )


def set_surface(ax: mpl.axes.Axes, config: dict[str, Any]) -> None:
    palette = config["palette"]
    ax.set_facecolor(palette["paper"])
    ax.grid(True, which="major", color=palette["grid"], linewidth=0.55, alpha=0.8)
    ax.grid(True, which="minor", color=palette["grid"], linewidth=0.35, alpha=0.35)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(palette["muted"])
        ax.spines[side].set_linewidth(0.65)
    ax.tick_params(axis="both", which="both", colors=palette["ink"], labelsize=7.0)


def panel_title(ax: mpl.axes.Axes, letter: str, title: str, subtitle: str, config: dict[str, Any]) -> None:
    palette = config["palette"]
    ax.text(
        -0.02,
        1.095,
        letter,
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=11.0,
        fontweight="bold",
        color=palette["ink"],
    )
    ax.text(
        0.0,
        1.095,
        title,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9.2,
        fontweight="bold",
        color=palette["ink"],
    )
    ax.text(
        0.0,
        1.025,
        subtitle,
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=6.7,
        color=palette["muted"],
    )


def research_blossom(fig: mpl.figure.Figure, config: dict[str, Any]) -> None:
    palette = config["palette"]
    ax = fig.add_axes([0.925, 0.902, 0.055, 0.065], zorder=20)
    ax.set_axis_off()
    angles = np.linspace(0.0, 2.0 * np.pi, 7)[:-1]
    for angle in angles:
        x = np.array([0.5, 0.5 + 0.34 * math.cos(angle)])
        y = np.array([0.5, 0.5 + 0.34 * math.sin(angle)])
        ax.plot(x, y, color=palette["ochre"], linewidth=0.8)
        ax.plot(
            [x[-1]],
            [y[-1]],
            marker="o",
            markersize=2.8,
            markerfacecolor=palette["paper"],
            markeredgecolor=palette["blue"],
            markeredgewidth=0.7,
        )
    ax.plot([0.5], [0.5], marker="o", markersize=3.2, color=palette["ink"])
    ax.set_xlim(0.05, 0.95)
    ax.set_ylim(0.05, 0.95)


def add_row(
    rows: list[dict[str, Any]],
    *,
    panel: str,
    route: str,
    series: str,
    kind: str,
    x: float,
    y: float,
    source: str,
    pointer: str,
    note: str,
    status: str,
    r_value: float | str = "",
    p_value: float | str = "",
    epsilon: float | str = "",
) -> None:
    for label, value in (("x", x), ("y", y)):
        if not math.isfinite(float(value)):
            raise ValueError(f"non-finite {label}: {value}")
    rows.append(
        {
            "panel": panel,
            "route": route,
            "series": series,
            "kind": kind,
            "x": f"{float(x):.17g}",
            "y": f"{float(y):.17g}",
            "R": r_value,
            "p": p_value,
            "epsilon": epsilon,
            "source": source,
            "pointer": pointer,
            "status": status,
            "note": note,
        }
    )


def main() -> None:
    started = time.perf_counter()
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    contract = json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))
    producer, independent, producer_deg, independent_deg, crosscheck = validate_inputs(config)
    progress = ROOT / "progress.ndjson"
    resources = ROOT / "resource-log.ndjson"
    progress.write_text("", encoding="utf-8")
    resources.write_text("", encoding="utf-8")
    append_ndjson(
        progress,
        {
            "time": utc_now(),
            "event": "start",
            "figureId": "fig-r072o-physical-reinsertion",
            "certificateRows": len(producer) + len(independent),
        },
    )

    palette = config["palette"]
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 8.0,
            "axes.labelcolor": palette["ink"],
            "text.color": palette["ink"],
            "figure.facecolor": palette["paper"],
            "savefig.facecolor": palette["paper"],
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "axes.unicode_minus": False,
        }
    )
    figure = config["figure"]
    width = float(figure["widthMillimetres"]) / 25.4
    height = float(figure["heightMillimetres"]) / 25.4
    fig = plt.figure(figsize=(width, height), facecolor=palette["paper"])
    grid = fig.add_gridspec(
        2,
        2,
        left=0.085,
        right=0.975,
        bottom=0.105,
        top=0.815,
        wspace=0.27,
        hspace=0.43,
    )
    axes = [fig.add_subplot(grid[index // 2, index % 2]) for index in range(4)]
    for ax in axes:
        set_surface(ax, config)
    rows: list[dict[str, Any]] = []

    # Panel A: old and ED one-carrier window scales.
    ax = axes[0]
    panel = config["panels"]["A"]
    r_grid = np.geomspace(panel["rMinimum"], panel["rMaximum"], panel["samples"])
    old_window = r_grid ** (2.0 / 3.0) * l_r(r_grid)
    ed_window = r_grid ** (4.0 / 3.0) * l_r(r_grid) ** 2
    ax.loglog(
        r_grid,
        old_window,
        color=palette["ink"],
        linewidth=1.35,
        linestyle="-.",
        label=r"old $R^{2/3}L_R$",
    )
    ax.loglog(
        r_grid,
        ed_window,
        color=palette["blue"],
        linewidth=1.8,
        label=r"ED $R^{4/3}L_R^2$",
    )
    for x_value, old_value, new_value in zip(r_grid, old_window, ed_window, strict=True):
        add_row(
            rows,
            panel="A",
            route="analytic algebra",
            series="old one-carrier window",
            kind="proved scale law",
            x=x_value,
            y=old_value,
            source=config["analyticSource"],
            pointer="(0.9) inherited R0.72L scale",
            status="unconditional one carrier",
            note="Unknown absolute theorem constant suppressed.",
            r_value=x_value,
        )
        add_row(
            rows,
            panel="A",
            route="analytic algebra",
            series="ED one-carrier window",
            kind="proved scale law",
            x=x_value,
            y=new_value,
            source=config["analyticSource"],
            pointer="(0.10)-(0.11)",
            status="unconditional one carrier",
            note="Polynomial-ray scale with unknown absolute constant suppressed.",
            r_value=x_value,
        )
    for route_name, route_rows, color, marker, fill in (
        ("producer audit", producer, palette["blue"], "o", palette["blue"]),
        ("independent audit", independent, palette["ochre"], "s", palette["paper"]),
    ):
        anchors = [
            row
            for row in route_rows
            if row["regime"] == "oneCarrier" and abs(float(row["level"]) - 1.0) < 1e-14
        ]
        xs = np.array([as_float(row, "R") for row in anchors])
        ys = np.array([as_float(row, "epsilon") for row in anchors])
        ax.scatter(
            xs,
            ys,
            s=20,
            marker=marker,
            facecolor=fill,
            edgecolor=color,
            linewidth=0.85,
            zorder=5,
            label=route_name,
        )
        for source_row, x_value, y_value in zip(anchors, xs, ys, strict=True):
            add_row(
                rows,
                panel="A",
                route=route_name,
                series="ED level-one audit anchor",
                kind="exact-arithmetic audit",
                x=x_value,
                y=y_value,
                source=f"research/certificates/r072o/{'producer' if route_name.startswith('producer') else 'independent'}-window.csv",
                pointer=f"R={int(x_value)}, regime=oneCarrier, level=1",
                status="corroboration",
                note="Coincident exact exponent audit; not a numerical theorem constant.",
                r_value=x_value,
                p_value=1.0,
                epsilon=y_value,
            )
    ax.set_xlabel(r"carrier scale $R$", fontsize=7.4)
    ax.set_ylabel(r"coupling-window scale", fontsize=7.4)
    ax.legend(loc="upper left", frameon=False, fontsize=6.25, handlelength=2.1, labelspacing=0.25)
    panel_title(
        ax,
        "A",
        "One-carrier window scales",
        "proved orders; absolute constants suppressed",
        config,
    )

    # Panel B: fixed-R algebra and the non-decaying boundary.
    ax = axes[1]
    panel = config["panels"]["B"]
    fixed_r = float(panel["fixedR"])
    epsilon_grid = np.geomspace(
        panel["epsilonMinimum"], panel["epsilonMaximum"], panel["samples"]
    )
    z_values = z_exact(fixed_r, epsilon_grid)
    denominator = 1.0 + z_values
    old_screen = epsilon_grid ** (7.0 / 3.0) / denominator
    ed_screen = epsilon_grid ** (11.0 / 6.0) / denominator
    ax.loglog(
        epsilon_grid,
        old_screen,
        color=palette["ink"],
        linestyle="-.",
        linewidth=1.25,
        label="old direct screen",
    )
    ax.loglog(
        epsilon_grid,
        ed_screen,
        color=palette["blue"],
        linewidth=1.8,
        label="ED direct screen",
    )
    ax.axhline(1.0, color=palette["muted"], linewidth=0.9, linestyle=":", label="scale-one guide")
    ymax = max(float(np.max(old_screen)), float(np.max(ed_screen)), 2.0)
    ax.axhspan(1.0, ymax * 1.2, color=palette["ochreLight"], alpha=0.32, zorder=-2)
    ax.text(
        0.97,
        0.93,
        r"fixed $R$: current bound eventually unpaid",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=6.25,
        color=palette["ochre"],
    )
    for x_value, old_value, new_value in zip(epsilon_grid, old_screen, ed_screen, strict=True):
        add_row(
            rows,
            panel="B",
            route="analytic algebra",
            series="old normalized direct screen",
            kind="scale diagnostic",
            x=x_value,
            y=old_value,
            source=config["analyticSource"],
            pointer="R0.72L (0.10) with R0.72O (0.7)",
            status="old one-carrier bound",
            note="Action-floor constant normalized to one; not an absolute theorem threshold.",
            r_value=fixed_r,
            p_value=1.0,
            epsilon=x_value,
        )
        add_row(
            rows,
            panel="B",
            route="analytic algebra",
            series="ED normalized direct screen",
            kind="scale diagnostic",
            x=x_value,
            y=new_value,
            source=config["analyticSource"],
            pointer="(0.4), (0.7), (3.8)",
            status="unconditional one-carrier upper-bound algebra",
            note="Action-floor constant normalized to one; fixed-R growth is a proof boundary.",
            r_value=fixed_r,
            p_value=1.0,
            epsilon=x_value,
        )
    for route_name, route_rows, color, marker, fill in (
        ("producer audit", producer, palette["blue"], "o", palette["blue"]),
        ("independent audit", independent, palette["ochre"], "s", palette["paper"]),
    ):
        anchors = [row for row in route_rows if int(row["R"]) == int(fixed_r) and row["regime"] == "oneCarrier"]
        xs = np.array([as_float(row, "epsilon") for row in anchors])
        ys = np.array([as_float(row, "edDirectNormalized") for row in anchors])
        ax.scatter(
            xs,
            ys,
            s=22,
            marker=marker,
            facecolor=fill,
            edgecolor=color,
            linewidth=0.85,
            zorder=5,
        )
        for source_row, x_value, y_value in zip(anchors, xs, ys, strict=True):
            add_row(
                rows,
                panel="B",
                route=route_name,
                series="ED fixed-R audit anchor",
                kind="finite exact-algebra audit",
                x=x_value,
                y=y_value,
                source=f"research/certificates/r072o/{'producer' if route_name.startswith('producer') else 'independent'}-window.csv",
                pointer=f"R={int(fixed_r)}, regime=oneCarrier, level={source_row['level']}",
                status="corroboration",
                note="Marker reads the committed audit row directly.",
                r_value=fixed_r,
                p_value=1.0,
                epsilon=x_value,
            )
    ax.set_ylim(bottom=min(float(np.min(ed_screen)), float(np.min(old_screen))) * 0.7, top=ymax * 1.2)
    ax.set_xlabel(r"coupling $\varepsilon$", fontsize=7.4)
    ax.set_ylabel(r"normalized direct screen (scale)", fontsize=7.4)
    ax.legend(loc="lower right", frameon=False, fontsize=6.3, handlelength=2.0, labelspacing=0.25)
    panel_title(
        ax,
        "B",
        rf"Fixed-geometry boundary ($R={int(fixed_r)}$)",
        r"ED improves the exponent but does not pay $\varepsilon\to\infty$",
        config,
    )

    # Panel C: proved one-carrier point versus conditional multi-carrier curve.
    ax = axes[2]
    panel = config["panels"]["C"]
    fixed_r_c = float(panel["fixedR"])
    p_min = fixed_r_c ** -0.5
    p_grid = np.geomspace(p_min, 1.0, panel["samples"])
    base_window = fixed_r_c ** (4.0 / 3.0) * float(l_r(fixed_r_c)) ** 2
    conditional_window = p_grid ** (4.0 / 3.0) * base_window
    ax.loglog(
        p_grid,
        conditional_window,
        color=palette["ochre"],
        linewidth=1.55,
        linestyle="--",
        label="multi-carrier, conditional on uniform full IED",
    )
    marker_indices = np.linspace(0, len(p_grid) - 1, 7, dtype=int)
    ax.scatter(
        p_grid[marker_indices],
        conditional_window[marker_indices],
        s=18,
        marker="s",
        facecolor=palette["paper"],
        edgecolor=palette["ochre"],
        linewidth=0.8,
        zorder=4,
    )
    ax.scatter(
        [1.0],
        [base_window],
        s=46,
        marker="o",
        facecolor=palette["blue"],
        edgecolor=palette["ink"],
        linewidth=0.65,
        zorder=7,
        label=r"$N=1,p=1$ proved",
    )
    ax.fill_between(p_grid, conditional_window * 0.72, conditional_window * 1.0, color=palette["ochreLight"], alpha=0.42, zorder=-2)
    ax.annotate(
        "unconditional only at the\ndeclared one-carrier point",
        xy=(1.0, base_window),
        xytext=(0.28, base_window * 0.48),
        fontsize=6.15,
        color=palette["blue"],
        arrowprops={"arrowstyle": "-", "color": palette["blue"], "linewidth": 0.7},
        ha="center",
    )
    for p_value, y_value in zip(p_grid, conditional_window, strict=True):
        add_row(
            rows,
            panel="C",
            route="conditional analytic implication",
            series="multi-carrier ED window",
            kind="conditional scale law",
            x=p_value,
            y=y_value,
            source=config["analyticSource"],
            pointer="(0.13)-(0.16)",
            status="conditional for N>1",
            note="Assumes integrated enhanced dissipation with constants uniform over the plotted full-superposition family.",
            r_value=fixed_r_c,
            p_value=p_value,
        )
    add_row(
        rows,
        panel="C",
        route="analytic theorem",
        series="proved one-carrier endpoint",
        kind="proved scale law",
        x=1.0,
        y=base_window,
        source=config["analyticSource"],
        pointer="(0.9)-(0.11)",
        status="unconditional N=1",
        note="The p=1 multi-carrier curve is not proved; only this N=1 point is unconditional.",
        r_value=fixed_r_c,
        p_value=1.0,
    )
    ax.set_xlabel(r"coherence parameter $p=\sqrt{N}/B$", fontsize=7.4)
    ax.set_ylabel(r"conditional ED window scale", fontsize=7.4)
    ax.legend(loc="upper left", frameon=False, fontsize=6.15, handlelength=2.0, labelspacing=0.3)
    panel_title(
        ax,
        "C",
        rf"Superposition status ($R={int(fixed_r_c)}$)",
        r"filled = proved one carrier; open/dashed = conditional for $N>1$",
        config,
    )

    # Panel D: exact flat critical point versus a Morse reference.
    ax = axes[3]
    panel = config["panels"]["D"]
    fixed_r_d = int(panel["fixedR"])
    theta = np.geomspace(panel["thetaMinimum"], panel["thetaMaximum"], panel["samples"]).astype(np.longdouble)
    r_long = np.longdouble(fixed_r_d)
    combined = np.sin(r_long * theta) - r_long / (r_long + 1.0) * np.sin((r_long + 1.0) * theta)
    degenerate = np.abs(combined) * 6.0 / (r_long * (2.0 * r_long + 1.0))
    morse = np.abs(1.0 - np.cos(r_long * theta)) * 2.0 / (r_long**2)
    theta_float = np.asarray(theta, dtype=float)
    degenerate_float = np.asarray(degenerate, dtype=float)
    morse_float = np.asarray(morse, dtype=float)
    ax.loglog(
        theta_float,
        degenerate_float,
        color=palette["blue"],
        linewidth=1.75,
        label=r"two-carrier flat point $\sim\theta^3$",
    )
    ax.loglog(
        theta_float,
        morse_float,
        color=palette["ink"],
        linewidth=1.25,
        linestyle="-.",
        label=r"Morse reference $\sim\theta^2$",
    )
    ax.text(0.70, 0.22, r"slope $3$", transform=ax.transAxes, fontsize=6.4, color=palette["blue"])
    ax.text(0.70, 0.68, r"slope $2$", transform=ax.transAxes, fontsize=6.4, color=palette["ink"])
    for x_value, deg_value, morse_value in zip(theta_float, degenerate_float, morse_float, strict=True):
        add_row(
            rows,
            panel="D",
            route="exact identity",
            series="two-carrier flat critical point",
            kind="exact theorem-applicability obstruction",
            x=x_value,
            y=deg_value,
            source=config["analyticSource"],
            pointer="(5.4)-(5.5)",
            status="unconditional exact identity",
            note="Leading coefficient normalized so the local cubic departure is theta^3.",
            r_value=fixed_r_d,
        )
        add_row(
            rows,
            panel="D",
            route="analytic reference",
            series="Morse quadratic reference",
            kind="comparison reference",
            x=x_value,
            y=morse_value,
            source=config["analyticSource"],
            pointer="Section 5.2 comparison",
            status="reference",
            note="Leading coefficient normalized so the nondegenerate departure is theta^2.",
            r_value=fixed_r_d,
        )
    ax.set_xlabel(r"distance from the critical point $|\theta|$", fontsize=7.4)
    ax.set_ylabel(r"normalized profile departure", fontsize=7.4)
    ax.legend(loc="upper left", frameon=False, fontsize=6.25, handlelength=2.1, labelspacing=0.3)
    panel_title(
        ax,
        "D",
        rf"Common band need not be Morse ($R={fixed_r_d}$)",
        r"exact two-carrier obstruction: $U'(0)=U''(0)=0$",
        config,
    )

    fig.text(
        0.085,
        0.952,
        "PHYSICAL REINSERTION AND THE STRONG-COUPLING BOUNDARY",
        ha="left",
        va="top",
        fontsize=12.1,
        fontweight="bold",
        color=palette["ink"],
    )
    fig.text(
        0.085,
        0.910,
        r"The $\varepsilon^{1/2}$ raw gain becomes $\varepsilon^{11/6}$ after the physical lift; one carrier closes a larger window, not fixed-$R$ infinity.",
        ha="left",
        va="top",
        fontsize=7.25,
        color=palette["muted"],
    )
    fig.text(
        0.085,
        0.036,
        "Blue/filled: proved one-carrier statement. Ochre/open/dashed: conditional multi-carrier implication or audit. "
        "Scale curves suppress unknown absolute constants; no fitted exponents.",
        ha="left",
        va="bottom",
        fontsize=6.15,
        color=palette["muted"],
    )
    research_blossom(fig, config)

    fieldnames = [
        "panel",
        "route",
        "series",
        "kind",
        "x",
        "y",
        "R",
        "p",
        "epsilon",
        "source",
        "pointer",
        "status",
        "note",
    ]
    with (ROOT / "data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    append_ndjson(
        progress,
        {
            "time": utc_now(),
            "event": "data-ready",
            "rows": len(rows),
            "panels": {panel_name: sum(row["panel"] == panel_name for row in rows) for panel_name in "ABCD"},
        },
    )

    pdf_metadata = {
        "Title": contract["title"],
        "Author": "Kasifa Navier-Stokes research log",
        "Subject": contract["supportedTakeaway"],
        "Keywords": "Navier-Stokes, enhanced dissipation, physical reinsertion, strong coupling",
    }
    svg_metadata = {
        "Title": contract["title"],
        "Creator": "Kasifa Navier-Stokes research log",
        "Description": contract["supportedTakeaway"],
        "Keywords": [
            "Navier-Stokes",
            "enhanced dissipation",
            "physical reinsertion",
            "strong coupling",
        ],
    }
    fig.savefig(ROOT / "figure.pdf", metadata=pdf_metadata)
    fig.savefig(ROOT / "figure.svg", metadata=svg_metadata)
    fig.savefig(ROOT / "figure.png", dpi=int(figure["pngDpi"]), metadata={"Software": "Matplotlib"})
    plt.close(fig)

    elapsed = time.perf_counter() - started
    package_sources = [
        "README.md",
        "caption.md",
        "figure-contract.md",
        "contract.json",
        "config.json",
        "plot.py",
    ]
    certificate = REPOSITORY / config["certificateDirectory"]
    certificate_sources = [certificate / name for name in config["certificates"].values()]
    results = {
        "schemaVersion": "r072o-figure-results-v1",
        "figureId": "fig-r072o-physical-reinsertion",
        "status": "passed",
        "rowCount": len(rows),
        "panelRowCounts": {panel_name: sum(row["panel"] == panel_name for row in rows) for panel_name in "ABCD"},
        "certificateWindowRowsPerRoute": len(producer),
        "certificateDegeneracyRowsPerRoute": len(producer_deg),
        "crosscheckStatus": crosscheck["status"],
        "maximumRelativeDifferences": crosscheck["maximumRelativeDifferences"],
        "oldWindowAtRMaximum": float(old_window[-1]),
        "edWindowAtRMaximum": float(ed_window[-1]),
        "fixedR": int(fixed_r),
        "fixedRLastOldScreen": float(old_screen[-1]),
        "fixedRLastEdScreen": float(ed_screen[-1]),
        "conditionalCurveOnlyForMultiCarrier": True,
        "provedOneCarrierPoint": {"R": int(fixed_r_c), "p": 1.0, "windowScale": float(base_window)},
        "degeneracyThirdDerivative": fixed_r_d * (2 * fixed_r_d + 1),
        "noPdeEvolution": True,
        "noFiniteFit": True,
        "formulaCurvesNotCertificateInterpolation": True,
        "elapsedSeconds": elapsed,
        "maxRssMb": max_rss_mb(),
        "sourceHashes": {
            str(path.relative_to(REPOSITORY)): sha256(path)
            for path in [REPOSITORY / config["analyticSource"], REPOSITORY / config["gapSource"], *certificate_sources]
        },
        "packageSourceHashes": {name: sha256(ROOT / name) for name in package_sources},
    }
    (ROOT / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    environment = (
        f"Python {platform.python_version()}\n"
        f"Matplotlib {mpl.__version__}\n"
        f"NumPy {np.__version__}\n"
        f"Platform {platform.platform()}\n"
    )
    (ROOT / "environment.txt").write_text(environment, encoding="utf-8")
    append_ndjson(
        resources,
        {
            "time": utc_now(),
            "event": "complete",
            "rows": len(rows),
            "elapsedSeconds": elapsed,
            "maxRssMb": max_rss_mb(),
            "pid": os.getpid(),
        },
    )
    append_ndjson(
        progress,
        {
            "time": utc_now(),
            "event": "complete",
            "status": "passed",
            "rows": len(rows),
            "elapsedSeconds": elapsed,
        },
    )
    print(
        json.dumps(
            {
                "figure": "R0.72O physical reinsertion",
                "status": "passed",
                "rows": len(rows),
                "outputs": ["figure.pdf", "figure.svg", "figure.png"],
                "elapsedSeconds": elapsed,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
