#!/usr/bin/env python3
"""Build the formal R0.72I physical-absorption figure."""

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


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


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


def numeric(row: dict[str, str], key: str) -> float:
    if key not in row or row[key] == "":
        raise KeyError(f"missing required column {key!r}")
    return float(row[key])


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


def add_certificate_rows(
    plotted: list[dict[str, Any]],
    certificate_rows: list[dict[str, str]],
    *,
    route: str,
    source_path: str,
) -> None:
    if route == "producer":
        panel_a = {
            "initial trace": ("ratioFirstRoot", "liftedTermFirstRoot"),
            "target diagonal": ("ratioTargetDiagonal", "liftedTermTargetDiagonal"),
            "mixed moment": ("ratioMixedMoment", "liftedTermMixedMoment"),
            "generic B term": ("ratioGenericB", "liftedTermGenericB"),
        }
        panel_c = {
            "measured BV upper": ("measuredBvLiftedRatio", "measuredBvUpper"),
            "one exact-root atom": ("exactRootRatio", "exactRootPhysicalAtom"),
        }
        required = {
            "M",
            "genericBToMeasuredHB",
            "rawTermGenericB",
            "deltaIntegralAbsHB",
            *(pair[0] for pair in panel_a.values()),
            *(pair[1] for pair in panel_a.values()),
            *(pair[0] for pair in panel_c.values()),
            *(pair[1] for pair in panel_c.values()),
        }
    else:
        panel_a = {
            "initial trace": ("liftedFirstRatio", "liftedFirst"),
            "target diagonal": ("liftedLambdaRatio", "liftedLambda"),
            "mixed moment": ("liftedMixedRatio", "liftedMixed"),
            "generic B term": ("liftedGenericBRatio", "liftedGenericB"),
        }
        # The independent route did not store the h^2 integral needed to
        # reconstruct the measured BV upper ledger.  Its exact root atom is
        # nevertheless the same physical observable and is overlaid.
        panel_c = {
            "one exact-root atom": ("liftedRootAtomRatio", "liftedRootAtom"),
        }
        required = {
            "M",
            "liftedGenericB",
            "liftedMeasuredCubic",
            "deltaAbsHbIntegral",
            *(pair[0] for pair in panel_a.values()),
            *(pair[1] for pair in panel_a.values()),
            *(pair[0] for pair in panel_c.values()),
            *(pair[1] for pair in panel_c.values()),
        }
    if not certificate_rows or not required.issubset(certificate_rows[0]):
        missing = sorted(required - set(certificate_rows[0] if certificate_rows else {}))
        raise RuntimeError(f"{route} certificate CSV is missing {missing}")

    for index, item in enumerate(certificate_rows):
        M = int(numeric(item, "M"))
        for label, (ratio_key, raw_key) in panel_a.items():
            add_row(
                plotted,
                panel="A",
                route=route,
                series=label,
                x=M,
                y=numeric(item, ratio_key),
                raw_value=numeric(item, raw_key),
                source=source_path,
                pointer=f"row[{index}].{ratio_key}",
            )
        if route == "producer":
            generic_to_measured = numeric(item, "genericBToMeasuredHB")
            generic_raw = numeric(item, "rawTermGenericB")
            measured_raw = numeric(item, "deltaIntegralAbsHB")
            generic_pointer = "genericBToMeasuredHB"
        else:
            generic_to_measured = numeric(item, "liftedGenericB") / numeric(
                item, "liftedMeasuredCubic"
            )
            generic_raw = numeric(item, "liftedGenericB")
            measured_raw = numeric(item, "deltaAbsHbIntegral")
            generic_pointer = "liftedGenericB/liftedMeasuredCubic"
        add_row(
            plotted,
            panel="B",
            route=route,
            series="generic bound / measured cubic exposure",
            x=M,
            y=generic_to_measured,
            raw_value=generic_raw,
            auxiliary=measured_raw,
            source=source_path,
            pointer=f"row[{index}].{generic_pointer}",
        )
        for label, (ratio_key, raw_key) in panel_c.items():
            add_row(
                plotted,
                panel="C",
                route=route,
                series=label,
                x=M,
                y=numeric(item, ratio_key),
                raw_value=numeric(item, raw_key),
                source=source_path,
                pointer=f"row[{index}].{ratio_key}",
            )


def theoretical_ratio(M: float, g: float) -> float:
    coefficient = M ** (-7.0 / 3.0) * math.log(M)
    return g ** (4.0 / 3.0) * M**-2 / (1.0 + coefficient * g * g)


def add_theory_rows(rows: list[dict[str, Any]]) -> None:
    source = "research/r072i_report-source.md"
    m_grid = np.geomspace(4.0, 4096.0, 96)
    for index, M in enumerate(m_grid):
        coefficient = M ** (-7.0 / 3.0) * math.log(M)
        g_star = math.sqrt(2.0 / coefficient)
        g_scan = g_star * np.geomspace(1.0e-3, 1.0e3, 1201)
        values = np.array([theoretical_ratio(float(M), float(g)) for g in g_scan])
        numeric_max = float(np.max(values))
        analytic_max = (
            2.0 ** (2.0 / 3.0)
            / 3.0
            * M ** (-4.0 / 9.0)
            * math.log(M) ** (-2.0 / 3.0)
        )
        for series, value, raw, auxiliary in (
            ("numeric coupling envelope", numeric_max, g_star, coefficient),
            ("analytic M^(-4/9) log^(-2/3)", analytic_max, analytic_max, g_star),
            ("section g=M", theoretical_ratio(float(M), float(M)), M, coefficient),
            (
                "section g=M^(3/2)",
                theoretical_ratio(float(M), float(M ** 1.5)),
                M ** 1.5,
                coefficient,
            ),
        ):
            add_row(
                rows,
                panel="D",
                route="analytic" if series != "numeric coupling envelope" else "numeric maximization",
                series=series,
                x=float(M),
                y=float(value),
                raw_value=float(raw),
                auxiliary=float(auxiliary),
                source=source,
                pointer=f"coupling-envelope-grid[{index}]",
            )


def prepare_rows(config: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any], list[Path]]:
    sources = config["sourceCertificates"]
    producer_csv_path = REPOSITORY / sources["producerCsv"]
    producer_result_path = REPOSITORY / sources["producerResult"]
    producer_result = load_json(producer_result_path)
    if producer_result.get("status") != "passed" or not all(
        producer_result.get("checks", {}).values()
    ):
        raise RuntimeError("R0.72I producer certificate did not pass")
    producer_rows = load_csv(producer_csv_path)
    expected_m = config["expected"]["mValues"]
    producer_m = [int(numeric(row, "M")) for row in producer_rows]
    if producer_m != expected_m:
        raise RuntimeError(f"producer M grid {producer_m} does not match {expected_m}")

    plotted: list[dict[str, Any]] = []
    add_certificate_rows(
        plotted,
        producer_rows,
        route="producer",
        source_path=sources["producerCsv"],
    )
    source_files = [producer_csv_path, producer_result_path]

    independent_csv_path = REPOSITORY / sources["independentCsv"]
    independent_result_path = REPOSITORY / sources["independentResult"]
    independent_present = independent_csv_path.exists()
    independent_m: list[int] = []
    if independent_present:
        independent_rows = load_csv(independent_csv_path)
        independent_m = [int(numeric(row, "M")) for row in independent_rows]
        if independent_m != expected_m[: len(independent_m)]:
            raise RuntimeError(
                f"independent M grid {independent_m} is not a prefix of {expected_m}"
            )
        add_certificate_rows(
            plotted,
            independent_rows,
            route="independent",
            source_path=sources["independentCsv"],
        )
        source_files.append(independent_csv_path)
        if independent_result_path.exists():
            independent_result = load_json(independent_result_path)
            if independent_result.get("status") != "passed":
                raise RuntimeError("independent result is present but did not pass")
            source_files.append(independent_result_path)

    add_theory_rows(plotted)
    producer_last = producer_rows[-1]
    summary = {
        "mValues": expected_m,
        "producerStatus": producer_result["status"],
        "independentOverlay": independent_present,
        "independentMValues": independent_m,
        "largestM": int(numeric(producer_last, "M")),
        "largestMGenericBRatio": numeric(producer_last, "ratioGenericB"),
        "largestMGenericToMeasured": numeric(producer_last, "genericBToMeasuredHB"),
        "largestMMeasuredBvRatio": numeric(producer_last, "measuredBvLiftedRatio"),
        "largestMExactRootRatio": numeric(producer_last, "exactRootRatio"),
        "largestMRootResidual": numeric(producer_last, "evolvedRootResidual"),
        "rowCount": len(plotted),
    }
    return plotted, summary, source_files


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
    rows: list[dict[str, Any]], panel: str, series: str, route: str | None = None
) -> list[dict[str, Any]]:
    selected = [
        row
        for row in rows
        if row["panel"] == panel
        and row["series"] == series
        and (route is None or row["route"] == route)
    ]
    return sorted(selected, key=lambda row: float(row["x"]))


def set_dyadic_ticks(ax: Any, values: list[int]) -> None:
    ax.set_xscale("log", base=2)
    ax.set_xticks(values, labels=[str(value) for value in values])
    ax.xaxis.set_minor_locator(mticker.NullLocator())


def render(rows: list[dict[str, Any]], config: dict[str, Any], summary: dict[str, Any]) -> None:
    palette = config["palette"]
    width = config["figure"]["widthMillimetres"] / 25.4
    height = config["figure"]["heightMillimetres"] / 25.4
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 7.0,
            "axes.titlesize": 7.8,
            "axes.labelsize": 7.0,
            "xtick.labelsize": 6.1,
            "ytick.labelsize": 6.1,
            "legend.fontsize": 5.5,
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
        left=0.09,
        right=0.965,
        bottom=0.135,
        top=0.82,
        wspace=0.32,
        hspace=0.48,
    )
    fig.suptitle(
        "Physical absorption: the generic row loss is not the physical ledger",
        x=0.09,
        y=0.965,
        ha="left",
        fontsize=10.0,
        fontweight="bold",
    )
    subtitle = (
        r"All-odd Rudin--Shapiro family · $a=1$, $\delta=M$ · parity-resolved cubic exposure"
    )
    if summary["independentOverlay"]:
        subtitle += " · producer + independent overlays"
    else:
        subtitle += " · producer finite audit"
    fig.text(0.09, 0.915, subtitle, ha="left", fontsize=6.7, color=palette["muted"])

    routes = ["producer"] + (["independent"] if summary["independentOverlay"] else [])
    route_marker = {"producer": "o", "independent": "s"}
    route_fill = {"producer": True, "independent": False}

    ax = axes[0, 0]
    term_styles = {
        "initial trace": (palette["blue"], "-"),
        "target diagonal": (palette["muted"], ":"),
        "mixed moment": (palette["green"], "-"),
        "generic B term": (palette["red"], "-"),
    }
    for label, (color, linestyle) in term_styles.items():
        for route in routes:
            points = select(rows, "A", label, route)
            if not points:
                continue
            marker = route_marker[route]
            ax.plot(
                [point["x"] for point in points],
                [point["y"] for point in points],
                color=color,
                linestyle=linestyle if route == "producer" else "none",
                marker=marker,
                markersize=3.2,
                markerfacecolor=color if route_fill[route] else palette["paper"],
                markeredgecolor=color,
                markeredgewidth=0.8,
                linewidth=1.15,
                label=label if route == "producer" else None,
                zorder=4 if route == "independent" else 3,
            )
    ax.axhline(1.0, color=palette["ink"], linewidth=0.8, linestyle="--")
    ax.text(0.035, 0.55, "candidate payment", transform=ax.transAxes, fontsize=5.5)
    set_dyadic_ticks(ax, summary["mValues"])
    ax.set_yscale("log")
    ax.set_xlabel("carrier count $M$")
    ax.set_ylabel("lifted term / physical payment")
    ax.set_title("A  Termwise absorption fails only at generic $B_A$", loc="left", fontweight="bold")
    ax.grid(True, which="both", color=palette["grid"], linewidth=0.45, alpha=0.76)
    ax.legend(frameon=False, loc="lower left", ncol=2, handlelength=1.7, columnspacing=0.9)

    ax = axes[0, 1]
    for route in routes:
        points = select(rows, "B", "generic bound / measured cubic exposure", route)
        if not points:
            continue
        ax.plot(
            [point["x"] for point in points],
            [point["y"] for point in points],
            color=palette["red"],
            linestyle="-" if route == "producer" else "none",
            marker=route_marker[route],
            markersize=3.5,
            markerfacecolor=palette["red"] if route_fill[route] else palette["paper"],
            markeredgecolor=palette["red"],
            markeredgewidth=0.8,
            linewidth=1.25,
            label=route,
        )
    set_dyadic_ticks(ax, summary["mValues"])
    ax.set_yscale("log")
    ax.set_xlabel("carrier count $M$")
    ax.set_ylabel(r"generic $B_AQ_*$ / measured $2|\delta|\int|hb|$")
    ax.set_title("B  Parity exposes the overestimate", loc="left", fontweight="bold")
    ax.grid(True, which="both", color=palette["grid"], linewidth=0.45, alpha=0.76)
    if summary["independentOverlay"]:
        ax.legend(frameon=False, loc="upper left")
    ax.text(
        0.04,
        0.08,
        f"M={summary['largestM']}: {summary['largestMGenericToMeasured']:.2e}×",
        transform=ax.transAxes,
        fontsize=5.8,
        color=palette["muted"],
    )

    ax = axes[1, 0]
    measured_styles = {
        "measured BV upper": palette["blue"],
        "one exact-root atom": palette["ochre"],
    }
    for label, color in measured_styles.items():
        for route in routes:
            points = select(rows, "C", label, route)
            if not points:
                continue
            ax.plot(
                [point["x"] for point in points],
                [point["y"] for point in points],
                color=color,
                linestyle="-" if route == "producer" else "none",
                marker=route_marker[route],
                markersize=3.3,
                markerfacecolor=color if route_fill[route] else palette["paper"],
                markeredgecolor=color,
                markeredgewidth=0.8,
                linewidth=1.15,
                label=label if route == "producer" else None,
            )
    producer_bv = select(rows, "C", "measured BV upper", "producer")
    m0 = float(producer_bv[0]["x"])
    y0 = float(producer_bv[0]["y"])
    guide_x = np.geomspace(m0, float(summary["mValues"][-1]), 80)
    guide_y = y0 * (guide_x / m0) ** (-2.0 / 3.0)
    ax.plot(
        guide_x,
        guide_y,
        color=palette["muted"],
        linestyle="--",
        linewidth=0.85,
        label=r"$M^{-2/3}$ guide",
    )
    set_dyadic_ticks(ax, summary["mValues"])
    ax.set_yscale("log")
    ax.set_xlabel("carrier count $M$")
    ax.set_ylabel("physical normalized ratio")
    ax.set_title("C  Measured ledger does not inherit the loss", loc="left", fontweight="bold")
    ax.grid(True, which="both", color=palette["grid"], linewidth=0.45, alpha=0.76)
    ax.legend(frameon=False, loc="lower left", handlelength=1.7)
    ax.text(
        0.97,
        0.94,
        "BV curve: continuous-integral upper ledger\nroot curve: one certified atom",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=5.6,
        color=palette["muted"],
        bbox={
            "boxstyle": "round,pad=0.18",
            "facecolor": palette["paper"],
            "edgecolor": "none",
            "alpha": 0.88,
        },
    )

    ax = axes[1, 1]
    theory_styles = {
        "numeric coupling envelope": (palette["red"], "-", "o"),
        "analytic M^(-4/9) log^(-2/3)": (palette["ink"], "--", None),
        "section g=M": (palette["blue"], "-", None),
        "section g=M^(3/2)": (palette["green"], "-", None),
    }
    theory_labels = {
        "numeric coupling envelope": "coupling envelope",
        "analytic M^(-4/9) log^(-2/3)": r"$M^{-4/9}(\log M)^{-2/3}$",
        "section g=M": r"$g=M$",
        "section g=M^(3/2)": r"$g=M^{3/2}$",
    }
    for series, (color, linestyle, marker) in theory_styles.items():
        points = select(rows, "D", series)
        markevery = 12 if marker else None
        ax.plot(
            [point["x"] for point in points],
            [point["y"] for point in points],
            color=color,
            linestyle=linestyle,
            marker=marker,
            markevery=markevery,
            markersize=2.8,
            linewidth=1.15 if series == "numeric coupling envelope" else 0.95,
            label=theory_labels[series],
        )
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xlabel("carrier count $M$")
    ax.set_ylabel(r"$R(M,g)$")
    ax.set_title("D  Coupling optimization still decays", loc="left", fontweight="bold")
    ax.grid(True, which="both", color=palette["grid"], linewidth=0.45, alpha=0.76)
    ax.legend(frameon=False, loc="upper right", handlelength=1.8)
    ax.text(
        0.04,
        0.08,
        r"$q=X=1$; physical-window generalization retains decay",
        transform=ax.transAxes,
        fontsize=5.6,
        color=palette["muted"],
    )

    fig.text(
        0.09,
        0.052,
        "Finite all-odd triangular audit · upper-bound loss ≠ physical counterexample · no general 3D claim.",
        fontsize=5.7,
        color=palette["muted"],
    )
    fig.text(
        0.965,
        0.052,
        "R0.72I · 2026-08-27",
        ha="right",
        fontsize=5.7,
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
    progress = ROOT / "progress.ndjson"
    resources = ROOT / "resource-log.ndjson"
    progress.write_text("", encoding="utf-8")
    resources.write_text("", encoding="utf-8")
    append(progress, {"time": utc_now(), "event": "figure_build_start"})
    config = load_json(ROOT / "config.json")
    rows, summary, certificate_sources = prepare_rows(config)
    write_data(rows)
    render(rows, config, summary)
    contract = load_json(ROOT / "contract.json")
    results = {
        "schemaVersion": "r072i-figure-results-v1",
        "allRequiredSourceChecksPassed": True,
        "summary": summary,
        "claimBoundary": contract["claimBoundary"],
    }
    (ROOT / "results.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    source_files = certificate_sources + [ROOT / "config.json", ROOT / "contract.json"]
    metadata = {
        "schemaVersion": "r072i-figure-data-metadata-v1",
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
        "independentOverlay": summary["independentOverlay"],
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
        resources,
        {
            "time": utc_now(),
            "elapsedSeconds": elapsed,
            "maxRssMb": rss_mb(),
            "rowCount": len(rows),
        },
    )
    append(
        progress,
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
