#!/usr/bin/env python3
"""Build the formal R0.72H mixed-row payment figure."""

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


def load(path: Path) -> dict[str, Any]:
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


def envelope(alpha: float) -> tuple[float, float]:
    upper = max(45.0, math.log1p(alpha) + 25.0)
    u = np.linspace(0.0, upper, 16001)
    values = np.exp(-u / 3.0 - alpha * np.exp(-u)) / (1.0 + u)
    index = int(np.argmax(values))
    phi = float(values[index])
    comparator = (1.0 + alpha) ** (-1.0 / 3.0) / (
        1.0 + math.log(2.0 + alpha)
    )
    return phi, phi / comparator


def prepare_rows(
    producer: dict[str, Any],
    independent: dict[str, Any],
    config: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    if producer["status"] != "passed" or independent["status"] != "passed":
        raise RuntimeError("both R0.72H certificates must pass")
    expected = config["expected"]["mValues"]
    producer_m = [int(row["M"]) for row in producer["cases"]]
    independent_m = [int(row["M"]) for row in independent["cases"]]
    if producer_m != expected or independent_m != expected:
        raise RuntimeError("certificate M grid does not match the figure contract")

    rows: list[dict[str, Any]] = []
    for alpha in np.logspace(-4, 7, 84):
        phi, ratio = envelope(float(alpha))
        rows.append(
            {
                "panel": "A",
                "route": "analytic grid",
                "series": "envelope ratio",
                "x": float(alpha),
                "y": ratio,
                "rawValue": phi,
                "source": "research/r072h_report-source.md",
                "pointer": "Lemma 3.1",
            }
        )

    series = {
        "mixed row": "mixedRowNormalized",
        "critical action": "criticalActionNormalized",
        "profile moment": "profileMomentNormalized",
    }
    producer_path = config["sourceCertificates"]["producer"]
    independent_path = config["sourceCertificates"]["independent"]
    for route, certificate, source_path in (
        ("producer", producer, producer_path),
        ("independent", independent, independent_path),
    ):
        for index, item in enumerate(certificate["cases"]):
            for label, key in series.items():
                rows.append(
                    {
                        "panel": "B",
                        "route": route,
                        "series": label,
                        "x": int(item["M"]),
                        "y": float(item[key]),
                        "rawValue": float(item[key.replace("Normalized", "")]),
                        "source": source_path,
                        "pointer": f"cases[{index}].{key}",
                    }
                )

    for index, item in enumerate(producer["cases"]):
        M = int(item["M"])
        rows.append(
            {
                "panel": "C",
                "route": "producer",
                "series": "action-only quotient",
                "x": M,
                "y": float(item["mixedRow"]) / float(item["criticalAction"]),
                "rawValue": float(item["actionOnlyScaledRatio"]),
                "source": producer_path,
                "pointer": f"cases[{index}]",
            }
        )
        rows.append(
            {
                "panel": "C",
                "route": "analytic guide",
                "series": "M^(4/3)/log M",
                "x": M,
                "y": M ** (4.0 / 3.0) / math.log(M),
                "rawValue": M,
                "source": "research/r072h_report-source.md",
                "pointer": "equation (0.10)",
            }
        )
        rows.append(
            {
                "panel": "C",
                "route": "producer",
                "series": "moment-resolved ratio",
                "x": M,
                "y": float(item["momentResolvedRatio"]),
                "rawValue": float(item["momentResolvedRatio"]),
                "source": producer_path,
                "pointer": f"cases[{index}].momentResolvedRatio",
            }
        )

    summary = {
        "mValues": expected,
        "producerStatus": producer["status"],
        "independentStatus": independent["status"],
        "maxCrossRouteRelativeError": float(
            independent["maxProducerRelativeError"]
        ),
        "largestM": int(producer["cases"][-1]["M"]),
        "atLargestMMixedRowNormalized": float(
            producer["cases"][-1]["mixedRowNormalized"]
        ),
        "atLargestMMomentResolvedRatio": float(
            producer["cases"][-1]["momentResolvedRatio"]
        ),
        "atLargestMActionOnlyScaledRatio": float(
            producer["cases"][-1]["actionOnlyScaledRatio"]
        ),
        "atLargestMRootResidual": float(
            producer["cases"][-1]["evolvedRootResidual"]
        ),
        "rowCount": len(rows),
    }
    return rows, summary


def write_data(rows: list[dict[str, Any]]) -> None:
    fields = [
        "panel",
        "route",
        "series",
        "x",
        "y",
        "rawValue",
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
    chosen = [
        row
        for row in rows
        if row["panel"] == panel
        and row["series"] == series
        and (route is None or row["route"] == route)
    ]
    return sorted(chosen, key=lambda row: float(row["x"]))


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
            "xtick.labelsize": 6.2,
            "ytick.labelsize": 6.2,
            "legend.fontsize": 5.7,
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
    fig, axes = plt.subplots(1, 3, figsize=(width, height))
    # Interactive backends quantize the initial canvas to whole pixels. Reset
    # the physical size without forwarding so PDF and 600 dpi PNG retain the
    # exact contracted geometry.
    fig.set_size_inches(width, height, forward=False)
    fig.subplots_adjust(left=0.068, right=0.945, bottom=0.235, top=0.78, wspace=0.43)
    fig.suptitle(
        "Critical-log payment of the finite-carrier mixed target row",
        x=0.068,
        y=0.95,
        ha="left",
        fontsize=10.0,
        fontweight="bold",
    )
    fig.text(
        0.068,
        0.885,
        "Carrier-free upper bound · all-odd Rudin–Shapiro sharpness · two independent finite audits",
        ha="left",
        fontsize=6.7,
        color=palette["muted"],
    )

    ax = axes[0]
    envelope_rows = select(rows, "A", "envelope ratio")
    ax.semilogx(
        [row["x"] for row in envelope_rows],
        [row["y"] for row in envelope_rows],
        color=palette["blue"],
        linewidth=1.5,
    )
    ax.axhline(1.0, color=palette["muted"], linewidth=0.8, linestyle="--")
    ax.fill_between(
        [row["x"] for row in envelope_rows],
        0.4,
        1.75,
        color=palette["ochre"],
        alpha=0.08,
    )
    ax.set_xlabel(r"$a$")
    ax.set_ylabel(r"$\Phi(a)\,[1+\log(2+a)](1+a)^{1/3}$")
    ax.set_title("A  Reciprocal-weight crossover", loc="left", fontweight="bold")
    ax.set_ylim(0.25, 1.9)
    ax.grid(True, which="both", color=palette["grid"], linewidth=0.45, alpha=0.75)
    ax.text(
        0.04,
        0.08,
        "bounded above and below",
        transform=ax.transAxes,
        fontsize=5.9,
        color=palette["muted"],
    )

    ax = axes[1]
    colors = {
        "mixed row": palette["red"],
        "critical action": palette["blue"],
        "profile moment": palette["ochre"],
    }
    for label, color in colors.items():
        producer_rows = select(rows, "B", label, "producer")
        independent_rows = select(rows, "B", label, "independent")
        ax.plot(
            [row["x"] for row in producer_rows],
            [row["y"] for row in producer_rows],
            color=color,
            marker="o",
            markersize=3.2,
            linewidth=1.15,
            label=label,
        )
        ax.scatter(
            [row["x"] for row in independent_rows],
            [row["y"] for row in independent_rows],
            facecolors=palette["paper"],
            edgecolors=color,
            marker="s",
            s=15,
            linewidths=0.75,
            zorder=4,
        )
    ax.set_xscale("log", base=2)
    ax.set_xticks(summary["mValues"], labels=[str(v) for v in summary["mValues"]])
    ax.set_xlabel("carrier count $M$")
    ax.set_ylabel("quantity / proved scale")
    ax.set_title("B  Scale-normalized finite audit", loc="left", fontweight="bold")
    ax.grid(True, color=palette["grid"], linewidth=0.45, alpha=0.75)
    ax.legend(frameon=False, loc="upper right", handlelength=1.8)
    ax.text(
        0.04,
        0.08,
        "● producer   □ independent",
        transform=ax.transAxes,
        fontsize=5.7,
        color=palette["muted"],
    )

    ax = axes[2]
    quotient = select(rows, "C", "action-only quotient")
    guide = select(rows, "C", "M^(4/3)/log M")
    moment = select(rows, "C", "moment-resolved ratio")
    line_q = ax.plot(
        [row["x"] for row in quotient],
        [row["y"] for row in quotient],
        color=palette["red"],
        marker="o",
        markersize=3.2,
        linewidth=1.2,
        label=r"$\mathcal{E}_Q/Q_*$",
    )[0]
    line_g = ax.plot(
        [row["x"] for row in guide],
        [row["y"] for row in guide],
        color=palette["muted"],
        linestyle="--",
        linewidth=0.9,
        label=r"$M^{4/3}/\log M$",
    )[0]
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xticks(summary["mValues"], labels=[str(v) for v in summary["mValues"]])
    ax.xaxis.set_minor_locator(mticker.NullLocator())
    ax.set_xlabel("carrier count $M$")
    ax.set_ylabel("action-only quotient")
    ax.grid(True, which="both", color=palette["grid"], linewidth=0.45, alpha=0.75)
    twin = ax.twinx()
    line_m = twin.plot(
        [row["x"] for row in moment],
        [row["y"] for row in moment],
        color=palette["green"],
        marker="s",
        markersize=3.0,
        linewidth=1.1,
        label=r"$\sqrt{Mm_*Q_*}/\mathcal{E}_Q$",
    )[0]
    twin.set_ylim(0.64, 0.74)
    twin.set_yticks([0.65, 0.70])
    twin.set_ylabel("moment-resolved ratio", color=palette["green"], labelpad=2)
    twin.tick_params(axis="y", colors=palette["green"])
    ax.set_title("C  Necessary moment", loc="left", fontweight="bold")
    ax.legend(
        [line_q, line_g, line_m],
        [line_q.get_label(), line_g.get_label(), line_m.get_label()],
        frameon=False,
        loc="upper left",
        handlelength=1.8,
    )
    ax.text(
        0.04,
        0.09,
        f"root residual at M=64: {summary['atLargestMRootResidual']:.1e}",
        transform=ax.transAxes,
        fontsize=5.7,
        color=palette["muted"],
    )

    fig.text(
        0.068,
        0.075,
        "Analytic theorem: triangular 2.5D finite-carrier row. Finite diagnostics do not prove the full physical normalization or 3D regularity.",
        fontsize=5.7,
        color=palette["muted"],
    )
    fig.text(
        0.985,
        0.075,
        "R0.72H · 2026-08-27",
        ha="right",
        fontsize=5.7,
        color=palette["muted"],
    )
    dpi = int(config["figure"]["pngDpi"])
    fig.savefig(ROOT / "figure.pdf")
    svg_path = ROOT / "figure.svg"
    fig.savefig(svg_path)
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines())
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
    config = load(ROOT / "config.json")
    producer_path = REPOSITORY / config["sourceCertificates"]["producer"]
    independent_path = REPOSITORY / config["sourceCertificates"]["independent"]
    producer = load(producer_path)
    independent = load(independent_path)
    rows, summary = prepare_rows(producer, independent, config)
    write_data(rows)
    render(rows, config, summary)
    results = {
        "schemaVersion": "r072h-figure-results-v1",
        "allRequiredSourceChecksPassed": True,
        "summary": summary,
        "claimBoundary": load(ROOT / "contract.json")["claimBoundary"],
    }
    (ROOT / "results.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    sources = [
        producer_path,
        independent_path,
        ROOT / "config.json",
        ROOT / "contract.json",
    ]
    metadata = {
        "schemaVersion": "r072h-figure-data-metadata-v1",
        "generatedAt": utc_now(),
        "sourceFiles": [
            {
                "path": str(path.relative_to(REPOSITORY)),
                "sha256": digest(path),
            }
            for path in sources
        ],
        "rowCount": len(rows),
        "panels": ["A", "B", "C"],
    }
    (ROOT / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
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
