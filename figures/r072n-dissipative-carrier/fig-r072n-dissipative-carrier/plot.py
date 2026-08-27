#!/usr/bin/env python3
"""Build the formal R0.72N dissipative one-carrier figure from certificates."""

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
from typing import Any

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
COMMON_REQUIRED_COLUMNS = {
    "sigma",
    "steps",
    "maxMoment",
    "momentBarrier",
    "momentOverBarrier",
    "momentRefinementRelativeDifference",
    "action",
    "scaledAction",
    "actionRefinementRelativeDifference",
    "liftedAction",
    "kProxy",
    "actionPoorRatio",
    "tProxy",
    "tOverV",
    "cubic",
    "cubicOverLogSigma",
    "cubicOverSqrtSigma",
    "cubicRefinementRelativeDifference",
    "finalMass",
    "passed",
}
ROUTE_REQUIRED_COLUMNS = {
    "producer": {"grid", "maxHighModeMass"},
    "independent": {"nmax", "boundaryMass"},
}
DATA_FIELDS = (
    "panel",
    "route",
    "series",
    "kind",
    "x",
    "y",
    "source",
    "pointer",
    "note",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def max_rss_mb() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024.0 * 1024.0) if sys.platform == "darwin" else value / 1024.0


def append_ndjson(path: Path, payload: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def read_certificate(path: Path, route: str) -> list[dict[str, str]]:
    if not path.is_file():
        raise FileNotFoundError(f"certificate CSV missing: {path}")
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or ())
        missing = sorted(
            (COMMON_REQUIRED_COLUMNS | ROUTE_REQUIRED_COLUMNS[route]) - columns
        )
        if missing:
            raise ValueError(f"certificate CSV {path.name} lacks columns: {missing}")
        rows = list(reader)
    if not rows:
        raise ValueError(f"certificate CSV is empty: {path}")
    return rows


def add_row(
    rows: list[dict[str, Any]],
    panel: str,
    route: str,
    series: str,
    kind: str,
    x_value: float,
    y_value: float,
    source: str,
    pointer: str,
    note: str,
) -> None:
    rows.append(
        {
            "panel": panel,
            "route": route,
            "series": series,
            "kind": kind,
            "x": x_value,
            "y": y_value,
            "source": source,
            "pointer": pointer,
            "note": note,
        }
    )


def prepare_data(
    config: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any], list[Path]]:
    rows: list[dict[str, Any]] = []
    certificate_root = REPOSITORY / config["certificateDirectory"]
    certificate_names = config["certificates"]
    crosscheck_path = certificate_root / certificate_names["crosscheck"]
    if not crosscheck_path.is_file():
        raise FileNotFoundError(f"certificate crosscheck missing: {crosscheck_path}")
    crosscheck = json.loads(crosscheck_path.read_text(encoding="utf-8"))
    if crosscheck.get("status") != "passed":
        raise RuntimeError("R0.72N certificate crosscheck must pass before plotting")

    route_rows: dict[str, list[dict[str, str]]] = {}
    for route in ("producer", "independent"):
        route_rows[route] = read_certificate(
            certificate_root / certificate_names[route], route
        )

    expected_sigmas = [float(value) for value in config["expectedSigmas"]]
    for route, values in route_rows.items():
        actual = [float(row["sigma"]) for row in values]
        if actual != expected_sigmas:
            raise ValueError(
                f"{route} sigma grid differs: actual={actual}, expected={expected_sigmas}"
            )

    sigma_min, sigma_max = expected_sigmas[0], expected_sigmas[-1]
    analytic_source = str(config["analyticSource"])
    panel_a_samples = int(config["panels"]["A"]["analyticSamples"])
    for index, sigma in enumerate(
        np.geomspace(sigma_min, sigma_max, panel_a_samples)
    ):
        add_row(
            rows,
            "A",
            "analytic theorem",
            "moment barrier",
            "theorem",
            float(sigma),
            max(1.0, (2.0 * float(sigma)) ** (2.0 / 3.0)),
            analytic_source,
            f"equation (1.7), sample {index}",
            "rigorous full-infinite-chain upper barrier",
        )

    for route, values in route_rows.items():
        source = str(
            (
                certificate_root / certificate_names[route]
            ).relative_to(REPOSITORY)
        )
        for value in values:
            sigma = float(value["sigma"])
            add_row(
                rows,
                "A",
                route,
                "D max",
                "finite diagnostic",
                sigma,
                float(value["maxMoment"]),
                source,
                "maxMoment",
                "finite maximum modal moment",
            )
            add_row(
                rows,
                "B",
                route,
                "scaled action",
                "finite diagnostic",
                sigma,
                float(value["scaledAction"]),
                source,
                "scaledAction",
                "finite normalized proxy sigma^(2/3) A_sigma / log sigma; mu=a=1",
            )
            add_row(
                rows,
                "B",
                route,
                "action-poor proxy",
                "finite diagnostic",
                sigma,
                float(value["actionPoorRatio"]),
                source,
                "actionPoorRatio",
                "finite normalized proxy sigma^(1/3) x_proxy/K_proxy with x_proxy=sigma^2 A and K_proxy=1+Dmax; mu=a=1 and fixed geometry constants suppressed",
            )
            add_row(
                rows,
                "C",
                route,
                "T_proxy/V_proxy",
                "finite diagnostic",
                sigma,
                float(value["tOverV"]),
                source,
                "tOverV",
                "finite normalized proxy T_proxy/V_proxy with U_proxy=sigma^(7/3), V_proxy=sigma^(1/3), x_proxy=sigma^2 A, and K_proxy=1+Dmax",
            )
            add_row(
                rows,
                "D",
                route,
                "C/log sigma",
                "finite diagnostic",
                sigma,
                float(value["cubicOverLogSigma"]),
                source,
                "cubicOverLogSigma",
                "finite near-logarithmic diagnostic; no logarithmic theorem",
            )
            add_row(
                rows,
                "D",
                route,
                "C/sqrt sigma",
                "finite diagnostic",
                sigma,
                float(value["cubicOverSqrtSigma"]),
                source,
                "cubicOverSqrtSigma",
                "finite mu=a=1 normalization controlled uniformly by the project corollary derived from Coble–He Theorem 1.2",
            )

    ceiling = float(config["panels"]["C"]["ceiling"])
    for index, sigma in enumerate((sigma_min, sigma_max)):
        add_row(
            rows,
            "C",
            "analytic theorem",
            "exact ceiling",
            "theorem",
            sigma,
            ceiling,
            analytic_source,
            f"equations (0.9)-(0.10), endpoint {index}",
            "exact algebraic ceiling for the scalar definition; finite markers use T_proxy/V_proxy",
        )

    source_paths = [
        REPOSITORY / config["analyticSource"],
        ROOT / "README.md",
        ROOT / "caption.md",
        ROOT / "figure-contract.md",
        ROOT / "contract.json",
        ROOT / "config.json",
        ROOT / "plot.py",
        certificate_root / certificate_names["producer"],
        certificate_root / certificate_names["independent"],
        crosscheck_path,
    ]
    summary = {
        "rowCount": len(rows),
        "certificateRowCount": sum(len(value) for value in route_rows.values()),
        "sigmaCountPerRoute": len(expected_sigmas),
        "sigmaMinimum": sigma_min,
        "sigmaMaximum": sigma_max,
        "strictMomentBarrierPlotted": True,
        "exactScalarCeilingPlotted": True,
        "projectCubicSqrtCorollary": "derived from Coble–He Theorem 1.2",
        "logarithmicCubicDiagnosticOnly": True,
        "finiteFitPlotted": False,
        "crosscheckStatus": crosscheck["status"],
        "maximumRelativeDifferences": crosscheck.get(
            "maximumRelativeDifferences", {}
        ),
        "producerLast": {
            field: float(route_rows["producer"][-1][field])
            for field in (
                "maxMoment",
                "scaledAction",
                "actionPoorRatio",
                "tOverV",
                "cubicOverLogSigma",
                "cubicOverSqrtSigma",
            )
        },
        "independentLast": {
            field: float(route_rows["independent"][-1][field])
            for field in (
                "maxMoment",
                "scaledAction",
                "actionPoorRatio",
                "tOverV",
                "cubicOverLogSigma",
                "cubicOverSqrtSigma",
            )
        },
    }
    return rows, summary, source_paths


def write_data(rows: list[dict[str, Any]]) -> None:
    with (ROOT / "data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=DATA_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def selected(
    rows: list[dict[str, Any]], panel: str, route: str, series: str
) -> list[dict[str, Any]]:
    return sorted(
        (
            row
            for row in rows
            if row["panel"] == panel
            and row["route"] == route
            and row["series"] == series
        ),
        key=lambda row: float(row["x"]),
    )


def style_axes(ax: mpl.axes.Axes, palette: dict[str, str]) -> None:
    ax.set_facecolor(palette["paper"])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(palette["muted"])
    ax.spines["bottom"].set_color(palette["muted"])
    ax.tick_params(
        colors=palette["ink"], labelsize=6.7, length=2.4, width=0.6
    )
    ax.grid(True, color=palette["grid"], linewidth=0.45, alpha=0.72)
    ax.set_axisbelow(True)


def panel_label(
    ax: mpl.axes.Axes, label: str, palette: dict[str, str]
) -> None:
    ax.text(
        -0.105,
        1.02,
        label,
        transform=ax.transAxes,
        fontsize=10,
        fontweight="bold",
        color=palette["ink"],
        va="bottom",
    )


def plot_points(
    ax: mpl.axes.Axes,
    points: list[dict[str, Any]],
    *,
    color: str,
    linestyle: str,
    marker: str,
    open_marker: bool,
    label: str,
    paper: str,
    linewidth: float = 1.12,
) -> None:
    ax.plot(
        [float(point["x"]) for point in points],
        [float(point["y"]) for point in points],
        color=color,
        linestyle=linestyle,
        linewidth=linewidth,
        marker=marker,
        markersize=3.35,
        markerfacecolor=paper if open_marker else color,
        markeredgecolor=color,
        markeredgewidth=0.75,
        label=label,
    )


def draw(
    rows: list[dict[str, Any]],
    config: dict[str, Any],
    summary: dict[str, Any],
) -> None:
    palette = config["palette"]
    width = float(config["figure"]["widthMillimetres"]) / 25.4
    height = float(config["figure"]["heightMillimetres"]) / 25.4
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 7.4,
            "axes.titlesize": 8.0,
            "axes.labelsize": 7.2,
            "legend.fontsize": 5.9,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )
    fig, axes = plt.subplots(
        2, 2, figsize=(width, height), constrained_layout=False
    )
    fig.patch.set_facecolor(palette["paper"])
    fig.subplots_adjust(
        left=0.085,
        right=0.975,
        bottom=0.105,
        top=0.84,
        wspace=0.34,
        hspace=0.50,
    )
    fig.suptitle(
        "Dissipative one-carrier barriers and finite diagnostics",
        x=0.085,
        y=0.965,
        ha="left",
        fontsize=9.7,
        fontweight="bold",
        color=palette["ink"],
    )
    fig.text(
        0.085,
        0.912,
        "Dark marker-free lines are rigorous; colored markers are finite normalized proxies at mu=a=1; no finite fit is plotted",
        ha="left",
        fontsize=6.55,
        color=palette["muted"],
    )
    fig.text(
        0.965,
        0.955,
        "✦",
        ha="right",
        va="center",
        fontsize=10,
        color=palette["ochre"],
    )

    route_style = {
        "producer": (palette["blue"], "-", "o", False),
        "independent": (palette["ochre"], "--", "s", True),
    }

    ax = axes[0, 0]
    style_axes(ax, palette)
    panel_label(ax, "A", palette)
    theorem = selected(rows, "A", "analytic theorem", "moment barrier")
    ax.plot(
        [point["x"] for point in theorem],
        [point["y"] for point in theorem],
        color=palette["ink"],
        linestyle="-.",
        linewidth=1.25,
        label=r"theorem $\max\{1,(2\sigma)^{2/3}\}$",
        zorder=3,
    )
    for route, (color, linestyle, marker, open_marker) in route_style.items():
        plot_points(
            ax,
            selected(rows, "A", route, "D max"),
            color=color,
            linestyle=linestyle,
            marker=marker,
            open_marker=open_marker,
            label=f"{route} finite",
            paper=palette["paper"],
        )
    ax.set_xscale("log", base=2)
    ax.set_yscale("log", base=2)
    ax.set_title("Maximum modal moment and strict barrier", loc="left", pad=6)
    ax.set_xlabel(r"coupling $\sigma$")
    ax.set_ylabel(r"$D_{\max}$")
    ax.legend(frameon=False, loc="upper left", handlelength=2.3)
    ax.text(
        0.98,
        0.08,
        "full-chain theorem",
        transform=ax.transAxes,
        ha="right",
        fontsize=6.1,
        color=palette["ink"],
    )

    ax = axes[0, 1]
    style_axes(ax, palette)
    panel_label(ax, "B", palette)
    for route, (color, route_line, marker, route_open) in route_style.items():
        plot_points(
            ax,
            selected(rows, "B", route, "scaled action"),
            color=color,
            linestyle=":" if route == "producer" else (0, (1, 1.6)),
            marker=marker,
            open_marker=True,
            label=f"{route}: scaled",
            paper=palette["paper"],
            linewidth=1.0,
        )
        plot_points(
            ax,
            selected(rows, "B", route, "action-poor proxy"),
            color=color,
            linestyle=route_line,
            marker=marker,
            open_marker=route_open,
            label=f"{route}: action-poor",
            paper=palette["paper"],
            linewidth=1.2,
        )
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_title("Critical-log action diagnostics", loc="left", pad=6)
    ax.set_xlabel(r"coupling $\sigma$")
    ax.set_ylabel(r"finite normalized proxy ($\mu=a=1$)")
    legend_handles = [
        Line2D(
            [0],
            [0],
            color=palette["blue"],
            marker="o",
            linestyle="None",
            markersize=4.0,
            label="producer",
        ),
        Line2D(
            [0],
            [0],
            color=palette["ink"],
            linestyle=":",
            linewidth=1.0,
            label="scaled action",
        ),
        Line2D(
            [0],
            [0],
            color=palette["ochre"],
            marker="s",
            markerfacecolor=palette["paper"],
            linestyle="None",
            markersize=4.0,
            label="independent",
        ),
        Line2D(
            [0],
            [0],
            color=palette["ink"],
            linestyle="-",
            linewidth=1.2,
            label="action-poor",
        ),
    ]
    ax.legend(
        handles=legend_handles,
        frameon=False,
        loc="upper left",
        ncol=2,
        handlelength=1.8,
        handletextpad=0.45,
        columnspacing=0.85,
    )
    ax.text(
        0.98,
        0.20,
        "actual theorem: ratio $\\gtrsim\\sigma\\log\\sigma$\nmarkers: finite normalized proxy",
        transform=ax.transAxes,
        ha="right",
        fontsize=5.95,
        color=palette["ink"],
    )

    ax = axes[1, 0]
    style_axes(ax, palette)
    panel_label(ax, "C", palette)
    for route, (color, linestyle, marker, open_marker) in route_style.items():
        plot_points(
            ax,
            selected(rows, "C", route, "T_proxy/V_proxy"),
            color=color,
            linestyle=linestyle,
            marker=marker,
            open_marker=open_marker,
            label=f"{route} finite proxy",
            paper=palette["paper"],
        )
    ceiling = selected(rows, "C", "analytic theorem", "exact ceiling")
    ax.plot(
        [point["x"] for point in ceiling],
        [point["y"] for point in ceiling],
        color=palette["ink"],
        linestyle="-.",
        linewidth=1.2,
        label=r"exact algebraic ceiling $=1$",
    )
    ax.set_xscale("log", base=2)
    ax.set_ylim(0.0, 1.045)
    ax.set_title("Scalar danger-screen proxy", loc="left", pad=6)
    ax.set_xlabel(r"coupling $\sigma$")
    ax.set_ylabel(r"$T_{\rm proxy}/V_{\rm proxy}$")
    ax.legend(frameon=False, loc="lower right", handlelength=2.2)
    ax.text(
        0.04,
        0.72,
        "actual theorem: $T_\\sigma\\asymp V_\\sigma$\nmarkers: finite normalized proxy",
        transform=ax.transAxes,
        fontsize=5.95,
        color=palette["ink"],
    )

    ax = axes[1, 1]
    style_axes(ax, palette)
    panel_label(ax, "D", palette)
    for route, (color, route_line, marker, route_open) in route_style.items():
        plot_points(
            ax,
            selected(rows, "D", route, "C/log sigma"),
            color=color,
            linestyle=route_line,
            marker=marker,
            open_marker=route_open,
            label=f"{route}: C/log",
            paper=palette["paper"],
            linewidth=1.2,
        )
        plot_points(
            ax,
            selected(rows, "D", route, "C/sqrt sigma"),
            color=color,
            linestyle=":" if route == "producer" else (0, (1, 1.6)),
            marker=marker,
            open_marker=True,
            label=f"{route}: C/sqrt",
            paper=palette["paper"],
            linewidth=1.0,
        )
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_title("True-cubic finite normalizations", loc="left", pad=6)
    ax.set_xlabel(r"coupling $\sigma$")
    ax.set_ylabel(r"finite cubic normalization ($\mu=a=1$)")
    ax.legend(frameon=False, loc="lower left", ncol=2, handlelength=2.1)
    ax.text(
        0.98,
        0.91,
        "project corollary from Coble–He Theorem 1.2:\nC/sqrt is bounded; C/log is diagnostic only",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=5.9,
        color=palette["ink"],
    )

    for suffix in ("pdf", "svg"):
        fig.savefig(ROOT / f"figure.{suffix}", facecolor=palette["paper"])
    svg = ROOT / "figure.svg"
    svg.write_text(
        "\n".join(
            line.rstrip()
            for line in svg.read_text(encoding="utf-8").splitlines()
        )
        + "\n",
        encoding="utf-8",
    )
    fig.savefig(
        ROOT / "figure.png",
        dpi=int(config["figure"]["pngDpi"]),
        facecolor=palette["paper"],
    )
    plt.close(fig)


def main() -> None:
    started = time.perf_counter()
    progress = ROOT / "progress.ndjson"
    resources = ROOT / "resource-log.ndjson"
    progress.write_text("", encoding="utf-8")
    resources.write_text("", encoding="utf-8")
    append_ndjson(progress, {"time": utc_now(), "event": "start"})
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    rows, summary, sources = prepare_data(config)
    write_data(rows)
    append_ndjson(
        progress, {"time": utc_now(), "event": "data", "rows": len(rows)}
    )
    draw(rows, config, summary)
    output_hashes = {
        name: digest(ROOT / name)
        for name in ("data.csv", "figure.pdf", "figure.svg", "figure.png")
    }
    source_hashes = {
        str(path.relative_to(REPOSITORY)): digest(path) for path in sources
    }
    result = {
        "schemaVersion": 1,
        "figureId": "R0.72N-1",
        "status": "built",
        "generatedAt": utc_now(),
        "summary": summary,
        "sourceSha256": source_hashes,
        "outputSha256": output_hashes,
        "elapsedSeconds": time.perf_counter() - started,
        "maxRssMb": max_rss_mb(),
        "newPdeEvolution": False,
        "pdeTimeStepping": False,
        "finiteFitsPlotted": False,
        "logarithmicCubicDiagnosticOnly": True,
    }
    (ROOT / "results.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (ROOT / "environment.txt").write_text(
        f"python={sys.version.split()[0]}\n"
        f"platform={platform.platform()}\n"
        f"matplotlib={mpl.__version__}\n"
        f"numpy={np.__version__}\n"
        f"cpuCount={os.cpu_count()}\n",
        encoding="utf-8",
    )
    append_ndjson(
        resources,
        {
            "time": utc_now(),
            "event": "complete",
            "elapsedSeconds": result["elapsedSeconds"],
            "maxRssMb": result["maxRssMb"],
            "rows": len(rows),
        },
    )
    append_ndjson(
        progress,
        {"time": utc_now(), "event": "complete", "outputs": output_hashes},
    )
    print(
        json.dumps(
            {
                "status": "built",
                "rows": len(rows),
                "elapsedSeconds": result["elapsedSeconds"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
