#!/usr/bin/env python3
"""Build the formal R0.72M danger-window figure from analytic formulae and certificates."""

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


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]


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


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise FileNotFoundError(f"certificate CSV missing: {path}")
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def add_row(rows: list[dict[str, Any]], panel: str, route: str, series: str,
            x: float, y: float, source: str, pointer: str, note: str) -> None:
    rows.append({
        "panel": panel,
        "route": route,
        "series": series,
        "x": x,
        "y": y,
        "source": source,
        "pointer": pointer,
        "note": note,
    })


def prepare_data(config: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any], list[Path]]:
    rows: list[dict[str, Any]] = []
    panel_a = config["panels"]["A"]
    r_values = np.geomspace(1.0e-3, 1.0e3, int(panel_a["samples"]))
    for kappa in panel_a["kappaValues"]:
        for index, r_value in enumerate(r_values):
            tau = min(float(r_value), 1.0) / (float(kappa) + float(r_value))
            add_row(rows, "A", "analytic", f"K/H = {kappa:g}", float(r_value), tau,
                    config["analyticSource"], f"equation (5.1), sample {index}",
                    "dimensionless T/V against x/H")

    panel_b = config["panels"]["B"]
    sigma_values = np.geomspace(float(panel_b["sigmaMin"]), float(panel_b["sigmaMax"]), int(panel_b["samples"]))
    branch_formulas = {
        "K/U": lambda sigma: sigma ** (-1.0 / 3.0),
        "x/H": lambda sigma: sigma ** (-2.0 / 3.0) * math.log(sigma),
        "Vx/K": lambda sigma: sigma ** (-1.0 / 3.0) * math.log(sigma),
    }
    for series, formula in branch_formulas.items():
        for index, sigma in enumerate(sigma_values):
            add_row(rows, "B", "analytic", series, float(sigma), float(formula(float(sigma))),
                    config["analyticSource"], f"equations (6.1)-(6.4), sample {index}",
                    "fixed-geometry exponent ledger; multiplicative constants suppressed")

    cert = REPOSITORY / config["certificateDirectory"]
    source_paths = [
        REPOSITORY / config["analyticSource"], ROOT / "config.json", ROOT / "contract.json",
        ROOT / "figure-contract.md", ROOT / "caption.md",
        cert / "producer-frozen-cubic.csv", cert / "independent-frozen-cubic.csv",
        cert / "producer-dissipative.csv", cert / "independent-dissipative.csv",
    ]
    for route, name in (("producer", "producer-frozen-cubic.csv"), ("independent", "independent-frozen-cubic.csv")):
        for row in read_csv(cert / name):
            add_row(rows, "C", route, route, float(row["sigma"]), float(row["cubicOverLogSigma"]),
                    str((cert / name).relative_to(REPOSITORY)), "cubicOverLogSigma",
                    "finite corroboration of the proved frozen-reference coefficient")
    for route, name in (("FFT split", "producer-dissipative.csv"), ("Cayley split", "independent-dissipative.csv")):
        for row in read_csv(cert / name):
            add_row(rows, "D", route, route, float(row["sigma"]), float(row["cubicOverLogSigma"]),
                    str((cert / name).relative_to(REPOSITORY)), "cubicOverLogSigma",
                    "finite dissipative diagnostic; no continuum asymptotic claim")

    summary = {
        "rowCount": len(rows),
        "frozenTheoremConstant": 16.0 / math.pi**2,
        "panelCProducerLast": next(row["y"] for row in reversed(rows) if row["panel"] == "C" and row["series"] == "producer"),
        "panelCIndependentLast": next(row["y"] for row in reversed(rows) if row["panel"] == "C" and row["series"] == "independent"),
        "dissipativeDiagnosticOnly": True,
        "newPdeEvolution": False,
    }
    return rows, summary, source_paths


def write_data(rows: list[dict[str, Any]]) -> None:
    with (ROOT / "data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def selected(rows: list[dict[str, Any]], panel: str, series: str) -> list[dict[str, Any]]:
    return sorted((row for row in rows if row["panel"] == panel and row["series"] == series), key=lambda row: float(row["x"]))


def style_axes(ax: mpl.axes.Axes, palette: dict[str, str]) -> None:
    ax.set_facecolor(palette["paper"])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(palette["muted"])
    ax.spines["bottom"].set_color(palette["muted"])
    ax.tick_params(colors=palette["ink"], labelsize=6.8, length=2.4, width=0.6)
    ax.grid(True, color=palette["grid"], linewidth=0.45, alpha=0.72)
    ax.set_axisbelow(True)


def panel_label(ax: mpl.axes.Axes, label: str, palette: dict[str, str]) -> None:
    ax.text(-0.105, 1.02, label, transform=ax.transAxes, fontsize=10, fontweight="bold", color=palette["ink"], va="bottom")


def draw(rows: list[dict[str, Any]], config: dict[str, Any], summary: dict[str, Any]) -> None:
    palette = config["palette"]
    width = float(config["figure"]["widthMillimetres"]) / 25.4
    height = float(config["figure"]["heightMillimetres"]) / 25.4
    mpl.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 7.5, "axes.titlesize": 8.1,
        "axes.labelsize": 7.3, "legend.fontsize": 6.2, "pdf.fonttype": 42,
        "ps.fonttype": 42, "svg.fonttype": "none", "hatch.linewidth": 0.45,
    })
    fig, axes = plt.subplots(2, 2, figsize=(width, height), constrained_layout=False)
    fig.patch.set_facecolor(palette["paper"])
    fig.subplots_adjust(left=0.085, right=0.975, bottom=0.105, top=0.85, wspace=0.34, hspace=0.48)
    fig.suptitle("Exact action danger window and a full-lattice phase-mixing screen", x=0.085, y=0.965, ha="left", fontsize=9.7, fontweight="bold", color=palette["ink"])
    fig.text(0.085, 0.912, "Panels A-C have analytic anchors; Panel D is a finite dissipative diagnostic, not a theorem", ha="left", fontsize=6.7, color=palette["muted"])

    ax = axes[0, 0]
    style_axes(ax, palette); panel_label(ax, "A", palette)
    styles = [("K/H = 0.05", palette["blue"], "-"), ("K/H = 0.2", palette["ochre"], "--"), ("K/H = 1", palette["muted"], ":")]
    for series, color, linestyle in styles:
        points = selected(rows, "A", series)
        ax.plot([p["x"] for p in points], [p["y"] for p in points], color=color, linestyle=linestyle, linewidth=1.25, label=series)
    kappa = 0.2; threshold = float(config["panels"]["A"]["thresholdOverV"])
    display_maximum = max(
        1.0 / (1.0 + float(value))
        for value in config["panels"]["A"]["kappaValues"]
    )
    left = threshold * kappa / (1.0 - threshold)
    right = 1.0 / threshold - kappa
    ax.axhline(threshold, color=palette["ink"], linewidth=0.7, linestyle="-.")
    ax.axvspan(left, right, facecolor=palette["ochreLight"], hatch="////", edgecolor=palette["ochre"], alpha=0.55, linewidth=0.4)
    ax.set_xscale("log"); ax.set_ylim(0, 1.03 * display_maximum)
    ax.set_title("Exact scalar superlevel window", loc="left", pad=6)
    ax.set_xlabel(r"dimensionless action $x/H$"); ax.set_ylabel(r"$T(x)/V$")
    ax.legend(frameon=False, loc="lower center", ncol=3, handlelength=2.1)
    ax.text(0.98, 0.90, r"shaded: $K/H=0.2$, $T/V>0.2$", transform=ax.transAxes, ha="right", fontsize=6.2, color=palette["ochre"])

    ax = axes[0, 1]
    style_axes(ax, palette); panel_label(ax, "B", palette)
    bstyles = {"K/U": (palette["muted"], ":", "^"), "x/H": (palette["blue"], "--", "s"), "Vx/K": (palette["ochre"], "-", "o")}
    for series, (color, linestyle, marker) in bstyles.items():
        points = selected(rows, "B", series)
        ax.plot([p["x"] for p in points], [p["y"] for p in points], color=color, linestyle=linestyle, linewidth=1.15, marker=marker, markevery=40, markersize=3.0, markerfacecolor=palette["paper"], markeredgecolor=color, label=series)
    ax.set_xscale("log", base=2); ax.set_yscale("log")
    ax.set_title("Fixed one-carrier branch placement", loc="left", pad=6)
    ax.set_xlabel(r"coupling $\sigma$"); ax.set_ylabel("dimensionless branch ratio")
    ax.legend(frameon=False, loc="upper right", handlelength=2.2)
    ax.text(0.04, 0.08, "all three ratios vanish", transform=ax.transAxes, fontsize=6.2, color=palette["blue"])

    ax = axes[1, 0]
    style_axes(ax, palette); panel_label(ax, "C", palette)
    for series, color, linestyle, marker in (("producer", palette["blue"], "-", "o"), ("independent", palette["ochre"], "--", "s")):
        points = selected(rows, "C", series)
        ax.plot([p["x"] for p in points], [p["y"] for p in points], color=color, linestyle=linestyle, linewidth=1.15, marker=marker, markersize=3.5, markerfacecolor=palette["paper"] if marker == "s" else color, markeredgecolor=color, label=series)
    constant = float(summary["frozenTheoremConstant"])
    ax.axhline(constant, color=palette["ink"], linestyle=":", linewidth=1.0, label=r"theorem $16/\pi^2$")
    ax.set_xscale("log", base=2)
    ax.set_title("Frozen true-cubic coefficient", loc="left", pad=6)
    ax.set_xlabel(r"coupling $\sigma$"); ax.set_ylabel(r"$\mathcal{C}_{\rm fr}/(a^2\log\sigma)$")
    ax.legend(frameon=False, loc="lower right", handlelength=2.2)
    ax.text(0.04, 0.83, "zero-diffusion reference", transform=ax.transAxes, fontsize=6.2, color=palette["muted"])

    ax = axes[1, 1]
    style_axes(ax, palette); panel_label(ax, "D", palette)
    for series, color, linestyle, marker in (("FFT split", palette["blue"], "-", "o"), ("Cayley split", palette["ochre"], "--", "s")):
        points = selected(rows, "D", series)
        ax.plot([p["x"] for p in points], [p["y"] for p in points], color=color, linestyle=linestyle, linewidth=1.15, marker=marker, markersize=3.5, markerfacecolor=palette["paper"] if marker == "s" else color, markeredgecolor=color, label=series)
    ax.set_xscale("log", base=2)
    ax.set_title("Dissipative chain: finite diagnostic", loc="left", pad=6)
    ax.set_xlabel(r"coupling $\sigma$"); ax.set_ylabel(r"finite $\mathcal{C}_{\rm diss}/\log\sigma$")
    ax.legend(frameon=False, loc="lower right", handlelength=2.2)
    ax.text(0.04, 0.91, "not a proved asymptotic", transform=ax.transAxes, fontsize=6.2, color=palette["ochre"])

    for suffix in ("pdf", "svg"):
        fig.savefig(ROOT / f"figure.{suffix}", facecolor=palette["paper"])
    svg = ROOT / "figure.svg"
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines()) + "\n", encoding="utf-8")
    fig.savefig(ROOT / "figure.png", dpi=int(config["figure"]["pngDpi"]), facecolor=palette["paper"])
    plt.close(fig)


def main() -> None:
    started = time.perf_counter()
    progress = ROOT / "progress.ndjson"; resources = ROOT / "resource-log.ndjson"
    progress.write_text("", encoding="utf-8"); resources.write_text("", encoding="utf-8")
    append_ndjson(progress, {"time": utc_now(), "event": "start"})
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    rows, summary, sources = prepare_data(config)
    write_data(rows); append_ndjson(progress, {"time": utc_now(), "event": "data", "rows": len(rows)})
    draw(rows, config, summary)
    output_hashes = {name: digest(ROOT / name) for name in ("data.csv", "figure.pdf", "figure.svg", "figure.png")}
    source_hashes = {str(path.relative_to(REPOSITORY)): digest(path) for path in sources}
    result = {
        "schemaVersion": 1, "figureId": "R0.72M-1", "status": "built",
        "generatedAt": utc_now(), "summary": summary, "sourceSha256": source_hashes,
        "outputSha256": output_hashes, "elapsedSeconds": time.perf_counter() - started,
        "maxRssMb": max_rss_mb(), "newPdeEvolution": False,
        "dissipativeDiagnosticOnly": True,
    }
    (ROOT / "results.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (ROOT / "environment.txt").write_text(
        f"python={sys.version.split()[0]}\nplatform={platform.platform()}\nmatplotlib={mpl.__version__}\n"
        f"numpy={np.__version__}\ncpuCount={os.cpu_count()}\n", encoding="utf-8")
    append_ndjson(resources, {"time": utc_now(), "event": "complete", "elapsedSeconds": result["elapsedSeconds"], "maxRssMb": result["maxRssMb"], "rows": len(rows)})
    append_ndjson(progress, {"time": utc_now(), "event": "complete", "outputs": output_hashes})
    print(json.dumps({"status": "built", "rows": len(rows), "elapsedSeconds": result["elapsedSeconds"]}, sort_keys=True))


if __name__ == "__main__":
    main()
