#!/usr/bin/env python3
"""Build the formal R0.72K directional-root figure without new PDE solves."""

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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rss_mb() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        return float(value) / (1024.0 * 1024.0)
    return float(value) / 1024.0


def append_ndjson(path: Path, payload: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def relative_error(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def common_cases(result: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("commonBandCases", "cases"):
        rows = result.get(key)
        if isinstance(rows, list) and rows and "R" in rows[0]:
            return rows
    ledger_rows = result.get("ledgerCases")
    if isinstance(ledger_rows, list) and ledger_rows:
        normalized: list[dict[str, Any]] = []
        for row in ledger_rows:
            n_squared = float(int(row["N"]) ** 2)
            normalized.append(
                {
                    "R": int(row["R"]),
                    "N": int(row["N"]),
                    "rootAtomOverN2": float(row["exactRootLower"])
                    / n_squared,
                    "measuredUpperOverN2": float(
                        row["measuredCompleteLedgerUpper"]
                    )
                    / n_squared,
                    "theoremProxyOverN2": float(
                        row["analyticCompleteLedgerProxy"]
                    )
                    / n_squared,
                    "normalizedMeasuredCompleteUpper": float(
                        row["normalizedMeasuredCompleteUpper"]
                    ),
                    "normalizedTheoremCompleteProxy": float(
                        row["normalizedAnalyticCompleteProxy"]
                    ),
                    "exactRootResidual": float(row["exactRootResidual"]),
                }
            )
        return normalized
    raise KeyError("certificate does not expose common-band cases")


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


def prepare_data(
    config: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any], list[Path]]:
    source_config = config["sourceCertificates"]
    producer_path = REPOSITORY / source_config["producerResult"]
    independent_path = REPOSITORY / source_config["independentResult"]
    crosscheck_path = REPOSITORY / source_config["crosscheck"]
    report_path = REPOSITORY / "research/r072k_report-source.md"
    producer = load_json(producer_path)
    independent = load_json(independent_path)
    crosscheck = load_json(crosscheck_path)
    for label, result in (
        ("producer", producer),
        ("independent", independent),
        ("crosscheck", crosscheck),
    ):
        if result.get("status") != "passed":
            raise RuntimeError(f"R0.72K {label} certificate did not pass")

    expected_r = [int(value) for value in config["expected"]["rValues"]]
    p_cases = {int(row["R"]): row for row in common_cases(producer)}
    i_cases = {int(row["R"]): row for row in common_cases(independent)}
    if sorted(p_cases) != expected_r or sorted(i_cases) != expected_r:
        raise RuntimeError("R0.72K certificate R grids do not match contract")

    rows: list[dict[str, Any]] = []
    t_values = np.linspace(0.0, 1.0, 241)
    trajectory = np.exp(2j * np.pi * t_values) - 1.0
    for index, (t_value, value) in enumerate(zip(t_values, trajectory)):
        add_row(
            rows,
            panel="A",
            route="analytic",
            series="complex trajectory",
            x=float(value.real),
            y=float(value.imag),
            raw_value=float(t_value),
            auxiliary=2.0 * math.pi,
            source="research/r072k_report-source.md",
            pointer=f"equation (1.9), sample {index}",
        )
    for t_value in (0.25, 0.75):
        value = complex(np.exp(2j * np.pi * t_value) - 1.0)
        add_row(
            rows,
            panel="A",
            route="analytic",
            series="directional projection zero",
            x=value.real,
            y=value.imag,
            raw_value=t_value,
            auxiliary="Re ell(X')=0",
            source="research/r072k_report-source.md",
            pointer="Section 1.1",
        )

    sharpness = producer.get("sharpnessCases", [])
    if len(sharpness) != int(config["expected"]["sharpnessCaseCount"]):
        raise RuntimeError("sharpness case count does not match contract")
    for index, row in enumerate(sharpness):
        epsilon = float(row["epsilonNumerator"]) / float(
            row["epsilonDenominator"]
        )
        add_row(
            rows,
            panel="B",
            route="exact rational",
            series="factor-two ratio",
            x=1.0 / epsilon,
            y=float(row["theoremRatio"]),
            raw_value=epsilon,
            auxiliary=float(row["weightedVariation"]),
            source=source_config["producerResult"],
            pointer=f"sharpnessCases[{index}]",
        )

    for R in expected_r:
        for route, case, source in (
            ("producer", p_cases[R], source_config["producerResult"]),
            ("independent", i_cases[R], source_config["independentResult"]),
        ):
            source_collection = (
                "commonBandCases" if route == "producer" else "ledgerCases"
            )
            for series, key in (
                ("exact root atom / N^2", "rootAtomOverN2"),
                ("measured upper / N^2", "measuredUpperOverN2"),
                ("theorem proxy / N^2", "theoremProxyOverN2"),
            ):
                source_key = key
                if route == "independent":
                    source_key = {
                        "rootAtomOverN2": "exactRootLower / N^2",
                        "measuredUpperOverN2": (
                            "measuredCompleteLedgerUpper / N^2"
                        ),
                        "theoremProxyOverN2": (
                            "analyticCompleteLedgerProxy / N^2"
                        ),
                    }[key]
                add_row(
                    rows,
                    panel="C",
                    route=route,
                    series=series,
                    x=float(R),
                    y=float(case[key]),
                    raw_value=float(case[key]),
                    auxiliary=float(case.get("exactRootResidual", 0.0)),
                    source=source,
                    pointer=f"{source_collection}[R={R}].{source_key}",
                )
            for series, key in (
                (
                    "measured complete upper",
                    "normalizedMeasuredCompleteUpper",
                ),
                (
                    "theorem complete proxy",
                    "normalizedTheoremCompleteProxy",
                ),
            ):
                source_key = key
                if route == "independent" and key == "normalizedTheoremCompleteProxy":
                    source_key = "normalizedAnalyticCompleteProxy"
                add_row(
                    rows,
                    panel="D",
                    route=route,
                    series=series,
                    x=float(R),
                    y=float(case[key]),
                    raw_value=float(case[key]),
                    auxiliary="physical normalized",
                    source=source,
                    pointer=f"{source_collection}[R={R}].{source_key}",
                )

    guide_r = np.geomspace(expected_r[0], expected_r[-1], 80)
    anchor_r = float(expected_r[-1])
    anchor_y = float(p_cases[expected_r[-1]]["normalizedMeasuredCompleteUpper"])
    for index, R in enumerate(guide_r):
        guide = anchor_y * (R / anchor_r) ** (-2.0 / 3.0)
        add_row(
            rows,
            panel="D",
            route="guide",
            series="R^-2/3 guide",
            x=float(R),
            y=float(guide),
            raw_value=float(R ** (-2.0 / 3.0)),
            auxiliary="anchored at largest producer measured upper",
            source="research/r072k_report-source.md",
            pointer=f"equation (6.11), sample {index}",
        )

    measured_errors = []
    proxy_errors = []
    for R in expected_r:
        measured_errors.append(
            relative_error(
                float(p_cases[R]["normalizedMeasuredCompleteUpper"]),
                float(i_cases[R]["normalizedMeasuredCompleteUpper"]),
            )
        )
        proxy_errors.append(
            relative_error(
                float(p_cases[R]["normalizedTheoremCompleteProxy"]),
                float(i_cases[R]["normalizedTheoremCompleteProxy"]),
            )
        )
    summary = {
        "producerStatus": producer["status"],
        "independentStatus": independent["status"],
        "crosscheckStatus": crosscheck["status"],
        "rValues": expected_r,
        "rowCount": len(rows),
        "sharpnessLargestRatio": max(
            float(row["theoremRatio"]) for row in sharpness
        ),
        "maximumMeasuredCrossRelativeError": max(measured_errors),
        "maximumProxyCrossRelativeError": max(proxy_errors),
        "producerMeasuredSlope": float(
            producer["slopes"]["normalizedMeasuredCompleteUpperAll"]
        ),
        "producerProxySlope": float(
            producer["slopes"]["normalizedTheoremCompleteProxyAll"]
        ),
        "largestProducerRootResidual": max(
            float(row["exactRootResidual"]) for row in p_cases.values()
        ),
        "largestIndependentRootResidual": max(
            float(row["exactRootResidual"]) for row in i_cases.values()
        ),
    }
    source_paths = [
        producer_path,
        independent_path,
        crosscheck_path,
        report_path,
        ROOT / "config.json",
        ROOT / "contract.json",
        ROOT / "figure-contract.md",
        ROOT / "caption.md",
    ]
    return rows, summary, source_paths


def write_data(rows: list[dict[str, Any]]) -> None:
    path = ROOT / "data.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(rows[0].keys()), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def blossom(fig: mpl.figure.Figure, color: str) -> None:
    center = (0.968, 0.972)
    for angle in range(0, 360, 72):
        petal = Ellipse(
            center,
            width=0.020,
            height=0.008,
            angle=angle,
            facecolor="none",
            edgecolor=color,
            linewidth=0.65,
            transform=fig.transFigure,
            zorder=20,
        )
        fig.add_artist(petal)


def style_axes(ax: mpl.axes.Axes, palette: dict[str, str]) -> None:
    ax.set_facecolor(palette["paper"])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(palette["muted"])
    ax.spines["bottom"].set_color(palette["muted"])
    ax.tick_params(colors=palette["ink"], labelsize=7, length=2.5, width=0.6)
    ax.grid(True, color=palette["grid"], linewidth=0.45, alpha=0.75)
    ax.set_axisbelow(True)


def panel_label(ax: mpl.axes.Axes, label: str, palette: dict[str, str]) -> None:
    ax.text(
        -0.10,
        1.02,
        label,
        transform=ax.transAxes,
        fontsize=10,
        fontweight="bold",
        color=palette["ink"],
        va="bottom",
    )


def draw_figure(
    rows: list[dict[str, Any]], config: dict[str, Any], summary: dict[str, Any]
) -> None:
    palette = config["palette"]
    width = float(config["figure"]["widthMillimetres"]) / 25.4
    height = float(config["figure"]["heightMillimetres"]) / 25.4
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 7.5,
            "axes.titlesize": 8.2,
            "axes.labelsize": 7.5,
            "legend.fontsize": 6.4,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )
    fig, axes = plt.subplots(2, 2, figsize=(width, height), constrained_layout=False)
    fig.patch.set_facecolor(palette["paper"])
    fig.subplots_adjust(
        left=0.085,
        right=0.975,
        bottom=0.105,
        top=0.855,
        wspace=0.34,
        hspace=0.46,
    )
    fig.suptitle(
        "Directional complex-root sampling and common-band payment",
        x=0.085,
        y=0.965,
        ha="left",
        fontsize=9.8,
        fontweight="bold",
        color=palette["ink"],
    )
    fig.text(
        0.085,
        0.912,
        "Analytic root packing; finite producer/independent lineages reuse archived R0.72J evolutions",
        ha="left",
        fontsize=6.7,
        color=palette["muted"],
    )
    blossom(fig, palette["ochre"])

    ax = axes[0, 0]
    style_axes(ax, palette)
    panel_label(ax, "A", palette)
    trajectory = [row for row in rows if row["panel"] == "A" and row["series"] == "complex trajectory"]
    zeros = [row for row in rows if row["panel"] == "A" and row["series"] == "directional projection zero"]
    ax.plot(
        [float(row["x"]) for row in trajectory],
        [float(row["y"]) for row in trajectory],
        color=palette["blue"],
        linewidth=1.5,
    )
    ax.scatter([0.0], [0.0], s=26, color=palette["ochre"], edgecolor=palette["ink"], linewidth=0.5, zorder=5)
    ax.scatter(
        [float(row["x"]) for row in zeros],
        [float(row["y"]) for row in zeros],
        marker="x",
        s=34,
        color=palette["ink"],
        linewidth=1.0,
        zorder=6,
    )
    ax.annotate("root: t=0=1", xy=(0, 0), xytext=(-1.42, 0.58), arrowprops={"arrowstyle": "-", "color": palette["muted"], "lw": 0.6}, fontsize=6.5, color=palette["ink"])
    ax.annotate("projection zeros", xy=(-1.0, 1.0), xytext=(-1.95, 1.23), arrowprops={"arrowstyle": "-", "color": palette["muted"], "lw": 0.6}, fontsize=6.5, color=palette["ink"])
    ax.text(0.03, 0.04, r"$|X'(t)|=2\pi>0$", transform=ax.transAxes, fontsize=7, color=palette["ochre"])
    ax.set_title("Complex return with no tangent zero", loc="left", pad=6)
    ax.set_xlabel(r"$\mathrm{Re}\,X(t)$")
    ax.set_ylabel(r"$\mathrm{Im}\,X(t)$")
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-2.15, 0.25)
    ax.set_ylim(-1.25, 1.35)

    ax = axes[0, 1]
    style_axes(ax, palette)
    panel_label(ax, "B", palette)
    sharp = [row for row in rows if row["panel"] == "B"]
    x_values = np.array([float(row["x"]) for row in sharp])
    y_values = np.array([float(row["y"]) for row in sharp])
    ax.plot(x_values, y_values, color=palette["blue"], linewidth=1.3)
    ax.scatter(x_values, y_values, s=24, color=palette["blue"], edgecolor=palette["ink"], linewidth=0.45, zorder=5)
    ax.axhline(1.0, color=palette["ochre"], linestyle="--", linewidth=0.9)
    ax.text(0.98, 0.86, "sharp boundary = 1", transform=ax.transAxes, ha="right", va="top", fontsize=6.5, color=palette["ochre"])
    ax.set_xscale("log", base=2)
    ax.set_ylim(0.78, 1.015)
    ax.set_title("Sharpness of the factor two", loc="left", pad=6)
    ax.set_xlabel(r"$1/\epsilon$")
    ax.set_ylabel("endpoint mass / theorem bound")
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%d"))

    ax = axes[1, 0]
    style_axes(ax, palette)
    panel_label(ax, "C", palette)
    series_styles = {
        "exact root atom / N^2": (palette["muted"], ":"),
        "measured upper / N^2": (palette["blue"], "-"),
        "theorem proxy / N^2": (palette["ochre"], "--"),
    }
    for series, (color, linestyle) in series_styles.items():
        for route, marker, fill in (
            ("producer", "o", color),
            ("independent", "s", "none"),
        ):
            marker_size = 3.4 if route == "producer" else 4.6
            selected = [row for row in rows if row["panel"] == "C" and row["series"] == series and row["route"] == route]
            selected.sort(key=lambda row: float(row["x"]))
            ax.plot(
                [float(row["x"]) for row in selected],
                [float(row["y"]) for row in selected],
                color=color,
                linestyle=linestyle,
                linewidth=1.05,
                marker=marker,
                markersize=marker_size,
                markerfacecolor=fill,
                markeredgecolor=color,
                markeredgewidth=0.7,
                label=series if route == "producer" else None,
            )
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_ylim(0.08, 42.0)
    ax.set_title("Complete raw root ledger", loc="left", pad=6)
    ax.set_xlabel("carrier scale R")
    ax.set_ylabel(r"raw mass / $N^2$")
    ax.set_xticks(summary["rValues"])
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%d"))
    for series, (color, _linestyle) in series_styles.items():
        endpoint = max(
            (
                row
                for row in rows
                if row["panel"] == "C"
                and row["series"] == series
                and row["route"] == "producer"
            ),
            key=lambda row: float(row["x"]),
        )
        ax.annotate(
            series,
            xy=(float(endpoint["x"]), float(endpoint["y"])),
            xytext=(-5, 5),
            textcoords="offset points",
            ha="right",
            va="bottom",
            fontsize=6.1,
            color=color,
        )

    ax = axes[1, 1]
    style_axes(ax, palette)
    panel_label(ax, "D", palette)
    for series, color, linestyle in (
        ("measured complete upper", palette["blue"], "-"),
        ("theorem complete proxy", palette["ochre"], "--"),
    ):
        for route, marker, fill in (
            ("producer", "o", color),
            ("independent", "s", "none"),
        ):
            marker_size = 3.4 if route == "producer" else 4.6
            selected = [row for row in rows if row["panel"] == "D" and row["series"] == series and row["route"] == route]
            selected.sort(key=lambda row: float(row["x"]))
            ax.plot(
                [float(row["x"]) for row in selected],
                [float(row["y"]) for row in selected],
                color=color,
                linestyle=linestyle,
                linewidth=1.05,
                marker=marker,
                markersize=marker_size,
                markerfacecolor=fill,
                markeredgecolor=color,
                markeredgewidth=0.7,
                label=series if route == "producer" else None,
            )
    guide = [row for row in rows if row["panel"] == "D" and row["series"] == "R^-2/3 guide"]
    ax.plot(
        [float(row["x"]) for row in guide],
        [float(row["y"]) for row in guide],
        color=palette["muted"],
        linestyle=":",
        linewidth=1.0,
        label=r"anchored $R^{-2/3}$ guide",
    )
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_title("Physical normalized complete ledger", loc="left", pad=6)
    ax.set_xlabel("carrier scale R")
    ax.set_ylabel(r"upper ledger / $D^{1/3}\Lambda_{1,*}$")
    ax.set_xticks(summary["rValues"])
    ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%d"))
    ax.legend(frameon=False, loc="upper right", handlelength=2.0)
    ax.text(
        0.03,
        0.05,
        f"producer slopes: {summary['producerMeasuredSlope']:.3f} measured, "
        f"{summary['producerProxySlope']:.3f} proxy",
        transform=ax.transAxes,
        fontsize=6.1,
        color=palette["muted"],
    )

    for axis in axes.flat:
        axis.margins(x=0.04)

    fig.savefig(ROOT / "figure.pdf", facecolor=palette["paper"])
    fig.savefig(ROOT / "figure.svg", facecolor=palette["paper"])
    svg_path = ROOT / "figure.svg"
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines())
        + "\n",
        encoding="utf-8",
    )
    fig.savefig(
        ROOT / "figure.png",
        dpi=int(config["figure"]["pngDpi"]),
        facecolor=palette["paper"],
    )
    plt.close(fig)


def main() -> int:
    started = time.perf_counter()
    progress_path = ROOT / "progress.ndjson"
    resource_path = ROOT / "resource-log.ndjson"
    progress_path.write_text("", encoding="utf-8")
    resource_path.write_text("", encoding="utf-8")
    append_ndjson(progress_path, {"time": utc_now(), "event": "figure_build_start"})
    config = load_json(ROOT / "config.json")
    rows, summary, source_paths = prepare_data(config)
    write_data(rows)
    append_ndjson(
        progress_path,
        {
            "time": utc_now(),
            "event": "data_prepared",
            "rows": len(rows),
            "summary": summary,
        },
    )
    draw_figure(rows, config, summary)
    elapsed = time.perf_counter() - started
    output_hashes = {
        name: sha256(ROOT / name)
        for name in ("figure.pdf", "figure.svg", "figure.png", "data.csv")
    }
    source_hashes = {str(path.relative_to(REPOSITORY)): sha256(path) for path in source_paths}
    results = {
        "schemaVersion": 1,
        "figureId": "R0.72K-1",
        "status": "built",
        "generatedAt": utc_now(),
        "summary": summary,
        "outputSha256": output_hashes,
        "sourceSha256": source_hashes,
        "elapsedSeconds": elapsed,
        "maxRssMb": rss_mb(),
        "newPdeEvolution": False,
    }
    (ROOT / "results.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    environment = {
        "generatedAt": utc_now(),
        "python": sys.version,
        "matplotlib": mpl.__version__,
        "numpy": np.__version__,
        "platform": platform.platform(),
        "cpuCount": os.cpu_count(),
        "maxRssMb": rss_mb(),
    }
    (ROOT / "environment.txt").write_text(
        "\n".join(f"{key}={value}" for key, value in environment.items()) + "\n",
        encoding="utf-8",
    )
    append_ndjson(
        resource_path,
        {
            "time": utc_now(),
            "elapsedSeconds": elapsed,
            "maxRssMb": rss_mb(),
            "rows": len(rows),
        },
    )
    append_ndjson(
        progress_path,
        {
            "time": utc_now(),
            "event": "figure_build_complete",
            "elapsedSeconds": elapsed,
            "outputs": output_hashes,
        },
    )
    print(json.dumps({"status": "built", "rows": len(rows), "elapsedSeconds": elapsed, "outputs": output_hashes}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
