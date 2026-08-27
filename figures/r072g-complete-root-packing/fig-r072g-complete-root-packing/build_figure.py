#!/usr/bin/env python3
"""Build the formal R0.72G complete-root packing figure."""

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
import numpy as np


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace(
        "+00:00", "Z"
    )


def peak_rss() -> int:
    raw = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return raw if sys.platform == "darwin" else 1024 * raw


def chart_row(
    panel: str,
    series: str,
    x: float,
    y: float,
    raw: float | int,
    evidence: str,
    source: str,
    pointer: str,
    note: str,
) -> dict[str, object]:
    return {
        "panel": panel,
        "series": series,
        "x": x,
        "y": y,
        "rawValue": raw,
        "evidence": evidence,
        "source": source,
        "sourcePointer": pointer,
        "note": note,
    }


def prepare_data(
    producer: dict[str, Any], independent: dict[str, Any], config: dict[str, Any]
) -> tuple[list[dict[str, object]], dict[str, Any]]:
    if not producer.get("allRequiredChecksPassed"):
        raise RuntimeError("producer certificate did not pass")
    if not independent.get("allRequiredChecksPassed"):
        raise RuntimeError("independent certificate did not pass")
    producer_r = [int(row["R"]) for row in producer["rows"]]
    independent_r = [int(row["R"]) for row in independent["rows"]]
    if producer_r != config["expected"]["producerR"]:
        raise RuntimeError(f"unexpected producer grid: {producer_r}")
    if independent_r != config["expected"]["independentR"]:
        raise RuntimeError(f"unexpected independent grid: {independent_r}")

    rows: list[dict[str, object]] = []
    producer_source = config["sourceCertificates"]["producer"]
    independent_source = config["sourceCertificates"]["independent"]
    for index, item in enumerate(producer["rows"]):
        log_delta = math.log(float(item["delta"]))
        rows.append(
            chart_row(
                "A",
                "producer complete",
                log_delta,
                float(item["completeSlopeMass"]),
                float(item["completeSlopeMass"]),
                "finite binary64",
                producer_source,
                f"rows[{index}].completeSlopeMass",
                f"R={item['R']}; delta={item['delta']}",
            )
        )
        rows.append(
            chart_row(
                "A",
                "producer selected",
                log_delta,
                float(item["selectedSlopeMass"]),
                float(item["selectedSlopeMass"]),
                "finite binary64",
                producer_source,
                f"rows[{index}].selectedSlopeMass",
                f"first R={item['R']} resolved roots",
            )
        )
        rows.append(
            chart_row(
                "B",
                "producer resolved roots",
                math.sqrt(float(item["delta"])),
                float(item["rootCount"]),
                int(item["rootCount"]),
                "finite binary64",
                producer_source,
                f"rows[{index}].rootCount",
                "window 0<tau<12 sqrt(delta)",
            )
        )
    for index, item in enumerate(independent["rows"]):
        rows.append(
            chart_row(
                "A",
                "independent complete",
                math.log(float(item["delta"])),
                float(item["completeSlopeMass"]),
                float(item["completeSlopeMass"]),
                "independent finite binary64",
                independent_source,
                f"rows[{index}].completeSlopeMass",
                f"R={item['R']}; delta={item['delta']}",
            )
        )

    fit = producer["logFit"]
    for index, item in enumerate(producer["rows"]):
        x = math.log(float(item["delta"]))
        y = float(fit["intercept"]) + (4 / math.pi**2) * x
        rows.append(
            chart_row(
                "A",
                "four-over-pi-squared diagnostic guide",
                x,
                y,
                y,
                "finite diagnostic, not theorem",
                producer_source,
                "logFit.intercept plus 4/pi^2 guide",
                "leading coefficient is not an analytic claim",
            )
        )
        root_x = math.sqrt(float(item["delta"]))
        root_y = (24 / math.pi) * root_x
        rows.append(
            chart_row(
                "B",
                "twenty-four-over-pi diagnostic guide",
                root_x,
                root_y,
                root_y,
                "finite diagnostic, not theorem",
                producer_source,
                f"rows[{index}].delta",
                "root-count guide only",
            )
        )

    largest = producer["rows"][-1]
    if int(largest["R"]) != int(config["expected"]["largestR"]):
        raise RuntimeError("largest producer row mismatch")
    positive_packets = 0
    for index, packet in enumerate(largest["dyadicPackets"]):
        mass = float(packet["slopeMass"])
        if mass <= 0:
            continue
        positive_packets += 1
        left = float(packet["tauLeft"])
        right = float(packet["tauRight"])
        rows.append(
            chart_row(
                "C",
                "R64 dyadic slope mass",
                float(index),
                mass,
                int(packet["rootCount"]),
                "finite binary64",
                producer_source,
                f"rows[-1].dyadicPackets[{index}]",
                f"tau in [{left:g},{right:g}); roots={packet['rootCount']}",
            )
        )

    independent_by_r = {int(row["R"]): row for row in independent["rows"]}
    common_gaps = []
    for item in producer["rows"]:
        r_value = int(item["R"])
        if r_value not in independent_by_r:
            continue
        other = independent_by_r[r_value]
        left = float(item["completeSlopeMass"])
        right = float(other["completeSlopeMass"])
        common_gaps.append(abs(left - right) / max(abs(left), abs(right)))
    summary = {
        "producerR": producer_r,
        "independentR": independent_r,
        "commonRootCountsEqual": all(
            int(item["rootCount"]) == int(independent_by_r[int(item["R"])]["rootCount"])
            for item in producer["rows"]
            if int(item["R"]) in independent_by_r
        ),
        "maximumCommonRelativeMassGap": max(common_gaps),
        "producerLogSlope": float(fit["slopeAgainstLogDelta"]),
        "diagnosticTarget": 4 / math.pi**2,
        "largestR": int(largest["R"]),
        "largestRootCount": int(largest["rootCount"]),
        "largestCompleteMass": float(largest["completeSlopeMass"]),
        "largestSelectedFraction": float(largest["selectedToCompleteMassRatio"]),
        "positiveDyadicPacketCount": positive_packets,
        "rowCount": len(rows),
    }
    return rows, summary


def write_csv(rows: list[dict[str, object]]) -> None:
    fields = [
        "panel",
        "series",
        "x",
        "y",
        "rawValue",
        "evidence",
        "source",
        "sourcePointer",
        "note",
    ]
    with (ROOT / "data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def render(rows: list[dict[str, object]], config: dict[str, Any]) -> None:
    palette = config["palette"]
    width = float(config["figure"]["widthMillimetres"]) / 25.4
    height = float(config["figure"]["heightMillimetres"]) / 25.4
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 7.2,
            "axes.titlesize": 8.0,
            "axes.labelsize": 7.2,
            "xtick.labelsize": 6.3,
            "ytick.labelsize": 6.3,
            "legend.fontsize": 6.0,
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
    fig.subplots_adjust(left=0.07, right=0.985, bottom=0.225, top=0.79, wspace=0.38)
    fig.suptitle(
        "Complete root packing in the exact one-carrier lattice",
        x=0.07,
        y=0.955,
        ha="left",
        fontsize=10.0,
        fontweight="bold",
    )
    fig.text(
        0.07,
        0.89,
        "Analytic order: G_all = Θ(log δ). Finite counts and leading-coefficient guides are diagnostic only.",
        ha="left",
        va="top",
        fontsize=6.7,
        color=palette["gray"],
    )

    def series(panel: str, name: str) -> list[dict[str, object]]:
        return sorted(
            [row for row in rows if row["panel"] == panel and row["series"] == name],
            key=lambda row: float(row["x"]),
        )

    ax = axes[0]
    complete = series("A", "producer complete")
    independent = series("A", "independent complete")
    selected = series("A", "producer selected")
    guide = series("A", "four-over-pi-squared diagnostic guide")
    ax.plot(
        [row["x"] for row in complete],
        [row["y"] for row in complete],
        color=palette["navy"],
        marker="o",
        markersize=3.6,
        linewidth=1.15,
        label="complete · RK4",
    )
    ax.plot(
        [row["x"] for row in independent],
        [row["y"] for row in independent],
        color=palette["rust"],
        marker="s",
        markerfacecolor=palette["open"],
        markeredgewidth=0.9,
        markersize=3.8,
        linewidth=0.95,
        linestyle="--",
        label="complete · Strang",
    )
    ax.plot(
        [row["x"] for row in selected],
        [row["y"] for row in selected],
        color=palette["gray"],
        marker="^",
        markerfacecolor=palette["open"],
        markersize=3.4,
        linewidth=0.85,
        linestyle=":",
        label="first R roots",
    )
    ax.plot(
        [row["x"] for row in guide],
        [row["y"] for row in guide],
        color=palette["ink"],
        linewidth=0.75,
        linestyle="-.",
        label=r"$4/\pi^2$ guide",
    )
    ax.set_title("A  Slope-weighted root mass", loc="left", fontweight="bold")
    ax.set_xlabel(r"$\log\delta$")
    ax.set_ylabel(r"$\sum |h(\tau_j)|^2$")
    ax.grid(axis="y", color=palette["light"], linewidth=0.55, alpha=0.8)
    ax.legend(frameon=False, loc="upper left", ncol=1, handlelength=2.3)
    ax.text(
        0.98,
        0.04,
        "common max gap\n$9.18\\times10^{-7}$",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=6.0,
        color=palette["gray"],
    )

    ax = axes[1]
    counts = series("B", "producer resolved roots")
    count_guide = series("B", "twenty-four-over-pi diagnostic guide")
    ax.loglog(
        [row["x"] for row in counts],
        [row["y"] for row in counts],
        color=palette["navy"],
        marker="o",
        markersize=3.6,
        linewidth=1.15,
        label="resolved roots",
    )
    ax.loglog(
        [row["x"] for row in count_guide],
        [row["y"] for row in count_guide],
        color=palette["ink"],
        linewidth=0.8,
        linestyle="-.",
        label=r"$(24/\pi)\sqrt{\delta}$ guide",
    )
    ax.set_title("B  Finite root count", loc="left", fontweight="bold")
    ax.set_xlabel(r"$\sqrt{\delta}$")
    ax.set_ylabel("resolved sign-changing roots")
    ax.grid(which="both", color=palette["light"], linewidth=0.5, alpha=0.72)
    ax.legend(frameon=False, loc="upper left", handlelength=2.4)
    ax.text(
        0.98,
        0.05,
        r"window: $0<\tau<12\sqrt{\delta}$",
        transform=ax.transAxes,
        ha="right",
        va="bottom",
        fontsize=5.9,
        color=palette["gray"],
    )

    ax = axes[2]
    packets = series("C", "R64 dyadic slope mass")
    packet_x = np.arange(len(packets))
    packet_y = np.asarray([float(row["y"]) for row in packets])
    ax.bar(
        packet_x,
        packet_y,
        width=0.76,
        color=palette["rust"],
        edgecolor=palette["ink"],
        linewidth=0.55,
    )
    ax.set_yscale("log")
    labels = []
    for row in packets:
        note = str(row["note"])
        interval = note.split(";", 1)[0].replace("tau in ", "")
        labels.append(interval)
    tick_positions = list(range(0, len(labels), 4))
    ax.set_xticks(tick_positions, [labels[index] for index in tick_positions], rotation=42, ha="right")
    ax.set_title("C  Dyadic packets · R=64", loc="left", fontweight="bold")
    ax.set_xlabel(r"scaled-time packet $[2^m,2^{m+1})$")
    ax.set_ylabel("packet slope mass")
    ax.grid(axis="y", which="both", color=palette["light"], linewidth=0.5, alpha=0.72)
    ax.text(
        0.98,
        0.96,
        "late roots remain numerous;\ntheir slope mass collapses",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=5.9,
        color=palette["gray"],
        bbox={"facecolor": palette["paper"], "edgecolor": "none", "alpha": 0.88, "pad": 1.5},
    )

    for ax in axes:
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    fig.text(
        0.985,
        0.025,
        "R0.72G · binary64 diagnostics · exact real one-carrier family",
        ha="right",
        va="bottom",
        fontsize=5.6,
        color=palette["gray"],
    )
    fig.savefig(ROOT / "figure.pdf")
    fig.savefig(ROOT / "figure.svg")
    fig.savefig(ROOT / "figure.png", dpi=int(config["figure"]["pngDpi"]))
    plt.close(fig)


def main() -> None:
    started = time.perf_counter()
    config = load(ROOT / "config.json")
    producer_path = REPOSITORY / config["sourceCertificates"]["producer"]
    independent_path = REPOSITORY / config["sourceCertificates"]["independent"]
    producer = load(producer_path)
    independent = load(independent_path)
    progress = [
        {
            "timestampUtc": utc_now(),
            "stage": "load",
            "status": "completed",
            "producerPassed": producer.get("allRequiredChecksPassed"),
            "independentPassed": independent.get("allRequiredChecksPassed"),
        }
    ]
    rows, summary = prepare_data(producer, independent, config)
    write_csv(rows)
    progress.append(
        {
            "timestampUtc": utc_now(),
            "stage": "data",
            "status": "completed",
            "rowCount": len(rows),
        }
    )
    render(rows, config)
    elapsed = time.perf_counter() - started
    progress.append(
        {
            "timestampUtc": utc_now(),
            "stage": "render",
            "status": "completed",
            "elapsedSeconds": elapsed,
            "outputs": ["figure.pdf", "figure.svg", "figure.png"],
        }
    )
    (ROOT / "progress.ndjson").write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in progress),
        encoding="utf-8",
    )
    (ROOT / "resource-log.ndjson").write_text(
        json.dumps(
            {
                "timestampUtc": utc_now(),
                "stage": "render",
                "elapsedSeconds": elapsed,
                "peakRssBytes": peak_rss(),
                "logicalCpus": os.cpu_count(),
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    metadata = {
        "schemaVersion": "r072g-figure-data-metadata-v1",
        "createdAtUtc": utc_now(),
        "sourceFiles": [
            {
                "path": str(producer_path.relative_to(REPOSITORY)),
                "sha256": digest(producer_path),
            },
            {
                "path": str(independent_path.relative_to(REPOSITORY)),
                "sha256": digest(independent_path),
            },
            {"path": str((ROOT / "contract.json").relative_to(REPOSITORY)), "sha256": digest(ROOT / "contract.json")},
            {"path": str((ROOT / "config.json").relative_to(REPOSITORY)), "sha256": digest(ROOT / "config.json")},
        ],
        "summary": summary,
        "claimBoundary": load(ROOT / "contract.json")["claimBoundary"],
    }
    (ROOT / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (ROOT / "results.json").write_text(
        json.dumps(
            {
                "schemaVersion": "r072g-figure-results-v1",
                "allRequiredSourceChecksPassed": True,
                "summary": summary,
                "elapsedSeconds": elapsed,
                "environment": {
                    "python": sys.version,
                    "matplotlib": mpl.__version__,
                    "numpy": np.__version__,
                    "platform": platform.platform(),
                    "logicalCpus": os.cpu_count(),
                },
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    (ROOT / "environment.txt").write_text(
        "\n".join(
            [
                f"captured={utc_now()}",
                f"python={sys.version.splitlines()[0]}",
                f"platform={platform.platform()}",
                f"logical_cpus={os.cpu_count()}",
                f"matplotlib={mpl.__version__}",
                f"numpy={np.__version__}",
                "renderer=Matplotlib static journal figure",
                "randomness=false",
                "interval_arithmetic=false",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
