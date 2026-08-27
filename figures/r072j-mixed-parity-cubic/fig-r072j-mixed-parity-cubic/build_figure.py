#!/usr/bin/env python3
"""Build the formal R0.72J mixed-parity cubic figure without rerunning ODEs."""

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
import matplotlib.ticker as mticker
import numpy as np
from matplotlib.patches import Ellipse


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rss_mb() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return float(value) / (1024.0 * 1024.0 if sys.platform == "darwin" else 1024.0)


def append(path: Path, payload: dict[str, Any]) -> None:
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
    source: str,
    pointer: str,
    auxiliary: float | str = "",
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
            "source": source,
            "pointer": pointer,
        }
    )


def cases_by_r(result: dict[str, Any]) -> dict[int, dict[str, Any]]:
    return {int(case["R"]): case for case in result["cases"]}


def prepare_rows(
    config: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any], list[Path]]:
    source_config = config["sourceCertificates"]
    producer_path = REPOSITORY / source_config["producerResult"]
    independent_path = REPOSITORY / source_config["independentResult"]
    crosscheck_path = REPOSITORY / source_config["crosscheck"]
    report_path = REPOSITORY / "research/r072j_report-source.md"
    producer = load_json(producer_path)
    independent = load_json(independent_path)
    crosscheck = load_json(crosscheck_path)
    for label, result in (
        ("producer", producer),
        ("independent", independent),
        ("crosscheck", crosscheck),
    ):
        if result.get("status") != "passed":
            raise RuntimeError(f"R0.72J {label} certificate did not pass")
    if not all(producer.get("checks", {}).values()):
        raise RuntimeError("producer result contains a failed check")
    if not all(independent.get("checks", {}).values()):
        raise RuntimeError("independent result contains a failed check")

    expected_r = [int(value) for value in config["expected"]["rValues"]]
    producer_cases = cases_by_r(producer)
    independent_cases = cases_by_r(independent)
    if sorted(producer_cases) != expected_r or sorted(independent_cases) != expected_r:
        raise RuntimeError("certificate R grids do not match the figure contract")

    rows: list[dict[str, Any]] = []
    graph_examples = [
        (1.0, 1.0, "{2,6} / gcd 2 -> {1,3}", "bipartite"),
        (2.0, 0.0, "{1,4}", "non-bipartite; no triangle"),
        (3.0, 1.0, "S_R={R,...,3R-1}", "triangle-rich"),
    ]
    for x, y, label, status in graph_examples:
        add_row(
            rows,
            panel="A",
            route="exact classification",
            series=label,
            x=x,
            y=y,
            raw_value=y,
            auxiliary=status,
            source="research/r072j_report-source.md",
            pointer="residue-graph-classification",
        )

    for R in expected_r:
        p_case = producer_cases[R]
        i_case = independent_cases[R]
        exact_triples = 3.0 * R * (R + 1)
        exact_b0 = exact_triples / math.sqrt(2.0)
        for series, value, pointer in (
            ("signed triples T_R", exact_triples, "signedTriangleFormula"),
            ("aligned |b(0)|", exact_b0, "uncorrectedB0Formula"),
            ("R^2 reference", float(R * R), "exact reference"),
        ):
            add_row(
                rows,
                panel="B",
                route="exact",
                series=series,
                x=R,
                y=value,
                raw_value=value,
                auxiliary=(
                    p_case[pointer] if pointer in p_case else "unit coefficient"
                ),
                source=source_config["producerResult"],
                pointer=f"cases[R={R}].{pointer}",
            )
        for route, case, source in (
            ("producer", p_case, source_config["producerResult"]),
            ("independent", i_case, source_config["independentResult"]),
        ):
            add_row(
                rows,
                panel="C",
                route=route,
                series="true raw cubic",
                x=R,
                y=float(case["deltaIntegralAbsHB"]),
                raw_value=float(case["deltaIntegralAbsHB"]),
                auxiliary=float(case["criticalQ"]),
                source=source,
                pointer=f"cases[R={R}].deltaIntegralAbsHB",
            )
            add_row(
                rows,
                panel="D",
                route=route,
                series="physical normalized true cubic",
                x=R,
                y=float(case["normalizedTrueCubic"]),
                raw_value=float(case["normalizedTrueCubic"]),
                auxiliary=float(case["normalizedMeasuredBvUpperProxy"]),
                source=source,
                pointer=f"cases[R={R}].normalizedTrueCubic",
            )

    raw_tail_slope = float(producer["slopes"]["rawTrueCubicTail"])
    normalized_tail_slope = float(
        producer["slopes"]["normalizedTrueCubicTail"]
    )
    raw_tail_r = np.array(expected_r[-3:], dtype=np.float64)
    raw_tail_y = np.array(
        [producer_cases[R]["deltaIntegralAbsHB"] for R in expected_r[-3:]],
        dtype=np.float64,
    )
    raw_intercept = float(
        np.mean(np.log(raw_tail_y) - raw_tail_slope * np.log(raw_tail_r))
    )
    normalized_tail_y = np.array(
        [producer_cases[R]["normalizedTrueCubic"] for R in expected_r[-3:]],
        dtype=np.float64,
    )
    normalized_intercept = float(
        np.mean(
            np.log(normalized_tail_y)
            - normalized_tail_slope * np.log(raw_tail_r)
        )
    )
    guide_r = np.geomspace(expected_r[0], expected_r[-1], 64)
    last_raw = float(producer_cases[expected_r[-1]]["deltaIntegralAbsHB"])
    last_normalized = float(
        producer_cases[expected_r[-1]]["normalizedTrueCubic"]
    )
    for index, R in enumerate(guide_r):
        for panel, series, y, raw_value, pointer in (
            (
                "C",
                "R^2 guide",
                last_raw * (R / expected_r[-1]) ** 2.0,
                R**2,
                "R^2 shape anchored at largest R",
            ),
            (
                "C",
                f"tail fit R^{raw_tail_slope:.3f}",
                math.exp(raw_intercept) * R**raw_tail_slope,
                raw_tail_slope,
                "last-three-point producer log fit",
            ),
            (
                "D",
                "R^-2/3 guide",
                last_normalized * (R / expected_r[-1]) ** (-2.0 / 3.0),
                R ** (-2.0 / 3.0),
                "R^-2/3 shape anchored at largest R",
            ),
            (
                "D",
                f"tail fit R^{normalized_tail_slope:.3f}",
                math.exp(normalized_intercept) * R**normalized_tail_slope,
                normalized_tail_slope,
                "last-three-point producer log fit",
            ),
        ):
            add_row(
                rows,
                panel=panel,
                route="guide" if "guide" in series else "finite fit",
                series=series,
                x=float(R),
                y=float(y),
                raw_value=float(raw_value),
                auxiliary="not an independent theorem constant",
                source=source_config["producerResult"],
                pointer=f"{pointer}[{index}]",
            )
        analytic_envelope = (
            R ** (-4.0 / 9.0) * (1.0 + math.log(R)) ** (-2.0 / 3.0)
        )
        add_row(
            rows,
            panel="D",
            route="analytic theorem reference",
            series="R^-4/9 (1+log R)^-2/3",
            x=float(R),
            y=float(analytic_envelope),
            raw_value=float(analytic_envelope),
            auxiliary="not plotted on measured-value scale and not fitted",
            source="research/r072j_report-source.md",
            pointer=f"universal-envelope-reference[{index}]",
        )

    last_r = expected_r[-1]
    summary = {
        "rValues": expected_r,
        "producerStatus": producer["status"],
        "independentStatus": independent["status"],
        "crosscheckStatus": crosscheck["status"],
        "rawTailSlope": raw_tail_slope,
        "normalizedTailSlope": normalized_tail_slope,
        "largestR": last_r,
        "largestSignedTriangles": int(producer_cases[last_r]["signedTriangles"]),
        "largestAlignedB0": float(producer_cases[last_r]["uncorrectedB0Abs"]),
        "largestRawTrueCubic": float(
            producer_cases[last_r]["deltaIntegralAbsHB"]
        ),
        "largestNormalizedTrueCubic": float(
            producer_cases[last_r]["normalizedTrueCubic"]
        ),
        "largestProducerRootResidual": float(
            producer_cases[last_r]["evolvedRootResidual"]
        ),
        "largestIndependentRootResidual": float(
            independent_cases[last_r]["evolvedRootResidual"]
        ),
        "maximumTrueCubicCrossRelativeError": float(
            crosscheck["maximumRelativeErrors"]["deltaIntegralAbsHB"]
        ),
        "maximumCriticalQCrossRelativeError": float(
            crosscheck["maximumRelativeErrors"]["criticalQ"]
        ),
        "rowCount": len(rows),
    }
    return rows, summary, [
        producer_path,
        independent_path,
        crosscheck_path,
        report_path,
    ]


def write_data(rows: list[dict[str, Any]]) -> None:
    fields = [
        "panel",
        "route",
        "series",
        "x",
        "y",
        "rawValue",
        "auxiliary",
        "source",
        "pointer",
    ]
    with (ROOT / "data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def select(
    rows: list[dict[str, Any]],
    panel: str,
    series: str,
    route: str | None = None,
) -> list[dict[str, Any]]:
    result = [
        row
        for row in rows
        if row["panel"] == panel
        and row["series"] == series
        and (route is None or row["route"] == route)
    ]
    return sorted(result, key=lambda row: float(row["x"]))


def set_dyadic_ticks(ax: Any, values: list[int]) -> None:
    ax.set_xscale("log", base=2)
    ax.set_xticks(values, labels=[str(value) for value in values])
    ax.xaxis.set_minor_locator(mticker.NullLocator())


def draw_node(
    ax: Any,
    x: float,
    y: float,
    *,
    filled: bool,
    palette: dict[str, str],
    size: float = 22.0,
) -> None:
    ax.scatter(
        [x],
        [y],
        s=size,
        facecolor=palette["ink"] if filled else palette["paper"],
        edgecolor=palette["ink"],
        linewidth=0.75,
        zorder=4,
        clip_on=False,
    )


def draw_panel_a(ax: Any, palette: dict[str, str]) -> None:
    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)
    ax.axis("off")
    ax.set_title(
        "A  Gcd-reduced carrier graph",
        loc="left",
        fontweight="bold",
        pad=4.0,
    )
    ax.text(
        0.0,
        0.95,
        r"bipartite $\Longleftrightarrow$ every $r/\gcd(S)$ is odd",
        fontsize=6.1,
        color=palette["muted"],
        va="top",
    )

    line_x = np.linspace(0.05, 0.43, 6)
    line_y = 0.70
    for index in range(5):
        ax.plot(
            line_x[index : index + 2],
            [line_y, line_y],
            color=palette["ink"],
            linewidth=0.75,
            zorder=2,
        )
    for index in range(3):
        ax.plot(
            [line_x[index], line_x[index + 3]],
            [line_y + 0.008, line_y + 0.008],
            color=palette["blue"],
            linewidth=0.8,
            linestyle="--",
            zorder=2,
        )
    for index, x in enumerate(line_x):
        draw_node(ax, float(x), line_y, filled=index % 2 == 0, palette=palette)
    ax.text(0.50, 0.75, r"$\{2,6\}/2=\{1,3\}$", fontsize=6.2, va="center")
    ax.text(0.50, 0.66, "two-color split", fontsize=5.7, color=palette["muted"])

    center = np.array([0.23, 0.39])
    radius = 0.13
    angles = np.deg2rad(np.array([90, 18, -54, -126, 162], dtype=float))
    pentagon = np.column_stack(
        (center[0] + radius * np.cos(angles), center[1] + radius * np.sin(angles))
    )
    for index in range(5):
        next_index = (index + 1) % 5
        edge_color = palette["ochre"] if index == 4 else palette["ink"]
        ax.plot(
            [pentagon[index, 0], pentagon[next_index, 0]],
            [pentagon[index, 1], pentagon[next_index, 1]],
            color=edge_color,
            linewidth=1.0 if index == 4 else 0.75,
            zorder=2,
        )
    for index, (x, y) in enumerate(pentagon):
        draw_node(ax, float(x), float(y), filled=index % 2 == 0, palette=palette)
    ax.text(0.50, 0.43, r"$\{1,4\}$", fontsize=6.2, va="center")
    ax.text(0.50, 0.34, "5-cycle; no triangle", fontsize=5.7, color=palette["muted"])

    triangle = np.array([[0.10, 0.07], [0.38, 0.07], [0.24, 0.25]])
    for index in range(3):
        next_index = (index + 1) % 3
        ax.plot(
            [triangle[index, 0], triangle[next_index, 0]],
            [triangle[index, 1], triangle[next_index, 1]],
            color=palette["ochre"],
            linewidth=1.05,
            zorder=2,
        )
    for x, y in triangle:
        draw_node(ax, float(x), float(y), filled=False, palette=palette)
    ax.text(0.50, 0.17, r"$S_R=\{R,\ldots,3R-1\}$", fontsize=6.2, va="center")
    ax.text(
        0.50,
        0.08,
        r"triangle-rich: $R+R=2R$",
        fontsize=5.7,
        color=palette["muted"],
    )


def add_blossom(fig: Any, palette: dict[str, str]) -> None:
    blossom = fig.add_axes([0.918, 0.895, 0.045, 0.065], frameon=False)
    blossom.set_xlim(-1.1, 1.1)
    blossom.set_ylim(-1.1, 1.1)
    blossom.axis("off")
    for angle in (0, 90, 180, 270):
        theta = math.radians(angle)
        petal = Ellipse(
            (0.38 * math.cos(theta), 0.38 * math.sin(theta)),
            width=0.72,
            height=0.30,
            angle=angle,
            facecolor="none",
            edgecolor=palette["ochre"],
            linewidth=0.75,
        )
        blossom.add_patch(petal)
    blossom.scatter([0], [0], s=7, color=palette["ink"], zorder=4)


def render(
    rows: list[dict[str, Any]], config: dict[str, Any], summary: dict[str, Any]
) -> None:
    palette = config["palette"]
    width = config["figure"]["widthMillimetres"] / 25.4
    height = config["figure"]["heightMillimetres"] / 25.4
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 7.0,
            "axes.titlesize": 7.7,
            "axes.labelsize": 6.8,
            "xtick.labelsize": 6.0,
            "ytick.labelsize": 6.0,
            "legend.fontsize": 5.4,
            "axes.edgecolor": palette["ink"],
            "axes.linewidth": 0.7,
            "xtick.color": palette["ink"],
            "ytick.color": palette["ink"],
            "text.color": palette["ink"],
            "axes.labelcolor": palette["ink"],
            "figure.facecolor": palette["paper"],
            "axes.facecolor": palette["paper"],
            "savefig.facecolor": palette["paper"],
            "pdf.fonttype": 42,
            "svg.fonttype": "none",
        }
    )
    fig, axes = plt.subplots(2, 2, figsize=(width, height))
    fig.set_size_inches(width, height, forward=False)
    fig.subplots_adjust(
        left=0.085,
        right=0.965,
        bottom=0.135,
        top=0.82,
        wspace=0.31,
        hspace=0.49,
    )
    fig.suptitle(
        "Mixed-parity cubic audit: graph obstruction and physical scaling",
        x=0.085,
        y=0.965,
        ha="left",
        fontsize=9.7,
        fontweight="bold",
    )
    fig.text(
        0.085,
        0.915,
        r"$S_R=\{R,\ldots,3R-1\}$  |  $\delta=0.05R$  |  one complex root  |  producer + independent",
        ha="left",
        fontsize=6.4,
        color=palette["muted"],
    )
    add_blossom(fig, palette)

    draw_panel_a(axes[0, 0], palette)

    ax = axes[0, 1]
    panel_b_styles = {
        "signed triples T_R": (palette["ink"], "-", "o", True),
        "aligned |b(0)|": (palette["blue"], "--", "s", False),
        "R^2 reference": (palette["muted"], ":", None, False),
    }
    panel_b_labels = {
        "signed triples T_R": r"$T_R=3R(R+1)$",
        "aligned |b(0)|": r"$|b_0|=T_R/\sqrt{2}$",
        "R^2 reference": r"$R^2$",
    }
    for series, (color, linestyle, marker, filled) in panel_b_styles.items():
        points = select(rows, "B", series, "exact")
        ax.plot(
            [point["x"] for point in points],
            [point["y"] for point in points],
            color=color,
            linestyle=linestyle,
            marker=marker,
            markersize=3.2,
            markerfacecolor=color if filled else palette["paper"],
            markeredgecolor=color,
            markeredgewidth=0.75,
            linewidth=1.1,
            label=panel_b_labels[series],
        )
    set_dyadic_ticks(ax, summary["rValues"])
    ax.set_yscale("log")
    ax.set_xlabel("block scale $R$")
    ax.set_ylabel("exact count or coefficient")
    ax.set_title("B  Exact triangle coefficient", loc="left", fontweight="bold")
    ax.grid(True, which="both", color=palette["grid"], linewidth=0.45, alpha=0.78)
    ax.legend(frameon=False, loc="upper left", handlelength=1.8)

    ax = axes[1, 0]
    producer_points = select(rows, "C", "true raw cubic", "producer")
    independent_points = select(rows, "C", "true raw cubic", "independent")
    ax.plot(
        [point["x"] for point in producer_points],
        [point["y"] for point in producer_points],
        color=palette["blue"],
        linestyle="-",
        marker="o",
        markersize=3.5,
        markerfacecolor=palette["blue"],
        markeredgecolor=palette["blue"],
        linewidth=1.25,
        label="producer",
        zorder=3,
    )
    ax.plot(
        [point["x"] for point in independent_points],
        [point["y"] for point in independent_points],
        color=palette["ink"],
        linestyle="none",
        marker="s",
        markersize=3.5,
        markerfacecolor=palette["paper"],
        markeredgecolor=palette["ink"],
        markeredgewidth=0.8,
        label="independent",
        zorder=4,
    )
    guide = select(rows, "C", "R^2 guide", "guide")
    fit_series = f"tail fit R^{summary['rawTailSlope']:.3f}"
    fit = select(rows, "C", fit_series, "finite fit")
    ax.plot(
        [point["x"] for point in guide],
        [point["y"] for point in guide],
        color=palette["muted"],
        linestyle="--",
        linewidth=0.9,
        label=r"$R^2$ guide",
    )
    ax.plot(
        [point["x"] for point in fit],
        [point["y"] for point in fit],
        color=palette["ochre"],
        linestyle=":",
        linewidth=1.0,
        label=rf"tail fit $R^{{{summary['rawTailSlope']:.3f}}}$",
    )
    set_dyadic_ticks(ax, summary["rValues"])
    ax.set_yscale("log")
    ax.set_xlabel("block scale $R$")
    ax.set_ylabel(r"$\delta\int |hP_0V^2F|\,dx$")
    ax.set_title("C  True raw cubic is order $R^2$", loc="left", fontweight="bold")
    ax.grid(True, which="both", color=palette["grid"], linewidth=0.45, alpha=0.78)
    ax.legend(frameon=False, loc="upper left", ncol=2, handlelength=1.8, columnspacing=0.9)

    ax = axes[1, 1]
    producer_points = select(
        rows, "D", "physical normalized true cubic", "producer"
    )
    independent_points = select(
        rows, "D", "physical normalized true cubic", "independent"
    )
    ax.plot(
        [point["x"] for point in producer_points],
        [point["y"] for point in producer_points],
        color=palette["blue"],
        linestyle="-",
        marker="o",
        markersize=3.5,
        markerfacecolor=palette["blue"],
        markeredgecolor=palette["blue"],
        linewidth=1.25,
        label="producer",
        zorder=3,
    )
    ax.plot(
        [point["x"] for point in independent_points],
        [point["y"] for point in independent_points],
        color=palette["ink"],
        linestyle="none",
        marker="s",
        markersize=3.5,
        markerfacecolor=palette["paper"],
        markeredgecolor=palette["ink"],
        markeredgewidth=0.8,
        label="independent",
        zorder=4,
    )
    guide = select(rows, "D", "R^-2/3 guide", "guide")
    fit_series = f"tail fit R^{summary['normalizedTailSlope']:.3f}"
    fit = select(rows, "D", fit_series, "finite fit")
    ax.plot(
        [point["x"] for point in guide],
        [point["y"] for point in guide],
        color=palette["muted"],
        linestyle="--",
        linewidth=0.9,
        label=r"$R^{-2/3}$ guide",
    )
    ax.plot(
        [point["x"] for point in fit],
        [point["y"] for point in fit],
        color=palette["ochre"],
        linestyle=":",
        linewidth=1.0,
        label=rf"tail fit $R^{{{summary['normalizedTailSlope']:.3f}}}$",
    )
    set_dyadic_ticks(ax, summary["rValues"])
    ax.set_yscale("log")
    ax.set_xlabel("block scale $R$")
    ax.set_ylabel("physical normalized true cubic")
    ax.set_title("D  Physical normalization still decays", loc="left", fontweight="bold")
    ax.grid(True, which="both", color=palette["grid"], linewidth=0.45, alpha=0.78)
    ax.legend(frameon=False, loc="upper right", ncol=2, handlelength=1.7, columnspacing=0.8)
    ax.text(
        0.035,
        0.055,
        r"Universal theorem-rate reference:"
        "\n"
        r"$R^{-4/9}(1+\log R)^{-2/3}$ (not fitted)",
        transform=ax.transAxes,
        fontsize=5.4,
        color=palette["muted"],
        va="bottom",
        bbox={
            "boxstyle": "square,pad=0.18",
            "facecolor": palette["paper"],
            "edgecolor": palette["grid"],
            "linewidth": 0.45,
            "alpha": 0.92,
        },
    )

    fig.text(
        0.085,
        0.051,
        "Finite mixed-parity block | one complex root | no complete-root or general 3D claim.",
        fontsize=5.55,
        color=palette["muted"],
    )
    fig.text(
        0.965,
        0.051,
        "R0.72J | 2026-08-27",
        ha="right",
        fontsize=5.55,
        color=palette["muted"],
    )

    dpi = int(config["figure"]["pngDpi"])
    fig.savefig(ROOT / "figure.pdf")
    svg_path = ROOT / "figure.svg"
    fig.savefig(svg_path)
    svg_path.write_text(
        "\n".join(
            line.rstrip()
            for line in svg_path.read_text(encoding="utf-8").splitlines()
        )
        + "\n",
        encoding="utf-8",
    )
    fig.savefig(ROOT / "figure.png", dpi=dpi)
    plt.close(fig)


def main() -> None:
    started = time.perf_counter()
    progress_path = ROOT / "progress.ndjson"
    resource_path = ROOT / "resource-log.ndjson"
    progress_path.write_text("", encoding="utf-8")
    resource_path.write_text("", encoding="utf-8")
    append(progress_path, {"time": utc_now(), "event": "figure_build_start"})
    config = load_json(ROOT / "config.json")
    rows, summary, certificate_sources = prepare_rows(config)
    write_data(rows)
    render(rows, config, summary)
    contract = load_json(ROOT / "contract.json")
    results = {
        "schemaVersion": "r072j-figure-results-v1",
        "allRequiredSourceChecksPassed": True,
        "analyticalQuestion": (
            "How does failure of the residue two-color split affect the true "
            "cubic row in one triangle-rich carrier block?"
        ),
        "takeaway": (
            "The exact graph obstruction permits an order-R-squared raw cubic "
            "term, while the declared finite physical normalization still decays."
        ),
        "summary": summary,
        "claimBoundary": contract["claimBoundary"],
    }
    (ROOT / "results.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    source_files = certificate_sources + [ROOT / "config.json", ROOT / "contract.json"]
    metadata = {
        "schemaVersion": "r072j-figure-data-metadata-v1",
        "generatedAt": utc_now(),
        "sourceFiles": [
            {
                "path": str(path.relative_to(REPOSITORY)),
                "sha256": digest(path),
            }
            for path in source_files
        ],
        "rowCount": len(rows),
        "panels": ["A", "B", "C", "D"],
        "odeRecomputed": False,
        "independentOverlay": True,
    }
    (ROOT / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    environment = {
        "generatedAt": utc_now(),
        "python": sys.version,
        "platform": platform.platform(),
        "numpy": np.__version__,
        "matplotlib": mpl.__version__,
        "executable": sys.executable,
        "cpuCount": os.cpu_count(),
        "maxRssMb": rss_mb(),
    }
    (ROOT / "environment.txt").write_text(
        "\n".join(f"{key}={value}" for key, value in environment.items()) + "\n",
        encoding="utf-8",
    )
    elapsed = time.perf_counter() - started
    append(
        resource_path,
        {
            "time": utc_now(),
            "elapsedSeconds": elapsed,
            "maxRssMb": rss_mb(),
            "rowCount": len(rows),
            "odeRecomputed": False,
        },
    )
    append(
        progress_path,
        {
            "time": utc_now(),
            "event": "figure_build_complete",
            "elapsedSeconds": elapsed,
            "outputs": ["figure.pdf", "figure.svg", "figure.png"],
        },
    )
    print(json.dumps({"status": "built", "elapsedSeconds": elapsed, **summary}, sort_keys=True))


if __name__ == "__main__":
    main()
